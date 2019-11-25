import telegram
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
import logging
from time import sleep
from gpiozero import MCP3008,PWMLED
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)


#when the user starts talking with bot
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Yo yo wasap boys it's Animesh 3000")
    #write the user id of the person who starts chatting with the bot
    text_file = open("users.txt", "a")
    text_read = open("users.txt", "r")
    #comma separated IDs are written in the users.txt if they are not written already
    if str(update.message.chat_id) not in text_read.read():
        text_file.write(str(update.message.chat_id)+' ')
    text_file.close()

#sends temperature from the sensor, replace the value of text with the actual value from the sensor
#it's slower to call this function(around several seconds in worst cases) than to just use bot.send_message in the loop - consider removing it completely
def temperature(update, context):
    try:
        kek = temp()
        bot.send_message(chat_id=update.message.chat_id, text="Temperature from the sensor goes here"+ str(kek))
    except BadRequest as e:
        if str(e)=="Chat not found":
            print("id from text file fuckery")
        print(e)


def temp():
    temp1 = MCP3008(0)
    T = 15 * temp1.raw_value - 2048
    whole = T / 100
    temp = T/100
    sleep(0.5)
    return(temp)

#alarm function
def alarm(temp, userid):
    alarm="***ALERT !!! TEMPERATURE BROKE THE THRESHHOLD, CURRENT TEMPERATURE: " + str(temp) + "C"
    #if the temperature goes lower than minimum or higher than maximum, the bot will send the message wit
    bot.send_message(chat_id=userid, text=alarm)
    #bot.send_message(chat_id="Ckti4BRuCEzsLJ6mFvczMQ", text=alarm)    
    
#unknown command handler    
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't understend")


#constants for temperature thresholds
min_temp = 1
max_temp = 22
bot = telegram.Bot(token='1011338484:AAHkUFziy2zyDWDgfANzpAgGJr9baERaO70')
#tests if the bot exists
print(bot.get_me())
#initialize updater and dispatcher
updater = Updater(token='1011338484:AAHkUFziy2zyDWDgfANzpAgGJr9baERaO70', use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
#/current_temp - command to check the current temperature of the sesnor
temperature_handler = CommandHandler('current_temp',temperature)
dispatcher.add_handler(temperature_handler)
#read the users from the users.txt  
#split the user IDs into the chatid array
while True: 
    text_file = open("users.txt", "r")
    #split the user IDs into the chatid array
    chatid = text_file.read()
    chatid = chatid.split(' ')
    #remove the comma from the last id in the text file
    #chatid[len(chatid)-1] = chatid[len(chatid)-1].replace(',','')
   # dispatcher.add_handler(temperature_handler)
    # bot.send_message(chat_id=chatid[1], text="Temperature is: ")
    """here goes the retrieval of temperature from the sensor"""
    """***TEMPERATURE FETCH***"""
    tem1 = temp() 
    for id in chatid:
        #it's faster to just use bot.send_message than to call the function
        #bot.send_message(chat_id=id, text="Temperature is: ")
        if not (max_temp>=tem1>=min_temp):
            if id:
                try:
                    alarm(tem1, id)
                except BadRequest as e:
                    print(e)
                    pass
    sleep(10)
text_file.close()
