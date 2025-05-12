# file for hashing passwords and verifying hashed passwords

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash


def hash_password(password):
    return PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8).hash(password)

def verify_password(hashed_password, plain_password):
    ph = PasswordHasher(time_cost=2, memory_cost=102400, parallelism=8)
    try:
        return ph.verify(hashed_password, plain_password)
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False
    except Exception as e:
        raise Exception(e)

