from flask import Flask, render_template, request, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'brahjadon_secret_key'


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()

    if form.validate_on_submit():

        name = form.name.data
        email = form.email.data
        message = form.message.data
        ip = request.remote_addr
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if not os.path.exists("messages"):
            os.makedirs("messages")

        with open("messages/messages.txt", "a") as file:
            file.write(
                f"\n--- New Message ---\n"
                f"Time: {time}\n"
                f"Name: {name}\n"
                f"Email: {email}\n"
                f"IP: {ip}\n"
                f"Message:\n{message}\n"
                f"--------------------\n"
            )

        flash("Message sent successfully!")
        return redirect("/")

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
