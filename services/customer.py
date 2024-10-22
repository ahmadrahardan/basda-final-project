import os, colorama, psycopg2 as pg, datetime as dt
from services.admin import lihatKatalogSaja, ambilHarga
from config.config import config
from tabulate import tabulate
from colorama import Fore, Style
from datetime import datetime


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

def cek_user_customer(username):
    params = config()
    try:
        with pg.connect(**params) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customer WHERE nama = %s", (username,))
                hasil = cursor.fetchone()
                if username in hasil:
                    return True
                else:
                    return False
    except (Exception, pg.DatabaseError) as error:
        return False

def daftar_customer_db(username, password, email, no_telepon):
    db_config = config()
    try:
        with pg.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO customer (nama, pass, email, no_telepon) VALUES (%s, %s, %s, %s)",
                    (username, password, email, no_telepon)
                )
                connection.commit()
                return cursor.rowcount > 0
    except (Exception, pg.DatabaseError) as error:
        print(error)
        return False

def cek_user_login(username, password):
    db_config = config()
    try:
        with pg.connect(**db_config) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customer WHERE nama = %s AND pass = %s", (username, password))
                return cursor.fetchone() is not None
    except (Exception, pg.DatabaseError) as error:
        print(error)
        return False

def headerBonsa():
    print(ungu_gelap+"="*96)
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(96))
    print(ungu_gelap+ "="*96)

