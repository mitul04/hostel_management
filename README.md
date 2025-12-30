# Hostel Management System

**A comprehensive digital solution for managing hostel operations, including room allocation, fee tracking, and student records.**

### 📄 [Click Here to View Full Documentation (PDF)](README.pdf)

---

### 🚀 Overview
This project refactors a legacy group assignment into a modern, modular Python application. It replaces manual record-keeping with a secure, database-backed system.

**Key Features:**
* **Role-Based Access:** Secure login for Staff and Hostellers.
* **Room Management:** Allocate and deallocate rooms efficiently.
* **Financial Tracking:** Manage bills and payment status.
* **Modern UI:** Built with Python `tkinter` (modernized with `ttk`).
* **Robust Backend:** Powered by PostgreSQL.

### 🛠️ Tech Stack
* **Language:** Python 3.12+
* **GUI:** Tkinter (ttk)
* **Database:** PostgreSQL
* **Driver:** Psycopg2

---

### 📦 Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/mitul04/hostel_management.git](https://github.com/mitul04/hostel_management.git)
    cd hostel_management
    ```

2.  **Install Dependencies**
    ```bash
    pip install psycopg2
    ```

3.  **Setup Database**
    * Import the provided SQL schema into your PostgreSQL database.
    * Update `db.py` with your database credentials.

4.  **Run the App**
    ```bash
    python main.py
    ```