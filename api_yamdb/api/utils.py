import uuid

from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_ADMIN
from reviews.models import User


def generate_confirmation_code_and_send_email(username, mail):
    """Функция для генерации кода подтверждения и отправки
    его на email"""

    conf_code = str(uuid.uuid4())

    user = User.objects.get(username=username, email=mail)
    user.confirmation_code = conf_code
    user.save()

    subject = 'Confirmation code'
    message = f'Your confirmation code is: {conf_code}'
    from_email = EMAIL_ADMIN
    recipient_list = [mail, ]
    send_mail(subject, message, from_email, recipient_list)
