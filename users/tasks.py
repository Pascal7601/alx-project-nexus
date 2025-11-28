from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from utils import User

@shared_task
def send_verification_email(user_id, token):
    """"Sends a verification email to the user with the provided token."""

    user = User.objects.get(id=user_id)
    verification_link = f"http://127.0.0.1:8000/api/auth/verify-email/?token={token}"
    subject = "Verify your email address"
    message = f"Hi {user.email},\n\nPlease verify your email address by clicking the link below:\n{verification_link}\n\nThank you!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)