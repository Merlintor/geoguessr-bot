from menu import Menu
from question import Question, OptionQuestion
from exceptions import IllegalResponse

from geoguessr import User
from .automated import AutomatedMenu
from .manual import ManualMenu


class TokenQuestion(Question):
    def process_response(self, response, menu):
        user = User(response)
        if not user.check_token():
            raise IllegalResponse("Invalid token given")

        return user


class MainMenu(Menu):
    def __init__(self):
        super().__init__(questions=[
            TokenQuestion("user", "Please input your user token:"),
            OptionQuestion("mode", "Which mode do you want to use?", options={
                "manual": ManualMenu,
                "automated": AutomatedMenu
            })
        ])
