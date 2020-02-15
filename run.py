from flask import Flask, render_template, jsonify, request
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
from filters import *

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.bernini

# jinja2 필터함수 등록
app.jinja_env.filters['datetime'] = format_datetime

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/book')
def book():
    dates = list(db.date.find({}, {'_id': 0}).sort("date", 1))
    times = list(db.time.find({}, {'_id': 0}).sort("time", 1))

    return render_template('book.html', dates=dates, times=times)


@app.route('/chkguest')
def chkguest():
    return render_template('chkguest.html')


@app.route('/bookdone')
def bookdone():
    return render_template('bookdone.html')


@app.route('/booklist', methods=['POST'])
def booklist():
    name_receive = request.form['name']
    phone_receive = request.form['phone']

    bookings = list(db.booking.find({'name': name_receive, 'phone': phone_receive}).sort("date", -1))

    for i in range(len(bookings)):
        if bookings[i]['status'] == 0:
            bookings[i]['status_str'] = "예약신청중"

        elif bookings[i]['status'] == 1:

            # 현재 날짜의 00:00 계산
            now = datetime.today()
            today = datetime(now.year, now.month, now.day)

            if bookings[i]['date'] >= today:
                bookings[i]['status_str'] = "예약승인"
            else:
                bookings[i]['status_str'] = "이용완료"

        elif bookings[i]['status'] == 2:
            bookings[i]['status_str'] = "예약취소"

    return render_template('booklist.html', name=name_receive, phone=phone_receive, bookings=bookings)


@app.route('/makebook', methods=['POST'])
def makebook():
    date_receive = datetime.strptime(request.form['date'], "%Y-%m-%d")
    time_receive = request.form['time']
    count_receive = int(request.form['count'])
    name_receive = request.form['name']
    phone_receive = request.form['phone']

    db.booking.insert_one(
        {'date': date_receive,
         'time': time_receive,
         'count': count_receive,
         'name': name_receive,
         'phone': phone_receive,
         'status': 0,  # 0: 예약신청중, 1: 예약승인, 2: 예약취소
         })

    return jsonify({'result': 'success'})

@app.route('/cancelbook', methods=['POST'])
def cancelbook():
    id = ObjectId(request.form['id'])

    update_result = db.booking.update_one({'_id': id}, {'$set': {'status': 2}}).raw_result

    if update_result:
        result = 'success'
    else:
        result = 'fail'

    return jsonify({'result': result})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
