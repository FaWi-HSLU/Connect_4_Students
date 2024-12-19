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
        

        # TODO: Implementieren Sie den Code hier

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
        

        sql_command = f"SELECT itemID,vendorID,orderNr,price FROM orderLookup WHERE itemID == {item_id}"
        self.cursor.execute(sql_command)

        print("""+----------+-------------+------------------+---------------+
 ItemID    | vendorID    | orderNr          | Preis [CHF]   |
+----------+-------------+------------------+---------------+""")

        for itemID,vendorID,orderNr,price in self.cursor:
            print(f"""| {str(itemID):<8} | {str(vendorID):<11} |  {str(orderNr):<16}| {str(price):<13} |
+----------+-------------+------------------+---------------+""")

    def scan_item(self):
        sub_menu = """+----------+-------------------------------------------------+
| 4        | Artikel scannen (nach Bestellnummer)            |
+----------+-------------------------------------------------+"""
        print(sub_menu)
        order_nr = input("\nGeben Sie die Bestellnummer ein: ")
        print(f"\nScanne Artikel mit Bestellnummer {order_nr}...")
        
        # search for article with this number
        sql_query = f"SELECT itemID,orderNr FROM orderLookup where orderNr == {order_nr}"
        self.cursor.execute(sql_query)

        item_ids = []
        for itemID,orderNr in self.cursor:
            item_ids.append(itemID)
        
        if len(item_ids)>1:
            print(f"Found Multiple Element with the Same orderNr - select correct ItemID to add to inventory")
        elif len(item_ids) ==1:
            sql_query = f"UPDATE inventory SET units = units + ? WHERE itemID = ?;"
            try:
                self.cursor.execute(sql_query, (1,itemID))
            except:
                self.db.rollback()
            else:
                self.db.commit()
        else:
            print(f"No Item found with this orderNr")

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
    interface = DatabaseInterface("inventory_SW14_2.db")
    interface.run()
