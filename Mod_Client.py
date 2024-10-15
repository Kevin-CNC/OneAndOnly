# ~ Kevin Caplescu ~ #
# ~ Client script for chat-room. ~ #
# ~ Must connect to a server ~ #

############################################################
# ~ Libraries ~ #

import socket
import threading
import MainApp

# ~ Main Values ~ #

MAXIMUM_CHARACTERS = 1025
FORMAT = "utf-8"
EXIT_COMMAND = "^DISCONNECT"
inServer = False

############################################################
# ~ Functions ~ #


def SEND_PACKET(CLIENT,msg):
    packet = msg.encode(FORMAT)
    packet_length = len(packet)
    s_Length = str(packet_length).encode(FORMAT)
    s_Length += b' '*(MAXIMUM_CHARACTERS-len(s_Length))

    CLIENT.send(s_Length)
    CLIENT.send(packet)

############################################################
# ~ Classes ~ # 
# Server Information #

class Server():
    def __init__(self):
        self.IP = str()
        self.PORT = 5050

    def ServerConnect(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            sock.connect((self.IP,self.PORT))
            print("You are now connected!")
            return([True,sock])
        except:
            print("An error has occurred!")
            sock.close()
            return([False,None])

    def ForceCloseConnection(self,Socket):
        print("forced closure")
        Socket.close() # Assume it's a socket Obj.

    def MESSAGE_FUNCTION(socket,msg,USER):
                if msg == "#":
                    socket.close()
                    inServer = False
                else:
                    new_pack = USER._GetUsername()+"->"+msg
                    SEND_PACKET(socket,new_pack)

    def Connect(self,USER,s):
        inServer = True
        
        try:
            def RECIEVE_PACKET():
                while inServer:
                    try:
                        RECIEVED_MESSAGE = (s.recv(2048)).decode(FORMAT)
                        if RECIEVED_MESSAGE:
                            # Invoke the message event on the main application.
                            MainApp.MessageEvent(RECIEVED_MESSAGE)
                        else:
                            pass
                    except:
                        inServer = False
                        s.close()
                        print("Host has shut down the server.")
                        break
                        

            sub_proc1 = threading.Thread(target=RECIEVE_PACKET,args=())
            sub_proc1.start() # Sub process which runs along with the main program
        
        except:
            inServer = False
            s.close()
            print("Oops! Unknown error with your connection!")
        
# Client Information #

class Client():
    def __init__(self):
        self._IP = socket.gethostbyname(socket.gethostname())
        self._Username = str()
        self._Membership = str()
        
    def _GetUsername(self):
        return(self._Username)

    def _SetUsername(self,new):
        self._Username = new

    def _GetUsername(self):
        return(self._Username)

    def _SetUsername(self,new):
        self._Username = new

    def _GetIP(self):
        return(self._IP)

    def _GetMS(self): #MS for membership
        return(self._Membership)

############################################################
# ~ Main Values ~ #
user = Client()
server = Server()


# ~ Gather Structure Function ~ #
def MenuFunction():
    return([user,server]) # returns tuple with class objects

# ~ Profile View Function ~ #
def ProfileView(C):
    print("Return profile Information")
    return([C._GetUsername(),C._GetIP(),C._GetMS()])

