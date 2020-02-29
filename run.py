from flask import Flask
from filters import *
from blueprints.admin import admin_api
from blueprints.user import user_api

app = Flask(__name__)

# blueprint 등록
app.register_blueprint(admin_api, url_prefix='/admin')
app.register_blueprint(user_api, url_prefix='')

# jinja2 필터함수 등록
app.jinja_env.filters['datetime'] = format_datetime


if __name__ == '__main__':
    app.secret_key = "123"
    app.run('0.0.0.0', port=5000, debug=True)
