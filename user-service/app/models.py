from datetime import datetime, timedelta
import jwt
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.engine.default import DefaultExecutionContext
from sqlalchemy_utils import PasswordType, UUIDType
from sqlalchemy.orm import Session
from .config import JWT_SECRET, JWT_ALGORITHM, JWT_VALID_FOR


from .database import Base


def generate_token_for_user(
    user_id: str, user_email: str, valid_for: int = JWT_VALID_FOR
) -> str:
    """Generate a jwt token for this user_id and user_email for a given valid_for minutes

    Args:
        user_id (str): the user_id of the user
        user_email (str): the email of the user
        valid_for (int): the time before the token expire in seconds

    Returns:
        str: The given jwt
    """
    validation_token = jwt.encode(
        {
            "user_id": user_id,
            "user_email": user_email,
            "exp": datetime.utcnow() + timedelta(seconds=valid_for),
        },
        key=JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    return validation_token


class NotValidToken(Exception):
    pass


class AccountAlreadyVerified(Exception):
    pass

class UserDoesNotExist(Exception)

def verify_user_token(token: str, db: Session) -> "User":
    """Check the token is valid for the user, an the account is not already verified.
       Then setup the user as verified.
       The session is not commited.
    Args:
        token (str): the token you want to verify
        db (Session): the session to be used to check and modify the user
    Raises:
        NotValidToken: The token is not valid or expired
    Returns:
        User: the user retrieved and verified
    """
    try:
        decoded_token = jwt.decode(token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = decoded_token.get("user_id")
        user: User = db.query(User).get(user_id)
        if user is None:
            raise UserDoesNotExist("This user does not exist")
        if user.email_validated is True:
            raise AccountAlreadyVerified("This user account is already verified")
        user.email_validated = True
        db.add(user)
        return user
    except jwt.ExpiredSignatureError as exc:
        raise NotValidToken("This verify token is expired") from exc
    except jwt.InvalidTokenError as exc_unknown:
        raise NotValidToken("The verify token is not valid") from exc_unknown


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(
        PasswordType(schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"])
    )
    is_active = Column(Boolean, default=True)
    email_validated = Column(Boolean, default=False)
    validation_token = Column(
        String
    )  # This will contain a JWT token that needs to be initialised when
