from flask import Flask
import pickle
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#create the Flask app
db = SQLAlchemy()
app = Flask(__name__)
login_manager = LoginManager(app)
login_manager.login_view ='login'
login_manager.login_message_category ='info'
# load configuration from config.cfg
app.config.from_pyfile('config.cfg')

import os
pwd = os.path.abspath(os.curdir)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}/database.db".format(pwd)
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
#postgres://car_database_vtln_user:xeR1kaIvzQrEd3FB2fRriIHyiG1rumVu@dpg-clmafppfb9qs739aaqe0-a.singapore-postgres.render.com/car_database_vtln
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db.init_app(app)
    from .models import Entry, Prediction
    db.create_all()
    db.session.commit()
    print('Created Database!')

# with app.app_context():
#     db.init_app(app)
#     from .models import Prediction
#     db.create_all()
#     db.session.commit()
#     print('Created Database!')

joblib_file = "./application/static/joblib_Model.pkl"
# Load from file
with open(joblib_file, 'rb') as f:
    ai_model = pickle.load(f)
#run the file routes.py
from application import routes