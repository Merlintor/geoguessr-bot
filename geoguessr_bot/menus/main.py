from menu import Menu
from question import OptionQuestion, DirectResponse

from geoguessr import User
from .automated import AutomatedMenu
from .manual import ManualMenu


class MainMenu(Menu):
    def __init__(self):
        super().__init__(questions=[
            DirectResponse("user", User(open("token.txt.").read().strip())),
            OptionQuestion("mode", "Which mode do you want to use?", options={
                "manual": ManualMenu,
                "automated": AutomatedMenu
            })
        ])
