from Manager import Manager

class UserManager(Manager):

    def __init__(self):
        super().__init__()

    def userInList(self, username):
        isIn = False
        for i in self.manageList:
            if i.getUsername() == username:
                isIn = True
                break
            else:
                continue

        return isIn
            