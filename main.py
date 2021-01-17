
from DB_Connection import db
f = db.cursor()
f.execute("SHOW TABLES")
tbl = f.fetchall()
if ("users",) in tbl:
    import SignIn
    import Welcome
else:
    import SignUp
    import SignIn
    import Welcome
