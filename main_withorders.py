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
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        container = tk.Frame()
        container.grid(row=0, column=0, sticky="nesw")
        self.id = tk.StringVar()
        #self.id.set = "CCB Tech Inventory System"
        
        self.carousel = {}
        
        for page in (LoginPage, MainPage , InventoryPage , OrderPage):
            page_name = page.__name__
            if page == OrderPage:
                frame = page(parent=container, controller=self, username=username)
            else:
                frame = page(parent=container , controller=self)
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
        global user_level
        
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
        new_user_btn = Checkbutton(self, variable=newUser, text="New User", onvalue="Yes").grid(row=2, column=1)
        
        #User_level
        user_level = IntVar()

        #Login button
        loginButton = Button(self, text="Login", command=lambda: submit_login()).grid(row=4, column=0)
        
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
                    controller.page_front('MainPage')
                    
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
        
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id
        
        go_inventory = Button(self, text="Review Inventory" , command= lambda: controller.page_front("InventoryPage"))
        go_order = Button(self, text="Orders Menu" , command= lambda: controller.page_front("OrderPage"))
        
        go_inventory.grid(row=0, column=0)
        go_order.grid(row=1, column=0)

class InventoryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.id = controller.id
        
        title = Label (self, text= "Inventory Page")
        title.grid(row=0, column=0)
              
