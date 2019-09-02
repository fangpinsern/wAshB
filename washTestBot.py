import schedule
import time, datetime
#import RPi.GPIO as GPIO
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

led = 26
now = datetime.datetime.now()
nowTime = datetime.datetime.now().time()
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)

#LED
# GPIO.setup(led, GPIO.OUT)
# GPIO.output(led,0) #initially off state

actionWord = ""

#t1 is the initial time
#t2 is the current time
def diffInTime(t1, t2):
    c = t2 - t1
    timeDiff = divmod(c.days * 86400 + c.seconds, 60)
    return timeDiff

def sendReminder(mArray):
    print("I am here")
    for i in mArray:
        machineUser = i[0]
        if machineUser != 0:
            if diffInTime(i[1], datetime.datetime.now())[0] > 1:
                telegram_bot.sendMessage(machineUser, "Your laundry has been in the machine for more than 2hrs! It may have already been completed")
    # if diffInTime(t1,t2)[0] > 1:
    #     message = "Your laundry has been in form more than 1hr!"
    #     telegram_bot.sendMessage(chat_id, message)

def scheduleTest():
    print("I am here")



def action(msg):
    global actionWord
    chat_id = msg['chat']['id']
    command = msg['text']

    print ('Recieved: ', command)
    print (nowTime)

    keyboard = ReplyKeyboardMarkup(keyboard=[['/start', '/done'], ['/use', '/status']])
    if actionWord == "":
        
        if "/start" in command:
            message = "Hi, how may i help you today?\n"
            

        if "/done" in command:
            message = "Which machine is done?"
            keyboard = ReplyKeyboardMarkup(keyboard=[['1', '2', '3'], ['4', '5']])
            actionWord = "done"
            # commandArr =  command.split()
            # if(len(commandArr) > 2):
            #     print(len(commandArr))
            #     message = "Sorry I do not understand this"
            # else :
            #     try:
            #         machineNumber = int(commandArr[1])
            #         message =  "We have notified the user, please give the user 5mins to arrive."
            #         telegram_bot.sendMessage(machineStatus[machineNumber - 1], "Your clothes are done")
            #         machineStatus[machineNumber - 1] = 0
            #     except ValueError:
            #         print(commandArr[1])
            #         message = "This machine does not exist"

        if "/use" in command:
            message = "Which machine would you like to use?"
            keyboard = ReplyKeyboardMarkup(keyboard=[['1', '2', '3'], ['4', '5']])
            actionWord = "use"
            # commandArr =  command.split()
            # if(len(commandArr) > 2):
            #     print(len(commandArr))
            #     message = "Sorry I do not understand this"
            # else:
            #     try:
            #         machineNumber = int(commandArr[1])
            #         message =  "Remember to come back when you receive the done message"
            #         machineStatus[machineNumber - 1] = chat_id
            #     except ValueError:
            #         print(commandArr[1])
            #         message = "This machine does not exist"

        if "/status" in command:
            message = ""
            for x in range(5):
                a = str(x + 1)
                if(machineStatus[x][0] == 0):
                    message = message + a + " is Available\n"
                else:
                    message = message + a + " is Unavailable (Time used: " + str(diffInTime(machineStatus[x][1], datetime.datetime.now())[0]) + " minutes)\n"
        
        
        telegram_bot.sendMessage(chat_id, message, reply_markup=keyboard)

    # telegram_bot.sendMessage(chat_id, message)

    else :
        if actionWord == "done":
            machineNumber = int(command)
            if machineStatus[machineNumber - 1][0] == 0:
                message = "Machine is currently not in use"
            else:
                
                if(machineStatus[machineNumber - 1][0] == chat_id):
                    message = "Thank you for colleting your clothes on time"
                else:
                    telegram_bot.sendMessage(machineStatus[machineNumber - 1][0], "Your clothes are done")
                    message =  "We have notified the user, please give the user 5mins to arrive."
                
                machineStatus[machineNumber - 1][0] = 0

        if actionWord == "use":
            machineNumber = int(command)
            if machineStatus[machineNumber - 1][0] !=0:
                message = "Sorry, this machine is currently being used."
            
            else:
                message =  "Remember to come back when you receive the done message"
                machineConfig = machineStatus[machineNumber - 1]
                machineConfig[0] = chat_id
                machineConfig[1] = datetime.datetime.now()

        actionWord = ""
            
        telegram_bot.sendMessage(chat_id, message, reply_markup=keyboard)

    
    # if 'on' in command:
    #     message = "Turned on "
    #     if 'led' in command:
    #         message = message + "led"
    #         GPIO.output(led, 1)
    #         telegram_bot.sendMessage(chat_id, message)

    # if 'off' in command:
    #     message = "Turned off "
    #     if 'led' in command:
    #         message = message + "led"
    #         # GPIO.output(led, 0)
    #         # telegram_bot.sendMessage(chat_id, message)


machineStatus = [[0,0],[0,0],[0,0],[0,0],[0,0]]
# for i in machineStatus:
#     machineUser = i[0]
#     if machineUser != 0:
#         if diffInTime(i[1], datetime.datetime.now())[0] > 1:
#             telegram_bot.sendMessage(machineUser, "Your laundry has been in the machine for more than 2hrs! It may have already been completed")

    
schedule.every(10).seconds.do(sendReminder, machineStatus)


telegram_bot = telepot.Bot('989321353:AAHpC8w6BAcfj6NM9Nz5hQuQF7KUl_Oj8-0')
print(telegram_bot.getMe())

MessageLoop(telegram_bot, action).run_as_thread()
print ('Up and Running')

while 1:
    schedule.run_pending()
    time.sleep(10)
