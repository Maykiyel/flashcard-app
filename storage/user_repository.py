import json
import os
from models.user import User

class UserRepository:
    def __init__(self, filename="users.json"):
        self.filename = filename
        self.users = {}
        self.load()
    
    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.users = {uid: User.from_dict(user_data) for uid, user_data in data.items()}
    
    def save(self):
        with open(self.filename, 'w') as f:
            data = {uid: user.to_dict() for uid, user in self.users.items()}
            json.dump(data, f, indent=2)
    
    def add_user(self, user):
        self.users[user.userID] = user
        self.save()
    
    def get_user(self, userID):
        return self.users.get(userID)
    
    def user_exists(self, userID):
        return userID in self.users