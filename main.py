from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert 

from flask import render_template, redirect, url_for, flash,  session
from werkzeug.security import check_password_hash

from user.user_operations import Labour
from user.admin_operations import Admin
from user.SM_operations import Salesmanager 
from datetime import datetime

import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:15182418@localhost/theoffice'
db = SQLAlchemy(app)

# Route to display the HTML form
class sales_manager_table(db.Model):
    __tablename__='sales_manager'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False) #(hidden login ids)
    # password = db.Column(db.String(60), nullable=False) #encryption
    area = db.Column(db.String(150), unique=False, nullable=False)


class labour_table(db.Model):
    __tablename__='labour'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    area = db.Column(db.String(150), unique=False, nullable=False)
    # sales_manager = db.Column(db.Integer, unique=False, nullable=False)

class check_in_time(db.Model):
    __tablename__='check_in_time'
    id = db.Column(db.Integer, primary_key=True)
    in_time = db.Column(db.DateTime, nullable=False)
    out_time=db.Column(db.DateTime, nullable=False)

class task_table(db.Model):
    __tablename__='tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(120), unique=True, nullable=False)
    assigned_labour = db.Column(db.Integer, unique=False, nullable=False)

class admin_table(db.Model):
    __tablename__='admin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

class human_resource_table(db.Model):
    __tablename__='human_resource'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Creating admin account
    db.session.execute(insert(admin_table).values(username="harshit", password="admin"))
    db.session.commit()
    

# Routing 
@app.route('/' )
def login_page():
    return render_template('login_page.html')

#login page 
@app.route('/login', methods=['GET','POST'])
def authenticator():
    if request.method == "POST":
        username = request.form['admin_username']
        password = request.form['admin_password']
        a = Admin(db, admin_table)
        if a.authorize_user(username, password):
            return redirect("/dashboard")

        return redirect("/")

    return redirect('/')
       

@app.route('/dashboard')
def dashboard():
    l = Labour(db, labour_table)
    s = Salesmanager(db, sales_manager_table)
    labour_data = l.GetAll()
    sm_data = s.GetAll()
    print("Render Data")

    return render_template("dashboard.html", data={"labour_data": labour_data, "sm_data": sm_data})


@app.route('/dashboard/delete_salemanager', methods=['GET','POST'])

def delete_SM():
    if request.method == "POST":
        data_dict = json.loads(request.data.decode('utf-8'))
        deleteID = data_dict["id"]
        sm = Salesmanager(db , sales_manager_table).Delete(id=deleteID)
        return render_template('/dashboard')

    return render_template("salesmanagerform.html")

@app.route('/dashboard/create_salemanager', methods=['GET','POST'])
def create_SM():
    if request.method == "POST":
        name = request.form['name']
        area = request.form['options']
        sm = Salesmanager(db , sales_manager_table).Create(name , area)
        return redirect('/dashboard')

    return render_template("salesmanagerform.html")

@app.route('/dashboard/delete_labour', methods=['GET','POST'])
def delete_labour():
    if request.method == "POST":
        data_dict = json.loads(request.data.decode('utf-8'))
        deleteID = data_dict["id"]
        l = Labour(db , labour_table).Delete(id=deleteID)
        return render_template('/dashboard')

    return render_template("labourform.html")

@app.route('/dashboard/create_labour', methods=['GET','POST'])
def create_labour():
    if request.method == "POST":
        name = request.form['name']
        area = request.form['options']
        sm = Labour(db , labour_table).Create(name , area)
        return redirect('/dashboard')

    return render_template("labourform.html")

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Route to handle the form submission and insert data into the database
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')
    
    return "Failed to connect to the database."

if __name__ == "__main__":
    app.run(debug=True)




