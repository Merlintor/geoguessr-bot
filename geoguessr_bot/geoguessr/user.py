from . import Game
import requests


class User:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.cookies.set(name="_ncfa", value=token)

    def check_token(self):
        return True

    def create_game(self, *args, **kwargs):
        return Game(user=self, *args, **kwargs)
