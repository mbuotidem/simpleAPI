# Contacts API app

## Description
This app I created stores contact information of people including their first and last name, email address, gender, and their IP address.
This app allows the user to perform CRUD operations on JSON data retrieved from https://www.mockaroo.com./

## Screenshots

![Alt text](https://i.postimg.cc/jSfWZC90/Contacts-overview.png "Contact Overview")
![Alt text](https://i.postimg.cc/rF3015fN/Edit-Contacts.png "Edit Contact")
![Alt text](https://i.postimg.cc/gdpygd0Y/Add-Contacts.png "Add Contact")
![Alt text](https://i.postimg.cc/SNJYYgfK/Delete-contacts.png "Delete Contact")


## Instructions
1. Clone this repo
2. Install the necessary requirements by running:
### You may wish to activate virualenv before this, but it is not necessary
```
pip3 install -r requirements.txt
```
3. Set up local database by running the following command:
```
python3
>>> from contact import db
>>> db.create_all()
>>> exit()
```
4. Run main.py 

```
python3 main.py
```
5. Navigate to "localhost:5000" the initial run automatically fetches all the data from `MOCK_DATA.json`
You should see 1000 records here.
