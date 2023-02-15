#!/usr/bin/env python
# coding: utf-8

# In[1]:


from datetime import date


import sqlite3

#This will create a table to keep track of item sold daily
class Sale_Summary:
    def __init__(self, item_ID, sold_item, sold_quantity, date):
        self.item_ID = item_ID
        self.sold_item = sold_item
        self.sold_quantity = sold_quantiy
        self.date = date

    def save_to_sold_database(self):
        conn = sqlite3.connect('sale_summary.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS orders
                     (item_ID text, item_name text, sold_quantiy integer, date integer)
                  """)
        date = date.today()
        #input from when a customer buys a products
        input(item_ID)
        input(item_name)
        input(sold_quantity)
        c.execute("""INSERT INTO orders (item_ID, item_name, sold_quantiy, date)
                     VALUES (?,?,?,?)
                  """, (self.item_ID, item_name, self.sold_quantity, self.date))
        
        conn.commit()
        print(cursor.fetchall())
        conn.close()
        
#This will create a table to keep track of total items available        
class Total_Inventory:
    def __init__(self, item_ID, item_name, total_quantity, sold_today):
        self.item_ID = item_ID
        self.item_name= item_name
        self.total_quantity = total_quantity
        self.sold_today = sold_today
        
    def save_to_total_database(self):
        conn = sqlite3.connect('total_inventory.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS orders
                     (item_ID text, item_name text, total_quantiy integer, sold_today integer)
                  """)
        total_quantity = total_quantity + item_quantity - sold_quantity
        sold_today = sold_quantity
        c.execute("""INSERT INTO orders (item_ID, item_name, total_quantiy, sold_today)
                     VALUES (?,?,?,?)
                  """, (self.item_ID, item_name, total_quantity, sold_today))
        conn.commit()
        print(cursor.fetchall())
        conn.close()
        
        
#search total database for a particular item
def search_item(priority):
    cur = conn.cursor()
    cur.execute("SELECT * FROM item_ID WHERE priority=?", (priority,))

    rows = cur.fetchall()

    for row in rows:
        print(row)
    
    
search_id = 0
conn = create_connection('total_inventory.db')
with conn:
        search_id = input("Type the item id to look up the item")
        search_item(search_id)

