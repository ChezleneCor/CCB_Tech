from tkinter import ttk
import tkinter as tk
import sqlite3
from tkinter import *

class Total_Inventory:
    
    def __init__(self, item_ID, item_name, total_quantity, sold_today, vendor_name):
        self.item_ID = item_ID
        self.item_name = item_name
        self.total_quantity = total_quantity
        self.vendor_name = vendor_name

    def connect():
            conn = sqlite3.connect('total_inventory.db')
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS total_inventory(item_ID text, item_name text, total_quantiy integer, vendor_name text)")
            conn.commit()
            conn.close()
            
    def display():
            conn = sqlite3.connect('total_inventory.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM total_inventory ORDER BY ITEM_NAME")
            rows = cur.fetchall()    
            for row in rows:
                print(row) 
            conn.close()
        
    #connected to Tkinter setting
    def view():
            conn = sqlite3.connect('total_inventory.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM total_inventory ORDER BY ITEM_NAME")
            rows = cur.fetchall()    
            for row in rows:
                print(row) 
                #tree.insert("", tk.END, values=row)
            conn.close()
            
    def search_item(item_name):
            conn = sqlite3.connect('total_inventory.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM total_inventory where item_name = ?",(item_name,))
            rows = cur.fetchall() 
            for row in rows:
                print(row) 
            conn.close()
            
    def search_vendor(vendor_name):
            conn = sqlite3.connect('total_inventory.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM total_inventory where vendor_name = ?",(vendor_name,))
            rows = cur.fetchall() 
            for row in rows:
                print(row) 
            conn.close()
        
    def insert(item_ID, item_name, total_quantity, vendor_name):
            conn = sqlite3.connect('total_inventory.db')
            cur = conn.cursor()
            cur.execute("""INSERT INTO total_inventory(item_ID, item_name, total_quantiy,vendor_name)
                         VALUES (?,?,?,?)
                      """, (item_ID, item_name, total_quantity, vendor_name))
            conn.commit()
            conn.close()
            
    def delete_all():
        
        x = input("Are you sure you want to delete all inventory data? Press y to confirm or press any other key to go back")
        if (x=='y'):
            conn = sqlite3.connect('total_inventory.db')
            cur = conn.cursor()
            cur.execute('DELETE FROM total_inventory;',)
            print("All inventory data deleted")
            conn.commit()
            conn.close()
        else:
            print("Incomplete confirmation inventory data not deleted!")

    def delete_item(item_ID):

            conn = sqlite3.connect('total_inventory.db')
            cur = conn.cursor()
            cur.execute("DELETE FROM total_inventory where item_ID = ?",(item_ID,))
            conn.commit()
            conn.close()
            
    def delete_vendor(vendor_name):

            conn = sqlite3.connect('total_inventory.db')
            cur = conn.cursor()
            cur.execute("DELETE FROM total_inventory where vendor_name = ?",(vendor_name,))
            conn.commit()
            conn.close()
