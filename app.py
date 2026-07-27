from flask import Flask
from db import db
from models import User
app=None

def create_app():
    app=Flask(__name__);
    app.debug=True;
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///trek-m.sqlite3'
    db.init_app(app)
    app.app_context().push() 
    return app


app=create_app()


if(__name__=="__main__"):
    with app.app_context():
        db.create_all()
        admin=User.query.filter_by(role="admin").first()
        if admin is None:
            admin=User(name="admin123",email="admin@gmail.com",password="admin@1234",role="admin")
            db.session.add(admin)
            db.session.commit()
        app.run()
 