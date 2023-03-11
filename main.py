import tkinter as tk
import sqlite3
from tkinter import *
from tkinter import ttk
# import messagebox from tkinter module
import tkinter.messagebox
import tkinter.simpledialog

# Author: Chez'lene Cornwall
# Added: 2/13/22
# Description: MainFrame class, LoginPage class 

class Mainframe(tk.Tk):
    """
    frame object to hold all of the pages
    """
    def __init__(self, master = None, *args, **kwargs):
        tk.Tk.__init__(self, master, *args, **kwargs)
        
        container = tk.Frame(bg="#fff")
        container.grid(row=0, column=0, sticky="nesw")
        self.id = tk.StringVar()
        
        #initialize variables for title font and colot
        global title_font
        title_font = 'Futura'
        
        global title_color
        title_color = "#003CFF"
        
        self.carousel = {}
        
        for page in (LoginPage, InventoryPage, OrderPage, UserPage):
            page_name = page.__name__
            if page == OrderPage:
                frame = page(parent=container, controller=self, username=username)
            else:
                frame = page(parent=container , controller=self)
            frame.grid(row=0, column=0, sticky="nesw")
            self.carousel[page_name] = frame
        
        self.page_front('LoginPage')
            
    def page_front(self, page_name):
        '''Show frame for given page'''
        page = self.carousel[page_name]
        
        # If the user is trying to access the UserPage,
        # check if their user_level is at least 2
        if page_name == "UserPage":
            # Initialize database
            connection = sqlite3.connect("inventory.db")
            # Select query
            cursor = connection.execute('SELECT user_level FROM login WHERE username = "%s"' % (username.get()))
            # Get user_level data
            user_level = cursor.fetchone()[0]
            # Check if user_level is at least 2
            if user_level < 2:
                tkinter.messagebox.showinfo("Access Denied", "You do not have permission to access this page.")
                return

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
        global user_level
        global menubar
        
        menubar = Menu(controller)
        filemenu = Menu(menubar,tearoff=0)
        
        filemenu.add_command(label="Inventory", command= lambda: controller.page_front("InventoryPage"))
        filemenu.add_command(label="Orders", command= lambda: controller.page_front("OrderPage"))
        filemenu.add_command(label="Users", command=lambda: controller.page_front("UserPage"))
        filemenu.add_separator()
        filemenu.add_command(label="Log Out", command= lambda: controller.page_front("LoginPage"))
        filemenu.add_command(label="Close", command = self.quit)
        menubar.add_cascade(label="Options",menu=filemenu)
        controller.configure(menu = menubar)
        
        self.update_menu(menubar, "disabled")

        #title
        login_title = Label(self, text="Inventory System" , font = (title_font, 50), fg= title_color).grid(row=0, column=1, columnspan = 2)
        
        #username label and textbox
        userLabel = Label(self, text = "Username").grid(row=2, column=0)
        username = StringVar()
        usernameEntry = Entry(self, textvariable=username).grid(row=2, column=1)

        #password label and textbox
        passwLabel = Label(self, text = "Password").grid(row=3 ,column=0)
        password = StringVar()
        usernameEntry = Entry(self, textvariable=password, show="*" ).grid(row=3, column=1)

        #Add new user check box
        newUser = StringVar()
        new_user_btn = Checkbutton(self, variable=newUser, text="New User", onvalue="Yes").grid(row=4, column=1)
        
        #User_level
        user_level = IntVar()

        #Login button
        loginButton = Button(self, text="Login", command=lambda: submit_login()).grid(row=6, column=1)

        #New user guide
        guide = Label(self, text = "New users click the 'New User' check box and ensure that the box is checked and type your desired username and password and click the login button.", fg = "blue").grid(row=8 ,column=1)
        guide2 = Label(self, text = "New users user level will be automatically set to 1. Your managers or supervisor can change your user level", fg = "blue").grid(row=9 ,column=1)
        guide3 = Label(self, text = "Uncheck the 'New User' check box and type your username and password to login.", fg = "blue").grid(row=10 ,column=1)
        guide4 = Label(self, text = "Professor use the username: feihongl and password: Pass5 to login as a user level 3.", fg = "purple").grid(row=12 ,column=1)
        def submit_login():

            #pulling data from the form
            user = username.get()
            passw = password.get()
            if_new_user = newUser.get() 
            

            #validating the data is not null
            if user == "" or passw == "":
                tkinter.messagebox.showinfo("ERROR" , "The needed information has not been provided!")
                
            elif if_new_user == "Yes":
                #initialize database
                connection = sqlite3.connect("inventory.db")
                
                #checking if username is already in database
                cursor = connection.execute('SELECT * from login where username= "%s"'%(user))
                
                #get data
                if cursor.fetchone():
                    tkinter.messagebox.showinfo("ERROR", "This username is already in the system. Please login.")
                
                #calling new_user() function to add new user
                else:
                    new_user(user, passw)
                        
            else:
                #initialize database
                connection = sqlite3.connect("inventory.db")
                #select query
                cursor = connection.execute('SELECT * from login where username= "%s" and password="%s"'%(user,passw))
                
                #get data
                if cursor.fetchone():
                    tkinter.messagebox.showinfo("Success", "Login Success")
                    controller.page_front('InventoryPage')
                    self.update_menu(menubar, "active")
                    
                else:
                    tkinter.messagebox.showinfo("ERROR", "Wrong username or password.")
                    display_logins()           
                        
        def new_user(user, passw):
            #Adding new users to database

            connection.execute("INSERT INTO login (username, password, user_level) VALUES (?, ?, ?)", (user, passw, 0))

            connection.commit()
            print("New user updated")
            connection.close()

        
        def display_logins():
            #open database
            connection = sqlite3.connect('inventory.db')
            cursor = connection.execute("SELECT * from login")
            print("ID\tUsername\tPassword\tUser Level")
            for row in cursor:
                print("{}\t{}\t{}\t{}".format(row[0],row[1],row[2], row[3]))
            connection.close()
        
    def update_menu(self, menubar, _state):
        menubar.entryconfig("Options" , state=_state)

