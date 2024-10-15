# ~ By Kevin Caplescu ~ #
# ~ Main Application Module for CLIENT usage ~ #
# ~ Contains GUI, Connection Handling, SQL/Firebase ~ #
# Libraries #
import tkinter as TK
from tkinter import  * #Get everything from tkinter (wildcard)
import socket
import time
import threading

# Modules created for this application #
import FireBase_Manager
import SQL_Mod
import LAN_Mod

############################
##### Themes stuff  ########
############################

# 1-Default, 2-Dark, 3-Tundra, 4-Gaia, 5-Sunset, 6-Universe, 7-Light, 8-Sakura  #

class Theme():
    def __init__(self):
        self._Background = str() # Hex Values for colours
        self._Foreground = str()
        self._TextColour = str()

    def _GetAttribute(self,attribute):
        if attribute == "background":
            return(self._Background)
        elif attribute == "foreground":
            return(self._Foreground)
        elif attribute == "textcolour":
            return(self._TextColour) # Main Theme Class 

####################
# Theme Subclasses #
####################

class Default(Theme):
    def __init__(self):
        super().__init__()
        self._Background = '#040b40'
        self._Foreground = '#b4b1b5'
        self._TextColour = '#ffffff'# Default

class Dark(Theme):
    def __init__(self):
        super().__init__()
        self._Background = '#222626'
        self._Foreground = '#0a0a0a'
        self._TextColour = '#ffffff' # Dark

class Tundra(Theme):
    def __init__(self):
        super().__init__()
        self._Background = '#009edb'
        self._Foreground = '#9fbce3'
        self._TextColour = '#0e139e' # Tundra

class Gaia(Theme):
    def __init__(self):
        super().__init__()
        self._Background = '#59C93C'
        self._Foreground = '#00cc66'
        self._TextColour = '#003300' # Gaia

class Sunset(Theme):
    def __init__(self):
        super().__init__()
        self._Background = '#ed0552'
        self._Foreground = '#ff4e3b'
        self._TextColour = '#5c0546'# Sunset

class Universe(Theme):
    def __init__(self):
        super().__init__()
        self._Background = '#351345'
        self._Foreground = '#670296'
        self._TextColour = '#f0b6ee'# Universe

class Light(Theme):
    def __init__(self):
        super().__init__()
        self._Background = '#f7f5f7'
        self._Foreground = '#a5a4a6'
        self._TextColour = '#030303'# Light

class Sakura(Theme):
    def __init__(self):
        super().__init__()
        self._Background = '#f792cd'
        self._Foreground = '#f24edf'
        self._TextColour = '#ffffff'# Sakura
        
Themes_List = {"default":Default(),
               "dark":Dark(),
               "tundra":Tundra(),
               "gaia":Gaia(),
               "sunset":Sunset(),
               "universe":Universe(),
               "light":Light(),
               "sakura":Sakura()
               }
#############################
class settings():
    def __init__(self):
        self._BackgroundC = '#040b40'
        self._Size = '700x700'
        self._ForegroundC = '#b4b1b5'
        self._TextColor = 'white'

    def GetAttribute(self,attribute):
        if attribute == "backgroundc":
            return(self._BackgroundC)
        elif attribute == "windowsize":
            return(self._Size)
        elif attribute == "foregroundc":
            return(self._ForegroundC)
        elif attribute == "textcolor" or attribute == "textcolour":
            return(self._TextColor)

    def SetNewTheme(self,Values): # Assuming 'Values' parameter is a list
        # Structure of Value: [background,foreground,text]
        self._BackgroundC = Values[0]
        self._ForegroundC = Values[1]
        self._TextColor = Values[2] #Settings class

Settings = settings()
#############################
class globals():
    def __init__(self):
        self.RecievedMessage = None
        self.InModify = False
        self.InLogIn = False
        self.InMainMenu = False
        self.InChatroom = False
        self.Message_Index = 0
        self.Database = FireBase_Manager.InitializeUsersDatabase()

    def _MessageIndxReset(self):
        self.Message_Index = 0

    def _MessageIndexIncrease(self):
        self.Message_Index += 1#Global Values Class

