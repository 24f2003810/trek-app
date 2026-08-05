from flask import session,render_template,redirect,request
from flask import current_app as app
from .models import User,Booking,Trek,Staff
from .db import db

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/staff/dashboard")
def staff_dashboard():
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    treks=Trek.query.filter_by(assigned_staff_id=(staff.id)).all()
    assigned_treks=len(treks)
    total_participants=sum(len(trek.bookings) for trek in treks)
    open_treks=sum(1 for trek in treks if trek.status=="open")
    return render_template("staff/dashboard.html",assigned_treks=assigned_treks,total_participants=total_participants,open_treks=open_treks,treks=treks)


@app.route("/staff/trek/<int:trek_id>")
def manage_trek(trek_id):
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    this_trek=Trek.query.filter_by(id=trek_id).first()
    bookings=db.session.query(Booking,User,Trek).join(User,Booking.user_id==User.id).join(Trek,Booking.trek_id==Trek.id).filter(Trek.assigned_staff_id == staff.id).order_by(Booking.booking_date.desc()).all()
    return render_template("staff/manage_trek.html",this_trek=this_trek,bookings=bookings)

@app.route("/staff/my_treks/")
def my_treks():
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    my_treks=Trek.query.filter_by(assigned_staff_id=staff.id).all()
    return render_template("staff/my_treks.html",my_treks=my_treks)


@app.route("/mark_started/<int:trek_id>")
def mark_started(trek_id):
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    this_trek=Trek.query.filter_by(id=trek_id).first()
    this_trek.status="started"
    db.session.commit()
    return redirect("/staff/dashboard")



@app.route("/mark_completed/<int:trek_id>")
def mark_completed(trek_id):
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    this_trek=Trek.query.filter_by(id=trek_id).first()
    this_trek.status="completed"
    db.session.commit()
    return redirect("/staff/dashboard")


@app.route("/cancel/booking/<int:b_id>")
def cancel_booking(b_id):
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    this_b=Booking.query.filter_by(id=b_id).first()
    this_b.status="cancelled"
    db.session.commit()
    return redirect("/staff/dashboard")