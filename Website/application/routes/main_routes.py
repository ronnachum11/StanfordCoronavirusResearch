from flask import render_template, flash, request, url_for, redirect, abort, session
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from application import app, bcrypt, db, mail
from application.forms.forms import ContactForm

@app.route("/home", methods=["GET"])
@app.route("/", methods=["GET"])
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

@app.route("/graphs", methods=["GET"])
def graphs():
    return render_template("graphs.html", title="graphs")

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