Globals = globals()
#############################
class sql_Data():
    def __init__(self):
        self._database = SQL_Mod.Database() # Initialize Database class in the main sql_Data class.
        
    def _FireSaveProtocol(self):
        self._database._SaveProtocol()

    def _Get_Primary_Key(self):
        packet = (self._database._ExecuteCommand("""SELECT key FROM localdatabase"""))
        return(str(packet[0][0]))

    def _Set_Primary_Key(self,nkey):
        self._database._ExecuteCommand(f"""UPDATE localdatabase SET key = '{nkey}'""")

    def _Get_Theme(self):
        theme = self._database._ExecuteCommand("""SELECT theme FROM localdatabase""")
        return(theme)

    def _Set_New_Theme(self,newtheme):
        self._database._ExecuteCommand(f"""UPDATE localdatabase SET theme = '{newtheme}'""")

    def _RawExecute(self,cmd): # Needed for any sort of light SQL work
        self._database._ExecuteCommand(cmd) # Sql Data

local_database = sql_Data()
#############################
def MessageEvent(Message):
    valid_message = True

    if len(Message) > 555:
        valid_message = False

    if valid_message:
        print("message inbound")
        Globals.RecievedMessage = Message

    elif not(valid_message):
        Globals.RecievedMessage = None#Message Event

class Client():
    def __init__(self):
        self._IP = socket.gethostbyname(socket.gethostname())
        self._Username = str()
        self._Membership = str()
        
    def _GetUsername(self):
        return(self._Username)

    def _SetUsername(self,new):
        self._Username = new

    def _GetIP(self):
        return(self._IP)

    def _GetMS(self): #MS for membership
        return(self._Membership)#Client class

class ServerFunctionalities():
    def __init__(self):
        self.IP = str()
        self.PORT = int()
        self.__Format = "utf-8"
        self.__Max_Chars = 1025

    def _SetPort(self,newPort):
        self.PORT = newPort

    def SEND_PACKET(self,client_socket,msg):
        try:
            if len(msg)<=self.__Max_Chars:
                CLIENT = client_socket
                packet = msg.encode(self.__Format)
                packet_length = len(packet)
                s_Length = str(packet_length).encode(self.__Format)
                s_Length += b' '*(self.__Max_Chars-len(s_Length))

                CLIENT.send(s_Length)
                CLIENT.send(packet)
            else:
                pass
        except:
            print("Fatal error during package sending.")
            self.ForceCloseConnection(client_socket)

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

    def MESSAGE_FUNCTION(self,socket,msg,USER):
                new_pack = USER._GetUsername()+"->"+msg
                self.SEND_PACKET(socket,new_pack)

    def Connect(self,s):
        def RECIEVE_PACKET():
                while Globals.InChatroom:
                    try:
                        RECIEVED_MESSAGE = (s.recv(2048)).decode(self.__Format)
                        print("recieved")
                        if RECIEVED_MESSAGE:
                            MessageEvent(RECIEVED_MESSAGE) # Invoke the message event on the main application.
                        else:
                            pass
                    except:
                        s.close()
                        print("Host has shut down the server.")
                        break



        message_process = threading.Thread(target=RECIEVE_PACKET,args=())
        try:
            Globals.InChatroom = True
            message_process.start() # Sub process which runs along with the main program
        
        except:
            Globals.InChatroom = False
            s.close()
            print("Oops! Unknown error with your connection!")#Server Functionalities

class Functionality():
    def SpacesInRow(root,rownumber,n):
        for i in range(1,n):
            return(TK.Label(root,bg=Settings.GetAttribute("backgroundc"),fg='white',text="          ",font=('Arial',17,'normal'))).grid(row=rownumber,column=i)
    def SpacesInColumn(root,colnumber,n):
        for i in range(1,n):
            return(TK.Label(root,bg=Settings.GetAttribute("backgroundc"),fg='white',text="          ",font=('Arial',17,'normal'))).grid(row=i,column=colnumber)#GUI Functionalities

########################################
class Lan_Server(LAN_Mod.SERVER): # Lan_Server subclass of superclass SERVER
    def __init__(self):
        super().__init__()

