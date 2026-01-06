# 🚀 FinDash – Role-Based FinTech Loan Management System

FinDash is a full-stack **FinTech Loan Management Dashboard** built using **Flask**, designed to simulate a **real-world banking workflow** with role-based access, admin approvals, and live loan status updates.

This project follows **production-style architecture** and is built with **future scalability** in mind.

---

## ✨ Key Features

### 🔐 Authentication & Authorization
- Single login system
- Role-based access control (User / Admin)
- Secure password hashing (Werkzeug)
- Session handling with Flask-Login

### 👤 User Dashboard
- Apply for loans
- View loan history
- Track loan status in real time
- Clean and modern FinTech UI

### 🛂 Admin Dashboard
- View all loan applications
- Approve or reject loans
- Status updates instantly reflect on user side
- Actions disabled after decision

### ⚡ Live Status Updates
- REST API using Flask
- Fetch API for auto-refresh
- No manual page reload required

---

## 🏗️ System Architecture

Browser (Client)
↓
Flask Application
↓
Blueprint-based Routing
↓
SQLAlchemy ORM
↓
Database (SQLite → PostgreSQL ready)

yaml
Copy code

---

## 👥 Roles & Permissions

| Role  | Access |
|------|-------|
| User | Apply loans, view loan status |
| Admin | Approve/reject loans, view all applications |

> Both roles use the **same login system** and **same database**, differentiated using role-based access control.

---

## 🧰 Tech Stack

### Backend
- Python
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Werkzeug

### Frontend
- HTML5
- CSS3 (modern UI & animations)
- JavaScript (Fetch API)

### Database
- SQLite (development)
- PostgreSQL-ready (production)

---

## 📁 Project Structure

fintech-dashboard/
│── app.py
│── config.py
│── extensions.py
│── requirements.txt
│
├── models/
│ ├── user.py
│ └── loan.py
│
├── routes/
│ ├── auth.py
│ ├── admin.py
│ └── user.py
│
├── templates/
│ ├── auth/
│ │ ├── login.html
│ │ └── register.html
│ ├── admin/
│ │ └── dashboard.html
│ └── user/
│ └── dashboard.html
│
├── static/
│ ├── css/
│ │ ├── base.css
│ │ └── animations.css
│ └── js/
│
└── README.md

