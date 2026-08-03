from flask import Flask
from application.db import db
app=None
import os

def create_app():
    app=Flask(__name__)
    app.debug=True
    app.secret_key="my-secret-key"
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///trek-m.sqlite3'
    db.init_app(app)
    app.app_context().push() 
    return app


app=create_app()

from application.auth_routes import *
from application.admin_routes import *
from application.staff_routes import *
from application.trekkers_route import *

if(__name__=="__main__"):
    with app.app_context():
        db.create_all()
        admin=User.query.filter_by(role="admin").first()
        if admin is None:
            admin=User(name="admin123",email="admin@gmail.com",password="admin@1234",role="admin")
            db.session.add(admin)
            db.session.commit()
        app.run()
 