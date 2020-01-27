from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def start():
    return render_template('start.html')


# @main.route('/profile')
# @login_required
# def profile():
#     return render_template('user-home.html', name=current_user.name)
