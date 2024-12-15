from application import db
from flask_login import UserMixin
from application import login_manager


@login_manager.user_loader
def load_user(email):
    return Entry.query.get(email)

class Entry(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    password = db.Column(db.String)

class Prediction(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String)
    tax = db.Column(db.Integer)
    engine_size = db.Column(db.Float)
    model = db.Column(db.String)
    mileage = db.Column(db.Integer)
    year = db.Column(db.Integer)
    mpg = db.Column(db.Float)
    prediction = db.Column(db.Float)
    predicted_on = db.Column(db.DateTime,nullable=False)
    
    
    
    