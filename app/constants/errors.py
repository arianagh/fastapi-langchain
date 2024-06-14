class Error:
    """
    Constants for the errors
    """
    USER_EXIST_ERROR = {
        'text': 'There is a user with this email or phone number',
        'status_code': 400,
        'code': 1,
        'description': "",
    }

    TOKEN_NOT_EXIST_OR_EXPIRATION_ERROR = {
        'text': 'Invalid token',
        'status_code': 403,
        'code': 2,
    }

    INACTIVE_USER = {'text': 'Inactive user', 'status_code': 400, 'code': 3}

    NOT_ACCEPTABLE_PASSWORD = {
        'text': 'Your password is not acceptable',
        'status_code': 400,
        'code': 4,
    }

    USER_PASS_WRONG_ERROR = {
        'text': 'Wrong username or password',
        'status_code': 401,
        'code': 5,
    }