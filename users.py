import os, pickle

allUsers = []

class aUser(object):
    def __init__(self):
        self.userName = ""
        self.userDesc = ""
        self.userMembers = []

    def addMember(self, newMember):
        if not self.userMembers.__contains__(newMember):
            self.userMembers.append(newMember)
            self.save()
            print("Member Added")
        else:
            print("Member Already Existed")

    def removeMember(self, existingMember):
        if self.userMembers.__contains__(existingMember):
            self.userMembers.remove(existingMember)
            self.save()
            print("Member Removed")
        else:
            print("Member Didn't Exist")

    def load(self, userName):
        userSave = "user." + userName
        loadedUser = pickle.load(open(userSave, "rb"))
        self.userName = loadedUser.userName
        self.userDesc = loadedUser.userDesc
        self.userMembers = loadedUser.userMembers

    def save(self):
        userSave = "user." + self.userName

        pickle.dump(self, open(userSave, "wb"))
        userList = [line.rstrip('\n') for line in open('users.List')]
        userFile = open("users.List", "a")
        alreadyExists = False
        for eachUser in userList:
            if self.userName == eachUser:
                alreadyExists = True
        if alreadyExists == False:
            userFile.write(self.userName + "\n")
        else:
            print("User Record Already Created")
        userFile.close()
        loadUsers()

    def delete(self):
        userSave = "user." + self.userName
        os.remove(userSave)
        userList = [line.rstrip('\n') for line in open('users.List')]
        userFile = open("users.List", "w+")
        for eachUser in userList:
            if self.userName != eachUser:
                userFile.write(eachUser)
        userFile.close()


def loadUsers():
    userList = [line.rstrip('\n') for line in open('users.List')]
    for eachUser in userList:
        if int(eachUser.__len__()) > 1:
            saveName = "user." + eachUser
            pickleUser = pickle.load(open(saveName, "rb"))
            pickleUser.load(eachUser)
            allUsers.append(pickleUser)

def listUsers():
    userList = [line.rstrip('\n') for line in open('users.List')]
    return userList


loadUsers()

