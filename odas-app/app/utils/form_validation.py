import re
import string


def check_username_length(username: str):
    if len(username) < 3:
        return False
    return True


def check_password_length(password: str):
    if len(password) < 8:
        return False
    return True


def check_password_chars(password: str):
    pass_regex = re.compile(r"[A-Za-z0-9{}#,!_@():;.`$=+*\-\[\]^?&%]+$")
    if not re.match(pass_regex, password):
        return False
    return True


def check_email_length(email: str):
    if len(email) < 5:
        return False
    return True


def check_email_pattern(email: str):
    email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
    if not re.match(email_regex, email):
        return False
    return True
