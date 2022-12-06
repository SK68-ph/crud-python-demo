import time
import os
import sys
import mysql.connector
from tabulate import tabulate
from mysql.connector import Error


class Database:
    def __init__(self):
        try:
            self.__db = mysql.connector.connect(host='localhost',
                                                 database='productsdb',
                                                 user='root',
                                                 password='')
            self.__cursor = self.__db.cursor(named_tuple=True)
            self.__cursor.execute("CREATE TABLE IF NOT EXISTS products (Id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,Name varchar(25) NOT NULL,Price float NOT NULL)")
            self.__db.commit()
        except Error as e:
            print("Failed to initialize database.", e)
            time.sleep(3)
            quit()

    def close(self):
        if self.isDbConnected():
            self.__cursor.close()
            self.__db.close()

    def isDbConnected(self):
        if self.__db.is_connected():
            return True
        else:
            print("Database connection error.")
            time.sleep(3)
            quit()

    def addProduct(self, name, price):
        if self.isDbConnected():
            self.__cursor.execute(
                f"insert into products SET Name='{name}',Price={price}")
            self.__db.commit()

    def getProducts(self):
        if self.isDbConnected():
            self.__cursor.execute("select * from products")
            data = []
            for row in self.__cursor:
                data.append(row)
            twPrint(tabulate(data, headers=[
                    "ID", "Product Name", "Product Price"]), 0)

    def removeProduct(self, id):
        if self.isDbConnected():
            self.__cursor.execute(f"DELETE FROM products WHERE id='{id}'")
            self.__db.commit()

    def editProduct(self, id, name, price):
        if self.isDbConnected():
            self.__cursor.execute(
                f"update products SET Name='{name}',Price={price} WHERE id={id}")
            self.__db.commit()

# Typewriter effect
def twPrint(text, speed=0.001):
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(speed)

db = Database()
# Main Menu
while True:
    os.system("cls")
    twPrint("============== Anteiku Coffee Shop ============== \n")
    twPrint("List of available products\n\n")

    db.getProducts()

    twPrint("\n\n1. Add product \n")
    twPrint("2. Delete product \n")
    twPrint("3. Edit product \n")
    twPrint("0. Exit \n")

    try:
        choice = int(input("Enter Selection :"))
        if choice == 1:
            name = str(input("Enter product name :"))
            price = float(input("Enter product price :"))
            db.addProduct(name, price)
            twPrint("Done.", 0.025)
            time.sleep(1)

        elif choice == 2:
            id = int(input("Enter product id :"))
            db.removeProduct(id)
            twPrint("Done.", 0.025)
            time.sleep(1)

        elif choice == 3:
            id = int(input("Enter product id :"))
            name = str(input("Enter new product name :"))
            price = float(input("Enter new product price :"))
            db.editProduct(id, name, price)
            twPrint("Done.", 0.025)
            time.sleep(1)

        elif choice == 0:
            db.close()
            print("Exiting.")
            time.sleep(3)
            break

    except ValueError as e:
        print("Invalid Input.", e)
        time.sleep(3)