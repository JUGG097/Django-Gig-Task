# Sample Invoice Generation Backend

This template was generated from a CMD using `Python` v "^3.9", it runs `Django` v "^4.0.4", `Sentry-sdk` v "^1.5.11", `Djangorestframework-simplejwt` v "^5.2.2" and `Djangorestframework` v "^3.13.1" libraries.

Feel free to clone repo and improve on it.

## Local Development
- Create a virtual environment and install dependencies (requirements.txt)
- Ensure you update the `settings.py` file with correct PostGres DB credentials
- Create `.env` file using `.env.example` as template and update Cloudinary credentials
- Run `python manage.py makemigrations` to generate the migration files
- Run `python manage.py migrate` to update the PostGres DB with the appropriate tables
- Start the wsgi server by running `python manage.py runserver`

## API Endpoints
*http://127.0.0.1:8000/api/v1/check Endpoint (server healt check)*

- METHOD: 'GET'

- SUCCESS RESPONSE (200): {'success': true}

- ERROR RESPONSE (4**, 5**): {'success': false, 'message': '***********'}


*http://127.0.0.1:8000/api/v1/register Endpoint*

- METHOD: 'POST'

- REQUEST BODY: {
    "email": "JohnDoe@gmail.com",
    "password": "ty12243fghhh",
    "first_name": "John",
    "last_name": "Doe"
}

- SUCCESS RESPONSE (200): {'success': true, 'user': '**********'}

- ERROR RESPONSE (4**, 5**): {'***********'}


*http://127.0.0.1:8000/api/token/ Endpoint*

- METHOD: 'POST'

- REQUEST BODY: {
    "username": "JohnDoe@gmail.com",
    "password": "ty12243fghhh"
}

- SUCCESS RESPONSE (200): {'refresh': '****', 'access': '****'}

- ERROR RESPONSE (4**, 5**): {'***********'}

*http://127.0.0.1:8000/api/v1/generateInvoice' Endpoint (Protected)*

- METHOD: 'POST'

- REQUEST BODY: {
    "invoice_list": [
        {"item": "Apple", "amount": 200}
    ]
}

- AUTHORIZATION: 'Bearer <access_token>'

- SUCCESS RESPONSE (200): {'invoice': '****', 'message': '****'}

- ERROR RESPONSE (4**, 5**): {'***********'}
