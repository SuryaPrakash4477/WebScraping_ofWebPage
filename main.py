# This Library will get the source code for below webpage url and store it in python as a string
import requests 

#This library will extract only particular information from all that source code
import selectorlib
import smtplib, ssl
import os
import time
import sqlite3
# from datetime import datetime

"INSERT INTO events VALUES('Tigers', 'Tiger city', '2088.10.14')"
"SELECT *FROM events WHERE city='Monkey city'"
"DELETE FROM events WHERE band='Tigers'"

URL = "https://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event: #Class is made of functions
    def scrape(self, url): #Now the functions are called as method in this class
        """Scrape the page source from the URL"""
        response = requests.get(url, headers = HEADERS)
        source = response.text

        return source


    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("D:\WebScraping_ofWebPage\extract.yml")
        value = extractor.extract(source)["tours"] # This part return dictionary

        return value

class Email:
    def send(self, message):
        host = "smtp.gmail.com"
        port = 465

        username = "suryaprakashsharma453@gmail.com"
        password = "fctb xbkz rdyu jwqz"

        receiver = "suryaprakashsharma453@gmail.com"
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)

        print("Email has been sent")


class Database:
    # Self is like a special variable and it is used as a middleman to access the variable
    # To give argument to the class is done by providing a parameter in init method
    def __init__(self, database_path):
        #Establishing a connection
        self.connection = sqlite3.connect(database_path) #Now connecton is the property of self argument

    def store(self, extracted):
        # # now = datetime.now().strftime("%y-%m- %d-%H:%M:%S")
        # with open("data.txt", "a") as file:
        #     # line = f"{now},{extracted}\n"
        #     file.write(extracted + "\n")
        if extracted is not None: 
            row = extracted.split(",")
            row = [item.strip() for item in row]
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
            self.connection.commit()

    def read(self, extracted):

        # with open("data.txt", "rb") as file:
        #     return file.read()
        if extracted is not None:
            row = extracted.split(",")
            row = [item.strip() for item in row]
            band, city, date = row
            cursor = self.connection.cursor()
            cursor.execute("SELECT *FROM events WHERE band=? AND city=? AND date=?", 
                          (band,city,date))
            rows = cursor.fetchall()
            return rows
        else:
            return []

      
        


if  __name__ == '__main__':
    while True:
        event = Event()
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)

        # content = read(extracted)
        if extracted and extracted != "No upcoming tours":
            db = Database(database_path = "data.db")
            row = db.read(extracted)
            # if extracted not in content:
            if not row:
                db.store(extracted)
                email = Email()
                email.send(message = "Hey, New event was Found!")
        time.sleep(2)