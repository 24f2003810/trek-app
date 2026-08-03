from flask import current_app as app
from flask import session,render_template,redirect,request
from .models  import User,Booking,Staff,Trek
from .db import db

@app.route("/")
def index():
    return render_template("index.html")



@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        pwd=request.form.get("pwd")
        this_user=User.query.filter_by(email=email).first()
        if(this_user):
            if(this_user.password==pwd):
                if(this_user.role=="admin"):
                    session["admin_id"]=this_user.id
                    return redirect("/admin/dashboard")
                elif(this_user.role=="staff"):
                    session["staff_id"]=this_user.id
                    session["name"]=this_user.name
                    return redirect("/staff/dashboard")
                else:
                    session["user_id"]=this_user.id
                    return redirect("/user/dashboard")
            else:
                return render_template("incorrect_pass.html")
        else:
            return render_template("already_exist.html")
    return render_template("login.html")



@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        pwd=request.form.get('pwd')
        role=request.form.get('role')
        user_email=User.query.filter_by(email=email).first()
        if(user_email):
            return render_template('already_exist.html')
        else:
            if(role=="admin" or role=="user"):
                new_user=User(name=name,email=email,password=pwd,role=role)
                db.session.add(new_user)
                db.session.commit()
                return redirect('/login')
            elif(role=="staff"):
                new_user_staff=User(name=name,email=email,password=pwd,role=role)
                db.session.add(new_user_staff)
                db.session.commit()
                new_staff=Staff(userid=new_user_staff.id,approval_status="pending")
                db.session.add(new_staff)
                db.session.commit()
                return redirect('/login')
    return render_template('register.html')



