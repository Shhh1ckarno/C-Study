import os
from dotenv import load_dotenv
load_dotenv()

class Settings():
    def __init__(self):
        self.SECRET_KEY=os.getenv("SECRET_KEY")
        self.alg=os.getenv("alg")
        self.access_token_expire_minutes=30
        self.refresh_token_expire_minutes=60*24*7

settings = Settings()