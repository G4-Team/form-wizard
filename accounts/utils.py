from random import randint

from .models import OtpVerificationCode


def create_verification_code(*, phone: str, code: str) -> OtpVerificationCode:
    return OtpVerificationCode.objects.create(phone=phone, code=code)


def get_or_create_verfication_code(*, phone: str) -> OtpVerificationCode:
    try:
        code = OtpVerificationCode.objects.get(phone=phone)
    except OtpVerificationCode.DoesNotExist:
        random_code = randint(100000, 1000000)
        code = create_verification_code(phone=phone, code=random_code)
    if not code.is_valid():
        code.delete()
        random_code = randint(100000, 1000000)
        code = create_verification_code(phone=phone, code=random_code)

    return code


def send_code(code: str, phone: str):
    pass
