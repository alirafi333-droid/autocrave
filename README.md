# AutozCraveStudio - Full-Stack Automotive Detailing & PPF Web Application

A complete, production-quality commercial web application built with **Python (Flask)**, **SQL (SQLAlchemy with SQLite / MySQL / PostgreSQL support)**, HTML5, Vanilla CSS3 (Dark cinematic aesthetic with red accent glow & glassmorphism), and JavaScript.

Designed specifically for **AutozCraveStudio** located in **DHA, Lahore, Pakistan**.

---

## 🚀 Key Features

* **Cinematic Dark Automotive Design**: Dark charcoal backgrounds, white typography, signature glowing red "Z" accent (`#ff1e27`), glassmorphism cards, and smooth scroll animations.
* **Dynamic Services Catalogue**: Fully loaded from SQL database; includes prices, durations, descriptions, and direct booking triggers.
* **Interactive Before & After Comparison**: Touch & mouse drag comparison slider allowing visitors to visually compare paint swirl correction against ceramic finish.
* **Portfolio Gallery with Filters**: Masonry layout gallery with category tabs (`ALL`, `CERAMIC`, `GLASS`, `GRAPHENE`, `PPF`, `DETAILING`) and fullscreen lightbox viewer.
* **Customer Booking System**: Multi-step booking form with vehicle make/model/year, preferred date & time, customer details, and instant reference code generation (e.g. `AZC-9A82F1`).
* **Secure Admin Control Panel (`/admin`)**:
  * Password-hashed session authentication (Werkzeug).
  * Real-time metrics overview cards (Total, Pending, Confirmed, Completed, Cancelled, Customers count, Contact messages).
  * Booking Manager (search query, date/status filter, status updates, deletion).
  * Service Manager (add, edit, toggle active status, thumbnail upload).
  * Gallery Manager (upload, assign category, delete).
  * Before & After Project Manager (upload before & after image pair).
  * Contact Inbox (read messages, toggle read/unread status, delete).
* **WhatsApp Integration**: Floating WhatsApp chat trigger button and pre-filled inquiry text links configured globally.

---

## 🛠️ Technology Stack

- **Backend**: Python 3.9+, Flask, Flask-SQLAlchemy, Flask-Login, Werkzeug Security, Pillow
- **Database**: SQLite (default local), compatible with PostgreSQL and MySQL via SQLAlchemy `DATABASE_URL`
- **Frontend**: Dynamic Jinja2 Templates, HTML5, Vanilla CSS3, JavaScript (ES6)

---

## 💻 Quick Start & Setup Instructions

### 1. Install Python Dependencies
Open your terminal in the project root directory and run:

```bash
pip install -r requirements.txt
```

### 2. Initialize and Seed the SQL Database
Run the seed script to automatically create database tables in `database/autozcrave.db` and populate initial services, gallery items, before/after projects, sample bookings, and the initial admin user:

```bash
python seed.py
```

### 3. Default Admin Credentials
* **Login URL**: `http://127.0.0.1:5000/admin/login`
* **Email**: `admin@autozcrave.com`
* **Password**: `Admin@123456`

### 4. Run the Flask Web Application
Start the application server:

```bash
python app.py
```

The website will be accessible locally at: `http://127.0.0.1:5000`

---

## ⚙️ Configuration Settings

All central application settings can be configured via environment variables or directly in `config.py`:

| Setting | Default Value | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | `autozcrave_studio_dha_lahore_secret_key_2026` | Flask session encryption key |
| `DATABASE_URL` | `sqlite:///.../database/autozcrave.db` | SQLAlchemy connection string |
| `PHONE` | `+92 300 1234567` | Phone number displayed on site |
| `WHATSAPP_NUMBER` | `923001234567` | WhatsApp link target number (without +) |
| `LOCATION` | `DHA, Lahore, Pakistan` | Primary business location |

### How to Change Phone & WhatsApp Number
To update the business contact or WhatsApp link across the entire website:
1. Open `config.py`.
2. Modify `PHONE` and `WHATSAPP_NUMBER`:
   ```python
   PHONE = "+92 300 9999999"
   WHATSAPP_NUMBER = "923009999999"
   ```
3. Save the file. All dynamic footer links, floating buttons, and contact cards will update automatically!

---

## 📁 Image Storage Location

All uploaded images (services, gallery portfolio, before & after projects) are validated for safe file extensions (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`), assigned a unique UUID timestamp filename, and stored under:

```text
autozcravestudio/static/uploads/
├── services/
├── gallery/
└── before_after/
```

Database tables store the web-accessible relative paths (`uploads/gallery/example.png`).

---

## 🗄️ Database Migration: SQLite to MySQL / PostgreSQL

The application uses **SQLAlchemy ORM**, making database engine migration simple:

### To Migrate to PostgreSQL:
1. Install PostgreSQL driver:
   ```bash
   pip install psycopg2-binary
   ```
2. Set the `DATABASE_URL` environment variable:
   ```bash
   export DATABASE_URL="postgresql://username:password@localhost:5432/autozcrave_db"
   ```
3. Run `python seed.py` to create the schema and seed initial data in PostgreSQL.

### To Migrate to MySQL:
1. Install MySQL driver:
   ```bash
   pip install pymysql
   ```
2. Set the `DATABASE_URL` environment variable:
   ```bash
   export DATABASE_URL="mysql+pymysql://username:password@localhost:3306/autozcrave_db"
   ```
3. Run `python seed.py`.

---

## 🔒 Security Practices Implemented

- **Password Hashing**: Admin passwords hashed using PBKDF2 with SHA-256 via `werkzeug.security`.
- **SQL Injection Prevention**: All queries execute parameterized ORM statements through SQLAlchemy.
- **Route Authorization**: Protected routes guarded with `@admin_required` decorators and session validation.
- **File Upload Security**: Strict file type validation (`ALLOWED_EXTENSIONS`) and filename sanitization via `secure_filename`.

---

&copy; 2026 AutozCraveStudio. DHA Lahore, Pakistan.
