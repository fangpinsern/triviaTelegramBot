
class Player:
    name="noname"
    score = 0
    chatId = None
    def __init__(self, name, chatId):
        self.name = name
        self.score  = 0
        self.chatId = chatId

    def getName(self):
        return self.name

    def getChatId(self):
        return self.chatId

    def getScore(self):
        return self.score

    def addPoints(self):
        self.score = self.score + 1

    def toString(self):
        return "{} ({}points)".format(self.name, self.score)