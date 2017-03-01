import model
from flask.ext.login import UserMixin

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def get_id(self):
        return self.username

    @classmethod
    def get(cls, id):
        userData = model.get_user(id)
        if not userData:
            return None
        return User(userData[0], userData[1])