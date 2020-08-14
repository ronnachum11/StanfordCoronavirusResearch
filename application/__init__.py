from flask import Flask
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import googlemaps

from graph_creation import update_all_graphs
from Scripts.update_covidtracking_data import update_raw_data

from apscheduler.schedulers.background import BackgroundScheduler
app = Flask(__name__)

app.config['SECRET_KEY'] = "5791628bb0b13ce0c676dfde280ba245"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

if path.exists(os.path.join('Website', 'application', 'environment_variables.txt')):
    f = open(os.path.join('Website', 'application', 'environment_variables.txt'), 'r')
    app.config["PATH"] = f.readline().strip()
else:
    app.config["PATH"] = ""

app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None

mail = Mail(app)

app.config['TEMPLATES_AUTO_RELOAD'] = True

sched = BackgroundScheduler(daemon=True)
sched.add_job(update_all_graphs, 'cron', minute=0)
sched.add_job(update_raw_data, 'cron', minute=0)
sched.start()

from application.routes import main_routes
from application.routes import data_api
from application.routes import handlers