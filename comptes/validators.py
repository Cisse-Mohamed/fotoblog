from django.core.exceptions import ValidationError




class ValidateNoSpace:
    
    def validate(self, password, user=None):
        if ' ' in password:
            raise ValidationError(
                "Le mot de passe ne doit pas contenir d'espaces.",
                code='password_no_space',
            )
    
    def get_help_text(self):
        return "Le mot de passe ne doit pas contenir d'espaces."