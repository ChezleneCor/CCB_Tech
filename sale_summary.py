from tkinter import ttk
import tkinter as tk
import sqlite3
import total_inventory



class Sale_Summary:
    
    Total_Inventory.connect()

    def connect():
            conn = sqlite3.connect('sale_summary.db')
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS sale_summary(item_ID text, item_name text, total_quantiy integer, sold_today integer, vendor_name text)")
            conn.commit()
            conn.close()
            
    def insert(item_ID, item_name, total_quantity, vendor_name):
            conn = sqlite3.connect('sale_summary.db')
            cur = conn.cursor()
            cur.execute("""INSERT INTO sale_summary(item_ID, item_name, total_quantiy,sold_today, vendor_name)
                         VALUES (?,?,?,?)
                      """, (item_ID, item_name, total_quantity, sold_today, vendor_name))
            conn.commit()
            conn.close()
            
    def display():
            conn = sqlite3.connect('sale_summary.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM sale_summary ORDER BY ITEM_NAME")
            rows = cur.fetchall()    
            for row in rows:
                print(row) 
            conn.close()
        
    #connected to Tkinter setting
    def view():
            conn = sqlite3.connect('sale_summary.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM sale_summary ORDER BY ITEM_NAME")
            rows = cur.fetchall()    
            for row in rows:
                print(row) 
                tree_s.insert("", tk.END, values=row)
            conn.close()
            
    def search_item(item_name):
            conn = sqlite3.connect('sale_summary.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM sale_summary where item_name = ?",(item_name,))
            rows = cur.fetchall() 
            for row in rows:
                print(row) 
            conn.close()
            
    def search_sold_item(sold_today):
            conn = sqlite3.connect('sale_summary.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM sale_summary where sold_today = ?",(sold_today,))
            rows = cur.fetchall() 
            for row in rows:
                print(row) 
            conn.close()
            
    def search_vendor(vendor_name):
            conn = sqlite3.connect('sale_summary.db')
            cur = conn.cursor()
            cur.execute("SELECT * FROM sale_summary where vendor_name = ?",(vendor_name,))
            rows = cur.fetchall() 
            for row in rows:
                print(row) 
            conn.close()

        
# connect to the database

#table setting in tkinter

Total_Inventory.connect()

root_s = tk.Tk()
tree_s = ttk.Treeview(root_s, column=("c1", "c2", "c3", "c4"), show='headings')

tree_s.column("#1", anchor=tk.CENTER)
tree_s.heading("#1", text="Item ID")

tree_s.column("#2", anchor=tk.CENTER)
tree_s.heading("#2", text="Item Name")

tree_s.column("#3", anchor=tk.CENTER)
tree_s.heading("#3", text="Total Quantity")

tree_s.column("#4", anchor=tk.CENTER)
tree_s.heading("#4", text="Vendor Name")


tree_s.pack()
button2 = tk.Button(text="Display sale data", command=Sale_Summary.view)
button2.pack(pady=10)

root.mainloop()
