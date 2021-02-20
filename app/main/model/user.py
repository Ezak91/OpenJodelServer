from .. import DB, FLASK_BCRYPT

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