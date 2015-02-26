from json import loads, dumps

class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __str__(self):
        return self.username


class Message:

    def __init__(self, user, message):
        self.user = user
        self.message = message

    def __str__(self):
        return '{}: {}'.format(self.user, self.message)


class Response:

    def __init__(self, **entries):
        self.timestamp = "None"
        self.sender = "None"
        self.response = "None"
        self.content = "None"
        self.__dict__.update(entries)

    def __str__(self):
        return "{} <{}> [{}]: {}".format(self.timestamp, self.sender,
                self.response, self.content)

class Request:

    def __init__(self, **entries):
        self.request = "None"
        self.content = "None"
        self.__dict__.update(entries)

    def __str__(self):
        return "{}: {}".format(self.request, self.content)


''' 
Vi vil ikke ha 'null' som 'feilverdi', men '"None"',
altså json strengen med ordet None.
'''
def to_json(obj):
    return (dumps(obj)).replace('null', '"None"')

