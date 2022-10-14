from os import environ as env

JWT_SECRET = env.get("JWT_SECRET", "supersecret")
JWT_ALGORITHM = "HS256"
JWT_VALID_FOR = 60 * 60 * 24  # Time to validate user account in seconds
