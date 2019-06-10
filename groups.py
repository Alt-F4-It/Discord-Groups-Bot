import os, pickle

allGroups = []

class aGroup(object):
    def __init__(self):
        self.groupName = ""
        self.groupDesc = ""
        self.groupMembers = []

    def addMember(self, newMember):
        if not self.groupMembers.__contains__(newMember):
            self.groupMembers.append(newMember)
            self.save()
            print("Member Added")
        else:
            print("Member Already Existed")

    def removeMember(self, existingMember):
        if self.groupMembers.__contains__(existingMember):
            self.groupMembers.remove(existingMember)
            self.save()
            print("Member Removed")
        else:
            print("Member Didn't Exist")

    def load(self, groupName):
        groupSave = "group." + groupName
        loadedGroup = pickle.load(open(groupSave, "rb"))
        self.groupName = loadedGroup.groupName
        self.groupDesc = loadedGroup.groupDesc
        self.groupMembers = loadedGroup.groupMembers

    def save(self):
        groupSave = "group." + self.groupName

        pickle.dump(self, open(groupSave, "wb"))
        groupList = [line.rstrip('\n') for line in open('groups.List')]
        groupFile = open("groups.List", "a")
        alreadyExists = False
        for eachGroup in groupList:
            if self.groupName == eachGroup:
                alreadyExists = True
        if alreadyExists == False:
            groupFile.write(self.groupName + "\n")
        else:
            print("Group Record Already Created")
        groupFile.close()
        loadGroups()

    def delete(self):
        groupSave = "group." + self.groupName
        os.remove(groupSave)
        groupList = [line.rstrip('\n') for line in open('groups.List')]
        groupFile = open("groups.List", "w+")
        for eachGroup in groupList:
            if self.groupName != eachGroup:
                groupFile.write(eachGroup)
        groupFile.close()


def loadGroups():
    groupList = [line.rstrip('\n') for line in open('groups.List')]
    for eachGroup in groupList:
        if int(eachGroup.__len__()) > 1:
            saveName = "group." + eachGroup
            pickleGroup = pickle.load(open(saveName, "rb"))
            pickleGroup.load(eachGroup)
            allGroups.append(pickleGroup)

def listGroups():
    groupList = [line.rstrip('\n') for line in open('groups.List')]
    return groupList


loadGroups()

