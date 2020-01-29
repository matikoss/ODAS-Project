from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import User
from .models import Note
from .utils import form_validation, pass_hash
from . import db

user = Blueprint('user', __name__)


@user.route('/user/home')
@login_required
def home():
    return render_template('user-home.html', name=current_user.name)


@user.route('/user/notes/public')
@login_required
def public_notes():
    notes = load_public_notes()
    return render_template('user-public-notes.html', notes=notes)


@user.route('/user/notes/private')
@login_required
def my_notes():
    notes = load_private_notes()
    return render_template('user-private-notes.html', notes=notes)


@user.route('/user/notes/private', methods=['POST'])
@login_required
def post_note():
    errors = False
    title = request.form.get('new_note_title')
    text = request.form.get('new_note_text')
    is_public = request.form.get('public_input')
    if is_public == 'true':
        public = True
    else:
        public = False

    if len(title) <= 0:
        errors = True
        flash("Title can't be empty", "warning")

    if len(title) > 150:
        errors = True
        flash("Title can't be longer than 150 characters", "warning")

    if len(text) <= 0:
        errors = True
        flash("Note content can't be empty", "warning")

    if len(text) > 500:
        errors = True
        flash("Note can't be longer than 500 characters", "warning")

    if errors:
        return redirect(url_for('user.my_notes'))

    new_note = Note(title=title, text=text, owner_mail=current_user.email, owner_name=current_user.name,
                    is_public=public)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('user.my_notes'))


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

    if not form_validation.check_username_chars(new_password):
        flash(
            'New password contains forbidden characters. (Only acceptable: letters, numbers and {}#,!_@().:;`$=+-*[]^?&%)',
            'warning')
        return redirect(url_for('user.profile'))

    if not form_validation.check_password_if_contains_required_chars(new_password):
        flash(
            'New password must contain at least one upper case letter, one lower case letter, one digit and one special character (#?!@$%^&*-)',
            'warning')
        return redirect(url_for('user.profile'))

    user_logged = User.query.filter_by(email=email).first()

    if not pass_hash.check_password(current_password, user_logged.password):
        flash('Invalid password.', 'warning')
        return redirect(url_for('user.profile'))

    setattr(user_logged, 'password', pass_hash.get_hashed_password(new_password))
    db.session.commit()
    flash('Password changed successfully!', 'success')
    return redirect(url_for('user.profile'))


def load_private_notes():
    email = current_user.email
    notes = Note.query.filter_by(owner_mail=email)
    return notes


def load_public_notes():
    notes = Note.query.filter_by(is_public=True)
    return notes
