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
        send_contact_email(form.name.data, form.email.data, form.subject.data, form.message.data)
        redirect(url_for('home'))

    return render_template("home.html", form=form)

@app.route("/research", methods=["GET"])
def research():
    return render_template("research.html", title="Research")

@app.route("/graphs/USA", methods=["GET"])
@app.route("/graphs", methods=["GET"])
def graphs():
    path = "C:\\Users\\Ron\\StanfordCoronavirusResearch"
    graph_folder = os.path.join(app.config["PATH"], 'Website', 'application', 'static', 'graphs', 'usa')
    graph_names = ['hospitalization_increase.html']
    graphs = []
    for graph in graph_names:
        graph_path = os.path.join(graph_folder, graph)
        graph = codecs.open(graph_path, "r").read() 
        graph = graph[graph.index('<div>'):graph.index('</body>')-1]
        graph = Markup(graph)
        graphs.append(graph)

    return render_template("graphs_plotly.html", title="graphs", states=states, graphs=graphs)

@app.route("/graphs/<string:state>", methods=["GET"])
def graphs_state(state):
    # update_graphs(state)
    graph_list = ["2cumulative_hospitalizations.png", "3doubling_times.png", "4reopenings.png",
                  "4reopenings_with_lag_times.png", "5doubling_times_reopenings.png", 
                  "6doubling_times_negative_reopenings.png", "7negative_reopenings.png",
                  "8predictions.png"]
    graph_list = ['graphs/' + state + "/" + graph for graph in graph_list]
    print(graph_list)
    return render_template("graphs_matplotlib.html", title="graphs", state=state, states=states, graphs=graph_list)

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