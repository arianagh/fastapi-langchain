import random
import re
import string


def validate_password(password) -> bool:
    if len(password) < 8:
        return False
    elif re.search('[0-9]', password) is None:
        return False
    elif re.search('[A-Z]', password) is None:
        return False
    elif re.search('[a-z]', password) is None:
        return False
    return True


def generate_random_token(length: int) -> str:
    return ''.join(random.choice(f'{string.ascii_letters}0123456789') for _ in range(length))


def generate_random_code(length: int) -> int:
    return random.randint(10 ** length, (10 ** (length + 1)) - 1)
