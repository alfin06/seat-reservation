# Study Seat Reservation System

A Django-based backend for managing study seat reservations.

## Features Implemented

### User Authentication
- User registration with email verification
- Secure login system
- Role-based access (Admin/Student)
- Session management

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and update the values
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Authentication
- `POST /users/register/` - Register a new user
  ```json
  {
    "email": "user@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "name": "User Name",
    "role": "STUDENT"
  }
  ```
- `POST /users/login/` - Login user
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```

## Team Members
- Project Manager: Alfin
- Backend Developers: Luke, Quan
- Frontend Developers: Ain, Chetona
- DevOps/Tester: Nick

## Tech Stack
- Backend: Django 5.1.4
- Database: MySQL
- Frontend: VueJS 3.0 (to be implemented)