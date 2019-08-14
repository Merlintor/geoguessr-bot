from menu import Menu
from question import Question, DirectResponse

from geoguessr import User


class AccuracyQuestion(Question):
    def process_response(self, response, menu):
        values = response.replace(" ", "").split(",")
        lat = float(values[0])
        lng = float(values[1])

        game = menu.find_result("game")
        game.answer(lat, lng)

        guess = game.get_last_guess()
        print("You were %s meters away and scored %s points" % (
            guess["distance"]["meters"]["amount"],
            guess["roundScore"]["amount"]
        ))
        if len(game.player["guesses"]) == game.roundCount:
            score = game.get_total_score()
            print("\nThe game is over. You scored %s points (%s percent)" % (score["amount"], score["percentage"]))

        return guess["roundScore"]

    def ask(self, menu):
        print("\nThe correct position is %s" % ", ".join([
            str(f) for f in menu.find_result("game").get_position().values()
        ]))
        return super().ask(menu)


class ManualGameMenu(Menu):
    def __init__(self, parent):
        super().__init__(questions=[], parent=parent)
        game = self.find_result("game")
        for i in range(game.roundCount):
            self.questions.append(AccuracyQuestion(
                "result%s" % i,
                "Input your position (lat, lng) for round %s:" % (i + 1)
            ))


class MapQuestion(Question):
    def process_response(self, response, menu):
        user = menu.find_result("user")
        return user.create_game(map=response)


class UserQuestion(Question):
    def process_response(self, response, menu):
        return User(response)


class ManualMenu(Menu):
    def __init__(self, parent):
        super().__init__(questions=[
            UserQuestion("user", "Input the user token you want to use:"),
            MapQuestion("game", "Which map do you want to play?"),
            DirectResponse("results", ManualGameMenu)
        ], parent=parent)
