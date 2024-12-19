import sqlite3

class DatabaseInterface:
    def __init__(self, db_path:str):
        self.db = sqlite3.connect(db_path)
        self.cursor = self.db.cursor()

        self.main_menu = """+----------+-------------------------------------------------+
| Auswahl  | Beschreibung                                    |
+----------+-------------------------------------------------+
| 1        | Lieferanten auflisten                           |
+----------+-------------------------------------------------+
| 2        | Artikel auflisten (nach Name)                   |
+----------+-------------------------------------------------+
| 3        | Bestellmöglichkeiten abrufen (nach ItemID)      |
+----------+-------------------------------------------------+
| 4        | Artikel scannen (nach Bestellnummer)            |
+----------+-------------------------------------------------+
| 5        | Beenden                                         |
+----------+-------------------------------------------------+
"""

    def display_menu(self):
        print(self.main_menu)

    def list_vendors(self):

        sql_command = "SELECT vendorID,name,url FROM vendors"
        self.cursor.execute(sql_command)

        print("""+-------------+-------------------------+------------------------------+
| vendorID    | name                    | url                          |
+-------------+-------------------------+------------------------------+""")
        for vendorID,name,url in self.cursor:
            print(f"""| {str(vendorID):<12}| {name:<24}| {url:<29}|
+-------------+-------------------------+------------------------------+""")
        

    def list_items(self):
        sub_menu = """+----------+-------------------------------------------------+
| 2        | Artikel auflisten (nach Name)                   |
+----------+-------------------------------------------------+"""
        print(sub_menu)
        item_name = input("\nGeben Sie den Artikelnamen ein: ")

        # get all items first
        sql_command = f"SELECT itemID,name,category,units FROM inventory"
        self.cursor.execute(sql_command)

        print("""+----------+---------------------+------------------+-----------------------+
| ID       | Name                | Category         | Units                 |
+----------+---------------------+------------------+-----------------------+""")
              
        for id,name,category,units in self.cursor:
            if item_name.upper() in name.upper():
                print(f"""| {str(id):<9}| {name:<19} | {category:<16} | {str(units):<22}|
+----------+---------------------+------------------+-----------------------+""")

    def get_orders(self):
        sub_menu = """+----------+-------------------------------------------------+
| 3        | Bestellmöglichkeiten abrufen (nach ItemID)      |
+----------+-------------------------------------------------+"""
        print(sub_menu)
        item_id = input("\nGeben Sie die ItemID ein: ")
        

        sql_command = f"SELECT itemID,orderNr,price FROM orderLookup WHERE itemID == {item_id}"
        
        self.cursor.execute(sql_command)
        print("""+----------+-------------+----------------------+------------+
| 3        | itemID      | orderNr              | price CHF  |
+----------+-------------+----------------------+------------+""")
        for itemID,orderNr,price in self.cursor:
            print(f"""|          | {itemID:<11} | {orderNr:<20} | {price:<10} |""")

        print("""+----------+-------------+----------------------+------------+""")

    def scan_item(self):
        sub_menu = """+----------+-------------------------------------------------+
| 4        | Artikel scannen (nach Bestellnummer)            |
+----------+-------------------------------------------------+"""
        print(sub_menu)
        order_nr = input("\nGeben Sie die Bestellnummer ein: ")
        
        # itemID: ID des Bauteils (PK mit itemID)
        # vendorID: Lieferant des Bauteils (PK mit itemID)
        # orderNr: Spezifische Bestellnummer vom Bauteil beim Lieferanten
        # price: Pr
        sql_command = """SELECT itemID,orderNr,price FROM orderLookup"""
        
        self.cursor.execute(sql_command)

        orders = {}

        for itemID,orderNr,price in self.cursor:
            
            orders[orderNr] = {}
            orders[orderNr]["itemID"] = itemID
            orders[orderNr]["price"] = price

        for orderNr in orders:
            if str(orderNr) == str(order_nr):
                second_select = f"""SELECT itemID,name from inventory WHERE itemID == {itemID}"""
                self.cursor.execute(second_select)

                for itemID,name in self.cursor:
                    answer = input(f"Found item {name} with given orderNr {orderNr} - Do you want to add this? [Y/N]")

                    if answer.upper() == "Y":
                        
                        try:
                            print(f"Adding 1 to {name} with id {itemID}")
                            update_query = f"""UPDATE inventory SET units = units + 1 WHERE itemID = {itemID};"""
                            self.cursor.execute(update_query)
                        except:
                            self.db.rollback()
                        else:
                            self.db.commit()
                            break
        print(f"New Inventory:")

        sql_3 = f"""SELECT itemID,name,units FROM inventory WHERE itemID = {itemID}"""
        
        self.cursor.execute(sql_3)

        print("""+----------+---------------------+-----------------------+
| ID       | Name                | Units                 |
+----------+---------------------+-----------------------+""")
        for itemID,name,units in self.cursor:
             print(f"""| {itemID:<8} | {name:<18} | {units:<21} |""")

        print("""+----------+---------------------+-----------------------+""")
        

    def end_menu(self):
        print("""+----------+-------------------------------------------------+
|  5       | Programm beendet. Auf Wiedersehen!              |
+----------+-------------------------------------------------+""")


    def run(self):
        while True:
            self.display_menu()
            choice = input("\nWählen Sie eine Option (1-5): ")

            if choice == "1":
                self.list_vendors()
            elif choice == "2":
                self.list_items()
            elif choice == "3":
                self.get_orders()
            elif choice == "4":
                self.scan_item()
            elif choice == "5":
                self.end_menu()
                break
            else:
                print("\nUngültige Eingabe. Bitte wählen Sie eine gültige Option (1-5).\n")
            
            # warte bis enter gedrückt zum weitermachen
            input("Drücker ENTER um zurück zum Hauptmenu zu gelangen")

# Hauptprogramm starten
if __name__ == "__main__":
    print("Willkommen im Datenbank-Interface! Bitte wählen Sie eine Option:")
    interface = DatabaseInterface("inventory_SW14.db")
    interface.run()
