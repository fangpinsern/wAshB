from Machine import Machine
from MachineManager import MachineManager
from UserManager import UserManager
from User import User
import time, datetime

class Storage:

    def __init__(self, filePath):
        self.filePath = filePath

    def saveToStorage(self, manager):
        f= open(self.filePath, "w+")
        for i in manager.getList():
            help = i.makeForStorage()
            f.write(help)
        f.close()

    def readMachineFromStorage(self, manager):
        rf = open(self.filePath, "r")
        if rf.mode == 'r':
            contents =rf.read()
            info = contents.split("|")
            # print(info)
            # print(int(len(info)/4))
            for i in range(int(len(info)/4)):
                user = int(info[i*4])
                time = info[i*4 + 1]
                if time != "0":
                    time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
                s = info[i*4 + 2]
                if s == "True":
                    hasNotified = True
                else:
                    hasNotified = False
                machType = info[i*4 + 3]
                newMachine = Machine(machType)
                newMachine.use(user, time, hasNotified)
                manager.addEntity(newMachine)

    def readUserFromStorage(self, manager):
        rf = open(self.filePath, "r")
        if rf.mode == 'r':
            contents =rf.read()
            info = contents.split("|")
            for i in range(int(len(info)/3)):
                username = info[i*3]
                userid = int(info[i*3 + 1])
                time = int(info[i*3 + 2])
                newUser = User(username, userid)
                newUser.setTime(time)
                manager.addEntity(newUser)