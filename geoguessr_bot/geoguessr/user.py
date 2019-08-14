from . import Game
import requests


class User:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.cookies.set(name="_ncfa", value=token)

    @classmethod
    def register(cls, email):
        resp = requests.post("https://geoguessr.com/api/v3/accounts/signup", data={
            "email": email,
        })
        return cls(resp.cookies.get("_ncfa"))

    @classmethod
    def login(cls, email, password):
        resp = requests.post("https://geoguessr.com/api/v3/accounts/signin", data={
            "email": email,
            "password": password
        })
        return cls(resp.cookies.get("_ncfa"))

    def create_game(self, *args, **kwargs):
        return Game(user=self, *args, **kwargs)
