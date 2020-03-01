#-*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import time
import requests
import json
import keys
from filters import *


def send(booking):
    url = "https://sens.apigw.ntruss.com"
    uri = "/sms/v2/services/" + keys.service_id + "/messages"
    api_url = url + uri
    timestamp = str(int(time.time() * 1000))
    access_key = keys.access_key
    string_to_sign = "POST " + uri + "\n" + timestamp + "\n" + access_key
    signature = make_signature(string_to_sign)

    # 예약내역 불러와서 변환
    phone = booking['phone'].replace("-", "")
    name = booking['name']
    booking_date = format_datetime(booking['date'])

    message = "{}님 bernini 예약이 승인되었습니다.\n예약일자: {}".format(name, booking_date)

    headers = {
        'Content-Type': "application/json; charset=UTF-8",
        'x-ncp-apigw-timestamp': timestamp,
        'x-ncp-iam-access-key': access_key,
        'x-ncp-apigw-signature-v2': signature
    }

    body = {
        "type": "SMS",
        "contentType": "COMM",
        "from": "01096876488",
        "content": message,
        "messages": [{"to": phone}]
    }

    body = json.dumps(body)

    response = requests.post(api_url, headers=headers, data=body)
    # print(response.json())
    response.raise_for_status()


def make_signature(string):
    secret_key = bytes(keys.secret_key, 'UTF-8')
    string = bytes(string, 'UTF-8')
    string_hmac = hmac.new(secret_key, string, digestmod=hashlib.sha256).digest()
    string_base64 = base64.b64encode(string_hmac).decode('UTF-8')
    return string_base64