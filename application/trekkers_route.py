from flask import current_app as app
from flask import render_template,redirect,session,flash,request
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
    this_trek=Trek.query.filter_by(id=trek_id).first()
    if(exist_booking):
        flash("Booking Already Exist","success")
        return redirect("/user/dashboard")
    if(this_trek.status!="open"):
        flash("Trek is Closed","success")
        return redirect("/user/dashboard")
    if(this_trek.avl_slots==0):
        flash("Trek is Completely Booked","success")
        return redirect("/user/dashboard")
    new_booking=Booking(user_id=this_user.id,trek_id=trek_id)
    db.session.add(new_booking)
    this_trek.avl_slots=this_trek.avl_slots-1
    db.session.commit()
    flash("Booking Succesfully Created","success")
    return redirect("/user/dashboard")

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


@app.route("/user/treks")
def avl_treks():
    this_user=User.query.filter_by(id=session["user_id"]).first()
    avl_treks=Trek.query.filter_by(status="open").all()
    return render_template("user/my_treks.html",this_user=this_user,avl_treks=avl_treks)


from sqlalchemy import or_

@app.route("/user/search")
def user_search():
    this_user=User.query.filter_by(id=session["user_id"]).first()
    query = request.args.get("q", "").strip()

    treks = []

    if query:

        treks = Trek.query.filter(
            or_(
                Trek.name.ilike(f"%{query}%"),
                Trek.location.ilike(f"%{query}%"),
                Trek.difficulty.ilike(f"%{query}%")
            )
        ).all()

    return render_template(
        "user/search.html",
        this_user=this_user,
        treks=treks,
        query=query
    )
    


@app.route("/trek/<int:trek_id>")
def trek_details(trek_id):
    this_user=User.query.filter_by(id=session["user_id"]).first()
    trek=Trek.query.filter_by(id=trek_id).first()
    return render_template("user/trek_details.html",this_user=this_user,trek=trek)


@app.route("/user/profile",methods=["GET","POST"])
def profile():
    user=User.query.filter_by(id=session["user_id"]).first()
    this_user=user
    if(request.method=="POST"):
        user.name=request.form.get("name")
        user.email=request.form.get("email")
        user.phone=request.form.get("phone")
        db.session.commit()
        curr_pwd=request.form.get("current_pwd")
        new_pwd=request.form.get("new_pwd")
        cnf_pwd=request.form.get("cnf_pwd")
        if(curr_pwd and new_pwd):
            if(curr_pwd==user.password):
                if(new_pwd==cnf_pwd):
                    user.password=new_pwd;
                    db.session.commit()
            else:
                return redirect("/user/profile")

    return render_template("user/profile.html",user=user,this_user=this_user)