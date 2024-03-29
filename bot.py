import groups
import discord_argparse
from discord.ext import commands

allGroups = groups.allGroups

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='>', description=description)

createGroupParams = discord_argparse.ArgumentConverter(
    name = discord_argparse.RequiredArgument(
        str,
        doc="The Name Of The Group",
        default="Default Group"
    ),
    desc = discord_argparse.RequiredArgument(
        str,
        doc="Description Of The Group",
        default="Default Description"
    )
)

defineGroupParams = discord_argparse.ArgumentConverter(
    name = discord_argparse.RequiredArgument(
        str,
        doc="The Name Of The Group",
        default="Default Group"
    )
)

defineBioParams = discord_argparse.ArgumentConverter(
    desc = discord_argparse.RequiredArgument(
        str,
        doc="The Name Of The Group",
        default="Default Group"
    )
)

defineUserParams = discord_argparse.ArgumentConverter(
    desc = discord_argparse.RequiredArgument(
        str,
        doc="The Name Of The User",
        default="UserX"
    )
)



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def commands(ctx):
        commands = "```Group Bot Commands\n\n" \
                   "command argName=value -- PRO TIP -- Use \"double quotes\" to surround any name, phrase, or sentence that has a space in it. Discord Python wrapper does not do a very good job of parsing commands.\n\n" \
                   "mkGroup name=\"Group Name\" desc=\"Group Description\" -- Allows you to create a group with a name and description\n" \
                   "defGroup name=\"Group Name\" desc=\"Group Description\" -- Retrieves the group definition and all subscribed users.\n" \
                   "descGroup name=\"Group Name\" desc=\"Group Description\" -- Allows you to change the definition of a group.\n" \
                   "lsGroup name=\"Group Name\" -- Lists all groups currently available.\n" \
                   "lsUser name=\"User Name\" -- Lists all groups the user queried is a member of.\n" \
                   "addUser name=\"Group Name\" -- Adds you as a member of a group.\n" \
                   "delUser name=\"Group Name\" -- Deletes your membership to a group.\n" \
                   "addBio desc=\"Your complete bio. Try not to use double quotes here.\" -- Yeah put your bio here that you want to make available to aeveryone else." \
                   "getBio name=\"User Name of the Person you want to read about.\" -- Put the person's name here if you want to read their Bio. Ppl with spaces in their names must be surrounded by double quotes." \
                   "```"

        await ctx.send(commands)



# region Group Commands
@bot.command()
async def mkGroup(ctx, *, params:createGroupParams=createGroupParams.defaults()):
        newGroup = groups.aGroup()
        newGroup.groupName = params['name']
        newGroup.groupDesc = params['desc']
        newGroup.save()
        await ctx.send(newGroup.groupName + " successfully created.")

@bot.command()
async def upGroupDesc(ctx, *, params:createGroupParams=createGroupParams.defaults()):
        isDone = False
        for eachGroup in allGroups:
            if not isDone:
                if eachGroup.groupName == params['name']:
                    eachGroup.groupDesc = params['desc']
                    eachGroup.save()
                    isDone = True
        await ctx.send("Group Name: " + params['name'] + " description updated.")

@bot.command()
async def getGroup(ctx, *, params:defineGroupParams=defineGroupParams.defaults()):
        isDone = False
        definition = ""
        groupMembers = []
        for eachGroup in allGroups:
            if not isDone:
                if eachGroup.groupName == params['name']:
                    definition = eachGroup.groupDesc
                    groupMembers = eachGroup.groupMembers
                    isDone = True
        await ctx.send("Group Name: " + params['name'] + "\n\nGroup Users: " + str(groupMembers) +"\n\nGroup Description: " + definition)

@bot.command()
async def addGroupMember(ctx, *, params:defineGroupParams=defineGroupParams.defaults()):
        isDone = False
        for thisGroup in allGroups:
            if not isDone:
                if thisGroup.groupName == params['name']:
                    thisGroup.addMember("\"" + ctx.author._user.display_name + "\"")
                    isDone = True
        await ctx.send(ctx.author._user.display_name + " successfully added to " + params['name'])

@bot.command()
async def delGroupMember(ctx, *, params:defineGroupParams=defineGroupParams.defaults()):
        isDone = False
        for thisGroup in allGroups:
            if not isDone:
                if thisGroup.groupName == params['name']:
                    thisGroup.removeMember("\"" + ctx.author._user.display_name + "\"")
                    isDone = True
        await ctx.send(ctx.author._user.display_name + " successfully removed from " + params['name'])

@bot.command()
async def listAllGroups(ctx):
        groupList = []
        for aGroup in allGroups:
            if not groupList.__contains__(aGroup.groupName):
                groupList.append(aGroup.groupName)
        await ctx.send(str(groupList))
        #isDone = False
        #userList = []
        #for thisGroup in allGroups:
        #    if not isDone:
        #        if thisGroup.groupName == params['name']:
        #            userList = thisGroup.groupMembers
        #            isDone = True
        #await ctx.send(thisGroup.groupName + " Users:\n" + str(userList))


@bot.command()
async def getUserGroups(ctx, *, params: defineGroupParams = defineGroupParams.defaults()):
    groupList = []
    fullName = "\"" + params["name"] + "\""
    for thisGroup in allGroups:
            for eachMember in thisGroup.groupMembers:
                print(eachMember)
                if eachMember == fullName:
                    if not groupList.__contains__(thisGroup.groupName):
                        groupList.append(thisGroup.groupName)
    await ctx.send(params['name'] + " belongs to these groups:\n" + str(groupList))
# endregion


@bot.command()
async def addUser(ctx):
    userName = ctx.author._user.display_name
    fileName = "user." + userName
    userFile = open(fileName, "w+")
    userFile.write("")
    userFile.close()
    await ctx.send("User File For: " + userName + " successfully created.")

@bot.command()
async def addBio(ctx, *, params: defineBioParams = defineBioParams.defaults()):
    bio = params['desc']
    author = ctx.author._user.display_name
    fileName = author + ".bio"
    bioFile = open(fileName, "w+")
    bioFile.write(bio)
    bioFile.close()
    await ctx.send("Bio for " + author + " successfully submitted.")

@bot.command()
async def getBio(ctx, *, params: defineGroupParams = defineGroupParams.defaults()):
    fileName = params['name'] + ".bio"
    bioFile = open(fileName, "r")

    #bioLines = [line.rstrip('\n') for line in open(fileName)]
    #output = "```"
    #for eachLine in bioLines:
    #    output = output + eachLine + "\n"
    await ctx.send("Bio for " + params['name'] + ":\n" + bioFile.read())

botToken = [line.rstrip('\n') for line in open('bot.Token')]
bot.run(botToken[0])

