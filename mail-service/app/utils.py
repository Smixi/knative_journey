from email.message import EmailMessage
from enum import Enum
import smtplib
from .config import SMTP_FROM_EMAIL, SMTP_SERVER, SMTP_PORT


class EmailClient:
    def send_mail(self, email: str, subject: str, body: str) -> None:
        pass


class DummyEmailClient(EmailClient):
    """A client that simply print the content of the mail in the console"""

    def send_mail(self, email: str, subject: str, body: str):
        print(f"Sending mail to {email}, subject: {subject}, body: {body}")


class SMTPEmailClient(EmailClient):
    def send_mail(self, email: str, subject: str, body: str) -> None:
        """Send a mail using a SMTP server

        Args:
            email (str): recipient to which the mail will be sent
            subject (str): the subject of the mail
            body (str): the body of the mail

        Returns:
            None
        """
        msg = EmailMessage()
        msg.set_content(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_FROM_EMAIL
        msg["To"] = email
        # We create a new connection everytime. It might be a good idea not to do that ?
        smtp_con = smtplib.SMTP(SMTP_SERVER, port=SMTP_PORT)
        smtp_con.send_message(msg)
        smtp_con.quit()


class EmailClassEnum(Enum):
    DUMMY = DummyEmailClient
    SMTP = SMTPEmailClient
