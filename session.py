from gameSession import GameSession

# General session for bot to manage the different game sessions
class Session: 
    
    sessionArr = []

    def __init__(self):
        self.addSession("hellostups", 0, "fang")

    #session [owner, gamename, newGame]
    def addSession(self, owner, ownerId, gamename):
        validAddSession = False
        if not self.gameExist(gamename):
            newGame = GameSession(owner, ownerId, gamename)
            self.sessionArr.append([owner, gamename, newGame])
            validAddSession = True
        return validAddSession

    def addPlayerToGame(self, gamename, username, chatId):
        validGame = False
        if self.isAnOwner(username):
            return validGame
        for game in self.sessionArr:
            if game[1] == gamename:
                game[2].addPlayer(username, chatId)
                validGame = True
                break

        return validGame
        
    def addQuestion(self, username, gamename, question):
        for game in self.sessionArr:
            if game[1] == gamename:
                game[2].addQuestion(username, question)
                return True
        return False

    def removeQuestion(self, username, gamename, removeQnNumber):
        for game in self.sessionArr:
            if game[1] == gamename:
                game[2].removeQuestionByIndex(username, removeQnNumber)
                return True
        return False

    def getGamebyOwner(self, username):
        for game in self.sessionArr:
            if game[0] == username:
                return game[2]
        return False

    def getGamebyGameName(self, gamename):
        for game in self.sessionArr:
            if game[1] == gamename:
                return game[2]
        return False

    def isAnOwner(self, ownername):
        for game in self.sessionArr:
            if game[0] == ownername:
                return True
        return False

    def gameExist (self, gamename):
        exist = False
        for game in self.sessionArr:
            if game[1] == gamename:
                exist = True
                break
        return exist


        