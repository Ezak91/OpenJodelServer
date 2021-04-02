import datetime
import jwt
from .. import DB, FLASK_BCRYPT

from ..config import key
from app.main.model.blacklist_token import BlacklistToken

class User(DB.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    email = DB.Column(DB.String(255), unique=True, nullable=False)
    registered_on = DB.Column(DB.DateTime, nullable=False)
    admin = DB.Column(DB.Boolean, nullable=False, default=False)
    public_id = DB.Column(DB.String(100), unique=True)
    username = DB.Column(DB.String(50), unique=True)
    password_hash = DB.Column(DB.String(100))

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = FLASK_BCRYPT.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return FLASK_BCRYPT.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod  
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key, algorithms=["HS256"])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
