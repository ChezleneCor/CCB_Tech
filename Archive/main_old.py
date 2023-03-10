import tkinter as tk
import sqlite3
from tkinter import *
# import messagebox from tkinter module
import tkinter.messagebox


class Mainframe(tk.Tk):
    """
    frame object to hold all of the pages
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame()
        container.grid(row=0, column=0, sticky="nesw")
        self.id = tk.StringVar()
        #self.id.set = "CCB Tech Inventory System"
        
        self.carousel = {}
        
        for page in (LoginPage, MainPage , InventoryPage , OrderPage):
            page_name = page.__name__
            frame = page(parent = container , controller = self)
            frame.grid(row=0, column=0, sticky="nesw")
            self.carousel[page_name] = frame
        
        self.page_front('LoginPage')
            
    def page_front(self, page_name):
        page = self.carousel[page_name]
        page.tkraise()
        
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id
        
        #declaring global variables
        global username
        global password
        global newUser
        
        #username label and textbox
        userLabel = Label(self, text = "Username").grid(row=0, column=0)
        username = StringVar()
        usernameEntry = Entry(self, textvariable=username).grid(row=0, column=1)

        #password label and textbox
        passwLabel = Label(self, text = "Password").grid(row=1 ,column=0)
        password = StringVar()
        usernameEntry = Entry(self, textvariable=password, show="*" ).grid(row=1, column=1)
        
        #Add new user check box
        newUser = StringVar()
        new_user_btn = Checkbutton(self, variable=newUser, text="New User", onvalue="yes").grid(row=2, column=1)
        
        #Login button
        loginButton = Button(self, text="Submit", command=lambda: submit_login()).grid(row=4, column=0)
        
        def submit_login():

            #pulling data from the form
            user = username.get()
            passw = password.get()
            if_new_user = newUser.get()
            

            #validating the data is not null
            if user == "" or passw == "":
                tkinter.messagebox.showinfo("ERROR" , "The needed information has not been provided!")
                
            elif if_new_user == "yes":
                #initialize database
                connection = sqlite3.connect("logins.db")
                
                #checking if username is already in database
                cursor = connection.execute('SELECT * from EMPLOYEE where USERNAME= "%s"'%(user,))
                #get data
                if cursor.fetchone():
                    tkinter.messagebox.showinfo("ERROR", "This username is already in the system. Please login.")
                    display_logins()
                
                #calling new_user() function to add new user
                else:
                    new_user(user, passw)
                
            else:
                #initialize database
                connection = sqlite3.connect("logins.db")
                #select query
                cursor = connection.execute('SELECT * from EMPLOYEE where USERNAME= "%s" and PASSWORD="%s"'%(user,passw))
                #get data
                if cursor.fetchone():
                    tkinter.messagebox.showinfo("Success", "Login Success")
                    controller.page_front('MainPage')
                    
                    
                else:
                    tkinter.messagebox.showinfo("ERROR", "Wrong username or password.")
                    
        def new_user(user, passw):
        #Adding new users to database
            
            connection.execute("INSERT INTO EMPLOYEE(USERNAME,PASSWORD) VALUES (?, ?)", (user, passw))
            
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
        
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id
        
        go_inventory = Button(self, text="Review Inventory" , command= lambda: controller.page_front("InventoryPage"))
        go_order = Button(self, text="Place an Order" , command= lambda: controller.page_front("OrderPage"))
        
        go_inventory.grid(row=0, column=0)
        go_order.grid(row=1, column=0)

class InventoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id
        
        title = Label (self, text= "Inventory Page")
        title.grid(row=0, column=0)                   

class OrderPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id  
        
        title = Label (self, text= "Order Page")
        title.grid(row=0, column=0)            

#initialize database
connection = sqlite3.connect("logins.db")
print("Database initialized")
    
connection.execute("""
    CREATE TABLE IF NOT EXISTS EMPLOYEE (
        EMPLOYEE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        USERNAME TEXT NOT NULL,
        PASSWORD TEXT NOT NULL)
                   """)
print("Emplyee table initialized")
               
if __name__ == '__main__':
    root = Mainframe()
    
    #setting screen title
    root.title("Test")
    #setting height and width of screen 
    root.geometry("700x500") 
    root.mainloop()      


