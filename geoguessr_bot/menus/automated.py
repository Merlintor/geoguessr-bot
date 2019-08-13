from menu import Menu
import random
import time
from question import Question, OptionQuestion, IntegerQuestion, FloatQuestion


class MapsQuestion(Question):
    def process_response(self, response, menu):
        user = menu.find_result("user")
        count = menu.find_result("count")
        accuracy = menu.find_result("accuracy")
        wait = menu.find_result("wait")
        maps = response.replace(" ", "").split(",")

        for i in range(count):
            game = user.create_game(map=random.choice(maps))
            for _ in range(game.roundCount):
                pos = game.get_position()
                lat_range = (pos["lat"] - pos["lat"] * (1 - accuracy), pos["lat"] + pos["lat"] * (1 - accuracy))
                lng_range = (pos["lng"] - pos["lng"] * (1 - accuracy), pos["lng"] + pos["lng"] * (1 - accuracy))

                game.answer(random.uniform(*lat_range), random.uniform(*lng_range))

            score = game.get_total_score()
            print("\n%s. game is over. You scored %s points (%s percent)" % (i + 1, score["amount"], score["percentage"]))

            if wait:
                time.sleep(1)


class AutomatedMenu(Menu):
    def __init__(self, parent):
        super().__init__(questions=[
            IntegerQuestion("count", "How many games should the bot play?"),
            FloatQuestion("accuracy", "Define the accuracy (0 - 1)"),
            OptionQuestion(
                "wait",
                "Should the bot wait a little bit between each game? (recommended)",
                options={"yes": True, "no": False}
            ),
            MapsQuestion(
                "game",
                "Which maps do you want to play (e.g. 'world, usa, european-union, famous-places, uk, netherlands')"
            )
        ], parent=parent)