#Author: Basharat Tunio
#added: 3/8/2023
#Description: Main page where we can manipulate inventory data
class InventoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        self.item_ID = StringVar()
        self.item_name = StringVar()
        self.item_quantity = IntVar()
        self.vendor_name = StringVar()
        
        
        title = Label (self, text= "Inventory Page", font = (title_font, 50), fg= title_color)
        title.grid(row=0, column=1,)

        #search field in the main page

        #search by item ID
        item_ID_label = Label(self, text="Search by Item ID:")
        item_ID_label.grid(row=2, column=0, padx=10, pady=10)
        item_ID_entry = Entry(self, textvariable=self.item_ID)
        item_ID_entry.grid(row=2, column=1)
        #search item ID button
        search_ID_button = Button(self, text="Search", command=lambda: InventoryPage.search_ID(item_ID_entry.get()))
        search_ID_button.grid(row=2, column=2, padx=10, pady=10)

        #search by item name
        item_name_label = Label(self, text="Search by Item Name:")
        item_name_label.grid(row=4, column=0, padx=10, pady=10)
        item_name_entry = Entry(self, textvariable=self.item_name)
        item_name_entry.grid(row=4, column=1)
        #search item name button
        search_button = Button(self, text="Search", command=lambda: InventoryPage.search_item(item_name_entry.get()))
        search_button.grid(row=4, column=2, padx=10, pady=10)

        vendor_label = Label(self, text="Seach by Vendor Name:")
        vendor_label.grid(row=6, column=0, padx=10, pady=10)
        vendor_entry = Entry(self, textvariable=self.vendor_name)
        vendor_entry.grid(row=6, column=1)
        #search vendor button
        search_button = Button(self, text="Search", command=lambda: InventoryPage.search_vendor(vendor_entry.get()))
        search_button.grid(row=6, column=2, padx=10, pady=10)

        #Buttons only functions

        DisplayButton = Button(self, text="Display the entire inventory", command=lambda:InventoryPage.display())
        DisplayButton.grid(row=8, column=1, padx=10, pady=10)

        InsertButton = Button(self, text="Add an item", command=lambda:InventoryPage.insert())
        InsertButton.grid(row=10, column=1, padx=10, pady=10)

        DeleteButton = Button(self, text="Delete an item", command=lambda:InventoryPage.delete())
        DeleteButton.grid(row=12, column=1, padx=10, pady=10)
        
        
    # search functions

    def search_ID(item_ID):
            
            # Create a new Toplevel window to display the result of the search
            search_window = tk.Toplevel() 
            search_window.title("Search item ID results")

            # Create a Frame to hold the Labels for each item
            search_frame = tk.Frame(search_window)
            search_frame.grid(padx=10, pady=10)

            # Create Labels for the headers of each column
            item_ID_header = tk.Label(search_frame, text="Item ID")
            item_ID_header.grid(row=0, column=0, padx=10, pady=10)

            item_name_header = tk.Label(search_frame, text="Item Name")
            item_name_header.grid(row=0, column=1, padx=10, pady=10)

            total_quantity_header = tk.Label(search_frame, text="Total Quantity")
            total_quantity_header.grid(row=0, column=2, padx=10, pady=10)

            vendor_name_header = tk.Label(search_frame, text="Vendor Name")
            vendor_name_header.grid(row=0, column=3, padx=10, pady=10)

            conn = sqlite3.connect('inventory.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM inventory where item_ID like ?",(item_ID,))
            rows = cur.fetchall()

            #error check
            if cur.execute("SELECT * FROM inventory where item_ID like ?",(item_ID,)).fetchall() == []:
                error_label = tk.Label(search_frame, text= "Error: " + item_ID + " not found", fg='red')
                error_label.grid(row=1, column=0, padx=10, pady=10)
                return 
            
            for row in rows:
                print(row) 
            conn.close()


            # loop that displays the results
            for i, row in enumerate(rows):

                item_ID_label = tk.Label(search_frame, text=row[0])
                item_ID_label.grid(row=i+1, column=0, padx=10, pady=10)

                item_name_label = tk.Label(search_frame, text=row[1])
                item_name_label.grid(row=i+1, column=1, padx=10, pady=10)

                item_quantity_label = tk.Label(search_frame, text=row[2])
                item_quantity_label.grid(row=i+1, column=2, padx=10, pady=10)

                vendor_name_label = tk.Label(search_frame, text=row[3])
                vendor_name_label.grid(row=i+1, column=3, padx=10, pady=10)
            
    def search_item(item_name):

            # Create a new Toplevel window to display the result of the search
            search_window = tk.Toplevel() 
            search_window.title("Search item name results")

            # Create a Frame to hold the Labels for each item
            search_frame = tk.Frame(search_window)
            search_frame.grid(padx=10, pady=10)

            # Create Labels for the headers of each column
            item_ID_header = tk.Label(search_frame, text="Item ID")
            item_ID_header.grid(row=0, column=0, padx=10, pady=10)

            item_name_header = tk.Label(search_frame, text="Item Name")
            item_name_header.grid(row=0, column=1, padx=10, pady=10)

            total_quantity_header = tk.Label(search_frame, text="Total Quantity")
            total_quantity_header.grid(row=0, column=2, padx=10, pady=10)

            vendor_name_header = tk.Label(search_frame, text="Vendor Name")
            vendor_name_header.grid(row=0, column=3, padx=10, pady=10)

            conn = sqlite3.connect('inventory.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM inventory where item_name like ?",(item_name,))
            rows = cur.fetchall()

            #error check
            if  cur.execute("SELECT * FROM inventory where item_name like ?",(item_name,)).fetchall() == []:
                error_label = tk.Label(search_frame, text= "Error: " + item_name + " not found", fg='red')
                error_label.grid(row=1, column=1, padx=10, pady=10)
                return 
             
            for row in rows:
                print(row) 
            conn.close()

            # Loop to display the results
            for i, row in enumerate(rows):
                item_ID_label = tk.Label(search_frame, text=row[0])
                item_ID_label.grid(row=i+1, column=0, padx=10, pady=10)

                item_name_label = tk.Label(search_frame, text=row[1])
                item_name_label.grid(row=i+1, column=1, padx=10, pady=10)

                item_quantity_label = tk.Label(search_frame, text=row[2])
                item_quantity_label.grid(row=i+1, column=2, padx=10, pady=10)

                vendor_name_label = tk.Label(search_frame, text=row[3])
                vendor_name_label.grid(row=i+1, column=3, padx=10, pady=10)
            
    def search_vendor(vendor_name):

            # Create a new Toplevel window to display the result of the search
            search_window = tk.Toplevel() 
            search_window.title("Search vendor results")

            # Create a Frame to hold the Labels for each item
            search_frame = tk.Frame(search_window)
            search_frame.grid(padx=10, pady=10)

            # Create Labels for the headers of each column
            item_ID_header = tk.Label(search_frame, text="Item ID")
            item_ID_header.grid(row=0, column=0, padx=10, pady=10)

            item_name_header = tk.Label(search_frame, text="Item Name")
            item_name_header.grid(row=0, column=1, padx=10, pady=10)

            total_quantity_header = tk.Label(search_frame, text="Total Quantity")
            total_quantity_header.grid(row=0, column=2, padx=10, pady=10)

            vendor_name_header = tk.Label(search_frame, text="Vendor Name")
            vendor_name_header.grid(row=0, column=3, padx=10, pady=10)

            conn = sqlite3.connect('inventory.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM inventory where vendor_name like ?",(vendor_name,))
            rows = cur.fetchall() 

            #error check
            if  cur.execute("SELECT * FROM inventory where vendor_name like ?",(vendor_name,)).fetchall() == []:
                error_label = tk.Label(search_frame, text= "Error: " + vendor_name + " not found", fg='red')
                error_label.grid(row=1, column=3, padx=10, pady=10)
                return 
            
            for row in rows:
                print(row) 
            conn.close()

            # loop to display the results
            for i, row in enumerate(rows):
                item_ID_label = tk.Label(search_frame, text=row[0])
                item_ID_label.grid(row=i+1, column=0, padx=10, pady=10)

                item_name_label = tk.Label(search_frame, text=row[1])
                item_name_label.grid(row=i+1, column=1, padx=10, pady=10)

                item_quantity_label = tk.Label(search_frame, text=row[2])
                item_quantity_label.grid(row=i+1, column=2, padx=10, pady=10)

                vendor_name_label = tk.Label(search_frame, text=row[3])
                vendor_name_label.grid(row=i+1, column=3, padx=10, pady=10)

    #display the full database by item name
    def display():
            conn = sqlite3.connect('inventory.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM inventory ORDER BY ITEM_QUANTITY")
            rows = cur.fetchall()    
            for row in rows:
                print(row) 
            conn.close()

            # Create a new Toplevel window to display the total database
            display_window = tk.Toplevel() 
            display_window.title("Inventory Table")

            # Create a Frame to hold the Labels for each item
            display_frame = tk.Frame(display_window)
            display_frame.grid(padx=10, pady=10)

            # Create Labels for the headers of each column
            item_ID_header = tk.Label(display_frame, text="Item ID")
            item_ID_header.grid(row=0, column=0, padx=10, pady=10)

            item_name_header = tk.Label(display_frame, text="Item Name")
            item_name_header.grid(row=0, column=1, padx=10, pady=10)

            total_quantity_header = tk.Label(display_frame, text="Item Quantity")
            total_quantity_header.grid(row=0, column=2, padx=10, pady=10)

            vendor_name_header = tk.Label(display_frame, text="Vendor Name")
            vendor_name_header.grid(row=0, column=3, padx=10, pady=10)

            # Create Labels for each order and add them to the Frame
            for i, row in enumerate(rows):
                item_ID_label = tk.Label(display_frame, text=row[0])
                item_ID_label.grid(row=i+1, column=0, padx=10, pady=10)

                item_name_label = tk.Label(display_frame, text=row[1])
                item_name_label.grid(row=i+1, column=1, padx=10, pady=10)

                item_quantity_label = tk.Label(display_frame, text=row[2])
                item_quantity_label.grid(row=i+1, column=2, padx=10, pady=10)

                vendor_name_label = tk.Label(display_frame, text=row[3])
                vendor_name_label.grid(row=i+1, column=3, padx=10, pady=10)

    #Add item function
    def insert():
            
            # Check if user is authorized to approve orders
            user_level = InventoryPage.get_user_level(username.get())
            if user_level < 2:
                tkinter.messagebox.showerror("Unauthorized", "You are not authorized to add items in the system. Only Level 2 users or above!")
                return
            
            item_ID = StringVar()
            name = StringVar()
            quantity = IntVar()
            vendor = StringVar()
            
            # Create a new Toplevel window to display the orders
            insert_window = tk.Toplevel()
            insert_window.title("Add items")

            # Create a Frame to hold the Labels for each item
            insert_frame = tk.Frame(insert_window)
            insert_frame.grid(padx=10, pady=10)

            # Creating fields to add data
            #add item ID
            item_ID_label = tk.Label(insert_frame, text="Item ID:")
            item_ID_label.grid(row=2, column=0, padx=10, pady=10)
            item_ID_entry = tk.Entry(insert_frame, textvariable=item_ID)
            item_ID_entry.grid(row=2, column=1)

            #add item name
            item_name_label = tk.Label(insert_frame, text="Item Name:")
            item_name_label.grid(row=4, column=0, padx=10, pady=10)
            item_name_entry = tk.Entry(insert_frame, textvariable=name)
            item_name_entry.grid(row=4, column=1)

            #add item quantity
            quantity_label = tk.Label(insert_frame, text="Item Quantity:")
            quantity_label.grid(row=6, column=0, padx=10, pady=10)
            quantity_entry = tk.Entry(insert_frame, textvariable=quantity)
            quantity_entry.grid(row=6, column=1)

            #add vendor item name
            vendor_label = tk.Label(insert_frame, text="Vendor:")
            vendor_label.grid(row=8, column=0, padx=10, pady=10)
            vendor_entry = tk.Entry(insert_frame, textvariable=vendor)
            vendor_entry.grid(row=8, column=1)

            #add button
            add_button = tk.Button(insert_frame, text="Add", command=lambda: add(item_ID_entry.get(), item_name_entry.get(), quantity_entry.get(), vendor_entry.get()))
            add_button.grid(row=10, column=2, padx=10, pady=10)


            def add(ID, name, quantity, vendor):
                #error messages
                if ID == '':
                    error_label = tk.Label(insert_frame, text= "Failed to add the item in the system database. Item ID " + ID + " is not given", fg='red')
                    error_label.grid(row=12, column=0, padx=10, pady=10)
                    return
                
                if name == '':
                    error_label = tk.Label(insert_frame, text= "Failed to add the item in the system database. Item name " + name + " is not given", fg='red')
                    error_label.grid(row=12, column=0, padx=10, pady=10)
                    return
                
                #error to check if the user actually input a number
                while True:
                    try:
                        int(quantity)
                        break
                    except ValueError:
                        error_label = tk.Label(insert_frame, text= "Failed to add the item in the system database. Item Quantity " + str(quantity) + " is not a valid number", fg='red')
                        error_label.grid(row=12, column=0, padx=10, pady=10)
                        return

                if int(quantity) < 0:
                    error_label = tk.Label(insert_frame, text= "Failed to add the item in the system database. Item Quantity " + str(quantity) + " is not a valid number", fg='red')
                    error_label.grid(row=12, column=0, padx=10, pady=10)
                    return
                
                if vendor == '':
                    error_label = tk.Label(insert_frame, text= "Failed to add the item in the system database. Vendor name " + vendor + " is not given", fg='red')
                    error_label.grid(row=12, column=0, padx=10, pady=10)
                    return
                
                #confirmation message
                confirm_label = tk.Label(insert_frame, text="Item ID: " + ID + "  Item Name: " + name + "  Item Quantity " +  str(quantity) + "  from Vendor: " + vendor + "  has been added in the system", fg='green')
                confirm_label.grid(row=12, column=0, padx=10, pady=10)

                conn = sqlite3.connect('inventory.db')
                cur = conn.cursor()
                cur.execute("INSERT INTO inventory (item_ID, item_name, item_quantity, qoo, vendor_name) VALUES (?, ?, ?, ?, ?)", (ID, name, int(quantity), '0', vendor))
                conn.commit()
                conn.close()

    #delete item function
    def delete():

        # Check if user is authorized to approve orders
        user_level = InventoryPage.get_user_level(username.get())
        if user_level < 2:
            tkinter.messagebox.showerror("Unauthorized", "You are not authorized to delete items in the system. Only Level 2 users or above!")
            return
        
        item_ID = StringVar()
        name = StringVar()
        vendor = StringVar()
        no_turning_back = StringVar()
        
        # Create a new Toplevel window to go to delete system
        delete_window = tk.Toplevel()
        delete_window.title("Delete system")

        # Create a Frame 
        delete_frame = tk.Frame(delete_window)
        delete_frame.grid(padx=10, pady=10)

        #Buttons that will show hidden function
        Delete_itemID_Button = tk.Button(delete_frame, text="Delete by item ID", command=lambda: delete_item_ID())
        Delete_itemID_Button.grid(row= 2, column=0, padx=10, pady=10)

        Delete_item_Button = tk.Button(delete_frame, text="Delete by item name", command=lambda: delete_item())
        Delete_item_Button.grid(row= 8, column=0, padx=10, pady=10)

        Delete_vendor_Button = tk.Button(delete_frame, text="Delete by vendor", command=lambda: delete_vendor())
        Delete_vendor_Button.grid(row= 14, column=0, padx=10, pady=10)

        Delete_all_Button = tk.Button(delete_frame, text="Delete All Data", command=lambda: delete_all())
        Delete_all_Button.grid(row= 20, column=0, padx=10, pady=10)


        def delete_item_ID():

            #delete item ID field
            item_ID_label = tk.Label(delete_frame, text="Item ID:")
            item_ID_label.grid(row=4, column=0, padx=10, pady=10)
            item_ID_entry = tk.Entry(delete_frame, textvariable=item_ID)
            item_ID_entry.grid(row=4, column=1)

            Delete_itemID_Button = tk.Button(delete_frame, text="Delete from the system", command=lambda: delete_ID(item_ID_entry.get()))
            Delete_itemID_Button.grid(row= 4, column=2, padx=10, pady=10)

            def delete_ID(item):

                conn = sqlite3.connect('inventory.db')
                cur = conn.cursor()

                #error check
                if cur.execute("SELECT * FROM inventory where item_ID like ?",(item,)).fetchall() == []:
                    error_label = tk.Label(delete_frame, text= "Error: " + item + " not found", fg='red')
                    error_label.grid(row=6, column=0, padx=10, pady=10)
                    return 

                cur.execute("DELETE FROM inventory where item_ID like ?",(item,))
                conn.commit()
                conn.close()

                #confirmation message
                confirm_label = tk.Label(delete_frame, text="Item ID: " + item + " has been deleted from the system", fg ='green')
                confirm_label.grid(row=6, column=0, padx=10, pady=10)

        def delete_item():

            #delete item name button
            item_name_label = tk.Label(delete_frame, text="Item Name:")
            item_name_label.grid(row=10, column=0, padx=10, pady=10)
            item_name_entry = tk.Entry(delete_frame, textvariable=name)
            item_name_entry.grid(row=10, column=1)

            Delete_item_Button = tk.Button(delete_frame, text="Delete from the system", command=lambda: delete_name(item_name_entry.get()))
            Delete_item_Button.grid(row= 10, column=2, padx=10, pady=10)

            def delete_name(name):
            
                conn = sqlite3.connect('inventory.db')
                cur = conn.cursor()

                #error check
                if cur.execute("SELECT * FROM inventory where item_name like ?",(name,)).fetchall() == []:
                    error_label = tk.Label(delete_frame, text= "Error: " + name + " not found", fg='red')
                    error_label.grid(row=12, column=0, padx=10, pady=10)
                    return
                
                cur.execute("DELETE FROM inventory where item_name like ?",(name,))
                conn.commit()
                conn.close()

                #confirmation message
                confirm_label = tk.Label(delete_frame, text="Item ID: " + name + " has been deleted from the system", fg ='green')
                confirm_label.grid(row=12, column=0, padx=10, pady=10)

        def delete_vendor():
              
            #delete vendor
            delete_vendor_label = tk.Label(delete_frame, text="Vendor name:")
            delete_vendor_label.grid(row=16, column=0, padx=10, pady=10)
            delete_vendor_entry = tk.Entry(delete_frame, textvariable=vendor)
            delete_vendor_entry.grid(row=16, column=1)

            Delete_item_Button = tk.Button(delete_frame, text="Delete from the system", command=lambda: delete_name(delete_vendor_entry.get()))
            Delete_item_Button.grid(row= 16, column=2, padx=10, pady=10)

            def delete_name(vendor):
            
                conn = sqlite3.connect('inventory.db')
                cur = conn.cursor()

                #error check
                if cur.execute("SELECT * FROM inventory where vendor_name like ?",(vendor,)).fetchall() == []:
                    error_label = tk.Label(delete_frame, text= "Error: " + vendor + " not found", fg='red')
                    error_label.grid(row=18, column=0, padx=10, pady=10)
                    return
                
                cur.execute("DELETE FROM inventory where vendor_name like ?",(vendor,))
                conn.commit()
                conn.close()

                #confirmation message
                confirm_label = tk.Label(delete_frame, text="Vendor: " + vendor + " has been deleted from the system", fg ='green')
                confirm_label.grid(row=18, column=0, padx=10, pady=10)

        def delete_all():

            # Check if user is authorized to approve orders
            user_level = InventoryPage.get_user_level(username.get())
            if user_level < 3:
                tkinter.messagebox.showerror("Unauthorized", "You are not authorized to delete all data in the system. Only Level 3 users!")
                return

            #confirmation message
            confirm_label = tk.Label(delete_frame, text="Are you sure. Type Y to confirm to delete all the data")
            confirm_label.grid(row=22, column=0, padx=10, pady=10)

            #delete all
            delete_all_label = tk.Label(delete_frame, text="Delete All Data")
            delete_all_label.grid(row=24, column=0, padx=10, pady=10)
            delete_all_entry = tk.Entry(delete_frame, textvariable=no_turning_back)
            delete_all_entry.grid(row=24, column=1)

            Delete_all_Button = tk.Button(delete_frame, text=" confirm to Delete Everything!!!", command=lambda: delete_A(delete_all_entry.get()))
            Delete_all_Button.grid(row=24, column=2, padx=10, pady=10)

            def delete_A(confirmation):
                if (confirmation=='y' or confirmation=='Y' ):
                    Delete_f_Button = tk.Button(delete_frame, text="Press here to Delete Everything!!!", command=lambda: delete_F())
                    Delete_f_Button.grid(row=26, column=1, padx=10, pady=10)
                
                else:
                    confirm_label = tk.Label(delete_frame, text="Incorrect Input", fg ='red')
                    confirm_label.grid(row=26, column=0, padx=10, pady=10)

                def delete_F():
                        confirm_label = tk.Label(delete_frame, text="All Inventory Data Erased", fg ='green')
                        confirm_label.grid(row=28, column=0, padx=10, pady=10)

                        conn = sqlite3.connect('inventory.db')
                        cur = conn.cursor()
                        cur.execute('DELETE FROM inventory;',)
                        conn.commit()
                        conn.close()

    def get_user_level(username):
        # Get user level from the database
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("SELECT user_level FROM login WHERE username=?", (str(username),))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else 0

# Author: Cody Foerster
# Added: 3/3/2023
# Description: OrderPage class, functions, and buttons.
# Allows a user to place orders, review orders,
# search by item, search by vendor,
# approve orders, and receive orders
class OrderPage(tk.Frame):
    def __init__(self, parent, controller, username):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id

        self.item_ID = tk.StringVar()
        self.item_name = tk.StringVar()
        self.item_quantity = tk.StringVar()
        self.vendor_name = tk.StringVar()
        self.approved = tk.BooleanVar()
        self.received = tk.BooleanVar()

        title = Label (self, text= "Order Page", font = (title_font, 50), fg= title_color)
        title.grid(row=0, column=1)

        #Item_ID label and entry box:
        item_ID_label = Label(self, text="Item ID:")
        item_ID_label.grid(row=1, column=0, padx=10, pady=10)
        item_ID_entry = Entry(self, textvariable=self.item_ID)
        item_ID_entry.grid(row=1, column=1)

        #Item_name label and entry box:
        item_name_label = Label(self, text="Item Name:")
        item_name_label.grid(row=2, column=0, padx=10, pady=10)
        item_name_entry = Entry(self, textvariable=self.item_name)
        item_name_entry.grid(row=2, column=1)

        #Item_quantity label and entry box:
        item_quantity_label = Label(self, text="Item Quantity:")
        item_quantity_label.grid(row=3, column=0, padx=10, pady=10)
        item_quantity_entry = Entry(self, textvariable=self.item_quantity)
        item_quantity_entry.grid(row=3, column=1)

        #Vendor_name label and entry box:
        vendor_name_label = Label(self, text="Vendor Name:")
        vendor_name_label.grid(row=4, column=0, padx=10, pady=10)
        vendor_name_entry = Entry(self, textvariable=self.vendor_name)
        vendor_name_entry.grid(row=4, column=1)

        #Save to database button:
        save_button = Button(self, text="Submit Order", command=self.save_to_database)
        save_button.grid(row=5, column=1, columnspan=2)

        #Review orders button:
        review_orders_button = Button(self, text="Review Orders", command=self.review_orders)
        review_orders_button.grid(row=2, column=3, columnspan=2)

        #Search by item button:
        search_item_button = Button(self, text="Search by Item Name", command=self.search_by_item)
        search_item_button.grid(row=3, column=3, columnspan=2)

        #Search by vendor button:
        search_vendor_button = Button(self, text="Search by Vendor Name", command=self.search_by_vendor)
        search_vendor_button.grid(row=4, column=3, columnspan=2)

        #Approve Orders button:
        approve_orders_button = Button(self, text="Approve Orders", command=lambda: self.approve_order())
        approve_orders_button.grid(row=5, column=3, columnspan=2)

        #Receive Orders button:
        receive_orders_button = Button(self, text="Receive Orders", command=self.receive_order)
        receive_orders_button.grid(row=6, column=3, columnspan=2)

    #Save order to the database:
    def save_to_database(self):
        connection = sqlite3.connect('inventory.db')
        c = connection.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS orders
                     (item_ID text, item_name text, item_quantity integer, vendor_name text, approved bool, received bool)
                  """)
        c.execute("""INSERT INTO orders (item_ID, item_name, item_quantity, vendor_name, approved, received)
                     VALUES (?,?,?,?,0,0)
                  """, (self.item_ID.get(), self.item_name.get(), self.item_quantity.get(), self.vendor_name.get()))
        connection.commit()
        connection.close()

        self.item_ID.set('')
        self.item_name.set('')
        self.item_quantity.set('')
        self.vendor_name.set('')

    #Review All Orders:
    def review_orders(self):
        connection = sqlite3.connect('inventory.db')
        c = connection.cursor()
        c.execute("""SELECT * FROM orders""")
        orders = c.fetchall()
        connection.close()

        # Create a new Toplevel window to display the orders
        orders_window = tk.Toplevel(self)
        orders_window.title("Review Orders")

        # Create a Frame to hold the Labels for each order
        orders_frame = tk.Frame(orders_window)
        orders_frame.pack(padx=10, pady=10)

        # Create Labels for the headers of each column
        order_ID_header = tk.Label(orders_frame, text="Order ID")
        order_ID_header.grid(row=0, column=0, padx=10, pady=10)

        item_ID_header = tk.Label(orders_frame, text="Item ID")
        item_ID_header.grid(row=0, column=1, padx=10, pady=10)

        item_name_header = tk.Label(orders_frame, text="Item Name")
        item_name_header.grid(row=0, column=2, padx=10, pady=10)

        item_quantity_header = tk.Label(orders_frame, text="Item Quantity")
        item_quantity_header.grid(row=0, column=3, padx=10, pady=10)

        vendor_name_header = tk.Label(orders_frame, text="Vendor Name")
        vendor_name_header.grid(row=0, column=4, padx=10, pady=10)

        approved_header = tk.Label(orders_frame, text="Approved")
        approved_header.grid(row=0, column=5, padx=10, pady=10)

        received_header = tk.Label(orders_frame, text="Received")
        received_header.grid(row=0, column=6, padx=10, pady=10)

        # Create Labels for each order and add them to the Frame
        for i, order in enumerate(orders):
            order_ID_label = tk.Label(orders_frame, text=order[0])
            order_ID_label.grid(row=i+1, column=0, padx=10, pady=10)

            item_ID_label = tk.Label(orders_frame, text=order[1])
            item_ID_label.grid(row=i+1, column=1, padx=10, pady=10)

            item_name_label = tk.Label(orders_frame, text=order[2])
            item_name_label.grid(row=i+1, column=2, padx=10, pady=10)

            item_quantity_label = tk.Label(orders_frame, text=order[3])
            item_quantity_label.grid(row=i+1, column=3, padx=10, pady=10)

            vendor_name_label = tk.Label(orders_frame, text=order[4])
            vendor_name_label.grid(row=i+1, column=4, padx=10, pady=10)

            approved_label = tk.Label(orders_frame, text="Yes" if order[5] else "No")
            approved_label.grid(row=i+1, column=5, padx=10, pady=10)

            received_label = tk.Label(orders_frame, text="Yes" if order[6] else "No")
            received_label.grid(row=i+1, column=6, padx=10, pady=10)

    #Search by Item:
    def search_by_item(self):
        search_window = Toplevel(self)
        search_window.title("Search by Item Name")

        search_label = Label(search_window, text="Enter Item Name:")
        search_label.grid(row=0, column=0, padx=10, pady=10)

        search_entry = Entry(search_window)
        search_entry.grid(row=0, column=1, padx=10, pady=10)

        search_button = Button(search_window, text="Search", command=lambda: self.perform_item_search(search_entry.get(), search_window))
        search_button.grid(row=0, column=2, padx=10, pady=10)

    #Performs Item Search from search_by_item function:
    def perform_item_search(self, search_term, search_window):
        connection = sqlite3.connect('inventory.db')
        c = connection.cursor()
        c.execute("""SELECT * FROM orders WHERE item_name LIKE ?""", ('%'+search_term+'%',))
        orders = c.fetchall()
        connection.close()

        search_results_window = Toplevel(search_window)
        search_results_window.title("Search Results")

        order_ID_header = tk.Label(search_results_window, text="Order ID")
        order_ID_header.grid(row=0, column=0, padx=10, pady=10)

        item_ID_header = tk.Label(search_results_window, text="Item ID")
        item_ID_header.grid(row=0, column=1, padx=10, pady=10)
    
        item_name_header = tk.Label(search_results_window, text="Item Name")
        item_name_header.grid(row=0, column=2, padx=10, pady=10)
    
        item_quantity_header = tk.Label(search_results_window, text="Item Quantity")
        item_quantity_header.grid(row=0, column=3, padx=10, pady=10)
    
        vendor_name_header = tk.Label(search_results_window, text="Vendor Name")
        vendor_name_header.grid(row=0, column=4, padx=10, pady=10)
    
        approved_header = tk.Label(search_results_window, text="Approved")
        approved_header.grid(row=0, column=5, padx=10, pady=10)
    
        received_header = tk.Label(search_results_window, text="Received")
        received_header.grid(row=0, column=6, padx=10, pady=10)

        try:
            for i, order in enumerate(orders):
                order_ID_header = tk.Label(search_results_window, text=order[0])
                order_ID_header.grid(row=i+1, column=0, padx=10, pady=10)
                
                item_ID_label = tk.Label(search_results_window, text=order[1])
                item_ID_label.grid(row=i+1, column=1, padx=10, pady=10)

                item_name_label = tk.Label(search_results_window, text=order[2])
                item_name_label.grid(row=i+1, column=2, padx=10, pady=10)

                item_quantity_label = tk.Label(search_results_window, text=order[3])
                item_quantity_label.grid(row=i+1, column=3, padx=10, pady=10)

                vendor_name_label = tk.Label(search_results_window, text=order[4])
                vendor_name_label.grid(row=i+1, column=4, padx=10, pady=10)

                approved_label = tk.Label(search_results_window, text="Yes" if order[5] else "No")
                approved_label.grid(row=i+1, column=5, padx=10, pady=10)

                received_label = tk.Label(search_results_window, text="Yes" if order[6] else "No")
                received_label.grid(row=i+1, column=6, padx=10, pady=10)
            if not orders:
                error_label = Label(search_results_window, text="Item not found.")
                error_label.grid(row=1, column=0, padx=10, pady=10)
        except:
            error_label = Label(search_results_window, text="Error: Could not retrieve search results.")
            error_label.grid(row=1, column=0, padx=10, pady=10)

    #Search by vendor:
    def search_by_vendor(self):
        search_window = Toplevel(self)
        search_window.title("Search by Vendor Name")

        search_label = Label(search_window, text="Enter Vendor Name:")
        search_label.grid(row=0, column=0, padx=10, pady=10)

        search_entry = Entry(search_window)
        search_entry.grid(row=0, column=1, padx=10, pady=10)

        search_button = Button(search_window, text="Search", command=lambda: self.perform_vendor_search(search_entry.get(), search_window))
        search_button.grid(row=0, column=2, padx=10, pady=10)

    #Performs Vendor Search from search_by_vendor function:
    def perform_vendor_search(self, search_term, search_window):
        connection = sqlite3.connect('inventory.db')
        c = connection.cursor()
        c.execute("""SELECT * FROM orders WHERE vendor_name LIKE ?""", ('%'+search_term+'%',))
        orders = c.fetchall()
        connection.close()

        search_results_window = Toplevel(search_window)
        search_results_window.title("Search Results")

        order_ID_header = tk.Label(search_results_window, text="Order ID")
        order_ID_header.grid(row=0, column=0, padx=10, pady=10)

        item_ID_header = tk.Label(search_results_window, text="Item ID")
        item_ID_header.grid(row=0, column=1, padx=10, pady=10)
    
        item_name_header = tk.Label(search_results_window, text="Item Name")
        item_name_header.grid(row=0, column=2, padx=10, pady=10)
    
        item_quantity_header = tk.Label(search_results_window, text="Item Quantity")
        item_quantity_header.grid(row=0, column=3, padx=10, pady=10)
    
        vendor_name_header = tk.Label(search_results_window, text="Vendor Name")
        vendor_name_header.grid(row=0, column=4, padx=10, pady=10)
    
        approved_header = tk.Label(search_results_window, text="Approved")
        approved_header.grid(row=0, column=5, padx=10, pady=10)
    
        received_header = tk.Label(search_results_window, text="Received")
        received_header.grid(row=0, column=6, padx=10, pady=10)
        try:
            for i, order in enumerate(orders):
                order_ID_header = tk.Label(search_results_window, text=order[0])
                order_ID_header.grid(row=i+1, column=0, padx=10, pady=10)

                item_ID_label = tk.Label(search_results_window, text=order[1])
                item_ID_label.grid(row=i+1, column=1, padx=10, pady=10)

                item_name_label = tk.Label(search_results_window, text=order[2])
                item_name_label.grid(row=i+1, column=2, padx=10, pady=10)

                item_quantity_label = tk.Label(search_results_window, text=order[3])
                item_quantity_label.grid(row=i+1, column=3, padx=10, pady=10)

                vendor_name_label = tk.Label(search_results_window, text=order[4])
                vendor_name_label.grid(row=i+1, column=4, padx=10, pady=10)

                approved_label = tk.Label(search_results_window, text="Yes" if order[5] else "No")
                approved_label.grid(row=i+1, column=5, padx=10, pady=10)

                received_label = tk.Label(search_results_window, text="Yes" if order[6] else "No")
                received_label.grid(row=i+1, column=6, padx=10, pady=10)
            if not orders:
                error_label = Label(search_results_window, text="Vendor not found.")
                error_label.grid(row=1, column=0, padx=10, pady=10)
        except:
            error_label = Label(search_results_window, text="Error: Could not retrieve search results.")
            error_label.grid(row=1, column=0, padx=10, pady=10)


    #Approve orders:
    def approve_order(self):
        # Check if user is authorized to approve orders
        user_level = self.get_user_level(username.get())
        if user_level < 3:
            tkinter.messagebox.showerror("Unauthorized", "You are not authorized to approve orders!")
            return

        # Get list of orders to approve
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE approved IS 0")
        orders = cursor.fetchall()
        connection.close()

        # Create a list of order IDs to display to the user
        #order_ids = [order[0] for order in orders]

        # Create a list of order details to display to the user
        order_ID = []
        for order in orders:
            order_ID.append(f"Order ID: {order[0]}, Item ID: {order[1]}, Item Name: {order[2]}, Item Quantity: {order[3]}, Vendor Name: {order[4]}")

        # Ask the user to select an order to approve
        selected_order_id = tkinter.simpledialog.askinteger("Select Order", f"Select the Order ID to approve:\n{order_ID}")

        # If the user clicked "Cancel" or closed the dialog, exit the function
        if selected_order_id is None:
            return

        # Find the selected order in the list of orders
        selected_order = None
        for order in orders:
            if order[0] == selected_order_id:
                selected_order = order
                break

        # If the selected order doesn't exist, show an error message and exit the function
        if selected_order is None:
            tkinter.messagebox.showerror("Invalid Order", f"The order with ID {selected_order_id} does not exist!")
            return

        # Get data from the selected order
        order_ID = selected_order[0]
        item_ID = selected_order[1]
        item_name = selected_order[2]
        item_quantity = selected_order[3]
        vendor_name = selected_order[4]

        # Perform database update
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE orders SET approved=?, received=? WHERE order_ID=?", (True, False, order_ID))
        cursor.execute("UPDATE inventory SET qoo=qoo+? WHERE item_ID=?", (item_quantity, item_ID))
        connection.commit()
        connection.close()

        tkinter.messagebox.showinfo("Success", "Order approved successfully!")

    #Receive orders:
    def receive_order(self):
        # Check if user is authorized to receive orders
        user_level = self.get_user_level(username.get())
        if user_level < 2:
            tkinter.messagebox.showerror("Unauthorized", "You are not authorized to receive orders!")
            return

        # Get list of orders to receive
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE approved IS 1 AND received IS 0")
        orders = cursor.fetchall()
        connection.close()

        # Create a list of order IDs to display to the user
        #order_ids = [order[0] for order in orders]

        # Create a list of order details to display to the user
        order_ID = []
        for order in orders:
            order_ID.append(f"Order ID: {order[0]}, Item ID: {order[1]}, Item Name: {order[2]}, Item Quantity: {order[3]}, Vendor Name: {order[4]}")

        # Ask the user to select an order to receive
        selected_order_id = tkinter.simpledialog.askinteger("Select Order", f"Select an Order ID to receive:\n{order_ID}")

        # If the user clicked "Cancel" or closed the dialog, exit the function
        if selected_order_id is None:
            return

        # Find the selected order in the list of orders
        selected_order = None
        for order in orders:
            if order[0] == selected_order_id:
                selected_order = order
                break

        # If the selected order doesn't exist, show an error message and exit the function
        if selected_order is None:
            tkinter.messagebox.showerror("Invalid Order", f"The order with ID {selected_order_id} does not exist!")
            return

        # Get data from the selected order
        order_ID = selected_order[0]
        item_ID = selected_order[1]
        item_name = selected_order[2]
        item_quantity = selected_order[3]
        vendor_name = selected_order[4]

        # Check if there is enough quantity of item in stock to receive the order
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("SELECT item_quantity FROM inventory WHERE item_ID=?", (item_ID,))
        result = cursor.fetchone()
        connection.close()

        # If item_ID exists in the inventory table, update the item_quantity and qoo columns
        if result is not None:
            connection = sqlite3.connect("inventory.db")
            cursor = connection.cursor()
            cursor.execute("UPDATE inventory SET item_quantity=item_quantity+?, qoo=qoo-? WHERE item_ID=?", (item_quantity, item_quantity, item_ID))
            cursor.execute("UPDATE orders SET received=? WHERE order_ID=?", (True, order_ID))
            connection.commit()
            connection.close()
        # If item_ID does not exist in the inventory table, add a new entry
        else:
            connection = sqlite3.connect("inventory.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO inventory (item_ID, item_name, item_quantity, qoo, vendor_name) VALUES (?, ?, ?, ?, ?)", (item_ID, item_name, item_quantity, '0', vendor_name))
            cursor.execute("UPDATE orders SET received=? WHERE order_ID=?", (True, order_ID))
            connection.commit()
            connection.close()

        # Show a success message to the user
        tkinter.messagebox.showinfo("Order Received", f"The order with ID {order_ID} has been received and added to the inventory!")

    #Get user level for approve and receive order functions:
    def get_user_level(self, username):
        # Get user level from the database
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("SELECT user_level FROM login WHERE username=?", (str(username),))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else 0

# Author: Cody Foerster
# Added: 3/9/2023
# Description: UserPage class, functions, and buttons.
# Allows the changing of user levels and 
# deletion of users
class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id
        
        # title
        title = Label(self, text="User Management", font=(title_font, 50), fg=title_color)
        title.grid(row=0, column=0, columnspan=4)

        # treeview to display users
        tree = ttk.Treeview(self, columns=('Username', 'User Level'))
        tree.heading('Username', text='Username')
        tree.heading('User Level', text='User Level')
        tree.grid(row=1, column=0, columnspan=4)

        '''# populate the treeview with data from the database
        connection = sqlite3.connect("inventory.db")
        cursor = connection.execute('SELECT username, user_level FROM login')
        for row in cursor:
            tree.insert('', 0, text='', values=(row[0], row[1]))
        connection.close()'''

        # populate the treeview with data from the database
        def populate_treeview():
            tree.delete(*tree.get_children())
            connection = sqlite3.connect("inventory.db")
            cursor = connection.execute('SELECT username, user_level FROM login')
            for row in cursor:
                tree.insert('', 0, text='', values=(row[0], row[1]))
            connection.close()

        populate_treeview()

        # refresh users button
        refresh_button = Button(self, text="Refresh Users", command=populate_treeview)
        refresh_button.grid(row=2, column=3)

        # user level label and combobox
        user_level_label = Label(self, text="Select User Level:").grid(row=2, column=0)
        user_levels = ['1', '2', '3']
        user_level_combo = ttk.Combobox(self, values=user_levels)
        user_level_combo.grid(row=2, column=1)

        # change user level button
        change_button = Button(self, text="Change User Level", command=lambda: update_user_level())
        change_button.grid(row=2, column=2)

        # delete user label and entry box
        delete_label = Label(self, text="Enter Username to Delete:").grid(row=3, column=0)
        delete_entry = Entry(self)
        delete_entry.grid(row=3, column=1)

        # delete user button
        delete_button = Button(self, text="Delete User", command=lambda: delete_user())
        delete_button.grid(row=3, column=2)

        # user level guide
        guide_label = Label(self, text="User Level Guide:").grid(row=4, column=0, sticky=W)
        employee_label = Label(self, text="1 - Employee", font=("Arial", 12)).grid(row=5, column=0, sticky=W)
        manager_label = Label(self, text="2 - Manager", font=("Arial", 12)).grid(row=6, column=0, sticky=W)
        ceo_label = Label(self, text="3 - CEO", font=("Arial", 12)).grid(row=7, column=0, sticky=W)

        def update_user_level():
            # get selected username from treeview
            selected_item = tree.focus()
            if selected_item:
                selected_username = tree.item(selected_item)['values'][0]
            else:
                tkinter.messagebox.showerror("Error", "Please select a user from the list.")

            # get selected user level from combobox
            selected_user_level = user_level_combo.get()

            # update user level in database
            connection = sqlite3.connect("inventory.db")
            connection.execute('UPDATE login SET user_level=? WHERE username=?', (selected_user_level, selected_username))
            connection.commit()
            connection.close()

            # update treeview with new user level
            tree.item(selected_item, values=(selected_username, selected_user_level))

        def delete_user():
            # get username to delete from entry box
            username = delete_entry.get()

            # confirm deletion with user
            confirm_delete = tkinter.messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete user {username}?")

            if confirm_delete:
                # delete user from database
                connection = sqlite3.connect("inventory.db")
                connection.execute('DELETE FROM login WHERE username=?', (username,))
                connection.commit()
                connection.close()

                # remove user from treeview
                for child in tree.get_children():
                    if tree.item(child)['values'][0] == username:
                        tree.delete(child)

                tkinter.messagebox.showinfo("Success", f"User {username} has been deleted.")


#initialize database
connection = sqlite3.connect("inventory.db")
print("Database initialized")

#employee table
connection.execute('''
    CREATE TABLE IF NOT EXISTS login (
        employee_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        user_level INTEGER NOT NULL)
                   ''')
print("Employee table initialized")

#orders table
connection.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        item_ID TEXT NOT NULL,
        item_name TEXT NOT NULL,
        item_quantity INTEGER NOT NULL,
        vendor_name TEXT NOT NULL,
        approved BOOL NOT NULL,
        received BOOL NOT NULL)
                ''')
print("Orders Table Initialized")

#inventory table
connection.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        item_ID TEXT NOT NULL,
        item_name TEXT NOT NULL,
        item_quantity INTEGER NOT NULL,
        vendor_name TEXT NOT NULL, 
        qoo INTEGER NOT NULL)
                ''')
print("Inventory Table Initialized")

if __name__ == '__main__':
    root = Mainframe()
        
    #setting screen title
    root.title("Inventory System")
    #setting height and width of screen 
    root.geometry("700x500")
    
    root.mainloop()
