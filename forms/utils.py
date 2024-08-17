import random
import string


def get_random_string(length: int) -> str:

    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for i in range(length))
    return result_str
