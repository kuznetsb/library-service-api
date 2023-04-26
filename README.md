# Library API
This is a full-fledged API for organizing the work of the library with the functionality of tracking the number of available books. It provides for the possibility of borrowing a book with tracking of the return time. If the user misses the date of delivery of the book, a fine is imposed on him. This API is written based on Django and Django REST technologies and Stripe payment gateway technology.
Swager documentation is available for review.

## The API has the following features:
Book management: add new books to the system, update book information, and track availability.
Borrowing management: check out books to users, set due dates, and track borrowing history.
User management: add new users, update user information, and track borrowing history.
Payment management: track payments made by users, generate payment reports.
Notification management: send automated notifications to library managers telegram chat about upcoming due dates

## Getting Started
### Python3 and PostgreSQL must be installed on your machine.

1. Clone this repository to your local machine ```git clone the-link-from-your-forked-repo```.
2. Create a virtual environment using ```python -m venv env```.
3. Activate the virtual environment using ```source env/bin/activate(on macOS)``` Or ```env\Scripts\activate (on Windows)```.
4. Install the required dependencies using ```pip install -r requirements.txt```.
5. Set up the database by running ```python manage.py migrate```.
6. Start the development server using ```python manage.py runserver```.
7. You can now access the API endpoints at http://localhost:8000/api/.

## Models in system
- Book: A model representing a book in the library, with fields for title, author, description, and quantity.
- User: A model representing a user of the library, with fields for name, email, and password.
- Borrowing: A model representing a borrowing of a book by a user, with fields for the user, the book, the date borrowed, and the date due.
- Payment: A model representing a payment made by a user for a late book return, with fields for the user, the amount, and the date paid.


## Endpoints for working with the API
- ### Books
    - GET /api/books/
    - GET /api/books/{id}/
    - POST /api/books/ (admin only)
    - PUT /api/books/{id}/ (admin only)
    - PATCH /api/books/{id}/ (admin only) 
    - DELETE /api/books/{id}/ (admin only)

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
    - PUT /api/borrowings/{id}/ (admin only)
    - PATCH /api/borrowings/{id}/ (admin only)
    - PATCH /api/borrowings/{id}/return/ 
    - DELETE /api/borrowings/{id}/ (admin only)

- ### Payments
    - GET /api/payments/success/
    - GET /api/payments/cancel/

## Dependencies
- Django
- Django REST framework
- Stripe
- Django REST framework Simple JWT
- Swagger
- Redis
- Django q


