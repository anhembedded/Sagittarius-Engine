class User:
    def __init__(self, user_id: str, name: str):
        self.id = user_id
        self.name = name

class UserCreatedEvent:
    def __init__(self, user: User):
        self.user = user
