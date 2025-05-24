<img src="frontend/src/assets/app_logo.png" alt="logo" />
# Study Reserve App

A full-stack web application for reserving student seats in study areas and classrooms. Built using **Vue 3** for the frontend, **Django** for the backend, and **MySQL** for data persistence.

## 📌 Features

- 🔐 User authentication and role-based access (Student & Admin)
- 🪪 Email verification and password reset flows
- 🪑 Real-time seat availability & reservation
- 🧑‍💻 Admin dashboard for managing seats and schedules
- 🌐 Responsive and clean user interface
- ⚙️ CI/CD pipeline integration for seamless deployment

---

## 🧰 Tech Stack

| Layer         | Technology           |
|---------------|----------------------|
| Frontend      | [Vue 3](https://vuejs.org/) + Element Plus |
| Backend       | [Django](https://www.djangoproject.com/) REST Framework |
| Database      | [MySQL](https://www.mysql.com/) |
| Authentication| JWT + CSRF protection |
| CI/CD         | GitHub Actions / Custom pipelines |
| Project Mgmt  | Jira (Free tier) |

---

## 🚀 Getting Started

### ⚙️ Backend Setup (Django)

```bash
# Clone the repository
git clone https://github.com/yourusername/student-seat-reservation.git
cd student-seat-reservation/backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up the database
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the server
python manage.py runserver
```

### ⚙️ Frontend Setup (Vue)
```bash
cd ../frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```