from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    iduser = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique = True, index = True)
    password = db.Column(db.String(100), nullable= False)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return int(self.iduser)

    def __repr__(self):
        return '<User: {}>'.format(self.name)