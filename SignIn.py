from Narrator import Narrator
from DB_Connection import db
import hashlib
print("*" + "--" * 25 + "*")
Narrator("Welcome To Fawad Petrol Pump Management System")
print("*" + "~~" * 25 + "*")
Narrator("Please Login To Your Account")
while True:
    Narrator(" Enter Your User Name : ")
    username = input().lower()
    Narrator(" Enter Your Password : ")
    password = input().lower()
    password = "%546" + hashlib.md5(password.encode('utf-8')).hexdigest() + "546%"
    print("*" + "~~" * 20 + "*")
    f = db.cursor()
    f.execute("SELECT * FROM `users` WHERE username='" + username + "' AND password='" + password + "'")
    f.fetchall()
    if f.rowcount > 0:
        Narrator("Login Successful")
        print("*" + "~~" * 20 + "*")
        # noinspection PyUnresolvedReferences
        import Welcome
        break
    else:
        Narrator("Invalid UserName Or Password Try Again")
        print("*" + "~~" * 20 + "*")
