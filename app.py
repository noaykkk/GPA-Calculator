from __future__ import division

import json
from flask import Flask, url_for, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import sqlite3

app = Flask(__name__)
app.cinfig['SERVER_NAME'] = 'https://the-gpa-calculator-noay.herokuapp.com/'
app.secret_key = 'Secret Key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sql/Course.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.String(20))
    credit_hours = db.Column(db.Float)
    grade = db.Column(db.String(3))
    quality_points = db.Column(db.Float)

    def __init__(self, course_id, credit_hours, grade, quality_points):
        self.course_id = course_id
        self.credit_hours = credit_hours
        self.grade = grade
        self.quality_points = quality_points


@app.route('/')
def home():
    all_info = Course.query.all()
    if Course.query.first():
        gpa = calculator()
    else:
        gpa = -1
    return render_template('home.html', Course=all_info, GPA=gpa)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        course_id = request.form['course_id']
        credit_hours = request.form['credit_hours']
        grade = request.form['grade']
        quality_points = qua_point_calculate(grade, credit_hours)
        insert_data = Course(course_id, credit_hours, grade, quality_points)
        db.session.add(insert_data)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    delete_data = Course.query.get(id)
    db.session.delete(delete_data)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/update/', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        update_id = request.form.get('id')
        update_data = Course.query.get(update_id)
        update_data.course_id = request.form['course_id_update']
        update_data.credit_hours = request.form['credit_hours_update']
        update_data.grade = request.form['grade_update']
        update_data.quality_points = qua_point_calculate(update_data.grade, update_data.credit_hours)
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))


def calculator():
    total_hours = db.session.query(func.sum(Course.credit_hours)).scalar()
    points_counter = float(total_hours) * 4
    total_qua_points = db.session.query(func.sum(Course.quality_points)).scalar()
    gpa = float(total_qua_points) / float(points_counter) * 4
    gpa = float("{:.2f}".format(gpa))
    return gpa


def qua_point_calculate(grade, credit_hours):
    quality_points = float
    if grade == 'A':
        quality_points = float(credit_hours) * 4
    elif grade == 'B':
        quality_points = float(credit_hours) * 3
    elif grade == 'C':
        quality_points = float(credit_hours) * 2
    elif grade == 'D':
        quality_points = float(credit_hours) * 1
    elif grade == 'F':
        quality_points = float(credit_hours) * 0

    return quality_points


if __name__ == '__main__':
    app.run()
