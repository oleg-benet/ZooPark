from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from aiosmtplib import SMTP
import asyncio

EMAIL = 'benetal@yandex.ru'
PWD = 'qivvyieszqqgilpv'

async def send_mail(subject, to, msg):
    message = MIMEMultipart()
    message["From"] = EMAIL
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(f"<html><body>{msg}</body></html>", "html", "utf-8"))

    smtp_client = SMTP(hostname="smtp.yandex.ru", port=465, use_tls=True)
    async with smtp_client:
        await smtp_client.login(EMAIL, PWD)
        await smtp_client.send_message(message)

if __name__ == '__main__':
    asyncio.run(send_mail(f'Сообщение от пользоателя с ID = {54432515125454}', 'benetal@yandex.ru', '<h1>Привет от бота</h1>'))