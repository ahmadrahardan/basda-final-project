import os,sys,colorama,psycopg2 as pg

from services import admin,customer
from repository.repocustomer import cek_user_customer, daftar_customer_db,cek_customer_login
from repository.repoadmin import cek_admin_login
from config.config import config
from colorama import Fore, Style


#Warna
colorama.init(autoreset=True)
ungu_gelap = Fore.MAGENTA + Style.DIM
ungu_terang = Fore.MAGENTA + Style.BRIGHT
putih_terang = Fore.WHITE + Style.BRIGHT
putih_gelap = Fore.WHITE + Style.DIM
hijau_terang = Fore.GREEN + Style.BRIGHT
hijau_gelap = Fore.GREEN + Style.DIM
merah_terang = Fore.RED + Style.DIM

def clear():
    os.system('cls')

def Dashboard():
    os.system("cls")
    print(ungu_gelap+"="*96)
    print(putih_terang+"SELAMAT DATANG".center(96))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(96))
    print(ungu_gelap+ "="*96)

def headerCustomer():
    print(ungu_gelap+"="*96)
    print(putih_terang+"MENU CUSTOMER".center(96))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(96))
    print(ungu_gelap+"="*96)

def headerAdmin():
    print(ungu_gelap+"="*96)
    print(putih_terang+"MENU ADMIN".center(96))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(96))
    print(ungu_gelap+"="*96)

def menu_admin(id_admin):
    while True:
        clear()
        Dashboard()
        print("\nMENU :")
        print("[1] Katalog Unit")
        print("[2] Data Merk")
        print("[3] Data Customer")
        print("[4] Riwayat Transaksi")
        print("\n[0] Keluar")
        menu = input("Pilih menu: ")
        match menu:
            case "1":
                clear()
                admin.lihatKatalog()
                continue
            case "2":
                clear()
                admin.lihatMerk()
            case "3":
                clear()
                admin.lihatCustomer()
            case "4":
                clear()
                admin.lihatTransaksi(id_admin)
            case "0":
                awal()
            case _:
                print(merah_terang+"Pilihan tidak tersedia!")
                input("Klik apapun untuk melanjutkan.")
            
def masuk_admin():
    os.system('cls' if os.name == 'nt' else 'clear')
    headerAdmin()
    email = input("Masukkan email: ")
    password = input("Masukkan Password: ")
    id_admin = ambilID_admin(email)

    if cek_admin_login(email, password):
        print("Login admin berhasil!")
        menu_admin(id_admin)
    else:
        print("Nama atau password salah, silakan coba lagi.")
        input("Untuk melanjutkan, tekan enter")
        awal()

def menu_customer(id_customer):
    while True:
        Dashboard()
        print("\nMENU :")
        print("[1] Katalog Unit")
        print("[2] Riwayat Transaksi")
        print("\n[0] Keluar")
        menu = input("Pilih menu: ")
        match menu:
            case "1":
                customer.menuKatalog(id_customer)
            case "2":
                customer.lihatTransaksi_Customer(id_customer)
            case "0":
                customer_awal()
            case _:
                print(merah_terang+"\nPilihan tidak tersedia!")
                input("Untuk melanjutkan, tekan enter")

def customer_awal():
    os.system('cls')
    headerCustomer()
    
    user_type = input("[1] Registrasi\n[2] Login\n\n[0] Kembali ke halaman awal\nPilihan =  ")

    if user_type == "1":
        daftar_customer()
    elif user_type == "2":
        masuk_customer()
    elif user_type == "0":
        awal()
    else:
        input("Masukkan pilihan yang benar!\nUntuk melanjutkan, tekan enter") 
        customer_awal()

def daftar_customer():
    while True :
        clear()
        headerCustomer()
        username = input("Masukkan nama: ")

        if cek_user_customer(username):
            print("Username sudah ada, silahkan coba lagi")
            input("Untuk melanjutkan, tekan enter")
            continue
        else:
            nik = input("Masukkan NIK: ")
            no_telepon = input("Masukkan No Telepon: ")
            email = input("Masukkan Email: ")
            password = input("Masukkan Password: ")
            if daftar_customer_db(username, nik, no_telepon, email, password):
                print("\nData telah ditambahkan")
                input("Untuk melanjutkan, tekan enter")
                customer_awal()
            else:
                print("Terjadi kesalahan, data tidak dapat ditambahkan")
        

def ambilID_customer(email):
    hasil = ''
    try:
        conn = None
        params = config()
        conn = pg.connect(**params)
        sql = f'''
        SELECT id_customer
        FROM customer
        where email = '{email}'
        ''' 
        cur = conn.cursor()
        cur.execute(sql)
        hasil = cur.fetchone()
    except ValueError:
        print("ID unit tidak valid. Masukkan angka.")
    finally:
        cur.close()
        conn.close()
        return hasil


def ambilID_admin(email):
    hasil = ''
    try:
        conn = None
        params = config()
        conn = pg.connect(**params)
        sql = f'''
        SELECT id_admin
        FROM admin
        where email = '{email}'
        ''' 
        cur = conn.cursor()
        cur.execute(sql)
        hasil = cur.fetchone()
    except ValueError:
        print("ID unit tidak valid. Masukkan angka.")
    finally:
        cur.close()
        conn.close()
        return hasil
        

def masuk_customer():
    clear()
    headerCustomer()
    email = input("Masukkan email: ")
    password = input("Masukkan Password: ")
    id_customer = ambilID_customer(email)
    if cek_customer_login(email, password):
        print(hijau_terang+"\nLogin berhasil!")
        input("Untuk melanjutkan, tekan enter")
        menu_customer(id_customer)
    else:
        print("Nama atau password salah, silakan coba lagi.")
        input("Untuk melanjutkan, tekan enter")
        customer_awal()


def awal():
    os.system('cls')
    
    print(ungu_gelap+"="*96)
    print(putih_terang+"SELAMAT DATANG".center(96))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(96))
    print(ungu_gelap+"="*96)
    user_type = input("[1] Customer\n[2] Admin\n\n[0] Keluar\nPilihan :  ")

    if user_type == "1":
        customer_awal() 
    elif user_type == "2":
        masuk_admin()
    elif user_type == "0":
        keluar()
    else:
        input("Masukkan pilihan yang ada\nUntuk melanjutkan, tekan enter") 
        awal()

def keluar():
    os.system('cls')

    print(ungu_gelap+"="*96)
    print(putih_terang+"Terimakasih telah menggunakan BonsaRental".center(96))
    print(ungu_gelap+"="*96)

    sys.exit()

awal()