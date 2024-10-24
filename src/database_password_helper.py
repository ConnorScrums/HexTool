"""
Password Salting, Hashing and
Verification
"""

import hashlib
import os
from dotenv import load_dotenv


class DatabasePasswordHelper:
    """
    Handle Password Salting,
    Hashing and Verification
    """

    def hash_password(self, password):
        """Password Salting and Hashing"""
        load_dotenv()
        password_hash = hashlib.sha256(
            (password + os.getenv("PW_SALT")).encode("utf-8")
        ).hexdigest()
        return password_hash

    def verify_password(self, stored_password, provided_password):
        """Password Verification for login"""
        load_dotenv()
        password_hash = hashlib.sha256(
            (provided_password + os.getenv("PW_SALT")).encode("utf-8")
        ).hexdigest()
        return password_hash == stored_password
