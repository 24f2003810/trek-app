from flask import current_app as app
from flask import render_template,redirect,session,request
from .models  import User,Booking,Staff,Trek
from .db import db
from datetime import datetime



@app.route("/admin/dashboard")
def admin():
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    total_treks=Trek.query.all().__len__()
    total_staff=Staff.query.all().__len__()
    total_user=User.query.all().__len__()-total_staff-1
    all_bookings=Booking.query.all()
    recent_booking=Booking.query.order_by(Booking.booking_date.desc()).limit(3).all()
    total_bookings=all_bookings.__len__()
    

    return render_template("admin/dashboard.html",this_admin=this_admin,total_user=total_user,total_bookings=total_bookings,total_staff=total_staff,total_treks=total_treks,all_bookings=all_bookings,recent_booking=recent_booking)




@app.route("/admin/treks")
def admin_trek():
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    all_treks=Trek.query.all()
    return render_template("admin/admin_treks.html",this_admin=this_admin,all_treks=all_treks)

@app.route("/trek/add",methods=["GET","POST"])
def add_trek():
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    ex_staff=Staff.query.all()
    if(request.method=="POST"):
        name=request.form.get("name")
        location=request.form.get("location")
        price=request.form.get("price")
        difficulty=request.form.get("difficulty")
        duration_days=request.form.get("duration")
        total_slots=request.form.get("total_slots")
        start_date=datetime.strptime(request.form.get("start_date"),"%Y-%m-%d")
        end_date=datetime.strptime(request.form.get("end_date"),"%Y-%m-%d")
        staff=request.form.get("staff")
        status=request.form.get("status")
        desc=request.form.get("desc")
        trek=Trek(name=name,location=location,price=price,difficulty=difficulty,duration_days=duration_days,total_slots=total_slots,avl_slots=total_slots,start_date=start_date,end_date=end_date,assigned_staff_id=staff,created_by=this_admin.id,desc=desc,status=status)
        db.session.add(trek)
        db.session.commit()
    return render_template("admin/add_trek.html",this_admin=this_admin,ex_staff=ex_staff)


@app.route("/edit/trek/<int:trek_id>",methods=["GET","POST"])
def edit_trek(trek_id):
    if("admin_id" not in session):
        return redirect("/login")
    this_trek=Trek.query.filter_by(id=trek_id).first()
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    ex_staff=Staff.query.join(User,Staff.userid==User.id).all()
    if(request.method=="POST"):
        old_total=this_trek.total_slots
        new_total=request.form.get("total_slots")
        this_trek.name=request.form.get("name")
        this_trek.location=request.form.get("location")
        this_trek.price=request.form.get("price")
        this_trek.difficulty=request.form.get("difficulty")
        this_trek.duration_days=request.form.get("duration")
        this_trek.avl_slots+=int(new_total)-int(old_total)
        this_trek.total_slots=new_total
        
        this_trek.start_date=datetime.strptime(request.form.get("start_date"),"%Y-%m-%d")
        this_trek.end_date=datetime.strptime(request.form.get("end_date"),"%Y-%m-%d")
        this_trek.assigned_staff_id=request.form.get("staff")
        this_trek.status=request.form.get("status")
        this_trek.desc=request.form.get("desc")
        db.session.commit()
        return redirect("/admin/treks")
    return render_template("admin/edit_trek.html",this_trek=this_trek,this_admin=this_admin,ex_staff=ex_staff)


@app.route("/delete/trek/<int:trek_id>")
def delete_trek(trek_id):
    if("admin_id" not in session):
        return redirect("/login")
    this_trek=Trek.query.filter_by(id=trek_id).first()
    db.session.delete(this_trek)
    db.session.commit()
    return redirect("/admin/treks")


@app.route("/admin/staff")
def all_staff():
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    all_staff=Staff.query.all()
    active_staff=Staff.query.filter_by(approval_status="approved").all().__len__()
    pending_staff=Staff.query.filter_by(approval_status="pending").all().__len__()
    blacklisted_staff=Staff.query.filter_by(approval_status="blacklisted").all().__len__()

    return render_template("admin/manage_staff.html",this_admin=this_admin,all_staff=all_staff,active_staff=active_staff,pending_staff=pending_staff,blacklisted_staff=blacklisted_staff)


@app.route("/approve_staff/<int:staff_id>")
def approve_staff(staff_id):
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    this_staff=Staff.query.filter_by(id=staff_id).first()
    this_staff.approval_status="approved"
    this_staff.approved_by=this_admin.id
    db.session.commit()
    return redirect("/admin/staff")


@app.route("/reject_staff/<int:staff_id>")
def reject_staff(staff_id):
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    this_staff=Staff.query.filter_by(id=staff_id).first()
    this_staff.approval_status="blacklisted"
    db.session.commit()
    return redirect("/admin/staff")


@app.route("/admin/all/booking")
def all_booking():
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    all_bookings=Booking.query.all()
    return render_template("admin/all_booking.html",all_bookings=all_bookings,this_admin=this_admin)



@app.route("/admin/users")
def all_users():
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    all_users=User.query.filter_by(role="user").all()
    return render_template("admin/all_users.html",all_users=all_users,this_admin=this_admin)

@app.route("/revoke/<int:user_id>")
def revoke_user(user_id):
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    this_user=User.query.filter_by(id=user_id).first()
    this_user.status="blacklisted"
    db.session.commit()
    return redirect("/admin/users")


@app.route("/activate/<int:user_id>")
def acticate_user(user_id):
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    this_user=User.query.filter_by(id=user_id).first()
    this_user.status="active"
    db.session.commit()
    return redirect("/admin/users")


@app.route("/admin/search")
def admin_search():
    if("admin_id" not in session):
        return redirect("/login")
    search_type = request.args.get("type", "trek")
    query = request.args.get("q", "").strip()
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    results = []

    if query:

        if search_type == "trek":
            results = Trek.query.filter(
                Trek.name.ilike(f"%{query}%")
            ).all()

        elif search_type == "user":
            results = User.query.filter(
                User.name.ilike(f"%{query}%"),
                User.role=="user"
            ).all()

        elif search_type == "staff":
            results = Staff.query.join(User,Staff.userid==User.id).filter(
                User.name.ilike(f"%{query}%")
            ).all()

    return render_template(
        "admin/search.html",
        results=results,
        search_type=search_type,
        query=query,this_admin=this_admin
    )



@app.route("/history/<int:user_id>")
def user_history(user_id):
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    user=User.query.filter_by(id=user_id).first()
    history=Booking.query.filter_by(user_id=user_id).all()
    
    return render_template("admin/history.html",user=user,history=history,this_admin=this_admin)


@app.route("/admin/trek_details/<int:trek_id>")
def trek_det(trek_id):
    if("admin_id" not in session):
        return redirect("/login")
    this_admin=User.query.filter_by(id=session["admin_id"]).first()
    trek=Trek.query.filter_by(id=trek_id).first()
    return render_template("admin/trek_details.html",this_admin=this_admin,trek=trek)
