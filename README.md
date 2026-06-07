# 🚗 Vehicle Parking Management System — Version 1

A server-side rendered Vehicle Parking Management System built with Flask, Jinja2, and SQLite. This version focuses on core parking management features with a clean MVC architecture.

---

## 🔗 Repository

[Vehicle_Parking_App](https://github.com/24dp1000047/Vehicle_Parking_App)

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask (Python) |
| Frontend | Jinja2 + Bootstrap |
| Database | SQLite |
| Authentication | Flask Sessions |

---

## ✨ Features

- 🔐 Secure authentication with **Role-Based Access Control** (Admin & User)
- 🏢 Full **CRUD operations** for parking lot and spot management
- 🤖 Automated parking spot allocation using **first-available assignment logic**
- ⏱️ Parking **duration tracking** and **fee calculation**
- 📋 Booking history management
- 📊 Admin dashboard for monitoring availability, reservations, and user activity
- 🖥️ Server-side rendered UI using **Jinja2** and **Bootstrap**

---

## 🗄️ Database Models

- `User` — Admin and regular user roles
- `ParkingLot` — Lot details and location
- `ParkingSpot` — Individual spots linked to lots
- `Reservation` — Booking records with duration and fee

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+

### Installation

```bash
git clone https://github.com/24dp1000047/Vehicle_Parking_App
cd Vehicle_Parking_App
pip install -r requirements.txt
flask run
```

Open your browser at `http://localhost:5000`

---

## 📁 Project Structure

```
Vehicle_Parking_App/
├── app.py
├── models.py
├── controllers/
├── models/
├── templates/
│   ├── admin/
│   └── user/
├── static/
├── instance/
└── requirements.txt
```

---

## 👤 Author

**24dp1000047**  
[GitHub Profile](https://github.com/24dp1000047)

---
