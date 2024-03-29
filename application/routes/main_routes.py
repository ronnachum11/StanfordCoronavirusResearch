from flask import render_template, flash, request, url_for, redirect, abort, session, Markup
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from application import app, bcrypt, db, mail
from application.forms.forms import ContactForm

import codecs
import os 

from graph_creation import update_graphs, update_all_graphs

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

states = ["USA"] + list(states_dict.keys())

@app.route("/home", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()

    if form.validate_on_submit():
        flash('Form submitted successfully, however functionality has not been implemented yet', 'danger')
        # send_contact_email(form.name.data, form.email.data, form.subject.data, form.message.data)
        redirect(url_for('home'))

    return render_template("home.html", form=form)

@app.route("/research", methods=["GET"])
def research():
    return render_template("research.html", title="Research")

@app.route("/graphs/USA", methods=["GET"])
@app.route("/graphs", methods=["GET"])
def graphs():
    path = "C:\\Users\\Ron\\StanfordCoronavirusResearch"
    graph_folder = os.path.join('application', 'static', 'graphs', 'USA')
    graph_names = ['hospitalization_increase.html']
    graphs = []
    for graph in graph_names:
        graph_path = os.path.join(graph_folder, graph)
        print(os.getcwd(), print(graph_path))
        graph = codecs.open(graph_path, "r").read() 
        graph = Markup(graph)
        graphs.append(graph)

    return render_template("graphs_plotly.html", title="graphs", states=states, graphs=graphs)

@app.route("/graphs/<string:state>", methods=["GET"])
def graphs_state(state):
    graph_folder = os.path.join('application', 'static', 'graphs', state.title())
    graph_names = os.listdir(graph_folder)
    graph_names = sorted(graph_names)
    graphs = []
    for graph in graph_names:
        if graph[-1] == "l":
            graph_path = os.path.join(graph_folder, graph)
            graph = codecs.open(graph_path, "r").read() 
            graph = Markup(graph)
            graphs.append(graph)

    return render_template("graphs_plotly.html", title="graphs", state=state, states=states, graphs=graphs)

@app.route("/data/api", methods=["GET"])
@app.route("/data", methods=["GET"])
def data():
    return render_template("data.html", title="Data API")



def send_contact_email(name, email, subject, message):
    msg = Message('COVID Reopenings - Contact Us Email', sender='COVID Reopenings Us Email', recipients=["ronnachum13@gmail.com"])
    msg.body = f'''A New Contact Form Was Submitted:
        Name: {name}
        Email: {email}
        Subject: {subject}
        Message:
        {message}
    '''
    mail.send(msg)