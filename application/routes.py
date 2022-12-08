from application import app
from flask import render_template, redirect, url_for, flash, request, session
from application.models import User
from application.forms import RegisterForm
from application import db
from application import spacy_summary
from application import nltk_summary
from application import sumy_summary
from application import sbert_summary
from application import news
import time


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        if request.form.get('login') is not None:
            session['username'] = request.form['username']
            print(session['username'])
            flash("You have been logged in successfully", category='success')

        if request.form.get('logout') is not None:
            session.pop('username', None)
            print('Session deleted')
            flash("You have been logout successfully", category='danger')
            # print(request.form.get['logout'])
    return render_template('home.html', session=session)



@app.route('/news/<news_category>')
def news_page(news_category):
    try:
        news_list = news.get_news_list(news_category=news_category)
        return render_template('newspaper.html', news_category=news_category, news_list=news_list, news_list_size=len(news_list))
    except Exception as error_message:
        flash("Failed to establish a new connection. You're offline. Check your connection.", category='danger')
        return redirect(url_for('home_page'))

    # for news_object in news_list:
    #     print(news_object.headline, "\n")



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

@app.route('/summarize_text', methods=['GET', 'POST'])
def summarize_text():
    if request.method == 'POST':
        entering_time = time.time()
        headline = request.form['headline']
        input_text = request.form['input_text']
        try:
            input_text_reading_time = spacy_summary.calculate_reading_time(input_text)

            summarized_text = spacy_summary.spacy_summary(headline, input_text)
            summarized_text_reading_time = spacy_summary.calculate_reading_time(summarized_text)
            finishing_time = time.time()
            flash("Congratulation! Summarization successfully completed within {:.2f} second".format(
                finishing_time - entering_time), category='success')

            return render_template("summarize_text.html",
                                   input_text_reading_time=input_text_reading_time,
                                   summarized_text_reading_time=summarized_text_reading_time,
                                   input_text=input_text,
                                   summarized_text=summarized_text)
        except Exception as e:
            flash(e, category='danger')
    return render_template('summarize_text.html')


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


@app.route('/summarize_file', methods=['GET', 'POST'])
def summarize_file():
    if request.method == 'POST':
        entering_time = time.time()
        input_file = request.files['file']
        try:
            input_text = input_file.read().decode('utf-8')
            headline = ""
            input_text_reading_time = spacy_summary.calculate_reading_time(input_text)

            summarized_text = spacy_summary.spacy_summary(headline, input_text)
            summarized_text_reading_time = spacy_summary.calculate_reading_time(summarized_text)
            finishing_time = time.time()
            flash("Congratulation! Summarization successfully completed within {:.2f} second".format(
                finishing_time - entering_time), category='success')

            return render_template("summarize_file.html",
                                   input_text_reading_time=input_text_reading_time,
                                   summarized_text_reading_time=summarized_text_reading_time,
                                   input_text=input_text,
                                   summarized_text=summarized_text)
        except Exception as e:
            flash("Please upload a .txt file", category='danger')

    return render_template("summarize_file.html")


@app.route("/summarize_compare_algorithm", methods=["GET", "POST"])
def summarize_compare_algorithm():
    parameter_dictionary = {}
    if request.method == 'POST':
        headline = request.form['headline']
        input_text = request.form['input_text']
        input_text_reading_time = spacy_summary.calculate_reading_time(input_text)
        parameter_dictionary["input_text"] = input_text
        parameter_dictionary["input_text_reading_time"] = input_text_reading_time

        entering_time = time.time()

        # ================================ Spacy Summary =============================
        spacy_summary_output = spacy_summary.spacy_summary(headline, input_text)
        spacy_summary_reading_time = spacy_summary.calculate_reading_time(spacy_summary_output)
        spacy_summary_finish_time = time.time()
        spacy_summary_execution_time = spacy_summary_finish_time - entering_time

        parameter_dictionary["spacy_summary_output"] = spacy_summary_output
        parameter_dictionary["spacy_summary_reading_time"] = spacy_summary_reading_time
        parameter_dictionary["spacy_summary_execution_time"] = "{:.4f}".format(spacy_summary_execution_time)

        # ================================ NLTK Summary =============================
        nltk_summary_output = nltk_summary.nltk_summary(headline, input_text)
        # nltk_summary_output = spacy_summary.spacy_summary(headline, input_text)
        nltk_summary_reading_time = spacy_summary.calculate_reading_time(nltk_summary_output)
        nltk_summary_finish_time = time.time()
        nltk_summary_execution_time = nltk_summary_finish_time - spacy_summary_finish_time

        parameter_dictionary["nltk_summary_output"] = nltk_summary_output
        parameter_dictionary["nltk_summary_reading_time"] = nltk_summary_reading_time
        parameter_dictionary["nltk_summary_execution_time"] = "{:.4f}".format(nltk_summary_execution_time)

        # ================================ Sumy Summary =============================
        # sumy_summary_output = sumy_summary.sumy_summary(input_text)
        sumy_summary_output = spacy_summary.spacy_summary(headline, input_text)
        sumy_summary_reading_time = spacy_summary.calculate_reading_time(sumy_summary_output)
        sumy_summary_finish_time = time.time()
        sumy_summary_execution_time = sumy_summary_finish_time - nltk_summary_finish_time

        parameter_dictionary["sumy_summary_output"] = sumy_summary_output
        parameter_dictionary["sumy_summary_reading_time"] = sumy_summary_reading_time
        parameter_dictionary["sumy_summary_execution_time"] = "{:.4f}".format(sumy_summary_execution_time)

        # ================================ SBERT Summary =============================
        # sbert_summary_output = sbert_summary.sbert_summary(input_text)
        sbert_summary_output = spacy_summary.spacy_summary(headline, input_text)
        sbert_summary_reading_time = spacy_summary.calculate_reading_time(sbert_summary_output)
        sbert_summary_finish_time = time.time()
        sbert_summary_execution_time = sbert_summary_finish_time - sumy_summary_finish_time

        parameter_dictionary["sbert_summary_output"] = sbert_summary_output
        parameter_dictionary["sbert_summary_reading_time"] = sbert_summary_reading_time
        parameter_dictionary["sbert_summary_execution_time"] = "{:.4f}".format(sbert_summary_execution_time)

        return render_template("summarize_compare_algorithm.html", parameter_dictionary=parameter_dictionary)

    return render_template("summarize_compare_algorithm.html", parameter_dictionary=parameter_dictionary)