lan_serv = Lan_Server()
########################################
class Connection():
    def __init__(self):
        self._GlobalServers = FireBase_Manager.GlobalServers(Globals.Database)

    def _GetInfoAndConnect(self,Mode,ServerFunctionality,Client,Extra):
        success = False
        Socket = None #Variable used for the storing of a socket.
        mode = str.lower(Mode)
        try:
            if mode == "lan":
                print("Lan mode...")
                ServerFunctionality._SetPort(3389)
                ServerFunctionality.IP = Client._GetIP() # User hosting manual server; We just need their IP.
                
                success,Socket = ServerFunctionality.ServerConnect()
             
            elif mode == "lan-guest":
                ServerFunctionality._SetPort(3389)
                ServerFunctionality.IP = Extra

                success,Socket = ServerFunctionality.ServerConnect()

            elif mode == "debug" and Client._GetMS() == "admin":
                manual_IP = str(input("IN DEBUG MODE, PLEASE ENTER IP MANUALLY -> "))
                ServerFunctionality.IP = socket.gethostbyname(manual_IP)
                ServerFunctionality._SetPort(3389)
                success,Socket = ServerFunctionality.ServerConnect()
            elif mode == "debug" and not(Client._GetMS() == "admin"):
                print("DEBUG MODE TRIED TO BE FIRED WHILE NOT BEING ADMIN! ABORT!")
            else:       
                statuses = self._GlobalServers._ServerStatuses()

                if statuses[0]:
                    ServerFunctionality.IP = self._GlobalServers._GetServerIP(1)
                    ServerFunctionality._SetPort(3389)
                elif statuses[1]:
                    ServerFunctionality.IP = self._GlobalServers._GetServerIP(2)
                    ServerFunctionality._SetPort(3389)
                elif statuses[3]:
                    ServerFunctionality.IP = self._GlobalServers._GetServerIP(3)
                    ServerFunctionality._SetPort(3389)
                else:
                    print("No world server currently available, aborting...")
                success,Socket = ServerFunctionality.ServerConnect()
        except:
            pass

        if success: #If the connection attemps are valid then connect.
            try:
                print("Connection established.")
                ServerFunctionality.Connect(Socket)
                return(Socket)
            except:
                print("Unknown connection error.")
                return(None)
        else:
            print("No connection, returning None value.")
            return(None)#Connection

#######################################
class Validation():
    def _Request_Deletion_Of_Account(C):
        p_key = FireBase_Manager.Hash_Function(C._GetIP())
        success = FireBase_Manager.UsersDatabase().RequestDeletion(Globals.Database,p_key)
        if success:
            local_database._Set_New_Theme("default") # Request account deletion

    def _Register(ROOT,C,S,Tag,values):
        p_key = FireBase_Manager.Hash_Function(C._GetIP()) # Gathers

        result = FireBase_Manager.UsersDatabase().FindUser(Globals.Database,p_key)
        if result == False:
            local_database._Set_Primary_Key(p_key) # Sets primary key in the database
            US = values[0].get()
            PW = values[1].get()
            # not found: New person!
            if not(PW == "") and not(US == "") and (len(US)>=3 and len(US)<=14):
                C._SetUsername(US)
                encryptedP = FireBase_Manager.EncryptPassword(p_key,PW)
                FireBase_Manager.UsersDatabase().AddUser(p_key,C._GetUsername(),encryptedP,"basic",Globals.Database)
                ROOT.destroy()
                menu._MenuPage()
                values[0].set("")
            else:
                if (len(US)<3 or len(US)>14):
                    Tag.config(text="Username must be between 3 and 14 characters.")
                else:
                    Tag.config(text="One of the fields is invalid.")
        elif result == True:
            Tag.config(text="You already have an account, please log in or request for a deletion.") #Register Verification

    def _UserCheck(guis,C,ROOT,warning_label,values):
        p_key = local_database._Get_Primary_Key()
        US = values[0].get()
        PW = FireBase_Manager.EncryptPassword(p_key,values[1].get())
        flag1 = False
        flag2 = False
        result = bool()
       
        if p_key == None:
            result = False
        else:
            result = FireBase_Manager.UsersDatabase().FindUser(Globals.Database,p_key)
        
        if result == True:
            records = FireBase_Manager.UsersDatabase().GetData(Globals.Database,p_key) # returns list
            recorded_username = records[0]
            recorded_password = records[1]

            if US == recorded_username:
                flag1 = True
            if PW == recorded_password:
                flag2 = True

            if not(US.find(" ") == -1):
                warning_label.config(text="No spaces allowed.")
            elif US == "": # code change
                warning_label.config(text="Field error - No username.") # code change
            elif PW == "": # code change
                warning_label.config(text="Field error - No password.") # code change
            else:
                if flag1:
                    if flag2:
                        global Themes_List

                        ROOT.destroy()
                        C._SetUsername(US)

                        themeOBJ = Themes_List[str.lower(local_database._Get_Theme()[0][0])]
                        theme_schemes = [themeOBJ._GetAttribute("background"),themeOBJ._GetAttribute("foreground"),themeOBJ._GetAttribute("textcolour")]
                        Settings.SetNewTheme(theme_schemes)

                        guis._MenuPage()

                        values[0].set("")
                        #FireBase_Manager.UsersDatabase().AddUser(p_key,C._GetUsername(),PW,"basic",Globals.Database)
                    else:
                        print("Incorrect password, retry.")
                        warning_label.config(text="Incorrect password, retry.")
                else:
                    warning_label.config(text="Wrong username, retry")
        elif result == False:
            warning_label.config(text="It seems that you don't have an account. Please register.")
        elif result == None:
            print("Something went wrong...") #Validation




