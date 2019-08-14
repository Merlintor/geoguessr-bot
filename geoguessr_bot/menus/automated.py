from menu import Menu
import random
import time
from question import OptionQuestion, IntegerQuestion, FloatQuestion


class WaitQuestion(OptionQuestion):
    def process_response(self, response, menu):
        wait = super().process_response(response, menu)
        user = menu.find_result("user")
        count = menu.find_result("count")
        accuracy = menu.find_result("accuracy")
        maps = open("maps.txt").read().replace(" ", "").split(",")

        for i in range(count):
            map = random.choice(maps)
            game = user.create_game(map=map)
            for _ in range(game.roundCount):
                pos = game.get_position()
                lat_range = (pos["lat"] - pos["lat"] * (1 - accuracy), pos["lat"] + pos["lat"] * (1 - accuracy))
                lng_range = (pos["lng"] - pos["lng"] * (1 - accuracy), pos["lng"] + pos["lng"] * (1 - accuracy))

                game.answer(random.uniform(*lat_range), random.uniform(*lng_range))

            score = game.get_total_score()
            print("\n%s. game is over. You scored %s points (%s percent) on %s" % (
                i + 1,
                score["amount"],
                score["percentage"],
                map
            ))

            if wait:
                time.sleep(1)


class AutomatedMenu(Menu):
    def __init__(self, parent):
        super().__init__(questions=[
            IntegerQuestion("count", "How many games should the bot play?"),
            FloatQuestion("accuracy", "Define the accuracy (0 - 1)"),
            WaitQuestion(
                "wait",
                "Should the bot wait a little bit between each game? (recommended)",
                options={"yes": True, "no": False}
            )
        ], parent=parent)
