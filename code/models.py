

class User:

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Message:

    def __init__(self, user, message):
        self.user = user
        self.message = message


class Response:

    def __init__(self, timestamp=None, sender=None, response=None, content=None):
        self.timestamp = timestamp
        self.sender = sender
        self.response = response
        self.content = content

    def __str__(self):
        return "{} <{}> [{}]: {}".format(self.timestamp, self.sender,
                self.response, self.content)

class Request:

    def __init__(self, request=None, content=None):
        self.request = request
        self.content = content

    def __str__(self):
        return "{}: {}".format(self.request, self.response)

