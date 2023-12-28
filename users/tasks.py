from django.core.mail import send_mail
from config.celery import app


@app.task()
def send_email(subject, message, recipient_lit):
    send_mail(
        subject,
        message,
        "bekhzodnabijonov@gmail.com",
        recipient_lit
    )