import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
import logging
from time import sleep
from gpiozero import MCP3008,PWMLED
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)


#when the user starts talking with bot
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Yo yo wasap boys it's Animesh 3000 🤖")
    #write the user id of the person who starts chatting with the bot
    text_file = open("users.txt", "a")
    text_read = open("users.txt", "r")
    #comma separated IDs are written in the users.txt if they are not written already
    if str(update.message.chat_id) not in text_read.read():
        text_file.write(str(update.message.chat_id)+' ')
    text_file.close()

#sends temperature from the sensor to the user who requested it
def temperature(update, context):
    try:
        kek = temp()
        bot.send_message(chat_id=update.message.chat_id, text="🌡️ Current temperature is: "+ str(kek))
    except BadRequest as e:
        pass

#returns the temperature from the sensor
def temp():
    temp1 = MCP3008(0)
    T = 15 * temp1.raw_value - 2048
    whole = T / 100
    temp = T/100
    sleep(0.5)
    return(temp)

#alarm function
def alarm(temp, userid):
    alarm="⚠️***ALERT ***⚠️ TEMPERATURE BROKE THE THRESHOLD, 🌡️ CURRENT TEMPERATURE: " + str(temp) + "C"
    #if the temperature goes lower than minimum or higher than maximum, the bot will send the message wit
    bot.send_message(chat_id=userid, text=alarm)
       
    
#unknown command handler    
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't understend")


#constants for temperature thresholds
min_temp = input("set the minimal temperature: ")
max_temp = input("set the maximum temperature: ")
#input the token once on startup
token = input("please input token")
bot = telegram.Bot(token=token)
#tests if the bot exists
print(bot.get_me())
#initialize updater and dispatcher (Telegram API)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
#/start - initiates the dialogue wiht the bot, default telegram bot command
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
#/current_temp - command to check the current temperature of the sesnor
temperature_handler = CommandHandler('current_temp',temperature)
dispatcher.add_handler(temperature_handler)
while True: 
    text_file = open("users.txt", "r")
    #split the user IDs into the chatid list
    chatid = text_file.read()
    chatid = chatid.split(' ')
    #receive temperature from sensor
    tem1 = temp()
    #cycles through the ids in the file while also checking the temperature and
    #sends the alert if the temperature goes over the limit
    for id in chatid:
        if not (int(max_temp)>=tem1>=int(min_temp)):
            try:
                alarm(tem1, id)
            except BadRequest as e:
                print(e)
                pass
    
    #sets the pause between the loop cycles to not overload the API and receive negative response from the server
    sleep(10)
text_file.close()
