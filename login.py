# Author: Chez'lene Cornwall
# Created: 2/14/23
# Description:  the opening page for our program and also the login window


import tkinter as tk
import sqlite3
from tkinter import *

# import messagebox from tkinter module
import tkinter.messagebox

#initialize database
connection = sqlite3.connect("logins.db")
print("Database created")
    
connection.execute("""
    CREATE TABLE EMPLOYEE (
        EMPLOYEE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        USERNAME TEXT NOT NULL,
        PASSWORD TEXT NOT NULL)
                   """)
print("Emplyee table created")


def submit_login():
    
    #pulling data from the form
    user = username.get()
    passw = password.get()

    #validating the data is not null
    if user == "" or passw == "":
        tkinter.messagebox.showinfo("ERROR" , "The needed information has not been provided!")
    else:
        #initialize database
        connection = sqlite3.connect("logins.db")
        #select query
        cursor = connection.execute('SELECT * from EMPLOYEE where USERNAME= "%s" and PASSWORD="%s"'%(user,passw))
        #get data
        if cursor.fetchone():
            tkinter.messagebox.showinfo("Success", "Login Success")
        else:
            tkinter.messagebox.showinfo("ERROR", "Wrong username or password.")



def new_user():
#Adding group members as test employees into database
    connection.execute("INSERT INTO EMPLOYEE(USERNAME,PASSWORD) VALUES ('chezlenec', 'Password1')" );
    connection.execute("INSERT INTO EMPLOYEE(USERNAME,PASSWORD) VALUES ('codyf', 'Password2')" );
    connection.execute("INSERT INTO EMPLOYEE(USERNAME,PASSWORD) VALUES ('basharatt', 'Password3')" );
    
    connection.commit()
    print("New user updated")
    connection.close()
    
def display_logins():
    #open database
    connection = sqlite3.connect('logins.db')
    cursor = connection.execute("SELECT * from EMPLOYEE")
    print("ID\tUSERNAME\tPASSWORD")
    for row in cursor:
        print("{}\t{}\t\t{}".format(row[0],row[1],row[2]))
    connection.close()
 
#initialize tkinter window        
root = Tk()
#setting screen title
root.title("Test")
#setting height and width of screen 
root.geometry("350x250")   

#declaring global variables
global username
global password
   
#username label and textbox
userLabel = Label(root, text = "Username").grid(row=0, column=0)
username = StringVar()
usernameEntry = Entry(root, textvariable=username).grid(row=0, column=1)

#password label and textbox
passwLabel = Label(root, text = "Password").grid(row=1 ,column=0)
password = StringVar()
usernameEntry = Entry(root, textvariable=password, show="*" ).grid(row=1, column=1)

# Adding test logins to database
new_user()

#checking new logins were added
display_logins()

#Login button
loginButton = Button(root, text="Login", command=submit_login).grid(row=4, column=0) 

root.mainloop() 

    