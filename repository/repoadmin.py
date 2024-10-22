import psycopg2 as pg
from config.config import config

def cek_admin_login(email, password):
    params = config()
    try:
        conn = None
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()
        sql = "SELECT * FROM admin WHERE email = %s AND pass = %s"
        cur.execute(sql, (email, password))
        if cur.fetchone() is not None:
            return True
        else:
            return False
    except (Exception, pg.DatabaseError) as error:
        print(error)
        return False
    finally:
        conn.close()
        cur.close()


def cekID_Admin(id_admin):
    params = config()
    try:
        conn = None
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()
        sql = "SELECT id_admin FROM admin WHERE id_admin = %s"
        cur.execute(sql, (id_admin))
        if cur.fetchone() is not None:
            return True
        else:
            return False
    except (Exception, pg.DatabaseError) as error:
        print(error)
        return False
    finally:
        conn.close()
        cur.close()