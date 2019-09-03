import schedule
import time, datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

led = 26
now = datetime.datetime.now()
nowTime = datetime.datetime.now().time()

actionWord = ""
actionWord2 = ""

#t1 is the initial time
#t2 is the current time
def diffInTime(t1, t2):
    c = t2 - t1
    timeDiff = divmod(c.days * 86400 + c.seconds, 60)
    return timeDiff

#Sends reminder for the clothing
def sendReminder(mArray):
    print("I am here")
    for i in mArray:
        machineUser = i[0]
        if machineUser != 0 and not i[2]:
            if diffInTime(i[1], datetime.datetime.now())[0] > 1:
                telegram_bot.sendMessage(machineUser, "Your laundry has been in the machine for more than 2hrs! It may have already been completed")
                i[2] = True

def action(msg):
    global actionWord2
    global actionWord
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Recieved: ', command)
    print (nowTime)

    keyboard = ReplyKeyboardMarkup(keyboard=[['/start', '/done'], ['/use', '/status'], ["/notify", "/reset"]])
    if command != "/reset":
        if actionWord == "" and actionWord2 == "":
            
            if "/start" in command:
                message = "Hi, how may i help you today?\n"
                message = message + "/start - Starts the bot and get help\n"
                message = message + "/done - When you are done using the machine\n"
                message = message + "/use - When you want to use a washing machine\n"
                message = message + "/notify - Notify the person that his/her laundry is ready for collection\n"
                message = message + "/status - Check the status of the laundrette\n\n"
                message = message + "Your small gesture would make it more convienient for everyone in the block."
                

            if "/done" in command:
                # found = False
                # machineCounter = 1
                # machineNumber = 0
                # for j in machineStatus:
                #     if(j[0] == chat_id):
                #         found = True
                #         machineNumber = machineCounter
                #     else:
                #         machineCounter = machineCounter + 1
                
                # if found:
                #     message = "Thank you for collecting your clothes! Hope you have a nice day"
                #     machineStatus[machineNumber - 1][0] = 0
                # else:
                #     message = "You are not using any machines at the moment!"
                message = "Which machine is done?"
                keyboard = ReplyKeyboardMarkup(keyboard=[['1', '2', '3'], ['4', '5', '/reset']])
                actionWord = "done"

            if "/use" in command:
                message = "Which machine would you like to use?"
                keyboard = ReplyKeyboardMarkup(keyboard=[['1', '2', '3'], ['4', '5', '/reset']])
                actionWord = "use"

            if "/status" in command:
                message = ""
                for x in range(5):
                    a = str(x + 1)
                    if(machineStatus[x][0] == 0):
                        message = message + a + " is Available\n"
                    else:
                        message = message + a + " is Unavailable (Time used: " + str(diffInTime(machineStatus[x][1], datetime.datetime.now())[0]) + " minutes)\n"
            
            if"/notify" in command:
                message = "Who would you like to notify?"
                keyboard = ReplyKeyboardMarkup(keyboard=[['1', '2', '3'], ['4', '5', '/reset']])
                # keyboard = ReplyKeyboardMarkup(keyboard=[['/surprise'], ['/expected']])
                actionWord = "notify"
            
            # telegram_bot.sendMessage(chat_id, message, reply_markup=keyboard)

        elif actionWord and not actionWord2:
            if actionWord == "done":
                # found = False
                # machineCounter = 1
                # machineNumber = 0
                # for j in machineStatus:
                #     if(j[0] == chat_id):
                #         found = True
                #         machineNumber = machineCounter
                #     else:
                #         machineCounter = machineCounter + 1
                
                # if found:
                #     message = "Thank you for collecting your clothes! Hope you have a nice day"
                #     machineStatus[machineNumber - 1][0] = 0
                # else:
                #     message = "You are not using any machines at the moment!"
                machineNumber = int(command)
                if machineStatus[machineNumber - 1][0] == 0:
                    message = "Machine is currently not in use"
                else:
                    if(machineStatus[machineNumber - 1][0] == chat_id):
                        message = "Thank you for colleting your clothes! Hope you have a great day"
                        machineStatus[machineNumber - 1][0] = 0
                    else:
                        message = "These are not your clothes!"

            elif actionWord == "use":
                machineNumber = int(command)
                if machineStatus[machineNumber - 1][0] !=0:
                    message = "Sorry, this machine is currently being used."
                
                else:
                    message =  "Remember to come back when you receive the done message"
                    machineConfig = machineStatus[machineNumber - 1]
                    machineConfig[0] = chat_id
                    machineConfig[1] = datetime.datetime.now()

            elif actionWord == "notify":
                machineNumber = int(command)
                if machineStatus[machineNumber - 1][0] == 0:
                    message = "Machine is currently not in use"
                else:
                    if(machineStatus[machineNumber - 1][0] == chat_id):
                        message = "This is your own clothes"
                    else:
                        telegram_bot.sendMessage(machineStatus[machineNumber - 1][0], "Your clothes are done. Do collect them soon as some one else may need to use it")
                        message =  "We have notified the user, please give the user 5mins to arrive."

                # actionWord2 = command
                
                # if actionWord2 == "/surprise":
                #     message = "Which machine surprised you?"
                #     keyboard = ReplyKeyboardMarkup(keyboard=[['1', '2', '3'], ['4', '5']])
                # elif actionWord2 == "/expected":
                #     message = "Which machine?"
                #     keyboard = ReplyKeyboardMarkup(keyboard=[['1', '2', '3'], ['4', '5']])
            
            actionWord = ""
            # telegram_bot.sendMessage(chat_id, message, reply_markup=keyboard)

        else:
            # userID = 39187936
            # machineNumber = int(command)
            # if actionWord2 == "/surprise":
            #     message = "We have notified the block chat!"
            #     message2 = "Hi, machine " + str(machineNumber) + " is in use but no one informed me!! Kindly let me know who has used it!"
            #     telegram_bot.sendMessage(userID, message2)
            # elif actionWord2 == "/expected":
            #     if machineStatus[machineNumber - 1][0] == 0:
            #         message = "Machine is currently not in use"
            #     else:
            #         if(machineStatus[machineNumber - 1][0] == chat_id):
            #             message = "This is your own clothes"
            #         else:
            #             telegram_bot.sendMessage(machineStatus[machineNumber - 1][0], "Your clothes are done. Do collect them soon as some one else may need to use it")
            #             message =  "We have notified the user, please give the user 5mins to arrive."
            #  else:
            actionWord = ""
            actionWord2 = ""
            keyboard = ReplyKeyboardMarkup(keyboard=[['/start', '/done'], ['/use', '/status'], ["/notify", "/reset"]])
            actionWord2 = ""
                
        telegram_bot.sendMessage(chat_id, message, reply_markup=keyboard)

    else:
        actionWord = ""
        actionWord2 = ""
        keyboard = ReplyKeyboardMarkup(keyboard=[['/start', '/done'], ['/use', '/status'], ["/notify", "/reset"]])
        message = "Back to homepage!"
        telegram_bot.sendMessage(chat_id, message, reply_markup=keyboard)


machineStatus = [[0,0,False],[0,0, False],[0,0, False],[0,0, False],[0,0, False]]
    
schedule.every(10).seconds.do(sendReminder, machineStatus)


telegram_bot = telepot.Bot('989321353:AAHpC8w6BAcfj6NM9Nz5hQuQF7KUl_Oj8-0')
print(telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print ('Up and Running')

while 1:
    schedule.run_pending()
    time.sleep(10)
