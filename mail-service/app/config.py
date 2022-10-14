from os import environ as env

EMAIL_CLIENT = env.get("EMAIL_CLIENT", "DUMMY")
SMTP_FROM_EMAIL = env.get("SMTP_FROM_EMAIL", "mail-service@internal.com")
SMTP_SERVER = env.get("SMTP_SERVER", "localhost")
SMTP_PORT = env.get("SMTP_PORT", 8025)
