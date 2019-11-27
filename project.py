import telegram
import os
import subprocess
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
import logging
from time import sleep
from gpiozero import MCP3008,PWMLED
from telegram.error import (TelegramError, Unauthorized, BadRequest, 
                            TimedOut, ChatMigrated, NetworkError)


#when the user starts talking with bot, stores the chat id in a separate file
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Yo yo wasap boys it's Animesh 3000 🤖")
    #write the user id of the person who starts chatting with the bot
    text_file = open("users.txt", "a")
    text_read = open("users.txt", "r")
    #comma separated IDs are written in the users.txt if they are not written already
    if str(update.message.chat_id) not in text_read.read():
        text_file.write(str(update.message.chat_id)+' ')
    text_file.close()


#sends the temperature to the user who requested it
def temperature(update, context):
    cmd1 = "sudo espeak \"The temperature is %s celcius\" -w /home/pi/src/fm_transmitter/file.wav"
    cmd2 = "sudo /home/pi/src/fm_transmitter/fm_transmitter -f 87.50 /home/pi/src/fm_transmitter/file.wav"

    try:
        kek = temp()
        bot.send_message(chat_id=update.message.chat_id, text="🌡️ Current temperature is: "+ str(kek))
        subprocess.call(cmd1 % kek, shell=True)
        sleep(2)
        subprocess.call(cmd2, shell=True)
    except BadRequest as e:
        print(e)

#calculation of the temperature from the sensor
def temp():
    temp1 = MCP3008(0)
    T = 15 * temp1.raw_value - 2048
    whole = T / 100
    temp = T/100
    sleep(0.5)
    return(temp)

#alarm function that is called when the temperature breaks the limit
def alarm(temp, userid):
    alarm="⚠️***ALERT ***⚠️ TEMPERATURE BROKE THE THRESHOLD, 🌡️ CURRENT TEMPERATURE: " + str(temp) + "C"
    #if the temperature goes lower than minimum or higher than maximum, the bot will send the message wit
    bot.send_message(chat_id=userid, text=alarm)
       
    
#unknown command handler    
def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I don't understend")


#constants for temperature thresholds
min_temp = 1
max_temp = 22
#first argument for cli to generate the temperature voice line
cmd1 = "sudo espeak \"The temperature is %s celcius\" -w /home/pi/src/fm_transmitter/file.wav"
cmd2 = "sudo /home/pi/src/fm_transmitter/fm_transmitter -f 87.50 /home/pi/src/fm_transmitter/file.wav"
#input the token once on start
token = input("enter the token")
bot = telegram.Bot(token=token)
#tests if the bot exists
print(bot.get_me())
#initialize updater and dispatcher
updater = Updater(token=token, use_context=True)
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
    #receive temperature from sensor
    tem1 = temp() 
    for id in chatid:
        if not (max_temp>=tem1>=min_temp):
            if id:
                try:
                    alarm(tem1, id)
                except BadRequest as e:
                    print(e)
                    pass
    sleep(10)
text_file.close()
