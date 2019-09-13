class Manager(object):

    def __init__(self):
        self.manageList = []

    def addEntity(self, entity):
        self.manageList.append(entity)

    def getEntity(self, number):
        return self.manageList[number - 1]

    def getList(self):
        return self.manageList

    def diffInTime(self, t1, t2):
        c = t2 - t1
        timeDiff = divmod(c.days * 86400 + c.seconds, 60)
        return timeDiff