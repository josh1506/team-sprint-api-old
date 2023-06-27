import secrets
import string


def generate_random_str(length=6):
    chars = string.ascii_letters + string.digits
    code = "".join(secrets.choice(chars) for i in range(length))
    return code
