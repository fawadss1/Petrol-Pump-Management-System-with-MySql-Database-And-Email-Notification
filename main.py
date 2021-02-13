try:
    from DB_Connection import db

    f = db.cursor()
    f.execute("SHOW TABLES")
    tbl = f.fetchall()
    if ("users",) in tbl:
        import SignIn
    else:
        import SignUp
except:
    pass
