import psycopg2
from config.config import config

# FUNGSI UNTUK CONNECT KE DATABASE POSTGRESQL
def connect():
    params = config()
    if params is None:
        return 
    try:
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        print('Hasil Cek - Data Admin :')
        cur.execute("SELECT * FROM admin")
        rows = cur.fetchall()
        for row in rows:
            print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
            print('Database connection closed.')

connect()  
