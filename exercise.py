import sqlite3

#Establishing a connection
connection = sqlite3.connect("data.db")
cursor = connection.cursor()

# Querying all data
cursor.execute("SELECT *FROM events WHERE band='Monkey'")
result = cursor.fetchall()

print(result)

# # Querying certain columns
# cursor.execute("SELECT band, date FROM events WHERE band='Monkey'")
# rows = cursor.fetchall()

# print(rows)


# #Inserting New rows
# new_rows = [('Cats', 'Cat City,', '2045.12.12'), 
#             ('Dogs', 'Dogs City', '2034.12.10')]
# cursor.executemany("INSERT INTO events VALUES (?,?,?)", new_rows)
# connection.commit()