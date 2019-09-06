import schedule
import time, datetime
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from Storage import Storage
from MachineManager import MachineManager

led = 26
now = datetime.datetime.now()
nowTime = datetime.datetime.now().time()

actionWord = ""
actionWord2 = ""
useCheckNumber = ""

manager = MachineManager()
store = Storage("status.txt")

alreadyOpened = False
lastUpdated = now 

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
        machineUser = i.getUser()
        if machineUser != 0 and not i.getNotified():
            if diffInTime(i[1], datetime.datetime.now())[0] > 120:
                telegram_bot.sendMessage(machineUser, "Your laundry has been in the machine for more than 2hrs! It may have already been completed")
                i.alrNotified()

#convert String to Boolean
def stringToBool(s):
    if s == "True":
        return True
    else:
        return False

def action(msg):
    global useCheckNumber
    global actionWord2
    global actionWord
    global alreadyOpened
    global lastUpdated
    global manager
    global store

    chat_id = msg['chat']['id']
    command = msg['text']
    
    if not alreadyOpened:
        store.readFromStorage(manager)
        alreadyOpened = True

    print ('Recieved: ', command)
    print (nowTime)

    keyboard = ReplyKeyboardMarkup(keyboard=[['/start', '/done'], ['/use', '/status'], ["/notify", "/reset"]])
    numberkeyboard = ReplyKeyboardMarkup(keyboard=[['1', '2', '3'], ['4', '5', '6'], ['7', '/reset']])
    if command != "/reset":
        if actionWord == "" and actionWord2 == "":
            
            if "/start" in command:
                message = "Hi, how may i help you today?\n"
                message = message + "/start - Starts the bot and get help\n"
                message = message + "/done - When you are done using the machine\n"
                message = message + "/use - When you want to use a washing machine\n"
                message = message + "/notify - Notify the person that his/her laundry is ready for collection\n"
                message = message + "/reset - go back to the main page\n"
                message = message + "/status - Check the status of the laundrette\n\n"
                message = message + "Your small gesture would make it more convienient for everyone in the block."
                

            if "/done" in command:
                message = "Which machine is done?"
                keyboard = numberkeyboard
                actionWord = "done"

            if "/use" in command:
                message = "Which machine would you like to use?"
                keyboard = numberkeyboard
                actionWord = "use"

            if "/status" in command:
                message = manager.statusOfMachine(chat_id, lastUpdated)

            if"/notify" in command:
                message = "Who would you like to notify?"
                keyboard = numberkeyboard
                actionWord = "notify"

        elif actionWord and not actionWord2:
            if actionWord == "done":
                machineNumber = int(command)
                machInFocus = manager.getMachine(machineNumber)
                if not machInFocus.isInUse():
                    message = "Machine is currently not in use"
                else:
                    if(machInFocus.getUser() == chat_id):
                        message = "Thank you for colleting your clothes! Hope you have a great day"
                        machInFocus.done()
                        lastUpdated = datetime.datetime.now()

                    else:
                        message = "These are not your clothes!"

            elif actionWord == "use":
                machineNumber = int(command)
                machInFocus = manager.getMachine(machineNumber)
                if machInFocus.isInUse() and machInFocus.getUser() == chat_id:
                    message = "Your own clothes are washing! Please remember to /done first before reusing so the timer will reset :)"
                elif machInFocus.isInUse():
                    message = "Is the machine empty and the person forgot to indicate?"
                    keyboard = ReplyKeyboardMarkup(keyboard=[["yes"], ["no"], ["/reset"]])
                    actionWord2 = "useCheck"
                    useCheckNumber = machineNumber
                else:
                    message =  "Remember to come back when you receive the done message"
                    lastUpdated = datetime.datetime.now()
                    machInFocus.use(chat_id, lastUpdated, False)
                    

            elif actionWord == "notify":
                machineNumber = int(command)
                machInFocus = manager.getMachine(machineNumber)
                if not machInFocus.isInUse():
                    message = "Machine is currently not in use"
                else:
                    machUser = machInFocus.getUser()
                    if(machUser == chat_id):
                        message = "This is your own clothes"
                    else:
                        telegram_bot.sendMessage(machUser, "Your clothes are done. Do collect them soon as some one else may need to use it")
                        message =  "We have notified the user, please give the user 5mins to arrive."

            actionWord = ""

        else:

            if actionWord2 == "useCheck":
                if command == "yes":
                    machineNumber = useCheckNumber
                    machInFocus = manager.getMachine(machineNumber)
                    telegram_bot.sendMessage(machInFocus.getUser(), "It seems that you are done with the machine.\n Please remember to let me know next time!", reply_markup=keyboard)

                    lastUpdated = datetime.datetime.now()
                    machInFocus.use(chat_id, lastUpdated, False)
                    message = "Okay, we have updated to you being the user of the machine! Remember to collect your clothes! :)"

                if command == "no":
                    message = "These are not your clothes!"

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

    # print(manager.getMachList())
    store.saveToStorage(manager)


# machineStatus = [[0,0,False],[0,0, False],[0,0, False],[0,0, False],[0,0, False],[0,0,False],[0,0,False]]
# machineStatus = []
schedule.every(10).seconds.do(sendReminder, manager.getMachList())

mainBot = telepot.Bot('989321353:AAHpC8w6BAcfj6NM9Nz5hQuQF7KUl_Oj8-0')
testBot = telepot.Bot('930788863:AAGbxJ4CwV-z8hCjky0lqE13Cgda-3S59qc')
telegram_bot = testBot
print(telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print ('Up and Running')

while 1:
    schedule.run_pending()
    time.sleep(10)
