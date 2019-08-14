from menu import Menu
import random
import time
from question import OptionQuestion, IntegerQuestion, FloatQuestion
import json
from exceptions import IllegalResponse
import threading

from geoguessr import User


class WaitQuestion(OptionQuestion):
    def __init__(self, *args, **kwargs):
        self.counter = 1
        super().__init__(*args, **kwargs)

    def run_games(self, user, wait, count, accuracy, maps):
        for _ in range(count):
            map = random.choice(maps)
            game = user.create_game(map=map)
            for _ in range(game.roundCount):
                pos = game.get_position()
                lat_range = (pos["lat"] - pos["lat"] * (1 - accuracy), pos["lat"] + pos["lat"] * (1 - accuracy))
                lng_range = (pos["lng"] - pos["lng"] * (1 - accuracy), pos["lng"] + pos["lng"] * (1 - accuracy))

                game.answer(random.uniform(*lat_range), random.uniform(*lng_range))

            score = game.get_total_score()
            print("\n%s. game is over. You scored %s points (%s percent) on %s" % (
                self.counter,
                score["amount"],
                score["percentage"],
                map
            ))

            self.counter += 1

            if wait:
                time.sleep(1)

    def process_response(self, response, menu):
        tokens = json.load(open("tokens.json"))
        if len(tokens) == 0:
            raise IllegalResponse("You need to create some accounts first")

        wait = super().process_response(response, menu)
        count = menu.find_result("count")
        accuracy = menu.find_result("accuracy")
        maps = open("maps.txt").read().replace(" ", "").split(",")

        threads = []
        for token in tokens:
            thread = threading.Thread(target=self.run_games, args=(User(token), wait, count, accuracy, maps))
            thread.start()
            threads.append(thread)

        for i, thread in enumerate(threads):
            thread.join()
            print("Thread %s finished" % i)

        return threads


class AutomatedMenu(Menu):
    def __init__(self, parent):
        super().__init__(questions=[
            IntegerQuestion("count", "How many games should each user play?"),
            FloatQuestion("accuracy", "Define the accuracy (0 - 1)"),
            WaitQuestion(
                "threads",
                "Should the bot wait a little bit between each game?",
                options={"yes": True, "no": False}
            )
        ], parent=parent)
