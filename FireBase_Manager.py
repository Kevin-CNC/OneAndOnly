# Script by Kevin Caplescu
# this script directly communicates with the firebase database where usernames will eventually be stored.
# Allows for .write and .read.
# IMPORTANT: Using current free plan, data sync + sending cannot surpass 10 GB Monthly.

# Libraries

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time

def Hash_Function(unhashed_key):
    lower = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    upper = []
    for letter in lower:
        upper.append(str.upper(letter)) # Fill 'upper' list


    def AssignCharacter(current_value,position):
        if current_value%2 >= 1: # lower nextcase
            X = (((current_value+1/(position+1)))/((current_value+1/10)))+(position*(position-1))
            X = (int(X))-position # Code change
            if X < 0:
                return(lower[(26+X)])
            elif X > 26:
                return(upper[(X-26)])
            else:
                return(lower[X])
        elif current_value%2 < 1 or position == 5:#higher nextcase
             X = (((current_value/(position+1)))/((current_value/10)))+(position+1)
             X = (int(X))-1
             if X < 0:
                 return(lower[26+X])
             elif X > 26:
                 return(upper[X-26])
             else:
                 return(upper[X])


    constructed_key = str()
    position = 0
    Values = str.split(unhashed_key,".") # Code change
    print(Values)
    for Val in Values:
        stringed = bytes(Val,'utf-8')
        for byte in stringed:
            if position == 0:
                constructed_key = str(byte)+AssignCharacter(byte,position)
            else:
                constructed_key += str(byte)+AssignCharacter(byte,position)
        position += 1

    return(constructed_key)


def EncryptPassword(p_key,actual_password):
    numbers = ["1","2","3","4","5","6","7","8","9","0"]
    lower = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    
    upper = []
    for letter in lower:
        upper.append(str.upper(letter)) # Fill 'upper' list

    try:
        byte_values = []
        raw_values = []


        encoded = bytes(p_key,'utf-8')
        for byte in encoded:
            byte_values.append(int(byte))

        encoded_password = bytes(actual_password,'utf-8')
        for pass_byte in encoded_password:
            raw_values.append(int(pass_byte))
       
        cntr = 1 # Code change
        max_index = (len(lower))+(len(upper))+len(numbers)
        encrypted_password = str()

        for value in raw_values:
            if cntr == len(byte_values):
                cntr = 1 # Code change

            character_index = value+byte_values[cntr-1]
            flag = True
            
            while flag:
                if character_index > max_index:
                    character_index -= max_index
                elif character_index <= 0 :
                    character_index =+ 1
                elif character_index <= max_index and character_index >= 0:
                    flag = False

                    if character_index > (len(lower)-1)+(len(upper)-1): # assign number
                        encrypted_password += numbers[(character_index-(len(lower)*2))-1]
                    elif character_index > len(lower)-1: # assign Uppercase
                        encrypted_password += upper[(character_index-len(lower))-1]
                    else: # assign Lowercase
                        encrypted_password += lower[character_index-1]
            cntr += 1

        return(encrypted_password)


    except ValueError:
        print("EncryptPassword - Error during encryption.")
        pass


# gets the 'users' JSON tree which is: 'users'
def InitializeUsersDatabase():
    try:
        CREDENTIALS = credentials.Certificate('json-certificate-here')
    
        firebase_admin.initialize_app(CREDENTIALS, {
        'databaseURL': 'your url to firebase database'})

        Reference = db.reference("")
        print("Database success!")
        return(Reference)
    #School Network locked this function.
    except:
        print("FireBase_Manager InitializeUserDatabase Critical Error - Couldn't Connect to firebase database.\nShutting down..")
        time.sleep(2)
        exit()
    


# tries to find the credentials in the JSON tree: 'users'
class UsersDatabase():
    def Get_Key(self,IP):
        key = str(IP).replace(".",",")
        return(Hash_Function(key))

    def AddUser(self,KEY,USER,PASSWORD,MEMBER,DatabaseRef):
        # password given
            
        hash_key = KEY

        base_Tree = {
            "username":USER,
            "password":PASSWORD,
            "member":MEMBER
            }    

        DatabaseRef.child("Users/"+hash_key).set(base_Tree)

    def FindUser(self,DATABASE_REF,KEY):
        # Purpose:{
        # Search the appropriate user through the key.
        # }
        hash_key = KEY
        reference = DATABASE_REF.child("Users/"+hash_key).get()
        if not(reference == None):
            return(True)
        else:
            print("FindUser - Couldn't find user.")
            return(False)
        
        

    def GetData(self,DATABASE_REF,KEY):
        hash_key = KEY
        try:
            data = DATABASE_REF.child("Users/"+hash_key).get()
            if data == False:
                print("GetData - Account Error: Trying to gather data from non-existant account.")
            else:
                main_data = [data['username'],data['password']]
                return(main_data)
        except:
            print("GetData - Critical Error: Exception Caught; Returning None-Containing Tuple.")
            return([None,None])

    def Change_Field(DATABASE_REF,MODE,KEY,NewData):
        # mode 1 = user
        # mode 2 = password 
        # mode 3 = membership
        hash_key= KEY
        if MODE == 1:
            branch = DATABASE_REF.child(f"Users/{hash_key}")
            branch.update({
                'username':NewData
                })
        elif MODE == 2:
            branch = DATABASE_REF.child(f"Users/{hash_key}")
            branch.update({
                'password':NewData
                })
        elif MODE == 3:
            branch = DATABASE_REF.child(f"Users/{hash_key}")
            branch.update({
                'member':NewData
                })
        else:
            print("Change_Field - Unknown mode, aborting.")

    def RequestDeletion(self,DATABASE_REF,KEY):
        success = False
        hash_key= KEY
        try:
            if self.FindUser(DATABASE_REF,hash_key):
                print("Account Found; Deleting record.")
                DATABASE_REF.child("Users/"+hash_key).delete()
                print("Success.")
                success = True
            else:
                print("RequestDeletion - Account Error: Trying to delete non-existant account.")

            return(success)
        except:
            print("Exception Caught.\nCheck error above.")
            return(None)

class GlobalServers():
    def __init__(self,Reference):
        self._server1Status = False
        self._server2Status = False
        self._server3Status = False
        self._Database = Reference
        self.__UpdateServerStats()

    def _ServerStatuses(self):
        return([self._server1Status,self._server2Status,self._server3Status])

    def __UpdateServerStats(self):
        world_Branch = self._Database.child("WorldServers")

        status1 = world_Branch.child("Server1").get("Status")
        status2 = world_Branch.child("Server2").get("Status")
        status3 = world_Branch.child("Server3").get("Status")

        self._server1Status = status1
        self._server2Status = status2
        self._server3Status = status3

    def _GetServerIP(self,ServerNumber):
        self.__UpdateServerStats()
        world_Branch = self._Database.child("WorldServers")
        servers = [world_Branch.child("Server1").get("IP"),world_Branch.child("Server2").get("IP"),world_Branch.child("Server3").get("IP")]

        return(servers[ServerNumber-1])


