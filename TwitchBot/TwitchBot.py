import json
import random
import socket
import threading
from tkinter import *
from tkinter.ttk import *

THREAD_LOCK = threading.Lock()

class BColors:
    HEADER = '\033[95m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    RED = '\u001b[31m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    BLUE = '\u001b[34m'
    WHITE = '\u001b[37m'

    ENDC = '\033[0m'


class BotFunctions:
    connected = False
    reconAttempt = False
    runThread = False
    currThread = None

    connection_data = ('irc.chat.twitch.tv', 6667)
    connected = False
    token = 'oauth:'
    user = 'foo'
    channel = '#'

    def connect(self):
        try:
            print(f"{BColors.YELLOW}CONSOLE:{BColors.WHITE} >>CONNECTING...{BColors.ENDC}")
            guiHandler.updateLog("Connecting...")
            server = socket.socket()
            server.connect(self.connection_data)

            server.send(bytes('PASS ' + self.token + '\r\n', 'utf-8'))
            server.send(bytes('NICK ' + "foo" + '\r\n', 'utf-8'))
            server.send(bytes('JOIN ' + self.channel + '\r\n', 'utf-8'))
            return server
        except:
            print(
                f"{BColors.YELLOW}CONSOLE:{BColors.RED} >> Couldn't connect to Twitch. Authentication failed{BColors.ENDC}")
            guiHandler.updateLog("Unable to connect to Twitch. Authentification Failed")

    def formatchatmessage(self, message):
        try:
            decodedMessage = message.decode()
            formattedmessage = decodedMessage.split("#")
            chatUsername = decodedMessage[decodedMessage.index(':') + 1:decodedMessage.index('!')]
            message = formattedmessage[len(formattedmessage) - 1].replace("\r\n", '')
            message.replace(' ', '')
            data = message.split(":")
            return chatUsername, data[1]
        except:
            print(f"{BColors.YELLOW}CONSOLE:{BColors.RED} >> UNABLE TO FORMAT RECIEVED MESSAGE{BColors.ENDC}")
            guiHandler.updateLog("Unable to format recieved message")
            return None, None

    def command(self, message, fromUser, command):
        if command:
            try:
                if isinstance(data['commands'][message], list):
                    returnMessage = str(data['commands'][message][random.randrange(0, len(data['commands'][message]))])
                else:
                    returnMessage = str(data['commands'][message])
            except:
                returnMessage = str(data['commands'][message])
        else:
            try:
                if isinstance(data['chats'][message], list):
                    returnMessage = str(data['chats'][message][random.randrange(0, len(data['chats'][message]))])
                else:
                    returnMessage = str(data['chats'][message])
            except:
                returnMessage = str(data['chats'][message])

        returnMessage = returnMessage.replace('{fromuser}', "@" + fromUser)
        return returnMessage

    def startBot(self):
        if self.runThread is True:
            self.runThread = False
        else:
            self.runThread = True
        self.connection = bot.connect()
        self.UpdateChat()

    def UpdateChat(self):
        while True:
            if bot is not None:
                messageReceived = self.connection.recv(2048)

                username, chat = bot.formatchatmessage(messageReceived)

                if chat is not None:
                    print(f'{BColors.BLUE}' + username + f'{BColors.WHITE}:' + chat)
                    guiHandler.updateLog(username + ": " + chat)

                    for p in data['banned-words']:
                        if chat.__contains__(p):
                            print(f"{BColors.YELLOW}CONSOLE: {BColors.WHITE}NO-NO WORD WAS SAID{BColors.ENDC}")
                            self.connection.send(
                                bytes('PRIVMSG ' + self.channel + " :" + "/timeout " + username + " 1 No-no words \r\n",
                                      'utf-8'))

                    if chat.find(commandPrefix, 0, len(commandPrefix)) > -1:
                        command = chat.replace(commandPrefix, '')
                        for p in data['commands']:
                            if p == command:
                                response = bot.command(p, username, True)
                                print(response)
                                self.connection.send(bytes('PRIVMSG ' + self.channel + " :" + response + '\r\n', 'utf-8'))
                    else:
                        for p in data['chats']:
                            if chat == p:
                                response = bot.command(p, username, False)
                                print(response)
                                self.connection.send(bytes('PRIVMSG ' + self.channel + " :" + response + '\r\n', 'utf-8'))
                else:
                    if not BotFunctions.reconAttempt:
                        BotFunctions.reconAttempt = True
                        print(
                            f'{BColors.YELLOW}CONSOLE:{BColors.RED} >> Bot disconnected. Attempting reconnection{BColors.ENDC}')
                        self.connection = bot.connect()
                    else:
                        break
        print(f'{BColors.YELLOW}CONSOLE:{BColors.RED} >> Bot disconnected{BColors.ENDC}')
        guiHandler.updateLog("Bot has disconnected")

    def UpdateInfo(self, UToken, UChannel):
        self.token = UToken

        if len(UChannel) > 0:
            if UChannel[0] != "#":
                UChannel = "#" + UChannel[0:]

        self.channel = UChannel.lower()
        guiHandler.updateLog("Stream info has been updated")


class GUIHandler:
    def __init__(self):
        window.title("ZEP BOT")
        window.geometry('640x480')
        window.wm_minsize(480, 180)
        leftFrame = Frame(master=window, relief=SUNKEN, borderwidth=5)
        leftFrame.pack(fill=BOTH, expand=TRUE, side=LEFT, padx=5, pady=5)

        rightFrame = Frame(master=window, relief=SUNKEN, borderwidth=5)
        rightFrame.pack(fill=BOTH, expand=TRUE, side=LEFT, padx=5, pady=5)

        titleFrame = Frame(master=leftFrame, relief=FLAT)
        titleFrame.pack(fill=X, side=TOP, padx=1, pady=1)

        holderFrame = Frame(master=leftFrame, relief=SUNKEN, borderwidth=5)
        holderFrame.pack(fill=BOTH, expand=TRUE, padx=1, pady=1)

        infoFrame = Frame(master=holderFrame, relief=FLAT, borderwidth=5)
        infoFrame.pack(fill=X, side=TOP, padx=1, pady=1)

        buttonsFrame = Frame(master=holderFrame, relief=FLAT, borderwidth=5)
        buttonsFrame.pack(fill=X, side=TOP, padx=1, pady=1)

        tokenFrame = Frame(master=infoFrame, relief=FLAT)
        tokenFrame.pack(fill=X, padx=1, pady=1)

        tokendescFrame = Frame(master=tokenFrame, relief=FLAT)
        tokendescFrame.pack(fill=X, side=LEFT, padx=1, pady=1)

        tokeninputsFrame = Frame(master=tokenFrame, relief=FLAT)
        tokeninputsFrame.pack(fill=X, expand=TRUE, side=LEFT, padx=1, pady=1)

        # CHANNEL FRAME
        channelFrame = Frame(master=infoFrame, relief=FLAT)
        channelFrame.pack(fill=X, padx=1, pady=1)

        channeldescFrame = Frame(master=channelFrame, relief=FLAT)
        channeldescFrame.pack(fill=X, side=LEFT, padx=1, pady=1)

        channelinputsFrame = Frame(master=channelFrame, relief=FLAT)
        channelinputsFrame.pack(fill=X, expand=TRUE, side=LEFT, padx=1, pady=1)

        logTitleFrame = Frame(master=rightFrame, relief=FLAT)
        logTitleFrame.pack(fill=BOTH, padx=1, pady=1)

        logFrame = Frame(master=rightFrame, relief=SUNKEN, borderwidth=5)
        logFrame.pack(fill=BOTH, expand=TRUE, padx=1, pady=1)

        logBoxFrame = Frame(master=logFrame, relief=FLAT, borderwidth=5)
        logBoxFrame.pack(fill=BOTH, expand=TRUE, side=LEFT, padx=1, pady=1)

        scrollBarFrame = Frame(master=logFrame, relief=FLAT, borderwidth=5)
        scrollBarFrame.pack(fill=BOTH, side=RIGHT, padx=1, pady=1)

        titleSetup = Label(master=titleFrame, text="SETUP").pack(fill=X)

        channelLabel = Label(master=channeldescFrame, text="CHANNEL:").pack()
        tokenLabel = Label(master=tokendescFrame, text="AUTH TOKEN:").pack()

        self.channelInput = Entry(master=channelinputsFrame)
        self.channelInput.pack(fill=X)
        self.tokenInput = Entry(master=tokeninputsFrame)
        self.tokenInput.pack(fill=X)

        updateBTN = Button(master=buttonsFrame, text="UPDATE INFO", command=self.press)
        updateBTN.pack(side=LEFT)
        connectBTN = Button(master=buttonsFrame, text="CONNECT", command=self.startBot)
        connectBTN.pack(side=LEFT)

        chatTitle = Label(master=logTitleFrame, text="CHAT LOG")
        chatTitle.pack(side=TOP)
        #self.logLabel = Label(master=logFrame, text="")
        #self.logLabel.pack(fill=BOTH)

        self.scrollLog = Scrollbar(scrollBarFrame)
        self.scrollLog.pack(fill=Y, side=RIGHT)

        self.logLabel = Listbox(logBoxFrame, yscrollcommand=self.scrollLog.set)
        self.logLabel.pack(fill=BOTH, expand=TRUE, side=LEFT)

        self.botF = BotFunctions()

        self.botThread = threading.Thread(target=self.botF.startBot)
        self.botThread.daemon = True

        self.botRunning = False

    def press(self):
        newChannel = self.channelInput.get()
        newToken = self.tokenInput.get()
        bot.UpdateInfo(newToken, newChannel)

    def updateLog(self, logMessage):
        self.logLabel.insert(END, logMessage + "\n")
        self.logLabel.yview(END)

    def startBot(self):
        print("STARTING BOT")
        self.updateLog("Starting bot")
        if self.botThread.is_alive() is False:
            self.botThread.start()
            self.botRunning = True
        else:
            print("BOT ALREADY RUNNING")
            self.updateLog("Bot is already running")

# Load database
with open('botData.json') as json_file:
    data = json.load(json_file)
commandPrefix = data['command-prefix']

bot = BotFunctions()

window = Tk()
guiHandler = GUIHandler()
window.mainloop()
