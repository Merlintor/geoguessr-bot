from menu import Menu
from question import IntegerQuestion
import string
import random
import json

from geoguessr import User


class CountQuestion(IntegerQuestion):
    def process_response(self, response, menu):
        count = super().process_response(response, menu)

        tokens = []
        for _ in range(count):
            letters = string.ascii_letters
            user = User.register(
                email="%s@%s.com" % (
                    "".join([random.choice(letters) for i in range(16)]),
                    "".join([random.choice(letters) for i in range(3)]))
            )
            tokens.append(user.token)

        json.dump(tokens, open("tokens.json", "w"))
        print("Successfully created %s accounts" % count)
        return tokens


class AccountsMenu(Menu):
    def __init__(self, parent):
        super().__init__(questions=[
            CountQuestion("accounts", "How many accounts do you want to create?")
        ], parent=parent)
