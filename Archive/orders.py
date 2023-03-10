#Orders class definition
class orders:
    #Minimum item quantity on orders
    MIN_QUANTITY = 0

    #Orders Constructor
    def __init__(self, item_ID, item_name, item_quantity, vendor_name):
        self.item_ID = item_ID
        self.item_name = item_name
        if item_quantity <= self.MIN_QUANTITY:
            raise ValueError("Quantity too low. Quantity to order must be at least 1.")
        else:
            self.item_quantity = item_quantity
        self.vendor_name = vendor_name

    #Check if item_id is equal to another item_id
    def __eq__(self, other):
        return True if self.item_ID == other.item_ID else False

    #Print out order:
    def __str__(self):
        return f"""
        Item Order:
            Item ID: {self.item_ID}
            Item Name: {self.item_name}
            Item Quantity: {self.item_quantity}
            Vendor Name: {self.vendor_name}
        """



import sqlite3

class Orders:
    def __init__(self, item_ID, item_name, item_quantity, vendor_name):
        self.item_ID = item_ID
        self.item_name = item_name
        self.item_quantity = item_quantity
        self.vendor_name = vendor_name

    def save_to_database(self):
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS orders
                     (item_ID text, item_name text, item_quantity integer, vendor_name text)
                  """)
        c.execute("""INSERT INTO orders (item_ID, item_name, item_quantity, vendor_name)
                     VALUES (?,?,?,?)
                  """, (self.item_ID, self.item_name, self.item_quantity, self.vendor_name))
        conn.commit()
        conn.close()
