from application import app
from flask import render_template


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/news/<news_type>')
def news_page(news_type):
    return f"Now we have to render {news_type} page"


@app.route('/login-registration')
def login_registration():
    return render_template('login_registration.html')
