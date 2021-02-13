from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Welcome import *
from Narrator import Narrator
from DB_Connection import db
import datetime as T
import pdfkit
import smtplib
import os

y = T.datetime.now()
today_date = y.strftime("%d/%b/%Y")
current_time = y.strftime("%I:%M:%S %p")

# Litters Sold Today
petrol_sold_A = crnt_ptrl_rdng_A - pris_ptrl_rdng_A
petrol_sold_B = crnt_ptrl_rdng_B - pris_ptrl_rdng_B
diesel_sold_A = crnt_dsil_rdng_A - pris_dsil_rdng_A
diesel_sold_B = crnt_dsil_rdng_B - pris_dsil_rdng_B

# Total Sold in Litters
total_petrol_sold = petrol_sold_A + petrol_sold_B
total_diesel_sold = diesel_sold_A + diesel_sold_B

# Stock of Petrol And Diesel
petrol_stock = ptrl_stck_updt - total_petrol_sold
diesel_stock = dsil_stck_updt - total_diesel_sold

# Rupees of Petrol and Diesel
petrol_rupees = total_petrol_sold * ptrl_price_updt
diesel_rupees = total_diesel_sold * dsil_price_updt

# Total Rupees
total_rs = petrol_rupees + diesel_rupees + cashback - total_expanses

# Total Month Rupees
total_mnth_rs += total_rs - cashout


class System:
    def update_DB(self):
        f = db.cursor()
        # Update Database for Fuel
        f.execute("UPDATE `day_summary` SET ptrl_price='" + str(ptrl_price_updt) + "',desl_price='" + str(
            dsil_price_updt) + "',ppra='" + str(crnt_ptrl_rdng_A) + "',pprb='" + str(
            crnt_ptrl_rdng_B) + "',ptrl_sld='" + str(total_petrol_sold) + "',ptrl_rs='" + str(
            petrol_rupees) + "',ptrl_stck='" + str(petrol_stock) + "',dpra='" + str(
            crnt_dsil_rdng_A) + "',dprb='" + str(crnt_dsil_rdng_B) + "',desl_sld='" + str(
            total_diesel_sold) + "',desl_rs='" + str(diesel_rupees) + "',dsil_stck='" + str(
            diesel_stock) + "' WHERE date='" + today_date + "'")
        # Update Database for money
        f.execute("UPDATE `day_summary` SET expanses='" + str(total_expanses) + "',cashback='" + str(
            cashback) + "',name='" + str(cashback_name) + "',ttl_dy_rs='" + str(total_rs) + "',ttl_mnth_rs='" + str(
            total_mnth_rs) + "' WHERE date='" + today_date + "'")
        db.commit()
        try:
            self.send_email()
        except:
            Narrator("Sorry Email Cannot be Send Due To Internet Connection Error")

    def pdfmaker(self):
        self.message = f"""<!DOCTYPE html>
            <html>
            <body>
            <img style="position: absolute;width: 99%;height: 95%;opacity: 0.2;" src="https://bit.ly/3r0WbeH">
            <h1 style="text-align: center;color: red">Fawad Petrol Management System</h>
            <h4 style="text-align: center;"> {pump_name}<br>Today Summary</h4>
            <h4 style="float: left;"><b>Date: {today_date}</b></h4>
            <h4 style="float: right;"><b>Time: {current_time}</b></h4>
            <table style="width: 100%;">
              <tr style="background-color: green;color:white">
                <th style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>*</b></th>
                <th style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>Petrol 'A'</b></th>
                <th style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>Petrol 'B'</b></th>
                <th style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>Diesel 'A'</b></th>
                <th style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>Diesel 'B'</b></th>
              </tr>
                  <tr>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Today Price</b></td>
                <td colspan="2" style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{ptrl_price_updt}</b></td>
                <td colspan="2" style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{dsil_price_updt}</b></td>
              </tr>
              <tr>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Previous Reading</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{pris_ptrl_rdng_A}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{pris_ptrl_rdng_B}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{pris_dsil_rdng_A}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{pris_dsil_rdng_B}</b></td>
              </tr>
                <tr>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Current Reading</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{crnt_ptrl_rdng_A}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{crnt_ptrl_rdng_B}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{crnt_dsil_rdng_A}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{crnt_dsil_rdng_B}</b></td>
              </tr>
                <tr>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Litters Sold</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{petrol_sold_A}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{petrol_sold_B}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{diesel_sold_A}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{diesel_sold_B}</b></td>
              </tr>
                <tr>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Total Litters Sold</b></td>
                <td colspan="2" style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{total_petrol_sold}</b></td>
                <td colspan="2" style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{total_diesel_sold}</b></td>
              </tr>
                <tr>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>In Stock Litters</b></td>
                <td colspan="2" style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{petrol_stock}</b></td>
                <td colspan="2" style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{diesel_stock}</b></td>
              </tr>
                <tr>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Fuel Rupees</b></td>
                <td colspan="2" style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{petrol_rupees}</b></td>
                <td colspan="2" style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{diesel_rupees}</b></td>
              </tr>
                <tr>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>*</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Today Cashback</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Today Expanses</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Today CashOut</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Today Rupees</b></td>
              </tr>
                <tr>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Rupees</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{cashback}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{total_expanses}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{cashout}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{total_rs}</b></td>
              </tr>
                <tr>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Names</b></td>
                <td colspan="2" style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{cashback_name}</b></td>
                <td colspan="2" style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{cashout_name}</b></td>
              </tr>
                <tr>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px; background: yellow;"><b>Total Month Rupees</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>*</b></td>
                <td colspan="2" style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>{total_mnth_rs}</b></td>
                <td style="border: 2px solid #dddddd;border-color: #a117eb;text-align: center;padding: 8px;"><b>*</b></td>
              </tr>
            </table>
            <br>
            <h4 style="text-align: right;"><b>Seal/Signature:_________________</b></h4>
            <br><br><br>
            <p style="position:fixed;bottom:0;width: 100%;background-color:black;color:yellow;text-align:center;">Copyright@ 2021 Fawad. All Rights Reserved</P>
            </body>
            </html>"""
        x_r = y.strftime("%d_%m_%y")
        if os.path.exists("Daily_Reports"):
            pass
        else:
            os.mkdir("Daily_Reports")
        try:
            cr = f"Daily_Reports\/{x_r}.pdf"
            pdfkit.from_string(self.message, cr, configuration=pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf/bin/wkhtmltopdf.exe'))
            os.startfile(cr)
            Narrator("Your Today Report Has Been Saved In Project Daily_Report Directory")
        except OSError:
            Narrator("Error 'Wkhtmltopdf' Doesn't Install in Your Computer\nPlease Download The Software And Install It In (C:\Program Files)")
            print("Click To Download (https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf)")
            print("*" + "~~~" * 30 + "*")

    def send_email(self):
        self.pdfmaker()
        msg = MIMEMultipart()
        msg["From"] = "Fawad Petrol Pump Management System"
        msg["To"] = "Pump Owner"
        msg["Subject"] = "Today Summary"
        msg["Bcc"] = email_address
        msg.attach(MIMEText(self.message, 'html'))
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login('email', 'pass')
        server.sendmail("email", email_address, msg.as_string())
        server.quit()
        Narrator(f"\nPlease Check Your Email Inbox {email_address} For Today Summary")
