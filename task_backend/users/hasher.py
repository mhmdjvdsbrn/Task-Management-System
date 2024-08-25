"""
Django uses a very complex algorithm to hash user passwords by default.
In this project, I changed Django's default password hashing to a simple SHA-256 hash.
"""

from django.contrib.auth.hashers import BasePasswordHasher
from django.utils.crypto import constant_time_compare, hashlib, force_bytes
class SHA256PasswordHasher(BasePasswordHasher):
    algorithm = 'sha256'

    def encode(self, password, salt, iterations=None):
        assert password is not None
        # Convert the password to bytes before hashing
        password_bytes = force_bytes(password)
        # Include the algorithm and a placeholder for salt in the encoded password
        return f'{self.algorithm}${hashlib.sha256(password_bytes).hexdigest()}'

    def verify(self, password, encoded):
        # Split the encoded password to extract the algorithm, salt, and hash
        algorithm, hash = encoded.split('$', 1)
        assert algorithm == self.algorithm
        # Verify the password using a constant-time compare
        return constant_time_compare(hashlib.sha256(force_bytes(password)).hexdigest(), hash)

