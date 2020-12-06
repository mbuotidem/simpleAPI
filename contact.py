import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = "sqlite:///{}".format(os.path.join(project_dir, "database.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = db_file

db = SQLAlchemy(app)

class Contact(db.Model):
	id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
	first_name = db.Column(db.String(100), nullable=False)
	last_name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	gender = db.Column(db.String(100), nullable=False)
	ip_address = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f"Contact(First Name = {first_name}, Last Name = {last_name}, email = {email}, gender = {gender}, IP Address = {ip_address})"
