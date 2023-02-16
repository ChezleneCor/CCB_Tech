from tkinter import *
import sqlite3

root = Tk()
root.title('Testing')

#Databases

#Create a database or connect to one
connection = sqlite3.connect("inventory.db")

#Create cursor to do things in the database
cursor = connection.cursor()

#Create Tables
#Orders Table
cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
    item_ID text,
    item_name text,
    item_quantity integer,
    vendor_name text,
    vendor_ID text
    )""")

#Inventory Table
cursor.execute("""CREATE TABLE IF NOT EXISTS inventory (
    item_ID text,
    item_name text,
    item_description text,
    qoh int,
    qoo int,
    min int,
    max int
    )""")

#Login Table
cursor.execute("""CREATE TABLE IF NOT EXISTS login (
    username text,
    password text,
    user_level int
    )""")

#Create Submit Function for Database
def submit():
    #Connect to database
    connection = sqlite3.connect('inventory.db')
    #Create cursor
    cursor = connection.cursor()

    cursor.execute("INSERT INTO orders VALUES (:item_ID, :item_name, :item_quantity, :vendor_name, :vendor_ID)",
        {
            'item_ID' : item_ID.get(),
            'item_name' : item_name.get(),
            'item_quantity' : item_quantity.get(),
            'vendor_name' : vendor_name.get(),
            'vendor_ID' : vendor_ID.get()
        })


    #Commit Changes
    connection.commit()

    #Close Connection
    connection.close()

    #Clear the text boxes
    item_ID.delete(0, END)
    item_name.delete(0, END)
    item_quantity.delete(0, END)
    vendor_name.delete(0, END)
    vendor_ID.delete(0, END)

#Create Query Function
def review():
    #Connect to database
    connection = sqlite3.connect('inventory.db')
    #Create cursor
    cursor = connection.cursor()

    cursor.execute("SELECT oid, * FROM orders")
    orders = cursor.fetchall()
    #print(orders)

    #Loop through results
    print_orders = ''
    for order in orders:
        print_orders += str(order) + " "

    review_label = Label(root, text=print_orders)
    review_label.grid(row=7, column=0, columnspan=2,)

    #Commit Changes
    connection.commit()

    #Close Connection
    connection.close()
    

#Create texts boxes for order
item_ID = Entry(root, width=30)
item_ID.grid(row=0, column=1, padx=20)
item_name = Entry(root, width=30)
item_name.grid(row=1, column=1, padx=20)
item_quantity = Entry(root, width=30)
item_quantity.grid(row=2, column=1, padx=20)
vendor_name = Entry(root, width=30)
vendor_name.grid(row=3, column=1, padx=20)
vendor_ID = Entry(root, width=30)
vendor_ID.grid(row=4, column=1, padx=20)

#Create text box labels
item_ID_label = Label(root, text="Item ID")
item_ID_label.grid(row=0, column=0)
item_name_label = Label(root, text="Item Name")
item_name_label.grid(row=1, column=0)
item_quantity_label = Label(root, text="Item Quantity")
item_quantity_label.grid(row=2, column=0)
vendor_name_label = Label(root, text="Vendor Name")
vendor_name_label.grid(row=3, column=0)
vendor_ID_label = Label(root, text="Vendor ID")
vendor_ID_label.grid(row=4, column=0)

#Create Submit Button
submit_button = Button(root, text="Submit Order", command=submit)
submit_button.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#Create Query Button
query_button = Button(root, text="Review Orders", command=review)
query_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)

#Commit changes
connection.commit()

#Close connection
connection.close()

root.mainloop()