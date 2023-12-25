from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings


# Create this utility function to redirect the user on specific dashboard
# Check the user type
def detectUser(user):
    if user.role == 1:
        redirectUrl = 'vendordashboard'
        return redirectUrl
    elif user.role == 2:
        redirectUrl = 'custdashboard'
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = '/admin'
        return redirectUrl


# Send registration verification email
def send_verification_email(request, user, email_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)

    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(email_subject, message, from_email, to=[to_email])
    mail.send()