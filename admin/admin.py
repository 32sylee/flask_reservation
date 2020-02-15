from flask import Blueprint, render_template

admin_api = Blueprint('admin_api', __name__, template_folder='templates')

@admin_api.route('')
def booklist():
    return render_template('main.html')