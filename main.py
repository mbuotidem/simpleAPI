import os
from flask import Flask, render_template, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
db_file = 'sqlite:///{}'.format(os.path.join(project_dir, 'database.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = db_file

db = SQLAlchemy(app)

class Contact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(100), nullable=False)
	last_name = db.Column(db.String(100), nullable=False)
	email = db.Column(db.String(100), nullable=False)
	gender = db.Column(db.String(100), nullable=False)
	ip_address = db.Column(db.String(100), nullable=False)

	def __repr__(self):
		return f'Contact(First Name = {self.first_name}, Last Name = {self.last_name}, email = {self.email}, gender = {self.gender}, IP Address = {self.ip_address})'


def read_json():
	with open('MOCK_DATA.json', 'r') as f:
		lines = list(f)
		content = ''.join(lines)
		data = json.loads(content)
	return data


def add_initial_entries():
	entries = read_json()
	for entry in entries:
		id, first_name, last_name, email, gender, ip_address = (entry['id'], entry['first_name'], entry['last_name'], entry['email'], entry['gender'], entry['ip_address'])
		crudOperation.put(id=id, first_name=first_name, last_name=last_name, email=email, gender=gender, ip_address=ip_address)


@app.route('/', methods=['GET'])
def index():
	contacts = Contact.query.all()
	return render_template('index.html', contacts=contacts)


@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
	if request.form:
		contact = request.form
		id, first_name, last_name, email, gender, ip_address = contact.get('id'), contact.get('firstName'), contact.get('lastName'), contact.get('email'), contact.get('gender'), contact.get('ipAddress')
		contact, status_code = crudOperation.put(id=id, first_name=first_name, last_name=last_name, email=email, gender=gender, ip_address=ip_address)
		return render_template('addContact.html', contact=contact, status_code=status_code)
	return render_template('addContact.html')


@app.route('/contact/<contact_id>/delete', methods=['GET', 'POST'])
def delete_contact(contact_id):
	if request.method == 'POST':
		contact, status_code = crudOperation.delete(contact_id)
		return render_template('deleteContact.html', contact=contact, status_code=status_code)
	if request.method == 'GET':
		contact, status_code = crudOperation.get(contact_id)
		return render_template('deleteContact.html', contact=contact)


@app.route('/contact/<contact_id>/', methods=['GET'])
def get_contact(contact_id):
	contact = crudOperation.get(contact_id)
	if contact:
		return render_template('getContact.html', contact=contact)


@app.route('/contact/<contact_id>/edit', methods=['GET', 'POST'])
def edit_contact(contact_id):
	if request.method == 'GET':
		contact, status_code = crudOperation.get(contact_id)
		return render_template('editContact.html', contact=contact)
	if request.method == 'POST':
		if request.form:
			contact = request.form
			first_name, last_name, email, gender, ip_address = contact.get('firstName'), contact.get('lastName'), contact.get('email'), contact.get('gender'), contact.get('ipAddress')
			contact, status_code = crudOperation.patch(id=contact_id, first_name=first_name, last_name=last_name, email=email, gender=gender, ip_address=ip_address)
			return render_template('editContact.html', contact=contact, status_code=status_code)


class ContactCRUDOperations:
	def get(self, id):
		result = Contact.query.filter_by(id=id).first()
		if not result:
			abort(404, message='Could not find a contact with that id')
		return result, 200

	def put(self, id, first_name, last_name, email, gender, ip_address):
		contact = Contact(id=id, first_name=first_name, last_name=last_name, email=email, gender=gender, ip_address=ip_address)
		contact_exists = Contact.query.filter_by(id=id).first()
		if contact_exists:
			return None, 409
		try:
			db.session.add(contact)
			db.session.commit()
		except:
			return None, 400
		return contact, 200


	def patch(self, id, first_name, last_name, email, gender, ip_address):
		contact = Contact.query.filter_by(id=id).first()
		if not contact:
			abort(404, message='Contact does not exist, cannot update')

		try:
			if first_name:
				contact.first_name = first_name
			if last_name:
				contact.last_name = last_name
			if email:
				contact.email = email
			if gender:
				contact.gender = gender
			if ip_address:
				contact.ip_address = ip_address

			db.session.commit()
		except:
			return contact, 400

		return contact, 200


	def delete(self, id):
		contact = Contact.query.filter_by(id=id).first()
		if not contact:
			abort(404, message='Contact does not exist, cannot delete')
		try:
			Contact.query.filter_by(id=id).delete()
			# db.session.delete(contact)
			db.session.commit
		except:
			return contact, 400
		return contact, 204

crudOperation = ContactCRUDOperations()
add_initial_entries()

if __name__ == '__main__':
	app.run(debug=True)
