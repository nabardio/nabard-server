from django.contrib.auth.tokens import PasswordResetTokenGenerator

from nabard.exceptions import InvalidToken


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )
    
    def check_token_with_exception(self, user, token):
        if not self.check_token(user, token):
            raise InvalidToken()

account_activation_token = TokenGenerator()
