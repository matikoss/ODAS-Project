from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from . import limiter
from flask_login import login_user, logout_user, login_required
from .models import User
from .utils import form_validation, pass_hash

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
@limiter.limit("1 per second")
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not form_validation.check_email_pattern(email):
        flash('Invalid login details', 'warning')
        return redirect(url_for('main.start'))

    if not form_validation.check_password_chars(password):
        flash('Invalid login details')
        return redirect(url_for('main.start'))

    user = User.query.filter_by(email=email).first()

    if not user:
        pass_hash.get_hashed_password('dummyPassword1!')
        flash('Invalid login details', 'warning')
        return redirect(url_for('main.start'))

    if not pass_hash.check_password(password, user.password):
        flash('Invalid login details', 'warning')
        return redirect(url_for('main.start'))

    login_user(user)

    return redirect(url_for('user.home'))


@auth.route('/signup', methods=['POST'])
def signup():
    errors = False
    email = request.form.get('email')
    name = request.form.get('username')
    password = request.form.get('password')

    if not form_validation.check_username_length(name):
        errors = True
        flash('Username is too short! (min. 3 characters)', 'warning')

    if not form_validation.check_password_length(password):
        errors = True
        flash('Password is too short! (min. 8 characters)', 'warning')

    if not form_validation.check_username_chars(name):
        errors = True
        flash('Username contains forbidden characters. (Only acceptable: letters, numbers and #!_@().$=+*-[]^?&%)',
              'warning')

    if not form_validation.check_password_chars(password):
        errors = True
        flash(
            'Password contains forbidden characters. (Only acceptable: letters, numbers and {}#,!_@().:;`$=+-*[]^?&%)',
            'warning')

    if not form_validation.check_password_if_contains_required_chars(password):
        errors = True
        flash(
            'Password must contain at least one upper case letter, one lower case letter, one digit and one special character (#?!@$%^&*-)',
            'warning')

    if not form_validation.check_email_pattern(email):
        errors = True
        flash('Wrong email address format!', 'warning')

    if errors:
        return redirect(url_for('main.start'))

    is_username_taken = User.query.filter_by(name=name).first()

    if is_username_taken:
        flash('Username is already taken.', 'warning')
        return redirect(url_for('main.start'))

    user = User.query.filter_by(email=email).first()

    if user:
        flash('User with this email already exists.', 'warning')
        return redirect(url_for('main.start'))

    new_user = User(email=email, name=name, password=pass_hash.get_hashed_password(password))
    db.session.add(new_user)
    db.session.commit()

    flash('Account created. Now you can sign in.', 'success')
    return redirect(url_for('main.start'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.start'))
