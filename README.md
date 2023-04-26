# Library API
This API allows users to borrow books from the library, with the ability to return them after a set period of time. Users who have overdue books will incur fines, and will be unable to borrow additional books until their fines are paid.

## Models
- Book: A model representing a book in the library, with fields for title, author, description, and quantity.
- User: A model representing a user of the library, with fields for name, email, and password.
- Borrowing: A model representing a borrowing of a book by a user, with fields for the user, the book, the date borrowed, and the date due.
- Payment: A model representing a payment made by a user for a late book return, with fields for the user, the amount, and the date paid.

## Features
* Users can register and log in to the system.
* Users can borrow a book from the library for a set period of time.
* Users can return a book to the library before or after the due date.
* Users who return a book after the due date will be charged a late fee.
* Users with outstanding fees or overdue books will be unable to borrow new books until their account is cleared.

## Getting Started
1. Clone this repository to your local machine.
2. Install the required dependencies using ```pip install -r requirements.txt```.
3. Set up the database by running ```python manage.py migrate```.
4. Start the development server using ```python manage.py runserver```.
5. You can now access the API endpoints at http://localhost:8000/api/.

## API Endpoints
- ### Books
    - GET /api/books/
    - GET /api/books/{id}/
    - POST /api/books/
    - PUT /api/books/{id}/
    - PATCH /api/books/{id}/
    - DELETE /api/books/{id}/

- ### Users
    - GET /api/users/me/
    - POST /api/users/
    - POST /api/users/token/
    - POST /api/users/token/refresh
    - PUT /api/users/me/
    - PATCH /api/users/me/

- ### Borrowings
    - GET /api/borrowings/
    - GET /api/borrowings/{id}/
    - POST /api/borrowings/
    - PUT /api/borrowings/{id}/
    - PATCH /api/borrowings/{id}/
    - PATCH /api/borrowings/{id}/return/
    - DELETE /api/borrowings/{id}/

- ### Payments
    - GET /api/payments/
    - GET /api/payments/{id}/
    - POST /api/payments/
    - PUT /api/payments/{id}/
    - DELETE /api/payments/{id}/

## Dependencies
- Django
- Django REST framework
