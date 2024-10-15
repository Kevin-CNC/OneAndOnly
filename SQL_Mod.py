# SQL DATABASE MODULE.
# By Kevin Caplescu.
import sqlite3
import sys

class Database():
    def  __init__(self):
        self.Connection = sqlite3.connect('userdatabase')
        print("Successfully created SQL Database.\nCursor created.")
        self.Cursor = self.Connection.cursor()

        self.Cursor.execute("""CREATE TABLE IF NOT EXISTS localdatabase 
                               (key text,theme text)""")
        
        result = self.Cursor.execute("SELECT key FROM localdatabase")
        if result.fetchone() == None:
           self.Cursor.execute("""INSERT INTO localdatabase VALUES 
                               ('','default')""")
           self.Connection.commit() 
        else:
            pass

    def _SaveProtocol(self):
        self.Connection.commit()
        self.Cursor.close()
        self.Connection.close()
        sys.exit()

    def _ExecuteCommand(self,cmd):
        return_list = []
        try:
            c = self.Cursor.execute(cmd)
            if str.find(cmd,"SELECT") > -1:
                return_list.append(c.fetchone())

            
            self.Connection.commit()
            return(return_list)
        except:
            print("================\nFailure to execute command\n===================:")