def lihatKatalog():
    try:
        conn = None
        params = config()
        conn = pg.connect(**params)
        sql = '''
        SELECT id_unit as ID, gambar_unit as Gambar, 
        j.nama_jenis ||' '||m.nama_merk||' '||u.tipe_unit as "Nama Unit",harga_sewa as "Harga Sewa",ketersediaan as Ketersediaan
        FROM unit u
        join jenis j on j.id_jenis = u.id_jenis
        join merk m on m.id_merk = u.id_merk
        order by id_unit
        '''
        cur = conn.cursor()
        cur.execute(sql)
        column_names = [desc[0].upper() for desc in cur.description]
        hasil = cur.fetchall()
        cur.close()
        headerBonsa()
        print(tabulate(hasil, headers=column_names, tablefmt="grid"))
    except (Exception, pg.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def menuKatalog(id_customer):
    while True :
        clear()
        lihatKatalog()
        print('''
    Pilihan :
        [1] Lakukan Pemesanan
                
        [0] Kembali
                ''')

        pilihan = input('Masukan pilihan anda : ')
        match pilihan:
            case "1":
                pesanUnit(id_customer)
            case "0":
                break
            case _:
                    os.system("cls")
                    print(merah_terang+"Pilihan tidak tersedia!")
                    input("Klik apapun untuk melanjutkan")

def pesanUnit(id_customer,id_admin=3, status_peminjaman="Dipesan", status_pembayaran="Menunggu Konfirmasi"):
    conn = None
    cur = None
    try:
        headerBonsa()
        print("Transaksi :")
        while True:
                lihatKatalogSaja()
                id_unit = input("Masukkan ID unit yang ingin disewa: ")
                try:
                    id_unit = int(id_unit)
                except ValueError:
                    print(merah_terang + "ID unit harus berupa angka.")
                    continue  
                harga_sewa = ambilHarga(id_unit)

                params = config()
                conn = pg.connect(**params)
                cur = conn.cursor()

                if harga_sewa is not None:
                    harga_sewa = harga_sewa[0] 
                    durasi_sewa = int(input("Masukkan durasi sewa unit (hari): "))
                    total_harga = harga_sewa * durasi_sewa
                    tanggal_sewa = input("Masukkan tanggal penyewaan (YYYY-MM-DD): ")
                    tanggal_kembali = input("Masukkan tanggal pengembalian (YYYY-MM-DD): ")


                    try:
                        tanggal_sewa = datetime.strptime(tanggal_sewa, "%Y-%m-%d").date()
                        tanggal_kembali = datetime.strptime(tanggal_kembali, "%Y-%m-%d").date()
                        if tanggal_kembali <= tanggal_sewa:
                            raise ValueError("Tanggal pengembalian harus setelah tanggal penyewaan.")
                    except ValueError:
                        print(merah_terang + "Format tanggal salah atau tanggal tidak valid.")
                        continue  

                    while True:
                        metode_pembayaran = input(
                            "Metode Pembayaran :\n[1] Tunai [2] Bank [3] QRIS\n Pilihan : "
                        )
                        if metode_pembayaran in ["1", "2", "3"]:
                            metode_pembayaran_mapping = {
                                "1": "Tunai",
                                "2": "Bank",
                                "3": "QRIS",
                            }
                            metode_pembayaran = metode_pembayaran_mapping[metode_pembayaran]
                            break
                        else:
                            print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")

                    cur.execute(
                        "INSERT INTO pembayaran (metode_pembayaran) VALUES (%s) RETURNING id_pembayaran",
                        (metode_pembayaran,),
                    )
                    id_pembayaran = cur.fetchone()[0]

                    cur.execute(
                        """
                        INSERT INTO transaksi (tanggal_transaksi, tanggal_peminjaman, tanggal_pengembalian, status_peminjaman, status_pembayaran, id_pembayaran, id_unit,id_admin, id_customer, total_pembayaran)
                        VALUES (now(), %s, %s, %s, %s, %s, %s, %s, %s,%s)
                        """,
                        (
                            tanggal_sewa,
                            tanggal_kembali,
                            status_peminjaman,
                            status_pembayaran,
                            id_pembayaran,
                            id_unit,
                            id_admin,
                            id_customer,
                            total_harga,
                        ),
                    )

                    if metode_pembayaran == "Tunai":
                        cur.execute(
                            "INSERT INTO cash (id_pembayaran) VALUES (%s)",
                            (id_pembayaran,),
                        )
                    elif metode_pembayaran == "Bank":
                        nama_bank = input("Masukkan nama bank: ")
                        nama_pemilik = input("Masukkan nama pemilik rekening: ")
                        cur.execute(
                            "INSERT INTO bank (id_pembayaran, nama_bank, nama_pemilik) VALUES (%s, %s, %s)",
                            (id_pembayaran, nama_bank, nama_pemilik),
                        )
                    elif metode_pembayaran == "QRIS":
                        username = input("Masukkan username QRIS: ")
                        cur.execute(
                            "INSERT INTO qris (id_pembayaran, username) VALUES (%s, %s)",
                            (id_pembayaran, username),
                        )
                    print(putih_terang+"\nPastikan data yang diiskan sudah benar!")
                    input("Enter Lanjutkan Transaksi")
                    conn.commit()
                    print(hijau_terang + "\nData Transaksi berhasil ditambahkan!")
                    input(hijau_gelap+"Silahkan menunggu konfirmasi dari Admin\nTekan Enter untuk melanjutkan...")
                    break
                else:
                    print(merah_terang + "Harga Sewa tidak ditemukan")
                    input("Enter untuk kembali")
                    break

    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk kembali ")
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def lihatTransaksi_Customer(id_customer):
    params = config()
    with pg.connect(**params) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    SELECT t.id_transaksi as ID,t.tanggal_transaksi as "Tanggal Transaksi", c.nama as Customer,u.tipe_unit as unit , t.tanggal_peminjaman as Pengambilan, t.tanggal_pengembalian as Pengembalian, t.status_peminjaman as "Status Penyewaan", t.status_pembayaran ||', '|| p.metode_pembayaran as Pembayaran, a.nama as Admin
                    FROM transaksi t
                    JOIN unit u on u.id_unit = t.id_unit
                    JOIN customer c ON t.id_customer = c.id_customer
                    JOIN admin a ON t.id_admin = a.id_admin
                    JOIN pembayaran p ON t.id_pembayaran = p.id_pembayaran
                    WHERE t.id_customer = %s
                    ORDER BY t.tanggal_transaksi DESC, t.id_transaksi DESC
                    """,
                    (id_customer),
                )

                column_names = [desc[0].upper() for desc in cur.description]
                hasil = cur.fetchall()
                clear()
                headerBonsa()
                print(tabulate(hasil, headers=column_names, tablefmt="grid"))
                print(hijau_gelap + "Hubungi Admin Jika Diperlukan")
                pilihan = input("Apakah anda ingin melihat Detail Pembayaran ? (y/n) : ")
                if pilihan == 'y': 
                    lihatDetailPembayaran(id_customer)
                elif pilihan == 'n':
                    return
                else:
                    print(merah_terang+"Masukkan pilihan yang benar! ")
                    input("Enter untuk kembali")
                    return

            except pg.DatabaseError as error:
                print(f"Terjadi kesalahan database: {error}")
                input("Enter untuk kembali")

def lihatTransaksi_CustomerSaja(id_customer):
    params = config()
    with pg.connect(**params) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(
                    """
                    SELECT t.id_transaksi as ID,t.tanggal_transaksi as "Tanggal Transaksi", c.nama as Customer,u.tipe_unit as unit, t.tanggal_peminjaman as Pengambilan, t.tanggal_pengembalian as Pengembalian, t.status_peminjaman as "Status Penyewaan", t.status_pembayaran ||', '|| p.metode_pembayaran as Pembayaran, a.nama as Admin
                    FROM transaksi t
                    JOIN unit u on u.id_unit = t.id_unit
                    JOIN customer c ON t.id_customer = c.id_customer
                    JOIN admin a ON t.id_admin = a.id_admin
                    JOIN pembayaran p ON t.id_pembayaran = p.id_pembayaran
                    WHERE t.id_customer = %s
                    ORDER BY t.tanggal_transaksi DESC, t.id_transaksi DESC
                    """,
                    (id_customer),
                )

                column_names = [desc[0].upper() for desc in cur.description]
                hasil = cur.fetchall()
                print(tabulate(hasil, headers=column_names, tablefmt="grid"))

            except pg.DatabaseError as error:
                print(f"Terjadi kesalahan database: {error}")
                input("Enter untuk kembali")

def lihatDetailPembayaran(id_customer):
    clear()
    print(ungu_gelap+"="*128)
    print(putih_terang+"DETAIL TRANSAKSI".center(128))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(128))
    print(ungu_gelap+ "="*128)
    try:
        lihatTransaksi_CustomerSaja(id_customer)
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        id_transaksi = int(input("Masukkan ID transaksi: "))

        cur.execute(
            """
            SELECT t.id_transaksi as ID,t.tanggal_transaksi as "Tanggal Transaksi", c.nama as Customer,u.tipe_unit as unit, t.total_pembayaran as "Total Pembayaran", p.metode_pembayaran as Pembayaran, p.id_pembayaran,a.nama as Admin
            FROM transaksi t 
            JOIN unit u on u.id_unit = t.id_unit
            JOIN pembayaran p on p.id_pembayaran = t.id_pembayaran
            JOIN customer c ON t.id_customer = c.id_customer
            JOIN admin a ON t.id_admin = a.id_admin
            WHERE t.id_transaksi = %s
            ORDER BY t.tanggal_transaksi DESC
            """,
            (id_transaksi,),
        )
        hasil_transaksi = cur.fetchone()
        column_names = [desc[0].upper() for desc in cur.description[:-1]] + ["DETAIL PEMBAYARAN"]

        if hasil_transaksi:
            metode_pembayaran = hasil_transaksi[5]
            id_pembayaran = hasil_transaksi[6] 
            detail_pembayaran = None

            if metode_pembayaran == "Bank":
                cur.execute(
                    "SELECT nama_bank || ' - ' || nama_pemilik FROM bank WHERE id_pembayaran = %s",
                    (id_pembayaran,),
                )
                detail_pembayaran = cur.fetchone()
            elif metode_pembayaran == "QRIS":
                cur.execute(
                    "SELECT username FROM qris WHERE id_pembayaran = %s",
                    (id_pembayaran,),
                )
                detail_pembayaran = cur.fetchone()

            if detail_pembayaran:
                detail_pembayaran = detail_pembayaran[0]

            hasil_lengkap = hasil_transaksi[:-1] + (detail_pembayaran,)  

            print(tabulate([hasil_lengkap], headers=column_names, tablefmt="grid"))
            input("Enter untuk kembali ")
            clear()
        else:
            print(merah_terang+"Transaksi tidak ditemukan.")
            input("Enter untuk kembali ")

    except (Exception, pg.DatabaseError) as error:
        print(f"Terjadi kesalahan: {error}")
        input("Enter Untuk Kembali")
    finally:
        if conn is not None:
            cur.close()
            conn.close()