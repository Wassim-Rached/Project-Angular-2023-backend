from django.core.exceptions import ValidationError
import re


def strongPassword(value):
    ...
    # if len(value) < 8:
    #     raise ValidationError("Password must be at least 8 characters long.")
    # if not any(char.isdigit() for char in value):
    #     raise ValidationError("Password must contain at least one digit.")
    # if not any(char.isalpha() for char in value):
    #     raise ValidationError("Password must contain at least one letter.")
    # if not re.search(r"[A-Z]", value):
    #     raise ValidationError("Password must contain at least one uppercase letter.")
    # if not re.search(r"[a-z]", value):
    #     raise ValidationError("Password must contain at least one lowercase letter.")
    # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
    #     raise ValidationError(
    #         'Password must contain at least one special character (!@#$%^&*(),.?":{}|<>).'
    #     )


def is_tunisian_phone_number(value):
    phone_number_pattern = r"^\d{8}$"

    if not re.match(phone_number_pattern, value):
        raise ValidationError("Please enter a valid 8-digit Tunisian phone number.")
