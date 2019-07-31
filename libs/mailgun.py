import os
from typing import List
from requests import Response, post


class MailgunException(Exception):
    def __init__(self, message: str):
        self.message = message


class Mailgun:
    @classmethod
    def send_mail(cls, email: List[str], subject: str, text: str, html: str) -> Response:
        MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY', None)
        MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', None)
        FROM_TITLE = 'Pricing Service'
        FROM_EMAIL = 'do-not-reply@sandbox97405985d45b4460b7f4cbf8cfe346e5.mailgun.org'

        if MAILGUN_API_KEY is None:
            raise MailgunException('Failed to load mailgun API key.')

        if MAILGUN_DOMAIN is None:
            raise MailgunException('Failed to load mailgun domain.')

        response = post(
            f'{MAILGUN_DOMAIN}/messages',
            auth=("api", MAILGUN_API_KEY),
            data={"from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                  "to": email,
                  "subject": subject,
                  "text": text,
                  "html": html,
                  }
        )
        if response.status_code != 200:
            raise MailgunException('An error occurred while sending e-mail.')
        return response