# Author: Cody Foerster
# Added: 3/3/2023
# Description:  OrderPage functions and buttons
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

        title = Label (self, text= "Order Page")
        title.grid(row=0, column=0)

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
        save_button.grid(row=5, column=0, columnspan=2)

        #Review orders button:
        review_orders_button = Button(self, text="Review Orders", command=self.review_orders)
        review_orders_button.grid(row=6, column=0, columnspan=2)

        #Search by item button:
        search_item_button = Button(self, text="Search by Item Name", command=self.search_by_item)
        search_item_button.grid(row=7, column=0, columnspan=2)

        #Search by vendor button:
        search_vendor_button = Button(self, text="Search by Vendor Name", command=self.search_by_vendor)
        search_vendor_button.grid(row=8, column=0, columnspan=2)

        #Approve Orders button:
        approve_orders_button = Button(self, text="Approve Orders", command=lambda: self.approve_order())
        approve_orders_button.grid(row=9, column=0, columnspan=2)

        #Receive Orders button:
        receive_orders_button = Button(self, text="Receive Orders", command=self.receive_order)
        receive_orders_button.grid(row=10, column=0, columnspan=2)

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
        item_ID_header = tk.Label(orders_frame, text="Item ID")
        item_ID_header.grid(row=0, column=0, padx=10, pady=10)

        item_name_header = tk.Label(orders_frame, text="Item Name")
        item_name_header.grid(row=0, column=1, padx=10, pady=10)

        item_quantity_header = tk.Label(orders_frame, text="Item Quantity")
        item_quantity_header.grid(row=0, column=2, padx=10, pady=10)

        vendor_name_header = tk.Label(orders_frame, text="Vendor Name")
        vendor_name_header.grid(row=0, column=3, padx=10, pady=10)

        approved_header = tk.Label(orders_frame, text="Approved")
        approved_header.grid(row=0, column=4, padx=10, pady=10)

        received_header = tk.Label(orders_frame, text="Received")
        received_header.grid(row=0, column=5, padx=10, pady=10)

        # Create Labels for each order and add them to the Frame
        for i, order in enumerate(orders):
            item_ID_label = tk.Label(orders_frame, text=order[0])
            item_ID_label.grid(row=i+1, column=0, padx=10, pady=10)

            item_name_label = tk.Label(orders_frame, text=order[1])
            item_name_label.grid(row=i+1, column=1, padx=10, pady=10)

            item_quantity_label = tk.Label(orders_frame, text=order[2])
            item_quantity_label.grid(row=i+1, column=2, padx=10, pady=10)

            vendor_name_label = tk.Label(orders_frame, text=order[3])
            vendor_name_label.grid(row=i+1, column=3, padx=10, pady=10)

            approved_label = tk.Label(orders_frame, text="Yes" if order[4] else "No")
            approved_label.grid(row=i+1, column=4, padx=10, pady=10)

            received_label = tk.Label(orders_frame, text="Yes" if order[5] else "No")
            received_label.grid(row=i+1, column=5, padx=10, pady=10)

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

        item_ID_header = tk.Label(search_results_window, text="Item ID")
        item_ID_header.grid(row=0, column=0, padx=10, pady=10)
    
        item_name_header = tk.Label(search_results_window, text="Item Name")
        item_name_header.grid(row=0, column=1, padx=10, pady=10)
    
        item_quantity_header = tk.Label(search_results_window, text="Item Quantity")
        item_quantity_header.grid(row=0, column=2, padx=10, pady=10)
    
        vendor_name_header = tk.Label(search_results_window, text="Vendor Name")
        vendor_name_header.grid(row=0, column=3, padx=10, pady=10)
    
        approved_header = tk.Label(search_results_window, text="Approved")
        approved_header.grid(row=0, column=4, padx=10, pady=10)
    
        received_header = tk.Label(search_results_window, text="Received")
        received_header.grid(row=0, column=5, padx=10, pady=10)

        for i, order in enumerate(orders):
            item_ID_label = tk.Label(search_results_window, text=order[0])
            item_ID_label.grid(row=i+1, column=0, padx=10, pady=10)

            item_name_label = tk.Label(search_results_window, text=order[1])
            item_name_label.grid(row=i+1, column=1, padx=10, pady=10)

            item_quantity_label = tk.Label(search_results_window, text=order[2])
            item_quantity_label.grid(row=i+1, column=2, padx=10, pady=10)

            vendor_name_label = tk.Label(search_results_window, text=order[3])
            vendor_name_label.grid(row=i+1, column=3, padx=10, pady=10)

            approved_label = tk.Label(search_results_window, text="Yes" if order[4] else "No")
            approved_label.grid(row=i+1, column=4, padx=10, pady=10)

            received_label = tk.Label(search_results_window, text="Yes" if order[5] else "No")
            received_label.grid(row=i+1, column=5, padx=10, pady=10)

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

        item_ID_header = tk.Label(search_results_window, text="Item ID")
        item_ID_header.grid(row=0, column=0, padx=10, pady=10)
    
        item_name_header = tk.Label(search_results_window, text="Item Name")
        item_name_header.grid(row=0, column=1, padx=10, pady=10)
    
        item_quantity_header = tk.Label(search_results_window, text="Item Quantity")
        item_quantity_header.grid(row=0, column=2, padx=10, pady=10)
    
        vendor_name_header = tk.Label(search_results_window, text="Vendor Name")
        vendor_name_header.grid(row=0, column=3, padx=10, pady=10)
    
        approved_header = tk.Label(search_results_window, text="Approved")
        approved_header.grid(row=0, column=4, padx=10, pady=10)
    
        received_header = tk.Label(search_results_window, text="Received")
        received_header.grid(row=0, column=5, padx=10, pady=10)

        for i, order in enumerate(orders):
            item_ID_label = tk.Label(search_results_window, text=order[0])
            item_ID_label.grid(row=i+1, column=0, padx=10, pady=10)

            item_name_label = tk.Label(search_results_window, text=order[1])
            item_name_label.grid(row=i+1, column=1, padx=10, pady=10)

            item_quantity_label = tk.Label(search_results_window, text=order[2])
            item_quantity_label.grid(row=i+1, column=2, padx=10, pady=10)

            vendor_name_label = tk.Label(search_results_window, text=order[3])
            vendor_name_label.grid(row=i+1, column=3, padx=10, pady=10)

            approved_label = tk.Label(search_results_window, text="Yes" if order[4] else "No")
            approved_label.grid(row=i+1, column=4, padx=10, pady=10)

            received_label = tk.Label(search_results_window, text="Yes" if order[5] else "No")
            received_label.grid(row=i+1, column=5, padx=10, pady=10)

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
        cursor.execute("SELECT qoh FROM inventory WHERE item_ID=?", (item_ID,))
        result = cursor.fetchone()
        connection.close()

        # Perform database update to receive the order
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE orders SET received=? WHERE order_ID=?", (True, order_ID))
        cursor.execute("UPDATE inventory SET qoh=qoh+?, qoo=qoo-? WHERE item_ID=?", (item_quantity, item_quantity, item_ID))
        cursor.execute("DELETE FROM orders WHERE order_ID=?", (order_ID,))
        connection.commit()
        connection.close()

        tkinter.messagebox.showinfo("Success", "Order received successfully!")

    #Get user level for approve and receive order functions:
    def get_user_level(self, username):
        # Get user level from the database
        connection = sqlite3.connect("inventory.db")
        cursor = connection.cursor()
        cursor.execute("SELECT user_level FROM login WHERE username=?", (str(username),))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else 0

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
        item_description TEXT NOT NULL,
        qoh INTEGER NOT NULL,
        qoo INTEGER NOT NULL,
        min INTEGER NOT NULL,
        max INTEGER NOT NULL)
                ''')
print("Inventory Table Initialized")

if __name__ == '__main__':
    root = Mainframe()
    
    #setting screen title
    root.title("Test")
    #setting height and width of screen 
    root.geometry("700x500") 

    root.mainloop()