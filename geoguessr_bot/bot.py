from menus.main import MainMenu


class GeoguessrBot:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def _start_menu(self):
        menu = MainMenu()
        print("\n\n", menu.get_results())

    def start(self):
        self._start_menu()


def start_bot(**kwargs):
    bot = GeoguessrBot(**kwargs)
    bot.start()
