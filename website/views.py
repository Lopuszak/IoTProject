from datetime import date, timedelta
import json
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from .models import *

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        if "search_id" in request.form:
            id = request.form['search_id']
            return redirect('/logs/'+str(id))
        else:
            new_name = request.form['employee_name']
            print(new_name)
            employee_id = request.form['employee_id']
            if len(new_name) < 1 or new_name is None:
                flash('Name is too short!', category='error')
            else:

                employee = Employee.query.filter_by(card_id=employee_id).first()
                employee.name = new_name
                db.session.commit()

    employee_list = Employee.query.all()
    return render_template('index.html', employee_list = employee_list)

@views.route('/all_logs', methods=['GET', 'POST'])
def all_logs():
    logs = Log.query.all()
    if request.method == 'POST':
        print(request.form)
        if request.form["time"] == "today":
            search = "%{}%".format(date.today().strftime("%Y-%m-%d"))
            logs = Log.query.filter(Log.time.ilike(search)).all()
        elif request.form["time"] == "yesterday":
            search = "%{}%".format((date.today() - timedelta(1)).strftime("%Y-%m-%d"))
            print(search)
            logs = Log.query.filter(Log.time.ilike(search)).all()
        elif request.form["time"] == "this_month":
            search = "%{}%".format(date.today().strftime("%Y-%m"))
            logs = Log.query.filter(Log.time.ilike(search)).all()
        elif request.form["time"] == "prev_month":
            search = "%{}%".format((date.today()- timedelta(31)).strftime("%Y-%m"))
            logs = Log.query.filter(Log.time.ilike(search)).all()
        elif request.form["time"] == "this_year":
            search = "%{}%".format(date.today().strftime("%Y"))
            logs = Log.query.filter(Log.time.ilike(search)).all()
            
    return render_template('all_logs.html', logs=logs)


@views.route('/group_logs')
def group_logs():
    logs_dict = db.session.query(Employee.name, Employee.card_id, func.count(Log.id)).join(Employee, Log.card_id == Employee.card_id).group_by(Employee.name).all()
    print(logs_dict)
    return render_template('group_logs.html', logs=logs_dict)


@views.route('/logs/<employee_id>', methods=['GET', 'POST'])
def logs(employee_id):
    employee = Employee.query.filter_by(card_id=employee_id).first()
    if employee:
        logs = Log.query.filter_by(card_id=employee_id).all()
        if request.method == 'POST':
            print(request.form)
            if request.form["time"] == "today":
                search = "%{}%".format(date.today().strftime("%Y-%m-%d"))
                logs = Log.query.filter(Log.time.ilike(search)).filter_by(card_id=employee_id).all()
            elif request.form["time"] == "yesterday":
                search = "%{}%".format((date.today() - timedelta(1)).strftime("%Y-%m-%d"))
                print(search)
                logs = Log.query.filter(Log.time.ilike(search)).all()
            elif request.form["time"] == "this_month":
                search = "%{}%".format(date.today().strftime("%Y-%m"))
                logs = Log.query.filter(Log.time.ilike(search)).all()
            elif request.form["time"] == "prev_month":
                search = "%{}%".format((date.today()- timedelta(31)).strftime("%Y-%m"))
                logs = Log.query.filter(Log.time.ilike(search)).all()
            elif request.form["time"] == "this_year":
                search = "%{}%".format(date.today().strftime("%Y"))
                logs = Log.query.filter(Log.time.ilike(search)).all()
                
        return render_template('logs.html', logs=logs)
    else:
        return 'Employee not found'

@views.route('/logs/avg/<card_id>')
def avg(card_id):
    card_id = request.args.get('card_id')
    card_id = '<Employee '+str(card_id)+'>'
    employee = Employee.query.filter_by(card_id=card_id).first()
    if employee:
        logs = Log.query.filter_by(card_id=card_id).all()

        

        return render_template('avg.html', logs=logs)
    else:
        return 'Employee not found'
