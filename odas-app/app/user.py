from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User
from .utils import form_validation, pass_hash
from . import db

user = Blueprint('user', __name__)


@user.route('/user/home')
@login_required
def home():
    return render_template('user-home.html', name=current_user.name)


@user.route('/user/notes')
@login_required
def public_notes():
    return render_template('user-public-notes.html')


@user.route('/user/notes/private')
@login_required
def my_notes():
    return render_template('user-private-notes.html')


@user.route('/user/profile')
@login_required
def profile():
    return render_template('user-profile.html', name=current_user.name, email=current_user.email)


@user.route('/user/profile/changepassword', methods=['POST'])
@login_required
def changepassword():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    email = current_user.email

    if not form_validation.check_password_length(new_password):
        flash('New password is too short. (min. 8 characters)', 'warning')
        return redirect(url_for('user.profile'))

    user_logged = User.query.filter_by(email=email).first()

    if not pass_hash.check_password(current_password, user_logged.password):
        flash('Invalid password.', 'warning')
        return redirect(url_for('user.profile'))

    setattr(user_logged, 'password', pass_hash.get_hashed_password(new_password))
    db.session.commit()
    flash('Password changed successfully!', 'success')
    return redirect(url_for('user.profile'))
