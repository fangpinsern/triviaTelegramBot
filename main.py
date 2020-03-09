import logging
import os

import sys

from session import Session
from userSession import UserSession

from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)

#startbotSession
session = Session()
userSession = UserSession()


startMessage = "Hi! Welcome to my trivia bot!\nTo start a game, use the /startGame command. \nTo join a game, use the /join command! \n\n Please be gentle. I am fragile"
userGuide = "Yo! Need help? \n /begin - start the game \n /addQuestion - add question to your game \n /endGame - end the game \n /players - get a list of the players who are in the game \n\nYour group name is: \n{}"

gameMasterKeyboard = ReplyKeyboardMarkup([["/begin", "/addQuestion"], ["/players", "/questions"], ["/endGame"]])

def start_handler(update: Update, context: CallbackContext):
    username = update.effective_user["username"]
    logger.info("User {} started bot".format(update.effective_user["username"]))
    userSession.end_session(username)
    context.bot.sendMessage(
        chat_id=update.effective_user["id"], text=startMessage, reply_markup=ReplyKeyboardMarkup([["/startGame"], ["/join"]]))
        
        
def join_handler(update: Update, context: CallbackContext):
    username = update.effective_user["username"]
    logger.info("User {} wants to join a game".format(update.effective_user["username"]))
    userSession.start_session(username, "/join")
    context.bot.sendMessage(
        chat_id=update.effective_user["id"], text="Please enter the name of the group you would like to join", reply_markup=ReplyKeyboardMarkup([["/restart"]]))


def restart_handler(update: Update, context: CallbackContext):
    username = update.effective_user["username"]
    logger.info("User {} went back to the start".format(update.effective_user["username"]))
    userSession.end_session(username)
    context.bot.sendMessage(
        chat_id=update.effective_user["id"], text=startMessage, reply_markup=ReplyKeyboardMarkup([["/startGame"], ["/join"]]))

def startGame_handler(update: Update, context: CallbackContext):
    username = update.effective_user["username"]
    logger.info("User {} would like to start game".format(update.effective_user["username"]))
    userSession.start_session(username, "/startGame")
    context.bot.sendMessage(
        chat_id=update.effective_user["id"], text="How would you like to name the group?", reply_markup=ReplyKeyboardMarkup([["/restart"]]))

    

def answer_handler(update: Update, context: CallbackContext):
    username = update.effective_user["username"]
    userInput = update.message.text
    chatId = update.effective_user["id"]
    
    if(userSession.get_last_command(username) == "/join"):
        #userInput should be the game name
        validGameName = session.addPlayerToGame(userInput, username, chatId)
        if validGameName:
            userSession.update_session(username, "/question")
            userSession.add_passing_arguments(username, [userInput])
            context.bot.sendMessage(
                chat_id=update.effective_user["id"], text="You have successfully joined the game. Please wait for the game to start", reply_markup=ReplyKeyboardMarkup([["/restart"]]))
        else:
            context.bot.sendMessage(
                chat_id=update.effective_user["id"], text="The game does not exist. Please try again. If you would like to start a game, you can use /startGame", reply_markup=ReplyKeyboardMarkup([["/restart"]]))

    elif(userSession.get_last_command(username) == "/question"):
        context.bot.sendMessage(
                chat_id=update.effective_user["id"], text="Game havent start yet...", reply_markup=ReplyKeyboardMarkup([["/restart"]]))

    elif(userSession.get_last_command(username) == "/startGame"):
        #userInput should be the new game name
        validGameSession = session.addSession(username, chatId, userInput)
        if validGameSession:
            userSession.update_session(username, "/gamemaster")
            userSession.add_passing_arguments(username,[userInput])
            context.bot.sendMessage(
                chat_id=update.effective_user["id"], text=userGuide.format(userInput), reply_markup=gameMasterKeyboard)
        else:
            context.bot.sendMessage(
                chat_id=update.effective_user["id"], text="Game name already exist. Please use another name.", reply_markup=ReplyKeyboardMarkup([["/restart"]]))

    elif(userSession.get_last_command(username) == "/addQuestion"):
        #userInput should be a question
        gameName = userSession.get_passing_arguments(username)[0]
        validAddQuestion = session.addQuestion(username, gameName, userInput)
        userSession.update_session(username, "/gamemaster")
        context.bot.sendMessage(
                chat_id=update.effective_user["id"], text="Question has been added. To see your questions, use /questions", reply_markup=gameMasterKeyboard)

    else:
        context.bot.sendMessage(
                chat_id=update.effective_user["id"], text="Invalid input. Please use /restart if you see this too many times.", reply_markup=ReplyKeyboardMarkup([["/restart"]]))
    
