import json
from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from .models import *
from datetime import datetime, timedelta, date

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        if "search_id" in request.form:
            id = request.form['search_id']
            return redirect('/logs/' + str(id))
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
    return render_template('index.html', employee_list=employee_list)


@views.route('/all_logs')
def all_logs():
    logs = Log.query.all()
    return render_template('all_logs.html', logs=logs)


@views.route('/group_logs')
def group_logs():
    logs_dict = db.session.query(Employee.name, Employee.card_id, func.count(Log.id)).join(Employee,
                                                                                           Log.card_id == Employee.card_id).group_by(
        Employee.name).all()
    print(logs_dict)
    return render_template('group_logs.html', logs=logs_dict)


@views.route('/logs/<employee_id>')
def logs(employee_id):
    employee = Employee.query.filter_by(card_id=employee_id).first()
    if employee:
        logs = Log.query.filter_by(card_id=employee_id).all()
        return render_template('logs.html', logs=logs)
    else:
        return 'Employee not found'


@views.route('/logs/avg/<card_id>')
def avg(card_id):
    card_id = request.args.get('card_id')
    card_id = '<Employee ' + str(card_id) + '>'
    employee = Employee.query.filter_by(card_id=card_id).first()
    if employee:
        logs = Log.query.filter_by(card_id=card_id).all()
        return render_template('avg.html', logs=logs)
    else:
        return 'Employee not found'


@views.route('/average_daily_work_time_and_total_days/<employee_id>', methods=['GET'])
def average_daily_work_time_and_total_days(employee_id):
    logs = Log.query.filter_by(card_id=employee_id).order_by(Log.time).all()
    work_time_by_day = {}
    current_day = None
    time_in = None
    for log in logs:
        log_time = datetime.strptime(log.time, '%Y-%m-%d %H:%M:%S.%f')

        if current_day is None or current_day != log_time.date():
            current_day = log_time.date()
            time_in = None

        if time_in is None:
            time_in = log_time.time()
        else:
            time_out = log_time.time()
            if current_day in work_time_by_day:
                work_time_by_day[current_day] += datetime.combine(date.today(), time_out) - datetime.combine(date.today(), time_in)
            else:
                work_time_by_day[current_day] = datetime.combine(date.today(), time_out) - datetime.combine(date.today(), time_in)
            time_in = None

    total_work_time = timedelta()
    for day in work_time_by_day:
        total_work_time += work_time_by_day[day]
    average_work_time = total_work_time / len(work_time_by_day)

    return jsonify(average_work_time=str(average_work_time), total_days=str(len(work_time_by_day)))
