import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def send_mail(to: str, subject: str, message: str, file: bytes = None) -> None:
    msg = MIMEMultipart()
    msg['From'] = 'golik.maxim83@yandex.by'
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(message))
    if file:
        part = MIMEApplication(file, Name='img.jpg')
        part['Content-Disposition'] = 'attachment; filename="img.jpg"'
        msg.attach(part)
    server = smtplib.SMTP('smtp.yndex.ru', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('golik.maxim83@yandex.by', 'ajhkgozkvccxwxvb')
    server.send('golik.maxim83@yandex.by', to, msg.as_string())
