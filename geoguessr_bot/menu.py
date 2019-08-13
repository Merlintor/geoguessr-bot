from exceptions import IllegalResponse
import types


class Menu:
    def __init__(self, questions, parent=None):
        self.questions = questions
        self.parent = parent
        self.results = {}

    def get_results(self):
        for question in self.questions:
            error = ""
            result = None
            while error is not None:
                try:
                    if error:
                        print(">",  error)

                    result = question.ask(self)
                except IllegalResponse as e:
                    error = str(e)
                else:
                    error = None

            if isinstance(result, type) and issubclass(result, Menu):
                self.results[question.name] = result(parent=self).get_results()

            elif result == "exit":
                break

            else:
                self.results[question.name] = result

        return self.results

    def find_result(self, name):
        if name in self.results:
            return self.results[name]

        if self.parent is not None:
            return self.parent.find_result(name)

        return None
