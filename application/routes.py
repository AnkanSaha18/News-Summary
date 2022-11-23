from application import app
from flask import render_template, redirect, url_for, flash, request
from application.models import User
from application.forms import RegisterForm
from application import db
from application import spacy_summary
from application import news
import time


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/news/<news_category>')
def news_page(news_category):
    news_list = news.get_news_list(news_category=news_category)
    print(news_list)

    for news_object in news_list:
        print(news_object.headline, "\n")

    return render_template('newspaper.html', news_category=news_category, news_list=news_list, news_list_size=len(news_list))


@app.route('/login-registration', methods=['GET', 'POST'])
def login_registration_page():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
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


@app.route('/summarize_link', methods=['GET', 'POST'])
def summarize_link():
    if request.method == 'POST':
        entering_time = time.time()
        link = request.form['link']
        try:
            headline, input_text = spacy_summary.get_headline_text(link)
            input_text_reading_time = spacy_summary.calculate_reading_time(input_text)

            summarized_text = spacy_summary.spacy_summary(headline, input_text)
            summarized_text_reading_time = spacy_summary.calculate_reading_time(summarized_text)
            finishing_time = time.time()
            flash("Congratulation! Summarization successfully completed within {:.2f} second".format(
                finishing_time - entering_time), category='success')

            return render_template("summarize_link.html",
                                   input_text_reading_time=input_text_reading_time,
                                   summarized_text_reading_time=summarized_text_reading_time,
                                   input_text=input_text,
                                   summarized_text=summarized_text)
        except Exception as e:
            flash(e, category='danger')

    return render_template("summarize_link.html", input_text_reading_time=0, summarized_text_reading_time=0)
