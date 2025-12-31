from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


from django.conf import settings

from itsdangerous import URLSafeTimedSerializer as Serializer, BadSignature, SignatureExpired


def generate_email_verification_token(user):
    """Generates a time-limited token for email verification."""
    serializer = Serializer(settings.SECRET_KEY)
    return serializer.dumps(str(user.id), salt='email-verification-salt')

def verify_email_token(token, expiration=3600):
    """Verifies the email token and returns the associated user if valid."""
    serializer = Serializer(settings.SECRET_KEY)
    try:
        user_id = serializer.loads(token, salt='email-verification-salt', max_age=expiration)
        return User.objects.get(id=user_id)
    except (BadSignature, SignatureExpired, User.DoesNotExist):
        return None   
