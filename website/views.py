import json
from flask import Blueprint, render_template, request, flash, jsonify
from .models import *

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def index():
    employee_list = Employee.query.all()
    return render_template('index.html', employee_list = employee_list)

@views.route('/all_logs')
def all_logs():
    logs = Log.query.all()
    return render_template('all_logs.html', logs=logs)


@views.route('/group_logs')
def group_logs():
    logs_dict = db.session.query(Employee.name, Employee.card_id, func.count(Log.id)).join(Employee, Log.card_id == Employee.card_id).group_by(Employee.name).all()
    print(logs_dict)
    return render_template('group_logs.html', logs=logs_dict)


@views.route('/logs/<card_id>')
def logs():
    card_id = request.args.get('card_id')
    employee = Employee.query.filter_by(card_id=card_id).first()
    if employee:
        logs = Log.query.filter_by(card_id=card_id).all()
        return render_template('logs.html', logs=logs)
    else:
        return 'Employee not found'

@views.route('/logs/avg/<card_id>')
def avg():
    card_id = request.args.get('card_id')
    employee = Employee.query.filter_by(card_id=card_id).first()
    if employee:
        logs = Log.query.filter_by(card_id=card_id).all()

        

        return render_template('avgs.html', logs=logs)
    else:
        return 'Employee not found'