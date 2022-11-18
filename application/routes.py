from application import app
from flask import render_template, redirect, url_for, flash
from application.models import User
from application.forms import RegisterForm
from application import db


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/news/<news_type>')
def news_page(news_type):
    return f"Now we have to render {news_type} page"


@app.route('/login-registration', methods=['GET', 'POST'])
def login_registration_page():
    register_form = RegisterForm()
    print("this is before if")
    print(register_form)
    if register_form.validate_on_submit():
        print("this is after if")
        user_to_create = User(username=register_form.username.data,
                              email=register_form.email.data,
                              password_hash=register_form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash("Congratulation! You have successfully created account. Please login now.", category='success')
        return redirect(url_for('home_page'))
    if register_form.errors != {}:
        for error_message in register_form.errors.values():
            flash(f"There was an error with creating a user: {error_message}", category='danger')
        return redirect(url_for('home_page'))

    return render_template('login_registration.html', form=register_form)
