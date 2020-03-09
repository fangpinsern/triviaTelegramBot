from player import Player

class GameSession:
    owner =""
    ownerId = 0
    gameName=""
    players = []
    listOfQuestions = []

    def __init__(self, owner, ownerId, gameName):
        self.owner = owner
        self.gameName = gameName
        self.ownerId = ownerId

    def isOwner(self, ownername):
        return self.owner == ownername

    def getOwnerId(self):
        return self.ownerId
    
    def addPlayer(self, username, chatId):
        newPlayer  = Player(username, chatId)
        self.players.append(newPlayer)
    
    def removePlayer(self, username):
        for player in self.players:
            if username == player.getName():
                self.players.remove(player)

    #owner exclusive commands
    def addQuestion(self, username, question):
        vaildAddQuestion = False
        if self.isOwner(username):
            self.listOfQuestions.append(question)    
            vaildAddQuestion = True
        return vaildAddQuestion

    def removeQuestionByIndex(self, username, qnNumber):
        validRemoveQuestion = False
        if self.isOwner(username):
            del self.listOfQuestions[qnNumber - 1]
            validRemoveQuestion = True
        return validRemoveQuestion

    def printPlayersInGame(self):
        if len(self.players) == 0:
            return "No one joined :("
        playerString ="Players: \n"
        count = 1
        
        for player in self.players:
            playerString = playerString + "{}. {} ({} points)".format(str(count), player.getName(), player.getScore())
            count = count + 1
        return playerString

    def printQuestionsInGame(self):
        if len(self.listOfQuestions) == 0:
            return "You should start adding some questions! use /addQuestion"
        questionString ="Questions:\n"
        count = 1
        
        for question in self.listOfQuestions:
            questionString = questionString + "{}. {}".format(str(count), question)
            count = count + 1
        return questionString
            