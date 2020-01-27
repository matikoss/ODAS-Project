import bcrypt


def get_hashed_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))


def check_password(password: str, hashed_pass):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_pass)
