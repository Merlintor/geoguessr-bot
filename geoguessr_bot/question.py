from exceptions import IllegalResponse


class Question:
    def __init__(self, name, text, **kwargs):
        self.name = name
        self.text = text
        self.__dict__.update(kwargs)

    def process_response(self, response, menu):
        return response

    def ask(self, menu):
        response = input(self.text + " ")
        return self.process_response(response, menu)


class OptionQuestion(Question):
    def __init__(self, name, text, options: dict):
        super().__init__(name, text)
        self.options = options

    def process_response(self, response, menu):
        if response not in self.options:
            raise IllegalResponse("Response must me one of " + " (" + ", ".join(self.options.keys()) + ")")

        return self.options[response]

    def ask(self, menu):
        response = input(self.text + " (" + ", ".join(self.options.keys()) + ") ")
        return self.process_response(response, menu)


class IntegerQuestion(Question):
    def process_response(self, response, menu):
        try:
            return int(response)
        except ValueError:
            raise IllegalResponse("%s is not a valid integer" % response)


class FloatQuestion(Question):
    def process_response(self, response, menu):
        try:
            return float(response)
        except ValueError:
            raise IllegalResponse("%s is not a valid float" % response)


class DirectResponse(Question):
    def __init__(self, name, response):
        super().__init__(name, None)
        self.response = response

    def ask(self, menu):
        return self.response
