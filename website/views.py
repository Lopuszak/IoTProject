import json
from wtforms.fields import DateField
from wtforms import validators, SubmitField
from flask import Blueprint, render_template, request, flash, jsonify
from flask_wtf import FlaskForm
from .models import *

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@views.route('/logs')
def logs():
    card_id = request.args.get('card_id')
    employee = Employee.query.filter_by(card_id=card_id).first()
    if employee:
        logs = Log.query.filter_by(card_id=card_id).all()
        return render_template('logs.html', logs=logs)
    else:
        return 'Employee not found'