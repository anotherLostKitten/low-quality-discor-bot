import atexit

import sqlite3

DB=sqlite3.connect("cic.db")
c=DB.cursor()

def in_bp(uid):
    return c.execute("SELECT id FROM bp WHERE bp.id = ?;",(uid,)).fetchone()!=None
def get_bp(uid):
    if(in_bp(uid)):
        return c.execute("SELECT pp FROM bp WHERE bp.id = ?;",(uid,)).fetchone()[0]
    c.execute("INSERT INTO bp VALUES (?, ?);",(uid,0))
    DB.commit()
    return 0
def set_bp(uid,x):
    if(in_bp(uid)):
        c.execute("UPDATE bp SET pp = ? WHERE bp.id = ?;", (x,uid))
    else:
        c.execute("INSERT INTO bp VALUES (?, ?);",(uid,x))
    DB.commit()
def mod_bp(uid,dx,neg):
    if(not in_bp(uid)):
        if(not neg and dx<0):
            return False
        c.execute("INSERT INTO bp VALUES (?, ?);",(uid,dx))
    else:
        if(not neg and dx<0 and get_bp(uid)+dx<0):
            return False
        c.execute("UPDATE bp SET pp = ? WHERE bp.id = ?;", (get_bp(uid)+dx,uid))
    DB.commit()
    return True
def top_bp():
    return c.execute("SELECT * FROM bp ORDER BY pp DESC;").fetchall()[:3]
def close_db():
    print("closing database")
    DB.close()
atexit.register(close_db)





if __name__=="__main__":
   c.execute("DROP TABLE IF EXISTS bp;")
   c.execute("CREATE TABLE bp (id INTEGER PRIMARY KEY, pp INTEGER);")
   DB.commit()
