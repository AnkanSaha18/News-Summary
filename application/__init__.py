from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '5a08924ed5f4f2052566d58a'               # For forms validators purposes
db = SQLAlchemy(app)

from application import routes
