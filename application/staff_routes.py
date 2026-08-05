from flask import session,render_template,redirect,request,flash
from flask import current_app as app
from .models import User,Booking,Trek,Staff
from .db import db
        

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/staff/dashboard")
def staff_dashboard():
    if("staff_id" not in session):
        return redirect("/login")   
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    treks=Trek.query.filter_by(assigned_staff_id=(staff.id)).all()
    assigned_treks=len(treks)
    total_participants=sum(len(trek.bookings) for trek in treks)
    open_treks=sum(1 for trek in treks if trek.status=="open")
    return render_template("staff/dashboard.html",assigned_treks=assigned_treks,total_participants=total_participants,open_treks=open_treks,treks=treks)


@app.route("/staff/trek/<int:trek_id>")
def manage_trek(trek_id):
    if("staff_id" not in session):
        return redirect("/login") 
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    this_trek=Trek.query.filter_by(id=trek_id).first()
    bookings=db.session.query(Booking,User,Trek).join(User,Booking.user_id==User.id).join(Trek,Booking.trek_id==Trek.id).filter(Trek.assigned_staff_id == staff.id).order_by(Booking.booking_date.desc()).all()
    return render_template("staff/manage_trek.html",this_trek=this_trek,bookings=bookings)

@app.route("/staff/my_treks/")
def my_treks():
    if("staff_id" not in session):
        return redirect("/login") 
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    my_treks=Trek.query.filter_by(assigned_staff_id=staff.id).all()
    return render_template("staff/my_treks.html",my_treks=my_treks)


@app.route("/mark_started/<int:trek_id>")
def mark_started(trek_id):
    if("staff_id" not in session):
        return redirect("/login")
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    this_trek=Trek.query.filter_by(id=trek_id).first()
    this_trek.status="started"
    db.session.commit()
    return redirect("/staff/dashboard")



@app.route("/mark_completed/<int:trek_id>")
def mark_completed(trek_id):
    if("staff_id" not in session):
        return redirect("/login")
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    this_trek=Trek.query.filter_by(id=trek_id).first()
    this_trek.status="completed"
    db.session.commit()
    return redirect("/staff/dashboard")


@app.route("/cancel/booking/<int:b_id>")
def cancel_booking(b_id):
    if("staff_id" not in session):
        return redirect("/login")
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    this_b=Booking.query.filter_by(id=b_id).first()
    this_b.status="cancelled"
    db.session.commit()
    return redirect("/staff/dashboard")

@app.route("/staff/update_trek/<int:trek_id>", methods=["GET","POST"])
def up_trek(trek_id):
    if("staff_id" not in session):
        return redirect("/login")
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    trek=Trek.query.filter_by(id=trek_id).first()
    if(request.method=="POST"):
        old_total=trek.total_slots
        new_total=request.form.get("total_slots")
        trek.avl_slots+=int(new_total)-int(old_total)
        trek.total_slots=new_total
        trek.status=request.form.get("status")
        db.session.commit()
        flash("Trek Details Updated","success")
    return redirect("/staff/dashboard")



@app.route("/staff/profile",methods=["POST","GET"])
def staff_profile():
    if("staff_id" not in session):
        return redirect("/login")
    staff=Staff.query.filter_by(userid=session["staff_id"]).first()
    if(request.method=="POST"):
            staff.user.name=request.form.get("name")
            staff.user.email=request.form.get("email")
            staff.user.phone=request.form.get("phone")
            db.session.commit()
            curr_pwd=request.form.get("current_pwd")
            new_pwd=request.form.get("new_pwd")
            cnf_pwd=request.form.get("cnf_pwd")
            if(curr_pwd and new_pwd):
                if(curr_pwd==staff.user.password):
                    if(new_pwd==cnf_pwd):
                        staff.user.password=new_pwd;
                        db.session.commit()
                        flash("Profile Updated","Success")
                        return redirect("/staff/dashboard")
                else:
                    flash("Password Not Correct","error")
                    return redirect("/staff/dashboard")
            else:
                return redirect("/staff/dashboard")
    return render_template("staff/profile.html",staff=staff)