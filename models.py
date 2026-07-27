from db import db

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    name=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    contact=db.Column(db.String(),nullable=True)
    role=db.Column(db.String(),default="user")       #admin | user | staff
    status=db.Column(db.String(),default="active")   # active | blacklisted | pending | rejected
    created_at=db.Column(db.DateTime(),server_default=db.func.now())
    updated_at=db.Column(db.DateTime(),server_default=db.func.now(),onupdate=db.func.now())

    # --- relationships ---
    staff_profile = db.relationship(
        "Staff",
        back_populates="user",
        uselist=False,                     # one-to-one
        foreign_keys="Staff.userid",
        cascade="all, delete-orphan",
    )

    assigned_treks = db.relationship(
        "Trek",
        back_populates="assigned_staff",
        foreign_keys="Trek.assigned_staff_id",
    )

    created_treks = db.relationship(
        "Trek",
        back_populates="creator",
        foreign_keys="Trek.created_by",
    )

    bookings = db.relationship(
        "Booking",
        back_populates="user",
        foreign_keys="Booking.user_id",
        cascade="all, delete-orphan",
    )


class Staff(db.Model):
    __tablename__="staff"
    id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    userid=db.Column(db.Integer(),db.ForeignKey("users.id"))
    approval_status=db.Column(db.String(),default="pending") # pending | approved | rejected | blacklisted
    approved_by=db.Column(db.Integer(),db.ForeignKey("users.id"))
    approved_at=db.Column(db.DateTime(),nullable=True,default=None)
    bio=db.Column(db.String(),default=None,nullable=True)

    # --- relationships ---
    user = db.relationship("User", back_populates="staff_profile", foreign_keys=[userid])
    approver = db.relationship("User", foreign_keys=[approved_by])

class Trek(db.Model):
    __tablename__="treks"
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(),nullable=False)
    location=db.Column(db.String(),nullable=False)
    difficulty=db.Column(db.String(),nullable=False) # Easy | Medium | Hard
    duration_days=db.Column(db.Integer(),nullable=False)
    total_slots=db.Column(db.Integer(),nullable=False)
    avl_slots=db.Column(db.Integer(),nullable=False)
    assigned_staff_id=db.Column(db.Integer(),db.ForeignKey("users.id"),nullable=True)
    status=db.Column(db.String(),default="pending") # pending | approved | open | closed | completed
    start_date=db.Column(db.DateTime(),nullable=False)
    end_date=db.Column(db.DateTime(),nullable=False)
    desc=db.Column(db.String(),nullable=True)
    created_by=db.Column(db.Integer(),db.ForeignKey("users.id"),nullable=False)
    created_at=db.Column(db.DateTime(),server_default=db.func.now())
    updated_at=db.Column(db.DateTime(),server_default=db.func.now(),onupdate=db.func.now())

    # --- relationships ---
    assigned_staff = db.relationship(
        "User", back_populates="assigned_treks", foreign_keys=[assigned_staff_id]
    )
    creator = db.relationship(
        "User", back_populates="created_treks", foreign_keys=[created_by]
    )
    bookings = db.relationship(
        "Booking", back_populates="trek", cascade="all, delete-orphan"
    )


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer(), db.ForeignKey("treks.id"), nullable=False)
    booking_date = db.Column(db.DateTime(), default=db.func.now())
    status = db.Column(db.String(20), nullable=False, default="Booked")
    payment_status = db.Column(db.String(20), nullable=False, default="Pending")
    cancelled_at = db.Column(db.DateTime, nullable=True)

    # --- relationships ---
    user = db.relationship("User", back_populates="bookings", foreign_keys=[user_id])
    trek = db.relationship("Trek", back_populates="bookings", foreign_keys=[trek_id])