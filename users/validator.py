import re

from django.core.exceptions import ValidationError

class Validation():
    def __init__(self, email, password):
        self.email     = email
        self.password  = password
        
    def email_validator(email):
        REGEX_EMAIL    = r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(REGEX_EMAIL, email):
            raise ValidationError('INVALID_EMAIL')
        
    def password_validator(password):
        REGEX_PASSWORD = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
        if not re.match(REGEX_PASSWORD, password):
            raise ValidationError('INVALID_PASSWORD')
    