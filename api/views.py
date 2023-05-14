from django.shortcuts import render

from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

# from .models import Tile, Task
from .serializers import RegisterSerializer, UserSerializer, InvoiceSerializer
from fpdf import FPDF
import requests
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


# Create your views here.
@api_view(["GET"])
def health_check(request):
    return Response({"success": True}, 200)


def invoiceGenerator(user: User, req):
    sales = req["invoice_list"] if req["invoice_list"] else []
    user_name = user.get_full_name()
    total_amount = 0
    line_counter = 0
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.set_font("courier", "B", 12)
    pdf.cell(40, 10, "Invoice For " + str(user_name), 0, 1)
    pdf.cell(40, 10, "", 0, 1)
    pdf.cell(
        200, 8, f"{'Company Name'.ljust(30)} {'Created: 01/01/2023'.rjust(20)}", 0, 1
    )
    pdf.cell(200, 8, f"{'Payment Method'.ljust(30)} {'Transfer'.rjust(20)}", 0, 1)
    pdf.cell(40, 10, "", 0, 1)
    pdf.set_font("courier", "", 12)
    pdf.cell(200, 8, f"{'Item'.ljust(30)} {'Amount'.rjust(20)}", 0, 1)
    pdf.line(10, 54, 150, 54)
    pdf.line(10, 62, 150, 62)

    for line in sales:
        line_counter += 1
        total_amount += line["amount"]
        formatted_amount = "$" + str(line["amount"]) + ".00"
        pdf.cell(200, 8, f"{line['item'].ljust(30)} {formatted_amount.rjust(20)}", 0, 1)
    pdf.line(90, 64 + (8 * line_counter), 150, 64 + (8 * line_counter))

    pdf.set_font("courier", "B", 12)
    formatted_total = "Total: $" + str(total_amount) + ".00"
    pdf.cell(200, 8, f"{''.ljust(30)} {formatted_total.rjust(20)}", 0, 1)

    pdf.output("api/pdf/temp.pdf", "F")

    # Upload Request to cloudinary 3rd party service
    cloudinary_response = requests.post(
        "https://api.cloudinary.com/v1_1/" + env("CLOUDINARY_CLOUD_NAME") + "/image/upload",
        data={"upload_preset": env("CLOUDINARY_UPLOAD_RESET")},
        files={"file": open("api/pdf/temp.pdf", "rb")},
    )

    # Validate response from cloudinary 3rd party service
    if cloudinary_response.status_code != 200:
        return Response(
            {"success": False, "error": "Invalid cloudinary credentials"}, 400
        )
        
    return cloudinary_response.json()


# Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        request.data["username"] = request.data["email"]

        # Checks if password meets minimum requirements to be registered
        validate_password(request.data["password"])
        # Hash password before sending to serializer
        request.data["password"] = make_password(request.data["password"])

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            }
        )


# Invoice API
class InvoiceApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvoiceSerializer

    # Run Generate PDF function and save pdf to cloud return file link
    # pass user id gotten from jwt token and file url to serializer
    def post(self, request, *args, **kwargs):
        invoice_generated = invoiceGenerator(request.user, request.data)
        serializer = self.get_serializer(
            data={
                "user": request.user.id,
                "file_url": invoice_generated["url"],
            }
        )
        serializer.is_valid(raise_exception=True)
        invoice = serializer.save()

        return Response(
            {
                "invoice": InvoiceSerializer(
                    invoice, context=self.get_serializer_context()
                ).data,
                "message": "Invoice Generated Successfully",
            }
        )
