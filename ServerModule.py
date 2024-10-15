## Kevin Caplescu ##
# ~ Main Server Module ~ #

# ~ Enstablishes server and accepts connections. ~#
# ~ To be used ONLY on server-hosting machines. ~#

######## ~ Libraries ~ #########
import sys
import socket
import threading

######## ~ Main Values ~ #########
CLIENT_LIST = []
# format: [(socket,(address,port))]
MESSAGE_QUEUE = [] #Queue ADT
MAXIMUM_CHARACTERS = 1025
FORMAT = "utf-8"

######## ~ Functions ~ #########
def ClientHandler(c,a):
    isOnline = True
    while isOnline:
        try:
            Bytes = c.recv(MAXIMUM_CHARACTERS) #Blocking line
            if Bytes:
                Bytes.decode(FORMAT)
                Bytes = int(Bytes)
                Message = c.recv(Bytes).decode(FORMAT)

                MESSAGE_QUEUE.append([Message,a[0]])
                print(MESSAGE_QUEUE)
                #Queue system here
                for X in range(len(MESSAGE_QUEUE)):
                    #Sender_IP = ((MESSAGE_QUEUE[X])[1]) #Ip string
                    for INDEX in range(len(CLIENT_LIST)):
                        #current_IP = (CLIENT_LIST[INDEX])[1][0]
                        wantedConnection = (CLIENT_LIST[INDEX])[0]
                        wantedConnection.send((MESSAGE_QUEUE[X])[0].encode(FORMAT))
                
                    MESSAGE_QUEUE.remove(MESSAGE_QUEUE[X])
        except ConnectionResetError:
            isOnline = False
            c.close()
            print(f"{a} has disconnected.")
            foundUser = False
            for index in range(len(CLIENT_LIST)):
                if not(foundUser):
                    ip = CLIENT_LIST[index-1][1][0]
                    if ip == a[0]:
                        foundUser = True
                        CLIENT_LIST.pop(index-1)

            print(CLIENT_LIST)

        except OSError:
            isOnline = False
            c.close()
            print(f" there has been an error with {a}'s connection.")
            foundUser = False
            for index in range(len(CLIENT_LIST)):
                if not(foundUser):
                    ip = CLIENT_LIST[index-1][1][0]
                    if ip == a[0]:
                        foundUser = True
                        CLIENT_LIST.pop(index)

                        for msg_index in range(len(MESSAGE_QUEUE)-1):
                            message = MESSAGE_QUEUE[msg_index]
                            if message[1] == ip:
                                MESSAGE_QUEUE.pop(msg_index)

            print(CLIENT_LIST)
            ###################################################
        else:
            pass

def START(server):
    server.listen()
    while True:
        CONNECTION, ADDRESS = server.accept() #Blocking line (waits for connection)
        # we start a thread with ClientHandler
        thread = threading.Thread(target=ClientHandler,args=(CONNECTION,ADDRESS))
        thread.start()
        print(f"NEW CONNECTION: {ADDRESS}")
        CLIENT_LIST.append((CONNECTION,ADDRESS))
        print(CLIENT_LIST)
######## ~ classes ~ #########
class SERVER():
    def __init__(self):
        self.Port = int()
        self.Host = str()
        self.Status = False
        self.Server_Mode = 1 # Server Module set as 'Server-1' by default.

    def _SetNewMode(self,Mode):
        if Mode > 3 or Mode < 1:
            print("Invalid mode, abort.")
        else:
            self.Server_Mode = Mode

    def GetStuff(self):
        PORT=3389
        self.Port = PORT
        self.Host = socket.gethostbyname(socket.gethostname())

    def Run(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((self.Host,self.Port))
        print("SERVER RUNNING")
        self.Status = True
        print(f"======================\nINFORMATION:\nHOST:{sock.getsockname()[0]}\nPORT:{self.Port}\nSTATUS: {self.Status}")
        try:
            START(sock)
        except:
            print("Critical Error, Server Shutdown.")
            self.Status = False
######## ~ MAIN ~ #########
server = SERVER() # server class
while True:
    server.GetStuff()
    choice = input("Server set-up: Complete.\nType 'startup' to start.\nType 'exit' to close the server.\n")
    if str.lower(choice) == "startup":
        server.Run()
    elif str.lower(choice) == "exit":
        break
    else:
        print("Invalid.")

sys.exit()

