from menu import Menu
from question import OptionQuestion

from .automated import AutomatedMenu
from .manual import ManualMenu
from .accounts import AccountsMenu


class MainMenu(Menu):
    def __init__(self):
        super().__init__(questions=[
            OptionQuestion("mode", "Which mode do you want to use?", options={
                "manual": ManualMenu,
                "automated": AutomatedMenu,
                "create-accounts": AccountsMenu
            })
        ])