class GUIs():
    def __init__(self,C_OBJ,ServerFun):
        self._ClientObj = C_OBJ
        self._ServerFunctionalities = ServerFun# Initializer
        
    def __ExitChatProtocol(self,sock,kinterRoot):
         # This is done in order to perform a proper closure of the socket.
        Globals.InChatroom = False # Bool set to false; Breaks the thread
        self._ServerFunctionalities.ForceCloseConnection(sock) #Forces connection closure, through socket retrieved.
        kinterRoot.destroy()
        self._MenuPage() # Exit-Chat Protocol

    def _OpenLanServer(self,WindowToDestroy):
        try:
            if not(Globals.InChatroom):
                Globals.InChatroom = True
                self._ServerFunctionalities.IP = self._ClientObj._GetIP()
                lan_serv.SetPort(3389)
                lan_thread = threading.Thread(target=lan_serv.Run,args=())
                lan_thread.start()
                WindowToDestroy.after(1)
                self._ChattingConnectWindow(WindowToDestroy,"LAN",None) # Open-Lan Server Method
        except:
            print("Fatal Hosting Error")
            self._MenuPage() # Open-Lan Method

    def _ChattingConnectWindow(self,Window_To_Destroy,mode,extra):
        sock = Connection()._GetInfoAndConnect(mode,self._ServerFunctionalities,self._ClientObj,extra) #Connects and returns the socket
        if not(Globals.InModify):
            Globals._MessageIndxReset() # Connected to a new chatroom; Index must be reset
            if not(sock==None):
                Window_To_Destroy.destroy()
                Globals.InChatroom = True
                Globals.InMainMenu = False

                chatROOT = TK.Tk()
                chatROOT.geometry('700x700')
                chatROOT.config(background=Settings.GetAttribute('backgroundc'))
                chatROOT.resizable(False,False)
                #WrittenMsg = TK.StringVar(chatROOT)

                canvasWidget = TK.Canvas(chatROOT,background=Settings.GetAttribute('backgroundc'),bd=0)
                frameWidget = TK.Frame(canvasWidget,bg=Settings.GetAttribute("backgroundc"),bd=0)

                def UpdateSR():
                    print("updated canvas")
                    canvasWidget.update_idletasks()
                    canvasWidget.config(scrollregion=frameWidget.bbox())

                scrolling_bar = TK.Scrollbar(chatROOT)
                scrolling_bar.pack(fill=TK.Y, side=TK.RIGHT,expand=TK.FALSE)
                scrolling_bar.config(orient=TK.VERTICAL,command=canvasWidget.yview)

                canvasWidget.config(yscrollcommand=scrolling_bar.set)
                canvasWidget.pack(fill=BOTH,expand=TRUE)
                canvasWidget.create_window(0,0,window=frameWidget,anchor=TK.NW)

                Chat_Box = TK.Canvas(chatROOT,background='white')
                Chat_Box.pack(side=TK.LEFT,fill=TK.BOTH)
                Chat_Box.config(height=100,width=700)

                MessageWriter =TK.Entry(Chat_Box,bg='white',justify=TK.LEFT)
                MessageWriter.config(width=550)
                MessageWriter.grid(column=1)

                def SendMessage(event):
                    message = self._ClientObj._GetUsername()+"-> "+(MessageWriter.get())
                    self._ServerFunctionalities.SEND_PACKET(sock,message)
                    MessageWriter.delete(0,len(MessageWriter.get()))

                chatROOT.title(f"CHATROOM: {str(self._ServerFunctionalities.IP)}")
                chatROOT.bind('<Return>', SendMessage)
                def message_displayer_function():
                    print("Thread started")
                    while Globals.InChatroom:
                        time.sleep(.0025)
                        if Globals.RecievedMessage is None:
                            pass # No message recieved, no need to add anything.
                        elif Globals.RecievedMessage and len(Globals.RecievedMessage) >= 1 and len(Globals.RecievedMessage) < 551:
                            print("msg recieved")
                            font_size = int()
                        
                            Globals._MessageIndexIncrease()

                            if len(Globals.RecievedMessage) <= 551:
                                if len(Globals.RecievedMessage) <= 200:
                                    if len(Globals.RecievedMessage) <= 100:
                                        if len(Globals.RecievedMessage) <= 45:
                                            font_size = 17
                                    else:
                                        font_size = 16
                                else:
                                    font_size = 14
                            else:
                                font_size = 13
                            textLabel = TK.Label(frameWidget,bg=Settings.GetAttribute("backgroundc"),fg='white',text=Globals.RecievedMessage,anchor=TK.W,font=('Calibri',font_size,'bold'),justify=TK.LEFT,width=50)
                            textLabel.grid(row=Globals.Message_Index)
                            textLabel.config(wraplength=620)
                    
                            print("Label inserted into the holder and text set as the message.")
                            UpdateSR()
                        

                        Globals.RecievedMessage = None # Sets the variable to nil as soon as it's done.
                        chatROOT.after(1,None)
                    else:
                        Globals.InChatroom = False
                        Globals.InMainMenu = True
                        print("Didn't connect.")

                Message_Process = threading.Thread(target=message_displayer_function,args=())#if 'sock' variable stores a socket
                try:
                    Message_Process.start() # Sub process which runs along with the main program
                except:
                    print("Exiting thread")
                    Globals.InChatroom = False
                    self.__ExitChatProtocol(sock,chatROOT)

                def ExitProtocol():
                    self.__ExitChatProtocol(sock,chatROOT)

                chatROOT.protocol("WM_DELETE_WINDOW",ExitProtocol)
                chatROOT.mainloop() # Chat-Window Method
            
    def _MenuPage(self):
        Globals.InLogIn = False
        Globals.InMainMenu = True

        def ExitProtocol():
            ROOT.destroy()
            local_database._FireSaveProtocol()
            


        ROOT = TK.Tk()
        ROOT.title('Chat system v.0.4(alpha)')
        ROOT.config(background=Settings.GetAttribute("backgroundc"))
        ROOT.geometry(Settings.GetAttribute("windowsize"))
        ROOT.maxsize(700,700)
        ROOT.minsize(700,700)
        
        ip_lan = TK.StringVar()
        ###### MAIN MENU ######
        Functionality.SpacesInRow(ROOT,1,4)
        Functionality.SpacesInRow(ROOT,2,4)
        Greet = TK.Label(ROOT,bg=Settings.GetAttribute("backgroundc"),fg=Settings.GetAttribute("textcolor"),text=f"Welcome to CSM, {self._ClientObj._GetUsername()} !",font=('fixed',20,'bold'))
        Greet.grid(row=1,column=5)
        LABEL1 = TK.Label(ROOT,bg=Settings.GetAttribute("backgroundc"),fg=Settings.GetAttribute("textcolor"),text=f"Choose your option.",font=('fixed',20,'bold'))
        LABEL1.grid(row=2,column=5)
        Functionality.SpacesInRow(ROOT,3,5)
        Functionality.SpacesInRow(ROOT,4,5)
        Functionality.SpacesInRow(ROOT,5,4)
        BUTTON = TK.Button(ROOT,text="Modify Your Profile",bg=Settings.GetAttribute("foregroundc"),fg=Settings.GetAttribute("textcolor"),font=('Arial',15,'bold'),command=lambda:self._EditingPage(ROOT,Greet))
        BUTTON.grid(row=5,column=5)
        ConnectB = TK.Button(ROOT,text="C o n n e c t",bg=Settings.GetAttribute("foregroundc"),fg=Settings.GetAttribute("textcolor"),font=('Arial',15,'bold'),command=lambda:self._ChattingConnectWindow(ROOT,"DEBUG",None)) # Change to'global'
        ConnectB.grid(row=6,column=5) # Main-Page
        LAN_B = TK.Button(ROOT,text="Host LAN",bg=Settings.GetAttribute("foregroundc"),fg=Settings.GetAttribute("textcolor"),font=('Arial',15,'bold'),command=lambda:self._OpenLanServer(ROOT))    
        LAN_B.grid(row=7,column=5) # Hosts Lan Server
        Connect_LAN = TK.Button(ROOT,text="Connect LAN",bg=Settings.GetAttribute("foregroundc"),fg=Settings.GetAttribute("textcolor"),font=('Arial',15,'bold'),command=lambda:self._ChattingConnectWindow(ROOT,"LAN-GUEST",ip_lan.get()))
        Connect_LAN.grid(row=8,column=5)
        Lan_IP = TK.Entry(ROOT,fg=Settings.GetAttribute("textcolor"),textvariable=ip_lan,bg=Settings.GetAttribute("foregroundc"))
        Lan_IP.grid(row=9,column=5)

        ROOT.protocol("WM_DELETE_WINDOW",ExitProtocol) # Menu Page Method

    def _EditingPage(self,OldMainR,Greet):
        if not(Globals.InChatroom):
            OldMainR.destroy()
            Globals.InModify = True
            Globals.InMainMenu = False
            def assign(value,Label1,Label2):
                new = value.get()
                illegal_flag = False
            #Check for illegal characters and switch flag if found

                for index in range(len(new)):
                    character = new[index-1]
                    illegal_character_list = [' ','-','{','}','?','"','%','/']
                    for I in range(len(illegal_character_list)):
                        if character == illegal_character_list[I]:
                            print("")
                            illegal_flag = True


                if len(new) == 0 or illegal_flag:
                    Label1.config(text="Illegal username. Change NOT saved.")
                    Label1.config(text=f"USER:{self._ClientObj._GetUsername()}")
                elif len(new) > 14: # username too big
                    Label1.config(text="Too big of a username!")
                    Label1.config(text=f"USER:{self._ClientObj._GetUsername()}")
                else:
                    self._ClientObj._SetUsername(new)
                    if len(new) > 12:
                        Label1.config(text=f"USER:{self._ClientObj._GetUsername()}",font=('fixed',12,'normal'))
                    elif len(new) > 10:
                        Label1.config(text=f"USER:{self._ClientObj._GetUsername()}",font=('fixed',13,'normal'))
                    elif len(new) <= 10:
                        Label1.config(text=f"USER:{self._ClientObj._GetUsername()}",font=('fixed',15,'normal'))

                    FireBase_Manager.UsersDatabase.Change_Field(Globals.Database,1,local_database._Get_Primary_Key(),new)
            
            wind = TK.Tk()
            wind.title('Profile Editing Window')
            wind.config(background=Settings.GetAttribute("backgroundc"))
            wind.geometry('650x350')
            wind.maxsize(650,350)
            wind.minsize(650,350) 

            def CloseWindow():
                wind.destroy()
                Globals.InModify = False
                Globals.InMainMenu = True
                self._MenuPage()

            NewUser_Val = TK.StringVar(wind)

            ########################################################
            LABEL1 = TK.Label(wind,bg=Settings.GetAttribute("backgroundc"),fg=Settings.GetAttribute("foreground"),text=f"-PROFILE EDITOR-",font=('fixed',20,'bold'))
            LABEL1.grid(row=1,column=2)


            exitButton = TK.Button(wind,text="Exit",bg=Settings.GetAttribute("foreground"),fg=Settings.GetAttribute("textcolor"),font=('fixed',12,'normal'),command=CloseWindow)
            exitButton.grid(row=1,column=3)

            usernamelabel = TK.Label(wind,bg=Settings.GetAttribute("backgroundc"),fg=Settings.GetAttribute("foreground"),text=f"USER:{self._ClientObj._GetUsername()}",font=('fixed',20,'normal'))
            usernamelabel.grid(row=2,column=2)

            changeLabel = TK.Label(wind,bg=Settings.GetAttribute("backgroundc"),fg=Settings.GetAttribute("foreground"),text=f"You can change your username here:",font=('fixed',13,'normal'))
            changeLabel.grid(row=3,column=2)

            changeEntry = TK.Entry(wind,fg='white',textvariable=NewUser_Val,bg='#433a5e')
            changeEntry.grid(row=3,column=3)

            confirmButton = TK.Button(wind,text="confirm change",fg='red',font=('fixed',12,'normal'),command=lambda:assign(NewUser_Val,usernamelabel,Greet))
            confirmButton.grid(row=3,column=4)
            
            themeLabel = TK.Label(wind,bg=Settings.GetAttribute("backgroundc"),fg=Settings.GetAttribute("foreground"),text=f"T H E M E S :",font=('fixed',13,'normal'))
            themeLabel.grid(row=5,column=1)

            def Update_Theme(THEME):
                #Creates a list with the new colours for the background
                selected_theme = Themes_List[str.lower(THEME)]
                new_colors = [selected_theme._GetAttribute("background"),selected_theme._GetAttribute("foreground"),selected_theme._GetAttribute("textcolour")]
                Settings.SetNewTheme(new_colors)
                wind.config(background=Settings.GetAttribute("backgroundc"))
                LABEL1.config(bg=Settings.GetAttribute("backgroundc"),fg=Settings.GetAttribute("textcolour"))
                exitButton.config(bg=Settings.GetAttribute("foregroundc"),fg=Settings.GetAttribute("textcolour"))
                usernamelabel.config(bg=Settings.GetAttribute("backgroundc"),fg=Settings.GetAttribute("textcolour"))
                changeLabel.config(bg=Settings.GetAttribute("backgroundc"),fg=Settings.GetAttribute("textcolour"))
                themeLabel.config(bg=Settings.GetAttribute("backgroundc"),fg=Settings.GetAttribute("textcolour"))

                try:
                    local_database._Set_New_Theme(THEME)
                except:
                    print("Couldn't update local database.")

            ThemeButton1 = TK.Button(wind,text="Default ",bg=Themes_List["default"]._GetAttribute("foreground"),fg=Themes_List["default"]._GetAttribute("textcolour"),command=lambda:Update_Theme("DEFAULT"))
            ThemeButton1.grid(row=6,column=1)

            ThemeButton2 = TK.Button(wind,text="  Dark  ",bg=Themes_List["dark"]._GetAttribute("foreground"),fg=Themes_List["dark"]._GetAttribute("textcolour"),command=lambda:Update_Theme("DARK"))
            ThemeButton2.grid(row=7,column=1)

            ThemeButton3 = TK.Button(wind,text=" Tundra ",bg=Themes_List["tundra"]._GetAttribute("foreground"),fg=Themes_List["tundra"]._GetAttribute("textcolour"),command=lambda:Update_Theme("TUNDRA"))
            ThemeButton3.grid(row=8,column=1)

            ThemeButton4 = TK.Button(wind,text="  Gaia  ",bg=Themes_List["gaia"]._GetAttribute("foreground"),fg=Themes_List["gaia"]._GetAttribute("textcolour"),command=lambda:Update_Theme("GAIA"))
            ThemeButton4.grid(row=9,column=1)

            ThemeButton5 = TK.Button(wind,text=" Sunset ",bg=Themes_List["sunset"]._GetAttribute("foreground"),fg=Themes_List["sunset"]._GetAttribute("textcolour"),command=lambda:Update_Theme("SUNSET"))
            ThemeButton5.grid(row=10,column=1)

            ThemeButton6 = TK.Button(wind,text="Universe",bg=Themes_List["universe"]._GetAttribute("foreground"),fg=Themes_List["universe"]._GetAttribute("textcolour"),command=lambda:Update_Theme("UNIVERSE"))
            ThemeButton6.grid(row=11,column=1)

            ThemeButton7 = TK.Button(wind,text=" Light  ",bg=Themes_List["light"]._GetAttribute("foreground"),fg=Themes_List["light"]._GetAttribute("textcolour"),command=lambda:Update_Theme("LIGHT"))
            ThemeButton7.grid(row=12,column=1)

            ThemeButton8 = TK.Button(wind,text=" Sakura ",bg=Themes_List["sakura"]._GetAttribute("foreground"),fg=Themes_List["sakura"]._GetAttribute("textcolour"),command=lambda:Update_Theme("SAKURA"))
            ThemeButton8.grid(row=13,column=1)



            def PROTOCOL():# Protocol for when forced closing; This protocol stops the window from closing
                pass
            wind.protocol("WM_DELETE_WINDOW",PROTOCOL) # Editing-Page Method
             
    def _LogInPage(self):
        Globals.InLogIn = True

        ROOT = TK.Tk() # Login Page
        ROOT.title('Chat system v.0.4')
        ROOT.config(background=Settings.GetAttribute("backgroundc"))
        ROOT.geometry(Settings.GetAttribute("windowsize"))
        ROOT.maxsize(700,700)
        ROOT.minsize(700,700)

        username_Value = TK.StringVar(ROOT)
        password_value = TK.StringVar(ROOT)
        label_value = TK.StringVar(ROOT)

        client_values = [username_Value,password_value]
        # Top Bar Menu #
    
        space1 = Functionality.SpacesInRow(ROOT,1,5)
        Deco1 = (Label(ROOT,bg='#040b40',fg='white',text="-",font=('Arial',20,'bold')))
        Deco1.grid(row=1,column=1)

        Deco2 = (Label(ROOT,bg='#040b40',fg='white',text="-",font=('Arial',20,'bold')))
        Deco2.grid(row=1,column=7)

        GreetL = (Label(ROOT,bg='#040b40',fg='white',text="Welcome to CSM!",font=('Arial',20,'bold')))
        GreetL.grid(row=1,column=6)

        space1_1 = Functionality.SpacesInRow(ROOT,2,5)
        InfoL = (Label(ROOT,bg='#040b40',fg='white',text="Enter login information.",font=('Arial',20,'bold')))
        InfoL.grid(row=2,column=6)

        InfoTag = TK.Label(ROOT,bg='#040b40',fg='red',text=" ",font=('Arial',13,'bold'))
        InfoTag.grid(row=3,column=6)

    # Entries Menu
        space2 = Functionality.SpacesInColumn(ROOT,3,5)
        InfoL = (Label(ROOT,bg='#040b40',fg='white',text="Username",font=('Arial',16,'normal')))
        InfoL.grid(row=4,column=6)

        Username = TK.Entry(ROOT,fg='white',textvariable=username_Value,bg='#433a5e')
        Username.grid(row=5,column=6)

        PInfoL = (Label(ROOT,bg='#040b40',fg='white',text="Password",font=('Arial',16,'normal')))
        PInfoL.grid(row=6,column=6)

        Password = TK.Entry(ROOT,fg='white',textvariable=password_value,bg='#433a5e',show='*')
        Password.grid(row=7,column=6)

    ## Login
        space3_1 = Functionality.SpacesInRow(ROOT,8,6)
        space3_2 = Functionality.SpacesInRow(ROOT,9,6)

        LogInButton = TK.Button(ROOT,text="Log In.",font=('Arial',12,'bold'),command=lambda:Validation._UserCheck(self,self._ClientObj,ROOT,InfoTag,client_values))
        LogInButton.grid(row=11,column=6)
    
    
        InfoL = (Label(ROOT,bg='#040b40',fg='white',text="Not registered? Come in!",font=('Boldoni',16,'bold')))
        InfoL.grid(row=14,column=6)

        SignInButton = TK.Button(ROOT,text="Register",font=('Arial',12,'bold'),command=lambda:Validation._Register(ROOT,self._ClientObj,self._ServerFunctionalities,InfoTag,client_values))
        SignInButton.grid(row=15,column=6)

        Del_Acc_Button = TK.Button(ROOT,text="Delete Account",font=('Arial',12,'bold'),command=lambda:Validation._Request_Deletion_Of_Account(self._ClientObj))
        Del_Acc_Button.grid(row=16,column=6)

        ROOT.mainloop()# Log-In Method


########################
###   Main Program   ###
########################

c = Client()
s = ServerFunctionalities()
menu = GUIs(c,s)
menu._LogInPage()




