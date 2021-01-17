from Narrator import Narrator

try:
    import mysql.connector as mysql

    Database_Name = "petrol_pump"

    chk_db = mysql.connect(
        host="127.0.0.1",
        user="root",
        password=""
    )
    f = chk_db.cursor()
    f.execute("SHOW DATABASES")
    DB = f.fetchall()
    if (Database_Name,) in DB:
        pass
    else:
        f.execute("CREATE DATABASE " + Database_Name)
    Database = Database_Name

    db = mysql.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database=Database
    )


except:
    Narrator("\n\n\n Sorry! Your DataBase Server is Down! Please Run Your Database Server")
