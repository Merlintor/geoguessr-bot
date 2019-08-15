from menu import Menu
from question import IntegerQuestion, Question
import string
import random
import json

from geoguessr import User


class NameQuestion(Question):
    def process_response(self, response, menu):
        name = response.replace(" ", ".")
        count = menu.find_result("count")
        tokens = []
        for _ in range(count):
            letters = string.ascii_letters
            user = User.register(
                email="%s@%s.com" % (
                    name,
                    "".join([random.choice(letters) for _ in range(10)]))
            )
            tokens.append(user.token)

        json.dump(tokens, open("tokens.json", "w"))
        print("Successfully created %s accounts" % count)
        return tokens


class AccountsMenu(Menu):
    def __init__(self, parent):
        super().__init__(questions=[
            IntegerQuestion("count", "How many accounts do you want to create?")
            NameQuestion("accounts", "What name should the accounts have?")
        ], parent=parent)
