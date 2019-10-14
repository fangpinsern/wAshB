class Machine:
    
    def __init__(self, machType):
        self.machType = machType
        self.user = 0
        self.time = 0
        self.hasNotified = False

    #machine is in Use
    def use(self, user, time, hasNotified):
        self.user = user
        self.time = time
        self.hasNotified = hasNotified
        return True

    def isInUse(self):
        return self.user != 0

    def getType(self):
        return self.machType
    
    def getUser(self):
        return self.user

    def getTime(self):
        return self.time

    def getNotified(self):
        return self.hasNotified

    def done(self):
        self.user = 0
        self.time = 0
        self.hasNotified = False
        return True

    def alrNotified(self):
        self.hasNotified = True
        return True

    def makeForStorage(self):
        # chat_ID = machineStatus[i][0]
        # startTime = machineStatus[i][1]
        # hasNotified = machineStatus[i][2]
        help = str(self.user) + "|" + str(self.time) + "|" + str(self.hasNotified) + "|" + str(self.machType) + "|"
        return help
