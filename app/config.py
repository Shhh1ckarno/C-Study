import os


class Settings():
    def __init__(self):
        self.key=os.getenv("key")
        self.alg=os.getenv("alg")
        self.secret_key=os.getenv("SECRET_KEY")
        self.access_token_expire_minutes=30
        self.refresh_token_expire_minutes=60*24*7
