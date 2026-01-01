from utils import send_email
from django.conf import settings
from celery import shared_task
from utils import User

@shared_task
def send_verification_email(user_id, token):
    """"Sends a verification email to the user with the provided token."""

    user = User.objects.get(id=user_id)
    verification_link = f"http://localhost:5173/auth/verify-email/?token={token}"
    subject = "Verify your email address"
    message = f"Hi {user.first_name},\n\nPlease verify your email address by clicking the link below:\n{verification_link}\n\nThank you!"
    recipient_list = [user.email]
    send_email(recipient_list, subject, message)