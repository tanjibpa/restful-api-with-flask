import os
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import(TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import random, string
from find_restaurant import app, Base
secret_key = ''.join(random.choice(string.ascii_uppercase+string.digits) for x in range(32))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    picture = Column(String)
    email = Column(String, index=True)
    password_hash = Column(String(250))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user_id = data['id']
        return user_id


class UserPref(Base):
    __tablename__ = 'user_pref'

    id = Column(Integer, ForeignKey("users.id"), primary_key=True, nullable=False)
    # user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    api_key = Column(String)
    user = relationship(User)

    def generate_api_key(self):
        self.api_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(32))
