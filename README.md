# Library API
This is a full-fledged API for organizing the work of the library with the functionality of tracking the number of available books. It provides for the possibility of borrowing a book with tracking of the return time. If the user misses the date of delivery of the book, a fine is imposed on him. This API is written based on Django and Django REST technologies and Stripe payment gateway technology.
Swager documentation is available for review.

## The API has the following features:
1. Book management: add new books to the system, update book information, and track availability.
2. Borrowing management: check out books to users, set due dates, and track borrowing history.
3. User management: add new users, update user information, and track borrowing history.
4. Payment management: track payments made by users, generate payment reports.
5. Notification management: send automated notifications to library managers telegram chat about book borrowing and successful payments
6. Scheduled tasks: Send notification about upcoming due dates and set expired status to payment with expired session


## Getting Started
### Python3 and PostgreSQL or Docker must be installed on your machine.

1. Clone this repository to your local machine ```git clone the-link-from-your-forked-repo```.
2. Create a virtual environment using ```python -m venv env```.
3. Activate the virtual environment using ```source env/bin/activate(on macOS)``` Or ```env\Scripts\activate (on Windows)```.
4. Install the required dependencies using ```pip install -r requirements.txt```.
5. Create postgres db and user (SEE INSTRUCTION BELOW)
6. Copy .env.sample -> .env and populate it
7. Set up the database by running ```python manage.py migrate```.
8. Create superuser ```python manage.py createsuperuser```
9. Start the development server using ```python manage.py runserver```.
10. Go to admin page and create scheduling tasks: borrow.tasks.check_borrowings_overdue, payment.tasks.track_expired_sessions
11. Start django-q ```python manage.py qcluster```
12. You can now access the API endpoints at http://localhost:8000/api/.

### DB setup instruction
If you have installed Postgresql locally:
```
Mac:
brew services start postgresql
psql postgres

Windows:
pg_ctl -D "C:\Program Files\PostgreSQL\9.6\data" start (Windows)
psql –U postgres

sudo service postgresql start (Linux)
```
If you are using Docker:
```
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres
docker exec -it "containter_id" bash
su - postgres
psql
```
- create database db_name;
- create user db_user with encrypted password 'db_password'
- grant all privileges on database db_name to db_user;
- ALTER DATABASE db_name OWNER TO db_user; (for Docker)


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
