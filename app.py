from flask import Flask, render_template, flash
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap5
import os
import smtplib



OWN_EMAIL = "matantestcode@gmail.com"
OWN_PASSWORD = "cggd tymf ltfh gkfg"


app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.urandom(24)

app.jinja_env.globals['current_year'] = datetime.now().year

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2)])
    email = EmailField('Email', validators=[DataRequired(), Email("Please enter a valid email address.")])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=4)])
    submit = SubmitField('Submit')


def send_email(name, email, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["POST", "GET"])
def contact():
    title = "Contact Me"
    form = ContactForm()
    if form.validate_on_submit():
        send_email(name=form.name.data, email=form.email.data, message=form.message.data)
        title = "Message Sent Successfully!"
        return render_template("contact.html", contact_form=form, page_title=title)
    return render_template("contact.html", contact_form=form, page_title=title)

if __name__ == "__main__":
    app.run(debug=True)