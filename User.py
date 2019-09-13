class User:
    
    def __init__(self, username, userid):
        self.username = username
        self.userid = userid
        self.usageTime = 120

    def setTime(self, usageTime):
        self.usageTime = usageTime

    def getUsername(self):
        return self.username

    #Update the usage time
    #Reasoning: The machine user usually use the same settings.
    #If they update the bot, we can see the time they take to use the machine 
    #and cater a personalized reminder to the user
    def updateUsageTime(self, usageTime):
        self.usageTime = usageTime

    def makeForStorage(self):
        help = str(self.username) + "|" + str(self.userid) + "|" + str(self.usageTime) + "|"
        return help