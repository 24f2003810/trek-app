from flask import current_app as app
from flask import render_template,redirect,session,request
from .models  import User,Booking,Staff,Trek
from .db import db
from datetime import datetime

@app.route("/admin/dashboard")
def admin():
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    total_user=User.query.all().__len__()
    total_treks=Trek.query.all().__len__()
    total_staff=Staff.query.all().__len__()
    all_bookings=Booking.query.all()
    recent_booking=Booking.query.order_by(Booking.booking_date.desc()).limit(3).all()
    total_bookings=all_bookings.__len__()
    

    return render_template("admin/dashboard.html",this_admin=this_admin,total_user=total_user,total_bookings=total_bookings,total_staff=total_staff,total_treks=total_treks,all_bookings=all_bookings,recent_booking=recent_booking)


@app.route("/admin/all/bookings")
def all_bookings():
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    all_bookings=Booking.query.all()
    return render_template("admin/all_bookings.html",this_admin=this_admin,all_bookings=all_bookings)



@app.route("/admin/treks")
def admin_trek():
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    all_treks=Trek.query.all()
    return render_template("admin/admin_treks.html",this_admin=this_admin,all_treks=all_treks)

@app.route("/trek/add",methods=["GET","POST"])
def add_trek():
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    ex_staff=Staff.query.all()
    if(request.method=="POST"):
        name=request.form.get("name")
        location=request.form.get("location")
        difficulty=request.form.get("difficulty")
        duration_days=request.form.get("duration")
        total_slots=request.form.get("total_slots")
        start_date=datetime.strptime(request.form.get("start_date"),"%Y-%m-%d")
        end_date=datetime.strptime(request.form.get("end_date"),"%Y-%m-%d")
        staff=request.form.get("staff")
        status=request.form.get("status")
        desc=request.form.get("desc")
        trek=Trek(name=name,location=location,difficulty=difficulty,duration_days=duration_days,total_slots=total_slots,avl_slots=total_slots,start_date=start_date,end_date=end_date,assigned_staff_id=staff,created_by=this_admin.id,desc=desc)
        db.session.add(trek)
        db.session.commit()
    return render_template("admin/add_trek.html",this_admin=this_admin,ex_staff=ex_staff)


@app.route("/edit/trek/<int:trek_id>",methods=["GET","POST"])
def edit_trek(trek_id):
    this_trek=Trek.query.filter_by(id=trek_id).first()
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    if(request.method=="POST"):
        this_trek.name=request.form.get("name")
        this_trek.location=request.form.get("location")
        this_trek.difficulty=request.form.get("difficulty")
        this_trek.duration_days=request.form.get("duration")
        this_trek.total_slots=request.form.get("total_slots")
        this_trek.start_date=datetime.strptime(request.form.get("start_date"),"%Y-%m-%d")
        this_trek.end_date=datetime.strptime(request.form.get("end_date"),"%Y-%m-%d")
        this_trek.assigned_staff_id=request.form.get("staff")
        this_trek.status=request.form.get("status")
        this_trek.desc=request.form.get("desc")
        db.session.commit()
        return redirect("/admin/treks")
    return render_template("admin/edit_trek.html",this_trek=this_trek,this_admin=this_admin)


@app.route("/delete/trek/<int:trek_id>")
def delete_trek(trek_id):
    this_trek=Trek.query.filter_by(id=trek_id).first()
    db.session.delete(this_trek)
    db.session.commit()
    return redirect("/admin/treks")


@app.route("/admin/staff")
def all_staff():
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    all_staff=Staff.query.all()
    active_staff=Staff.query.filter_by(approval_status="approved").all().__len__()
    pending_staff=Staff.query.filter_by(approval_status="pending").all().__len__()
    blacklisted_staff=Staff.query.filter_by(approval_status="blacklisted").all().__len__()

    return render_template("admin/manage_staff.html",this_admin=this_admin,all_staff=all_staff,active_staff=active_staff,pending_staff=pending_staff,blacklisted_staff=blacklisted_staff)


@app.route("/approve_staff/<int:staff_id>")
def approve_staff(staff_id):
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    this_staff=Staff.query.filter_by(id=staff_id).first()
    this_staff.approval_status="approved"
    this_staff.approved_by=this_admin.id
    db.session.commit()
    return redirect("/admin/staff")


@app.route("/reject_staff/<int:staff_id>")
def reject_staff(staff_id):
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    this_staff=Staff.query.filter_by(id=staff_id).first()
    this_staff.approval_status="blacklisted"
    db.session.commit()
    return redirect("/admin/staff")


