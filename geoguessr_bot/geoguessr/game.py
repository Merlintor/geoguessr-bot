from exceptions import IllegalResponse
from datetime import datetime


class Game:
    def __init__(self, user, map):
        self.user = user
        self.map = map
        self.raw = None
        self._initialize_game()

    def _initialize_game(self):
        resp = self.user.session.post("https://geoguessr.com/api/v3/games/", data={
            "map": self.map,
            "type": "standard"
        })

        if resp.status_code == 404:
            raise IllegalResponse("Unknown map")

        if resp.status_code != 200:
            raise IllegalResponse("Something went wrong while creating the game")

        self.raw = resp.json()

    def reload(self):
        resp = self.user.session.get("https://geoguessr.com/api/v3/games/" + self.token)
        if resp == 404:
            raise IllegalResponse("Game terminated")

        if resp.status_code != 200:
            raise IllegalResponse("Something went wrong while reloading the game")

        self.raw = resp.json()

    def get_last_guess(self):
        player = self.player
        return player["guesses"][self.round - 2]

    def get_total_score(self):
        return self.player["totalScore"]

    def get_position(self):
        round = self.rounds[self.round - 1]
        return {
            "lat": round["lat"],
            "lng": round["lng"]
        }

    def answer(self, lat=None, lng=None):
        correct_pos = self.get_position()
        self.user.session.post("https://geoguessr.com/api/v3/games/" + self.token, data={
            "lat": lat or correct_pos["lat"],
            "lng": lng or correct_pos["lng"],
            "localTime": str(datetime.utcnow())
        })
        self.reload()

    def __getattr__(self, item):
        return self.raw.get(item)


