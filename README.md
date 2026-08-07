# Trekking Management Application

A full-featured role-based trekking management system built with Flask for managing trekking events, staff, and user bookings.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Jinja2, HTML, CSS, Bootstrap 5
- **Database**: SQLite (SQLAlchemy ORM)
- **Authentication**: Session-based authentication using Flask sessions

---

## Setup & Run

```bash
# 1. Clone the repository
git clone <repository-url>

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the application
python app.py

# 6. Open in browser
http://127.0.0.1:5000
```

---

## Default Admin Credentials

- **Email:** admin@gmail.com
- **Password:** admin@1234

> *(Replace these credentials with your actual seeded admin credentials if different.)*

---

## Project Structure

```text
trekking_management/
├── api/                         # OpenAPI YAML specifications
│
├── application/
│   ├── admin_routes.py          # Admin routes
│   ├── auth_routes.py           # Authentication routes
│   ├── db.py                    # SQLAlchemy initialization
│   ├── models.py                # Database models
│   ├── staff_routes.py          # Staff dashboard & trek management
│   └── trekkers_route.py        # Trekker dashboard & booking
│
├── instance/
│   └── database.db              # SQLite database
│
├── templates/
│   ├── admin/
│   ├── staff/
│   ├── user/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── already_exist.html
│   └── incorrect_pass.html
│
├── app.py                       # Flask application entry point
├── README.md
└── requirements.txt
```

---

## Database Schema

| Table | Key Fields |
|-------|------------|
| **users** | id, name, email, phone, password, contact, role, status, created_at, updated_at |
| **staff** | id, userid, approval_status, approved_by, approved_at, bio |
| **treks** | id, name, location, price, difficulty, duration_days, total_slots, avl_slots, assigned_staff_id, status, start_date, end_date, desc, created_by, created_at, updated_at |
| **bookings** | id, user_id, trek_id, booking_date, status, payment_status, cancelled_at |

---

## Roles & Workflows

### Admin

- Pre-seeded administrator account
- Create, edit, and delete treks
- Assign staff to treks
- Approve, reject, or blacklist staff
- View and manage all users
- Search users, staff, and treks
- Monitor bookings and trekking activities

### Trek Staff

- Self-register and await admin approval
- View assigned treks
- Update trek status and available slots
- View registered participants for assigned treks

### User (Trekker)

- Self-register and log in
- Browse approved/open treks
- Search and filter treks by location and difficulty
- Book available treks
- View booking status and trekking history

---

## Core Features

- Secure user authentication with role-based authorization.
- Separate dashboards for Admin, Trek Staff, and Trekkers.
- Complete trek management including creation, assignment, and status updates.
- Staff approval workflow managed by the administrator.
- Online trek booking with overbooking prevention.
- Booking history and status tracking.
- Search and filtering for treks, users, and staff.
- Responsive Bootstrap-based user interface.
- SQLite database managed using SQLAlchemy ORM.

---

## Application Routes

| Method | URL | Description |
|--------|-----|-------------|
| GET / POST | `/login` | User login |
| GET / POST | `/register` | User registration |
| GET | `/admin/dashboard` | Admin dashboard |
| GET | `/staff/dashboard` | Staff dashboard |
| GET | `/user/dashboard` | Trekker dashboard |
| GET | `/staff/my_treks` | View assigned treks |
| GET | `/user/history` | View booking history |

---

## Database Relationships

- **User → Staff** (One-to-One)
- **User → Booking** (One-to-Many)
- **Staff → Trek** (One-to-Many)
- **Trek → Booking** (One-to-Many)
- **Admin → Trek** (One-to-Many)
- **Admin → Staff** (One-to-Many)

---

## Future Enhancements

- Online payment gateway integration
- Email and SMS notifications
- Trek image gallery
- Weather integration for trekking locations
- GPS-based trek tracking
- Admin analytics dashboard
- Trek review and rating system
- Export booking reports to CSV/PDF

---