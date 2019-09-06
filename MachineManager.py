import time, datetime

class MachineManager:

    def __init__(self):
        self.machineList = []
    
    def addMachine(self, machine):
        self.machineList.append(machine)

    def getMachine(self, i):
        return self.machineList[i - 1]

    def diffInTime(self, t1, t2):
        c = t2 - t1
        timeDiff = divmod(c.days * 86400 + c.seconds, 60)
        return timeDiff

    def statusOfMachine (self, user, lastUpdated):
        message = ""
        machList = self.machineList
        for x in range(len(machList)):
            a = str(x + 1)
            mach = self.getMachine(x + 1)
            if not mach.isInUse():
                message = message + a + " (" + mach.getType() + ")" + " is Available\n"
            else:
                message = message + a + " is Unavailable (Time used: " + str(self.diffInTime(mach.getTime(), datetime.datetime.now())[0]) + " minutes)\n"
        message = message + "\n"
        for i in range(len(machList)):
            mach = self.getMachine(i + 1)
            if mach.getUser() == user:
                message = message + "Currently using: " + str(i+1) + "\n"
        s2 = lastUpdated.strftime("%d/%m/%Y, %H:%M:%S")
        message = message + "\n"
        message = message + "Last Updated: " + s2

        return message

    def getMachList(self):
        return self.machineList
