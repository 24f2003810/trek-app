from flask import current_app as app
from flask import render_template,redirect,session,flash
from .models import User,Trek,Booking,Staff
from .db import db


@app.route("/user/dashboard")
def dashboard():
    this_user=User.query.filter_by(id=session["user_id"]).first()
    all_trek=Trek.query.all()
    my_bookings=Booking.query.filter_by(user_id=session["user_id"]).all()
    return render_template("user/dashboard.html",this_user=this_user,all_trek=all_trek,my_bookings=my_bookings)


@app.route("/book/<int:trek_id>")
def book_trek(trek_id):
    this_user=User.query.filter_by(id=session["user_id"]).first()
    exist_booking=Booking.query.filter_by(trek_id=trek_id,user_id=this_user.id).first()
    if(exist_booking):
        flash("Booking Already Exist","success")
        return redirect("/user/dashboard")
    new_booking=Booking(user_id=this_user.id,trek_id=trek_id)
    db.session.add(new_booking)
    db.session.commit()
    flash("Booking Succesfully Created","success")
    return redirect("/user/dashboard")\

@app.route("/user/bookings")
def my_bookings():
    this_user=User.query.filter_by(id=session["user_id"]).first()
    my_bookings=Booking.query.filter_by(user_id=session["user_id"]).all()
    return render_template("user/my_bookings.html",this_user=this_user,my_bookings=my_bookings)


@app.route("/user/history")
def history():
    this_user=User.query.filter_by(id=session["user_id"]).first()
    completed_treks=Booking.query.join(Trek).filter(Trek.status=="completed").all()
    return render_template("user/history.html",this_user=this_user,completed_treks=completed_treks)