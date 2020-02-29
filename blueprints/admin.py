import json

from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from pymongo import MongoClient

from filters import *
from functions import *
from datetime import timedelta
from bson.objectid import ObjectId

admin_api = Blueprint('admin_api', __name__, template_folder='templates/admin')

# MongoDB 연결
client = MongoClient('localhost', 27017)
db = client.bernini


@admin_api.route('/login', methods=['GET'])
def login():
    if request.args.get('next'):
        next = request.args.get('next')
    else:
        next = "booklist"
    return render_template('admin/login.html', next=next)


@admin_api.route('/booklist', methods=['GET'])
def booklist():
    if not session.get('logged_in'):
        return redirect(url_for('admin_api.login', next=request.full_path))

    today = get_today()

    id = ObjectId(request.args.get('id'))
    status = 3

    if request.args.get('id') is not None:
        bookings = []
        bookings.append(db.booking.find_one({'_id': id}))
    else:
        condition = {'date': {'$gte': today}}

        if request.args.get('status'):
            status = int(request.args.get('status'))
            # status가 0,1,2인 경우만 condition에 추가
            if status < 3:
                condition['status'] = status

        bookings = list(db.booking.find(condition).sort('_id', -1))

    # 예약상태 구하기
    for i in range(len(bookings)):
        if bookings[i]['status'] == 0:
            bookings[i]['status_str'] = "예약신청중"

        elif bookings[i]['status'] == 1:

            if bookings[i]['date'] >= today:
                bookings[i]['status_str'] = "예약승인"
            else:
                bookings[i]['status_str'] = "이용완료"

        elif bookings[i]['status'] == 2:
            bookings[i]['status_str'] = "예약취소"

    return render_template('admin/booklist.html', bookings=bookings, id=request.args.get('id'), status=status)


@admin_api.route('/settingdate')
def settingdate():
    if not session.get('logged_in'):
        return redirect(url_for('admin_api.login', next=request.full_path))

    today = get_today()
    dates = list(db.date.find({'date': {'$gte': today}}).sort('date', 1))

    return render_template('admin/settingdate.html', dates=dates)


@admin_api.route('/datebook', methods=['GET'])
def datebook():
    if not session.get('logged_in'):
        return redirect(url_for('admin_api.login', next=request.full_path))

    if request.args.get('date') is None:
        date = get_today()
        selected_date = datetime.strftime(date, "%Y-%m-%d")
    else:
        selected_date = request.args.get('date')
        date = datetime.strptime(selected_date, "%Y-%m-%d")

    today = get_today()
    dates = list(db.date.find({'date': {'$gte': today}}).sort('date', 1))

    bookings = list(db.booking.find({'date': date, 'status': {'$lte': 1}}).sort('time', 1))

    # 예약상태 구하기
    for i in range(len(bookings)):
        if bookings[i]['status'] == 0:
            bookings[i]['status_str'] = "예약신청중"

        elif bookings[i]['status'] == 1:
            bookings[i]['status_str'] = "예약승인"

    return render_template('admin/datebook.html', bookings=bookings, dates=dates, selected_date=selected_date)


@admin_api.route('/adddate', methods=['POST'])
def adddate():
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    inserted_date = datetime.strptime(start_date, "%Y-%m-%d")
    convert_end_date = datetime.strptime(end_date, "%Y-%m-%d")
    while inserted_date <= convert_end_date:
        # 기존에 있던 날짜가 아닐 때만 insert
        if not db.date.find({'date': inserted_date}).count():
            db.date.insert_one({'date': inserted_date})
        inserted_date += timedelta(days=1)
    return jsonify({'result': 'success'})


@admin_api.route('/deletedate', methods=['POST'])
def deletedate():
    delete_dates = json.loads(request.form['delete_dates'])
    for date in delete_dates:
        date_id = ObjectId(date)
        db.date.remove({'_id': date_id})
    return jsonify({'result': 'success'})


@admin_api.route('/approve', methods=['POST'])
def approve():
    booking_id = ObjectId(request.form['booking_id'])
    db.booking.update_one({'_id': booking_id}, {'$set': {'status': 1}})
    return jsonify({'result': 'success'})


@admin_api.route('/cancel', methods=['POST'])
def cancel():
    booking_id = ObjectId(request.form['booking_id'])
    db.booking.update_one({'_id': booking_id}, {'$set': {'status': 2}})
    return jsonify({'result': 'success'})


@admin_api.route('/login-chk', methods=['POST'])
def login_chk():
    id = request.form['id']
    password = request.form['password']
    result = db.admin.find_one({'id': id, 'password': password})

    if result is None:
        return jsonify({'result': 'fail'})
    else:
        session['logged_in'] = True
        return jsonify({'result': 'success'})


@admin_api.route('/logout', methods=['POST'])
def logout():
    session['logged_in'] = False
    return jsonify({'result': 'success'})