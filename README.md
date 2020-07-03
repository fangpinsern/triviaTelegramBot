# Trivia Telegram Bot

## Description

Designed to host trivia quizes on the telegram chat app! Fun for groups!

## User Guide

The bot will guide you through the process of how to join a game.

To set up a game:

1. `/start` to start the bot
2. `/startGame` - This command starts a new game
3. The bot will then ask you to enter your game room name. This name will be used by your group to join the game. Hence it is recommended to go with a simple name. (it is case senstive)
4. While the others are joining, you will need to add questions to your game using the `/addQuestion` command. You have the option to add manually, or allow the bot to access the questions in a google sheet. The format of the google sheet has to be strictly followed. It is attached at the bottom.
5. To check the players who have joined, use the `/players` command.
6. Once all the players have joined, you can hit the `/begin` command.
7. Once everyone has answered the question, you will hit the `/next` command to move on to the stage of giving points.
8. At this stage, the user names of all the players in games will show up on your keyboard. Hit those that have given the correct answer.
9. Once done, hit `/next`
10. Once the game is finished, enter the `/endgame` command and they will show who is the winner as well as send a message to all the users with their positions.

To join a game:

1. `/start` to start the bot
2. `/join` to join a game
3. You will be prompted to enter a game name. The person hosting the game will provide you with that information.
4. At any point in time you decide to exit the game, enter the command `/exit`

### Commands - For reference. The bot should have all the commands you can use available on the keyboard

`/start` - Start up the bot
`/join` - join a game
`/startGame` - start a new game
`/restart` - if you get stuck at any point, hit to restart the bot
`/exit` - for players to exit the game
`/questions` - to see the questions that are for the game
`/addQuestion` - to add questions to the game
`/players` - to see the players in game
`/begin` - to start the game proper
`/next` - move on to the next portion whether question or points giving
`/endGame` - ends the game and give the points
`/burden` - To see who has yet to answer hence holding the game back
`/addQnByGoogleSheet` - adds question by google sheet

## Google Sheet Format

| Questions                    |
| ---------------------------- |
| What is my name?             |
| How far is the nearest star? |
| Is the earth round?          |
