import json

from flask import Blueprint, render_template, jsonify, request
from pymongo import MongoClient
from filters import *
from datetime import timedelta
from bson.objectid import ObjectId

admin_api = Blueprint('admin_api', __name__, template_folder='templates/admin')

# MongoDB 연결
client = MongoClient('localhost', 27017)
db = client.bernini

@admin_api.route('/booklist')
def booklist():
    # 현재 날짜의 00:00 계산
    now = datetime.today()
    today = datetime(now.year, now.month, now.day)

    bookings = list(db.booking.find({'date': {'$gte': today}}).sort('_id', -1))

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

    return render_template('admin/booklist.html', bookings=bookings)

@admin_api.route('/settingdate')
def settingdate():
    # 현재 날짜의 00:00 계산
    now = datetime.today()
    today = datetime(now.year, now.month, now.day)

    dates = list(db.date.find({'date': {'$gte': today}}).sort('date', 1))

    return render_template('admin/settingdate.html', dates=dates)

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