from django.core.mail import EmailMessage


def send_email(content, email):
    subject = "Welcome to BlogNest!"
    from_email = "hadelesmatullah@gmail.com"
    recipient_list = [email]
    email_message = EmailMessage(subject, content, from_email, recipient_list)
    email_message.content_subtype = "html"
    email_message.send()
