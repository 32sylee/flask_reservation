from datetime import datetime
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.bernini

# db.booking.insert_one(
#     {'date': datetime(2020, 2, 11, 0, 0, 0),
#      'booking_list':
#          {
#              'time': '12:00',
#              'name': '홍길동',
#              'num': 2,
#              'phone': '010-9687-6488',
#              'state': 1    # 0: 예약신청중, 1: 예약완료, 2: 예약취소
#          }
#      })

# db.date.insert_one({'date': datetime(2020, 2, 11)})
# db.date.insert_one({'date': datetime(2020, 2, 12)})
# db.date.insert_one({'date': datetime(2020, 2, 12)})
# db.date.insert_one({'date': datetime(2020, 2, 13)})
# db.date.insert_one({'date': datetime(2020, 2, 14)})
# db.date.insert_one({'date': datetime(2020, 2, 15)})
# db.date.insert_one({'date': datetime(2020, 2, 16)})
# db.date.insert_one({'date': datetime(2020, 2, 17)})
# db.date.insert_one({'date': datetime(2020, 2, 18)})
# db.date.insert_one({'date': datetime(2020, 2, 19)})
# db.date.insert_one({'date': datetime(2020, 2, 20)})

# db.time.insert_one({'time': '11:00'})
# db.time.insert_one({'time': '11:30'})
# db.time.insert_one({'time': '12:00'})
# db.time.insert_one({'time': '12:30'})
# db.time.insert_one({'time': '13:00'})
# db.time.insert_one({'time': '13:30'})
# db.time.insert_one({'time': '14:00'})
# db.time.insert_one({'time': '17:00'})
# db.time.insert_one({'time': '17:30'})
# db.time.insert_one({'time': '18:00'})
# db.time.insert_one({'time': '18:30'})
# db.time.insert_one({'time': '19:00'})
# db.time.insert_one({'time': '19:30'})
# db.time.insert_one({'time': '20:00'})
# db.time.insert_one({'time': '20:30'})