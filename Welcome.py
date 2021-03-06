from DB_Connection import db
from Narrator import Narrator
import datetime as T

y = T.datetime.now() - T.timedelta(days=1)
previous_date = y.strftime("%d/%b/%Y")
y = T.datetime.now()
today_date = y.strftime("%d/%b/%Y")
current_time = y.strftime("%I:%M:%S %p")
prc_updt = y.strftime("%d")
try:
    f = db.cursor()
    f.execute("SELECT * FROM `day_summary`,`users` WHERE date='" + previous_date + "'")
    fd = f.fetchall()
    for i in fd:
        date = i[1]
        ptrl_price = float(i[2])
        dsil_price = float(i[3])
        pris_ptrl_rdng_A = float(i[4])
        pris_ptrl_rdng_B = float(i[5])
        ptrl_stck = float(i[8])
        # Diesel
        pris_dsil_rdng_A = float(i[9])
        pris_dsil_rdng_B = float(i[10])
        dsil_stck = float(i[13])
        total_mnth_rs = float(i[18])
        name = str(i[20])
        email_address = i[21]
        pump_name = i[22]
    # *================================Developed by Fawad on 13 of Jan 2021(2 Days-11:09PM)===============================*
    print("*" + "--" * 35 + "*")
    Narrator("I am Showing You Recode Of Date : " + previous_date + " Please Fill Up The Following Fields CareFully Thank You ")
    print("*" + "--" * 35 + "*")

    if prc_updt == "16" or prc_updt == "16":
        while True:
            Narrator("Your Petrol Price is : " + str(ptrl_price) + " And Diesel Price Is : " + str(dsil_price))
            Narrator("Is It Change Press (Y Or N) :")
            price_update = input().upper()
            if price_update == "Y":
                Narrator("Enter Your New Petrol Price : ")
                ptrl_price_updt = float(input())
                Narrator("Enter Your New Diesel Price : ")
                dsil_price_updt = float(input())
                Narrator(f"Your New Petrol Price is {ptrl_price_updt} Rs/Ltr And Diesel Price is {dsil_price_updt} Rs/Ltr")
                print("*" + "~~" * 35 + "*")
                break
            elif price_update == "N":
                ptrl_price_updt = ptrl_price
                dsil_price_updt = dsil_price
                break
            else:
                Narrator("Invalid Key Try Again")
                print("*" + "~~" * 35 + "*")
    else:
        ptrl_price_updt = ptrl_price
        dsil_price_updt = dsil_price
    while True:
        Narrator("Do You Have New Fuel Stock (Y or N) :")
        cnfrm_stock = input().upper()
        if cnfrm_stock == "Y":
            print("*" + "~~" * 35 + "*")
            Narrator("Enter Your New Petrol Stock Your Previous Stock Is " + str(ptrl_stck) + " Litters")
            ptrl_stck_updt = float(input())
            ptrl_stck_updt += ptrl_stck
            Narrator("Enter Your New Diesel Stock Your Previous Stock Is " + str(dsil_stck) + " Litters")
            dsil_stck_updt = float(input())
            dsil_stck_updt += dsil_stck
            Narrator(f"Your New Petrol Stock is {ptrl_stck_updt} Litters And Diesel Stock is {dsil_stck_updt} Litters")
            print("*" + "~~" * 35 + "*")
            break
        elif cnfrm_stock == "N":
            ptrl_stck_updt = ptrl_stck
            dsil_stck_updt = dsil_stck
            print("*" + "~~" * 35 + "*")
            break
        else:
            Narrator("Invalid Key Try Again")
            print("*" + "~~" * 35 + "*")
    Narrator("Enter Your New Reading of Petrol Machine 'A' Your Previous Reading is: " + str(pris_ptrl_rdng_A))
    crnt_ptrl_rdng_A = float(input())
    print("*" + "~~" * 35 + "*")
    Narrator("Enter Your New Reading of Petrol Machine 'B' Your Previous Reading is: " + str(pris_ptrl_rdng_B))
    crnt_ptrl_rdng_B = float(input())
    print("*" + "~~" * 35 + "*")
    Narrator("Enter Your New Reading of Diesel Machine 'A' Your Previous Reading is: " + str(pris_dsil_rdng_A))
    crnt_dsil_rdng_A = float(input())
    print("*" + "~~" * 35 + "*")
    Narrator("Enter Your New Reading of Diesel Machine 'B' Your Previous Reading is: " + str(pris_dsil_rdng_B))
    crnt_dsil_rdng_B = float(input())
    print("*" + "~~" * 35 + "*")
    Narrator("Enter Your Today Total Expanses( ٹوٹل خرچہ ) :")
    total_expanses = float(input())
    print("*" + "~~" * 35 + "*")
    Narrator("Enter Your Today Total Cashback( ٹوٹل وصولی )  :")
    cashback = float(input())
    if cashback == 0:
        print("*" + "~~" * 35 + "*")
        cashback_name = ""
    else:
        Narrator("Enter Your Cashback Man Name(وصولی والےکانام) :")
        cashback_name = input().title()
        print("*" + "~~" * 35 + "*")
    Narrator("Enter Your Today Total Cash Out(ٹوٹل نقددیا )  :")
    cashout = float(input())
    if cashout == 0:
        print("*" + "~~" * 35 + "*")
        cashout_name = ""
    else:
        Narrator("Enter Your CashOut Man Name(نقددینےوالےکانام) :")
        cashout_name = input().title()
        print("*" + "~~" * 35 + "*")
    # *===========================================================================================================*
    Narrator("Please Wait System is in Process................")
    f.execute("SELECT * FROM `day_summary` WHERE date='" + today_date + "'")
    f.fetchall()
    if f.rowcount > 0:
        pass
    else:
        f.execute("INSERT INTO `day_summary` (date) VALUES ('" + today_date + "')")
        db.commit()
    import System
    obj = System.System()
    obj.update_DB()
    f.execute("CREATE TABLE IF NOT EXISTS `login_stats` (date VARCHAR(15),time VARCHAR(255),name VARCHAR(255))")
    f.execute("INSERT INTO `login_stats` (date,time,name) VALUES ('" + today_date + "','" + current_time + "','" + name + "')")
    db.commit()

except NameError:
    Narrator("Sorry You Don't Have Any Record At Date " + previous_date + " Thank You")
    print("*" + "~~" * 35 + "*")
except ValueError:
    Narrator("Sorry You Have Entered Invalid Value During Signup Or Missed Values \nPlease Change Your Database Name From DB_Connection To Create New Account Thank You")
    print("*" + "~~" * 35 + "*")
