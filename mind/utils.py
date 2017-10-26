import base64
import hashlib

from flask import current_app


def hash_email(email, salt=None):
    if salt is None:
        salt = current_app.config['EMAIL_HASH_SALT']
    h = hashlib.sha256()
    h.update(email.encode('utf-8'))
    h.update(salt.encode('utf-8'))
    return base64.b85encode(h.digest()).decode('utf-8')
