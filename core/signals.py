from django.dispatch import receiver
from djoser.signals import user_registered
from django.core.mail import send_mail

@receiver(user_registered)
def send_welcome_email_after_registration(sender, user, request, **kwargs):
    subject = "Welcome to Sky Reservation ✈️"
    message = (
        f"Hello {user.username},\n\n"
        "Thank you for registering with Sky Reservation!\n"
        "We’re thrilled to have you onboard.\n"
        "We wish you a comfortable experience and a pleasant journey! 😊"
    )

    send_mail(
        subject,
        message,
        None,
        [user.email],
        fail_silently=False
    )
