## By Kevin Caplescu ##
## LAN Server Module ##
#######################

# Libraries #
import socket
import time
import threading
################


######## ~ Main Values ~ #########
CLIENT_LIST = []
MESSAGE_QUEUE = []
MAXIMUM_CHARACTERS = 1025
FORMAT = "utf-8"
Hosting = True # Code Change
##################################

def ClientHandler(c,a):
    global Hosting
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
                        if ip == socket.gethostbyname(socket.gethostname()):
                            Hosting = False

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
        if Hosting == False:
            break


    server.close()
    server.shutdown(socket.SHUT_RDWR)

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

    def SetPort(self,newPort):
        self.Port = newPort

    def Run(self):
        time.sleep(1)
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host = socket.gethostbyname(socket.gethostname())
        print("LAN SERVER RUNNING")
        self.Status = True
        self.SetPort(3389)
        #host = sock.getsockname()[0]
        print(f"======================\nINFORMATION:\nHOST:{host}\nPORT:{self.Port}\nSTATUS: {self.Status}")
        try:
            sock.bind((host,self.Port))
            START(sock)
            self.Status = False
        except:
            print("Critical Error, Server Shutdown.")
            self.Status = False
            sock.close()

        sock.close()