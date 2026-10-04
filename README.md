# K-Shop — E-Commerce Website with M-PESA Demo

A student e-commerce web application built with Python Flask, SQLite, HTML, CSS and JavaScript.

## Features
- Home page
- Product catalogue
- Product categories
- Search
- Product details
- Shopping cart
- Checkout
- M-PESA demo payment flow
- Order storage in SQLite
- Simple admin product management
- Responsive design

## Important note about M-PESA
The checkout currently uses a **DEMO M-PESA payment status** so the project can be demonstrated without real money or Safaricom credentials.

For a live M-PESA Daraja integration, you would need:
- Safaricom Daraja developer account
- Consumer key and consumer secret
- Passkey
- Business short code
- A publicly reachable callback URL

Do not put real API credentials into a school project that will be shared publicly.

## How to run on a laptop later

1. Install Python 3.
2. Open a terminal in this project folder.
3. Create a virtual environment:
   `python -m venv venv`
4. Activate it.
5. Install dependencies:
   `pip install -r requirements.txt`
6. Create the database:
   `python create_db.py`
7. Start the website:
   `python app.py`
8. Open the local address shown by Flask, normally:
   `http://127.0.0.1:5000`

## Demo pages
- `/` Home
- `/products` Products
- `/cart` Shopping cart
- `/checkout` Checkout
- `/orders` Orders
- `/admin` Admin product page

## Suggested project title
DESIGN AND IMPLEMENTATION OF AN E-COMMERCE WEBSITE WITH M-PESA PAYMENT INTEGRATION
