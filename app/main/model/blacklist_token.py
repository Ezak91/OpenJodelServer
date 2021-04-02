from .. import DB
import datetime


class BlacklistToken(DB.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    token = DB.Column(DB.String(500), unique=True, nullable=False)
    blacklisted_on = DB.Column(DB.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=auth_token).first()
        if res:
            return True
        else:
            return False