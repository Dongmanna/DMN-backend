# main/validators.py
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _

@deconstructible
class NicknameValidator(validators.RegexValidator):
    regex = r'^[\w]+$'
    message = _('닉네임은 문자, 숫자만 사용할 수 있습니다.')
