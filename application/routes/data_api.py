from flask import render_template, flash, request, url_for, redirect, abort, session, Markup
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from application import app, bcrypt, db, mail
from application.forms.forms import ContactForm

import pandas as pd 

states_dict = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

states = list(states_dict.keys())

@app.route("/data/api/covid", methods=["GET"])
def covid_all():
    return {"Status": "Not Implemented"}

@app.route("/data/api/covid/<string:state>", methods=["GET"])
def covid_state(state):
    return {"Status": "Not Implemented"}

@app.route("/data/api/covid/<string:field>", methods=["GET"])
def covid_field(field):
    return {"Status": "Not Implemented"}

@app.route("/data/api/covid/<string:state>/<string:field>", methods=["GET"])
def covid_state_field(state, field):
    return {"Status": "Not Implemented"}



@app.route("/data/api/reopening", methods=["GET"])
def reopening_all():
    return {"Status": "Not Implemented"}

@app.route("/data/api/reopening/<string:state>", methods=["GET"])
def reopening_state(state):
    return {"Status": "Not Implemented"}

@app.route("/data/api/reopening/<string:type>", methods=["GET"])
def reopening_type(type):
    return {"Status": "Not Implemented"}

@app.route("/data/api/reopening/<string:state>/<string:type>", methods=["GET"])
def reopening_state_type(state, type):
    return {"Status": "Not Implemented"}
