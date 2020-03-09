from player import Player

class GameSession:
    owner =""
    ownerId = 0
    gameName=""
    started = False
    players = []
    listOfQuestions = []
    answerToQuestions = []
    currentQuestionNumber = 0

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
    
    def nextQuestion(self):
        qnNum = self.currentQuestionNumber
        self.currentQuestionNumber = qnNum + 1

    def getCurrentQuestion(self):
        return self.listOfQuestions[self.currentQuestionNumber]
    
    def getPlayerList(self):
        return self.players

    def isLastQn(self):
        return len(self.listOfQuestions) == self.currentQuestionNumber

    def startGame(self):
        self.started = True
    
    def hasStarted(self):
        return self.started

    def addAnswerArr(self):
        self.answerToQuestions.append([])
    
    def addAnswer(self, username, answer):
        qnNumber = self.currentQuestionNumber
        for player in self.players:
            if player.getName() == username:
                self.answerToQuestions[self.currentQuestionNumber].append([player, answer])

    def printAnswer(self):
        answerString = ""
        for answer in self.answerToQuestions[self.currentQuestionNumber]:
            answerString = answerString + "{} - {}\n".format(answer[0].getName(), answer[1])
        return answerString
    
    def getAnswerKeyboard(self):
        mainKeyboard = []
        for answer in self.answerToQuestions[self.currentQuestionNumber]:
            mainKeyboard.append([answer[0].getName()])

        return mainKeyboard

    def getPlayerId(self, username):
        for player in self.players:
            if player.getName() == username:
                return player.getChatId()
        

    def hasAllAnswered(self):
        return len(self.players) == len(self.answerToQuestions[self.currentQuestionNumber])

    def addPointsToUser(self, username):
        for player in self.players:
            if player.getName() == username:
                player.addPoints()

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
            playerString = playerString + "{}. {} ({} points)\n".format(str(count), player.getName(), player.getScore())
            count = count + 1
        return playerString

    def printQuestionsInGame(self):
        if len(self.listOfQuestions) == 0:
            return "You should start adding some questions! use /addQuestion"
        questionString ="Questions:\n"
        count = 1
        
        for question in self.listOfQuestions:
            questionString = questionString + "{}. {}\n".format(str(count), question)
            count = count + 1
        return questionString
            