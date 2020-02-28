from django.core.exceptions import ValidationError

def validate_username(username):
    if len(username) < 3:
        raise ValidationError('Username must contain at least 3 characters')