def addQuestion_handler(update: Update, context: CallbackContext):
    username = update.effective_user["username"]
    logger.info("User {} would like to add question to the game".format(update.effective_user["username"]))
    if (userSession.get_last_command(username) == "/gamemaster"):
        userSession.update_session(username, "/addQuestion")
        context.bot.sendMessage(
            chat_id=update.effective_user["id"], text="Please type in your question. Remember to add the question mark!", reply_markup=ReplyKeyboardRemove())
    else:
        context.bot.sendMessage(
            chat_id=update.effective_user["id"], text="You cannot add questions", reply_markup=ReplyKeyboardMarkup([["/restart"]]))
        
def seePlayers_handler(update: Update, context: CallbackContext):
    username = update.effective_user["username"]
    logger.info("User {} would like to see the players".format(update.effective_user["username"]))
    if (userSession.get_last_command(username) == "/gamemaster"):
        # userSession.update_session("/addQuestion")
        game = session.getGamebyOwner(username)
        players = game.printPlayersInGame()
        context.bot.sendMessage(
            chat_id=update.effective_user["id"], text=players, reply_markup=gameMasterKeyboard)
    else:
        context.bot.sendMessage(
            chat_id=update.effective_user["id"], text="You cannot do this", reply_markup=ReplyKeyboardMarkup([["/restart"]]))

def seeQuestions_handler(update: Update, context: CallbackContext):
    username = update.effective_user["username"]
    logger.info("User {} would like to see the players".format(update.effective_user["username"]))
    if (userSession.get_last_command(username) == "/gamemaster"):
        # userSession.update_session("/addQuestion")
        game = session.getGamebyOwner(username)
        questions = game.printQuestionsInGame()
        context.bot.sendMessage(
            chat_id=update.effective_user["id"], text=questions, reply_markup=gameMasterKeyboard)
    else:
        context.bot.sendMessage(
            chat_id=update.effective_user["id"], text="You cannot do this", reply_markup=ReplyKeyboardMarkup([["/restart"]]))

def exit_handler(update: Update, context: CallbackContext):
    username = update.effective_user["username"]
    if userSession.get_last_command(username) == "/gamemaster":
        context.bot.sendMessage(
                chat_id=update.effective_user["id"], text="dude... you are the game master", reply_markup=gameMasterKeyboard)
    else:
        gamename = userSession.get_passing_arguments(username)[0]
        game = session.getGamebyGameName(gamename)
        game.removePlayer(username)
        # context.bot.sendMessage(
        #         chat_id=game.getOwnerId(), text="Player {} has left the game".format(username))
        context.bot.sendMessage(
                chat_id=update.effective_user["id"], text="Thank you for playing", reply_markup=ReplyKeyboardMarkup([["/start"]]))
    


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("join", join_handler))
    updater.dispatcher.add_handler(CommandHandler("startGame", startGame_handler))
    updater.dispatcher.add_handler(CommandHandler("questions", seeQuestions_handler))
    updater.dispatcher.add_handler(CommandHandler("addQuestion", addQuestion_handler))
    updater.dispatcher.add_handler(CommandHandler("players", seePlayers_handler))
    updater.dispatcher.add_handler(CommandHandler("restart", restart_handler))
    updater.dispatcher.add_handler(CommandHandler("exit", exit_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, answer_handler))

    run(updater)