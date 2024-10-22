import os
import psycopg2 as pg
import configparser
from config.config import config

def cek_user_customer(username):
    params = config()
    try:
        conn = None
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()
        sql = f"SELECT * FROM customer WHERE nama = {username}"
        cur.execute(sql)
        if cur.fetchone() is not None:
            return True
        else:
            return False
    except (Exception, pg.DatabaseError) as error:
        return False
    
    finally:
        conn.close()
        cur.close()

def daftar_customer_db(username, nik, password, email, no_telepon):
    params = config()
    try:
        conn = None
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()
        sql = "INSERT INTO customer (nama, nik, pass, email, no_telepon) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql,(username, nik, password, email, no_telepon))
        conn.commit()
        return cur.rowcount > 0
    except (Exception, pg.DatabaseError) as error:
        print(error)
        return False
    finally:
        conn.close()
        cur.close()

def cek_customer_login(email, password):
    params = config()
    try:
        conn = None
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()
        sql = "SELECT * FROM customer WHERE email = %s AND pass = %s"
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

def cekID_Customer(id_customer):
    params = config()
    try:
        conn = None
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()
        sql = "SELECT id_customer FROM customer WHERE id_customer = %s"
        cur.execute(sql, (id_customer))
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