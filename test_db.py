import MySQLdb

try:
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="paryul",  
        db="webdb"
    )
    print("Successfully connected to the database!")
    db.close()
except Exception as e:
    print(f"Connection failed: {e}")