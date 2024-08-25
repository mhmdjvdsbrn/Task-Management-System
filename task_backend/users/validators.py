from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

import re


def number_validator(password):
    regex = re.compile('[0-9]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include number"),
                code="password_must_include_number"
                )

def letter_validator(password):
    regex = re.compile('[a-zA-Z]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include letter"),
                code="password_must_include_letter"
                )

def special_char_validator(password):
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if regex.search(password) == None:
        raise ValidationError(
                _("password must include special char"),
                code="password_must_include_special_char"
                )

def validate_phone_number(phone):

    phone_validator = RegexValidator(
        regex=r'^09\d{9}$',
        message="Phone number must be 11 digits and start with '09'."
    )
    # Check if phone number is valid
    try:
        phone_validator(phone)
    except ValidationError as e:
        raise ValidationError(e.message)
