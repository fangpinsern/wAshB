from Machine import Machine
from MachineManager import MachineManager
import time, datetime

class Storage:

    def __init__(self, filePath):
        self.filePath = filePath

    def saveToStorage(self, machineManager):
        f= open(self.filePath, "w+")
        for i in machineManager.getMachList():
            help = i.makeForStorage()
            print(help)
            f.write(help)
        f.close()

    #incomplete!
    def readFromStorage(self, machineManager):
        rf = open(self.filePath, "r")
        if rf.mode == 'r':
            contents =rf.read()
            info = contents.split("|")
            print(info)
            print(int(len(info)/4))
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
                machineManager.addMachine(newMachine)
                # if du == "0":
                #     machineStatus[i][0] = 0
                # else:
                #     machineStatus[i][0] = int(info[i*3])
                # dt = info[i*3 + 1]
                # if dt != "0":
                #     machineStatus[i][1] = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")
                # machineStatus[i][2] = stringToBool(info[i*3 + 2])
            print(machineManager.getMachList())