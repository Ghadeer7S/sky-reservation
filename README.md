# ✈️ Sky Reservation API

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Django](https://img.shields.io/badge/Django-REST_Framework-green?logo=django)
![Database](https://img.shields.io/badge/Database-MySQL-blue?logo=mysql)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Deployed](https://img.shields.io/badge/Hosted-PythonAnywhere-lightgrey?logo=pythonanywhere)

---

## 📘 Overview

**Sky Reservation** is a flight booking system built using **Django** and **Django REST Framework**.  
It allows authenticated users to create and manage flight reservations, while administrators have full control over airlines, airports, flights, users, and bookings.

---

## 🚀 Features

### 👤 User Features
- Register and log in using JWT authentication.  
- Receive a **welcome email** upon successful registration.  
- **Reset password** via email link containing a reset token.  
- View all available flights, airlines, and airports.  
- Create, view, edit, or delete **their own reservations only**.  
- Manage their **own profile** and **account information**.

### 🛠️ Admin Features
- Full CRUD access to:
  - Airlines  
  - Airports  
  - Flights  
  - Reservations  
  - User accounts  
  - User profiles  
- Ability to **confirm or cancel reservations**.  
- Access to **all reservations** across the system.

### ✈️ Smart Validation Features
- **Intelligent Flight Validation:**  
  Automatically checks flight data before saving to ensure:
  - Departure and arrival airports cannot be the same.  
  - **Arrival time must be after departure time.**  
  - **An airplane cannot be assigned to multiple flights in the same time window.**  
- **Reservation Restrictions:**  
  - Cannot add passengers beyond the reserved seat count.  
  - Cannot modify a **confirmed** or **cancelled** reservation.  
  - Cannot create a reservation for a **cancelled** or **completed** flight.

---

## ⚙️ Tech Stack

- **Backend:** Python, Django, Django REST Framework  
- **Authentication:** Djoser + JWT  
- **Database:** MySQL  
- **Deployment:** PythonAnywhere  
- **Optimization:** Avoids extra queries using Django ORM efficiently  

---

## 🔐 API Overview

### 🔸 Registration & Authentication Flow
1. The user registers via the `/register/` endpoint.  
2. A **welcome email** is automatically sent to the user's Gmail address.  
3. The user logs in and receives **JWT access/refresh tokens**.  
4. If the user forgets their password, they can request a **reset token** via email to securely reset it.

### 🔸 Reservation Management
- Authenticated users can create a reservation by selecting a flight and specifying the number of seats.  
- They can add passengers up to the reserved seat limit.  
- They can modify or delete their reservation unless it has been **confirmed** or **cancelled**.

### 🔸 Admin Management
- Admins can manage all system data through the **Django Admin Dashboard**.  
- Only admins can **confirm** or **cancel** reservations.

---

## 🧠 Business Rules & Permissions

- Users **cannot confirm** their own reservations — only admins can.  
- Users **cannot modify** reservations that are **confirmed** or **cancelled**.  
- Users can access only **their own reservations, profiles, and accounts**.  
- Reservations cannot be created for **cancelled** or **completed** flights.  
- Passengers cannot exceed the number of reserved seats.  
- Flights must have **different departure and arrival airports**.  
- Flights must have **arrival times after departure times**.  
- Each airplane can only be scheduled for one flight at a given time.  
- Strict validation ensures there are no time or airplane conflicts.  
- Admins have unrestricted access to all resources.

---
## 🗂️ Project Structure

PROJECT/
├── airlines/ # Airline management
├── core/ # Authentication and user core logic
├── flight_reservation/ # Main project configuration
├── flights/ # Flight management
├── reservations/ # Reservations and passenger management
├── users/ # User profiles and account management
└── requirements.txt

-----------------

## ⚙️ Installation & Setup

1️⃣ Create a virtual environment
    ```bash
    python -m venv venv
2️⃣ Activate the environment

    Windows:
        venv\Scripts\activate

    macOS / Linux:
        source venv/bin/activate

3️⃣ Install dependencies
    pip install -r requirements.txt

4️⃣ Apply migrations
    python manage.py migrate

5️⃣ Run the development server
    python manage.py runserver

### Then open your browser at:
👉 http://127.0.0.1:8000/


# 🛫 Future Improvements

    Add a visual airplane seat map for better booking experience.

    Integrate online payment systems.

    Add flight filtering and sorting options.

    Implement email verification before account activation.

    Provide full API documentation using Swagger or ReDoc.

📄 License

    This project is licensed under the MIT License.
    You are free to use, modify, and distribute it for learning or development purposes.

    