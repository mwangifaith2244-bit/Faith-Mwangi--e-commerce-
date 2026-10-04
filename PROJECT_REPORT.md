# PROJECT REPORT
## DESIGN AND IMPLEMENTATION OF AN E-COMMERCE WEBSITE WITH M-PESA PAYMENT INTEGRATION

### 1. Introduction
This project presents the design and implementation of a web-based e-commerce application called K-Shop. The system allows customers to browse products, search for products, add products to a shopping cart and complete an order through a simulated M-PESA payment process.

### 2. Problem Statement
Many small businesses need affordable online platforms through which customers can view products and place orders. A simple e-commerce system can improve product visibility, reduce manual order handling and provide customers with a convenient purchasing process.

### 3. Objectives
- To design a user-friendly e-commerce website.
- To provide product browsing and search.
- To implement a shopping cart.
- To store products and orders in a database.
- To provide an M-PESA payment demonstration.
- To provide basic product management for an administrator.

### 4. Technologies Used
- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript

### 5. System Modules
1. Home page
2. Product catalogue
3. Product details
4. Shopping cart
5. Checkout
6. M-PESA payment demonstration
7. Order records
8. Product administration

### 6. Database
The system uses SQLite. The main tables are:
- products
- orders

### 7. M-PESA
The project includes a clearly labelled demonstration payment flow. A live M-PESA integration would require Safaricom Daraja credentials, a short code and a secure callback endpoint. The demonstration avoids real-money transactions.

### 8. Testing
The following should be tested during demonstration:
- Opening the home page.
- Searching for a product.
- Opening product details.
- Adding a product to the cart.
- Removing a product.
- Proceeding to checkout.
- Entering customer information.
- Completing the demo payment.
- Viewing the created order.
- Adding and deleting products through the admin page.

### 9. Conclusion
K-Shop demonstrates the major components of a basic e-commerce system. It provides a foundation that can later be expanded with customer accounts, stock management, delivery tracking, image uploads and a live payment gateway.
