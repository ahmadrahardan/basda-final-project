import os, colorama, psycopg2 as pg
from repository.repoadmin import cekID_Admin
from datetime import datetime
from config.config import config
from tabulate import tabulate
from colorama import Fore, Style

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

def headerBonsa():
    print(ungu_gelap+"="*128)
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(128))
    print(ungu_gelap+ "="*128)

def lihatKatalog():
    while True:
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
            clear()
            headerBonsa()
            print(tabulate(hasil, headers=column_names, tablefmt="grid")) 
            print('''
    Pilihan :
        [1] Tambah Unit
        [2] Edit Unit
        [3] Hapus Unit
                
        [0] Kembali
                ''')
            pilihan = input('Masukan pilihan anda : ')
            match pilihan:
                case "1":
                    clear()
                    tambahUnit()
                case "2":
                    clear()
                    editUnit()
                case "3":
                    clear()
                    hapusUnit()
                case "0":
                    break
                case _:
                    print(merah_terang+"\nPilihan tidak tersedia!")
                    input("Klik apapun untuk melanjutkan")
        except (Exception, pg.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
def lihatKatalogSaja():
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
        clear()
        headerBonsa()
        print(tabulate(hasil, headers=column_names, tablefmt="grid")) 
    except (Exception, pg.DatabaseError) as error:
        print('Error:'+error)
        input("Enter untuk kembali ") 
    finally:
        if conn is not None:
            conn.close()

def tambahUnit():
    try:    
        headerBonsa()
        gambar_unit = input("Masukkan nama file gambar unit: ")
        tipe_unit = input("Masukkan tipe unit: ")
        harga_sewa = int(input("Masukkan harga sewa per hari: "))
        ketersediaan = input("Masukkan status ketersediaan: ")
        id_jenis = int(input("[1] Kamera\n[2] Lensa\n[3] Lighting\n[4] Microphone\nMasukkan ID jenis unit: "))
        id_merk = int(input("[1] Canon\n[2] Sony\n[3] Fujifilm\n[4] Nikon\nMasukkan ID merk unit: "))

        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()
        sql = """
            INSERT INTO unit (gambar_unit, tipe_unit, harga_sewa, ketersediaan, id_jenis, id_merk)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (gambar_unit, tipe_unit, harga_sewa, ketersediaan, id_jenis, id_merk)
        cur.execute(sql, values)

        conn.commit()
        print("Unit berhasil ditambahkan!")
        input("Tekan Enter untuk melanjutkan...")
    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk kembali ") 
    finally:
        if conn is not None:
            cur.close()
            conn.close() 

def editUnit():
    headerBonsa()
    try:
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        cur.execute("SELECT id_unit, tipe_unit FROM unit order by id_unit")
        units = cur.fetchall()
        print("Daftar unit:")
        for unit in units:
            print(f"\t[{unit[0]}] {unit[1]}")

        id_unit = int(input("Masukkan ID unit yang ingin diubah: "))

        print("""
Atribut yang dapat diubah:
    [1] Gambar
    [2] Tipe
    [3] Harga Sewa
    [4] Ketersediaan
    [5] Jenis 
    [6] Merk
              """)
        pilihan = int(input("Pilih nomor atribut yang ingin diubah: "))

        if pilihan == 1:
            sql = "UPDATE unit SET gambar_unit = %s WHERE id_unit = %s"
        elif pilihan == 2:
            sql = "UPDATE unit SET tipe_unit = %s WHERE id_unit = %s"
        elif pilihan == 3:
            sql = "UPDATE unit SET harga_sewa = %s WHERE id_unit = %s"
            nilai_baru = int(nilai_baru)  
        elif pilihan == 4:
            sql = "UPDATE unit SET ketersediaan = %s WHERE id_unit = %s"
        elif pilihan == 5:
            print("""
Daftar Jenis:
    [1] Kamera
    [2] Lensa
    [3] Lighting
    [4] Microphone
            """)
            sql = "UPDATE unit SET id_jenis = %s WHERE id_unit = %s"
        elif pilihan == 6:
            try:
                params = config()
                conn = pg.connect(**params)
                cur = conn.cursor()

                cur.execute("SELECT id_merk, nama_merk FROM merk order by id_merk")
                merkdb = cur.fetchall()
                print("\nDaftar merk:")
                for merk in merkdb:
                    print(f"{merk[0]}. {merk[1]}")

                sql = "UPDATE unit SET id_merk = %s WHERE id_unit = %s"
            except (Exception, pg.DatabaseError) as error:
                print(f"Error: {error}")
                input("Enter untuk melanjutkan ")
        else:
            print("Pilihan tidak valid.")
            return
        
        nilai_baru = input("Masukkan nilai baru : ")
        cur.execute(sql, (nilai_baru, id_unit))
        conn.commit()
        print(hijau_terang+"Data berhasil diubah !")
        input("Enter untuk kembali ")
    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk melanjutkan ")
    finally:
        if conn is not None:
            cur.close()
            conn.close()


def hapusUnit():
    headerBonsa()
    try:
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()


        cur.execute("SELECT id_unit, tipe_unit FROM unit")
        units = cur.fetchall()
        print("Daftar unit:")
        for unit in units:
            print(f"{unit[0]}. {unit[1]}")

        id_unit = int(input("Masukkan ID unit yang ingin dihapus: "))

        confirm = input(f"Apakah Anda yakin ingin menghapus unit dengan ID {id_unit}? (y/n): ")
        if confirm.lower() == 'y':

            sql = "DELETE FROM unit WHERE id_unit = %s"
            cur.execute(sql, (id_unit,))
            conn.commit()
            print("Unit berhasil dihapus!")
            input("Tekan Enter untuk melanjutkan...")
        else:
            print("Penghapusan unit dibatalkan.")

    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def lihatMerk():
    while True:
        try:
            conn = None
            params = config()
            conn = pg.connect(**params)
            sql = '''
        SELECT id_merk as ID, nama_merk as "Nama Merk" 
        FROM merk
        order by id_merk
            '''
            cur = conn.cursor()
            cur.execute(sql)
            column_names = [desc[0].upper() for desc in cur.description]
            hasil = cur.fetchall()
            cur.close()
            clear()
            headerBonsa()
            print(tabulate(hasil, headers=column_names, tablefmt="grid")) 
            print('''
    Pilihan :
        [1] Tambah Merk
        [2] Edit Merk
        [3] Hapus Merk
                
        [0] Kembali
                ''')
            pilihan = input('Masukan pilihan anda : ')
            match pilihan:
                case "1":
                    clear()
                    tambahMerk()
                case "2":
                    clear()
                    editMerk()
                case "3":
                    clear()
                    hapusMerk()
                case "0":
                    break
                case _:
                    print(merah_terang+"\nPilihan tidak tersedia!")
                    input("Klik apapun untuk melanjutkan")
        except (Exception, pg.DatabaseError) as error:
            print(error)
            break
        finally:
            if conn is not None:
                conn.close()

def tambahMerk():
    try:     
        headerBonsa()
        merk = input("\nMasukkan merk baru: ")

        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()
        sql = f"""
            INSERT INTO merk (nama_merk)
            VALUES ('{merk}')
        """
        cur.execute(sql)

        conn.commit()
        print("Merk berhasil ditambahkan!")
        input("Tekan Enter untuk melanjutkan...")
    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk kembali ") 
    finally:
        if conn is not None:
            cur.close()
            conn.close() 

def editMerk():
    headerBonsa()
    try:
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        cur.execute("SELECT id_merk, nama_merk FROM merk order by id_merk")
        merkdb = cur.fetchall()
        print("Daftar merk:")
        for merk in merkdb:
            print(f"\t[{merk[0]}] {merk[1]}")

        id_merk = int(input("Masukkan ID merk yang ingin diubah: "))
        merk_baru = input("Masukkan nama merk baru: ")

        sql = "UPDATE merk SET nama_merk = %s WHERE id_merk = %s"
        cur.execute(sql, (merk_baru, id_merk))
        conn.commit()
        print("Data merk berhasil diubah!")
        input("Tekan Enter untuk melanjutkan...")
    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk kembali ") 
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def hapusMerk():
    headerBonsa()
    try:
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()


        cur.execute("SELECT * FROM merk")
        merkdb = cur.fetchall()
        print("Daftar unit:")
        for merk in merkdb:
            print(f"\t[{merk[0]}] {merk[1]}")

        id_merk = int(input("Masukkan ID merk yang ingin dihapus: "))

        confirm = input(f"Apakah Anda yakin ingin menghapus unit dengan ID {id_merk}? (y/n): ")
        if confirm.lower() == 'y':

            sql = "DELETE FROM merk WHERE id_merk = %s"
            cur.execute(sql, (id_merk,))
            conn.commit()
            print("Unit berhasil dihapus!")
            input("Tekan Enter untuk melanjutkan...")
        else:
            input("Penghapusan merk dibatalkan.")

    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk melanjutkan ")
    finally:
        if conn is not None:
            cur.close()
            conn.close()  


def lihatCustomer():
    while True:
        try:
            clear()
            conn = None
            params = config()
            conn = pg.connect(**params)
            sql = '''
        SELECT * 
        FROM customer
        order by id_customer
            '''
            cur = conn.cursor()
            cur.execute(sql)
            column_names = [desc[0].upper() for desc in cur.description]
            hasil = cur.fetchall()
            cur.close()
            clear()
            headerBonsa()
            print(tabulate(hasil, headers=column_names, tablefmt="grid")) 
            print('''
    Pilihan :
        [1] Tambah Customer
        [2] Edit Customer
        [3] Hapus Customer
                
        [0] Kembali
                ''')
            pilihan = input('Masukan pilihan anda : ')
            match pilihan:
                case "1":
                    clear()
                    tambahCustomer()
                case "2":
                    clear()
                    editCustomer()
                case "3":
                    clear()
                    hapusCustomer()
                case "0":
                    break
                case _:
                    print(merah_terang+"\nPilihan tidak tersedia!")
                    input("Klik apapun untuk melanjutkan")
        except (Exception, pg.DatabaseError) as error:
            print('Error:'+error)
            input("Enter untuk kembali ") 
            break
        finally:
            if conn is not None:
                conn.close()
def lihatCustomerSaja():
        try:
            clear()
            conn = None
            params = config()
            conn = pg.connect(**params)
            sql = '''
        SELECT * 
        FROM customer
        order by id_customer
            '''
            cur = conn.cursor()
            cur.execute(sql)
            column_names = [desc[0].upper() for desc in cur.description]
            hasil = cur.fetchall()
            cur.close()
            clear()
            headerBonsa()
            print(tabulate(hasil, headers=column_names, tablefmt="grid"))
        except (Exception, pg.DatabaseError) as error:
            print('Error:'+error)
            input("Enter untuk kembali ") 
        finally:
            if conn is not None:
                conn.close()
def tambahCustomer():
    try:  
        headerBonsa()
        nama = input("\nMasukkan nama : ")
        nik = input("Masukkan NIK : ")
        no_telepon = input("Masukkan nomor telepon : ")
        email = input("Masukkan email : ")
        
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()
        sql = """
            INSERT INTO customer (nama,nik,no_telepon,email,pass)
            VALUES (%s,%s,%s,%s,'admin')
        """
        values = (nama,nik,no_telepon,email)
        cur.execute(sql,values,)

        conn.commit()
        print(hijau_terang+"Data Customer berhasil ditambahkan!")
        input("Tekan Enter untuk melanjutkan...")
    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk kembali ") 
    finally:
        cur.close()
        conn.close() 

def editCustomer():
    headerBonsa()
    try:
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        cur.execute("SELECT * from customer order by id_customer")
        merkdb = cur.fetchall()
        print("Daftar customer:")
        for merk in merkdb:
            print(f"\t[{merk[0]}] {merk[1]}".title())

        id_customer = int(input("Masukkan ID customer yang ingin diubah: "))

        print("""
Atribut yang dapat diubah:
    [1] Nama
    [2] NIK
    [3] No Telepon
    [4] Email
              """)
        
        pilihan = int(input("Pilih nomor atribut yang ingin diubah: "))
        nilai_baru = input("Masukkan nilai baru : ")

        if pilihan == 1:
            sql = "UPDATE customer SET nama = %s WHERE id_customer = %s"
        elif pilihan == 2:
            sql = "UPDATE customer SET NIK = %s WHERE id_customer = %s"
        elif pilihan == 3:
            sql = "UPDATE customer SET no_telepon = %s WHERE id_customer = %s"
            nilai_baru = int(nilai_baru)  
        elif pilihan == 4:
            sql = "UPDATE customer SET email = %s WHERE id_customer = %s"
        else:
            print(merah_terang+"Pilihan tidak valid.")
            input("Enter untuk melanjutkan ")

            return
        
        cur.execute(sql, (nilai_baru, id_customer))
        conn.commit()
        print(hijau_terang+"Data berhasil diubah !")
        input("Enter untuk kembali ")
    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk melanjutkan ")
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def hapusCustomer():
    headerBonsa()
    try:
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()


        cur.execute("SELECT * FROM customer")
        merkdb = cur.fetchall()
        print("Daftar customer:")
        for merk in merkdb:
            print(f"\t[{merk[0]}] {merk[1]}")

        id_customer = int(input("Masukkan ID customer yang ingin dihapus: "))
        if id_customer == 0:
            input("Penghapusan customer dibatalkan.")
        else:
            confirm = input(putih_terang+f"Apakah Anda yakin ingin menghapus unit dengan ID {id_customer} ? (y/n): ")
            if confirm.lower() == 'y':

                sql = "DELETE FROM customer WHERE id_customer = %s"
                cur.execute(sql, (id_customer,))
                conn.commit()
                print(hijau_terang+"Data Customer berhasil dihapus!")
                input("Tekan Enter untuk melanjutkan...")
            else:
                input("Penghapusan customer dibatalkan.")

    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk melanjutkan ")
    finally:
        if conn is not None:
            cur.close()
            conn.close()     


def lihatTransaksi(id_admin):
    while True:
        try:
            clear()
            params = config()
            conn = pg.connect(**params)
            cur =conn.cursor()

            cur.execute(
                """
                SELECT t.id_transaksi as ID, t.tanggal_transaksi as Transaksi, c.nama as Customer,tipe_unit as unit, t.tanggal_peminjaman as Pengambilan, t.tanggal_pengembalian as Pengembalian, t.status_peminjaman as "Status Penyewaan", t.status_pembayaran ||', '|| p.metode_pembayaran as Pembayaran, a.nama as Admin
                FROM transaksi t
                JOIN unit u on u.id_unit = t.id_unit
                JOIN customer c ON t.id_customer = c.id_customer
                JOIN admin a ON t.id_admin = a.id_admin
                JOIN pembayaran p ON t.id_pembayaran = p.id_pembayaran
                ORDER BY t.tanggal_transaksi DESC, t.id_transaksi DESC
                """
            )

            column_names = [desc[0].upper() for desc in cur.description]
            hasil = cur.fetchall()
            headerBonsa()
            print(tabulate(hasil, headers=column_names, tablefmt="grid"))

            print('''
    Pilihan :
        [1] Tambah Transaksi
        [2] Edit Transaksi
        [3] Hapus Transaksi
        [4] Detail Pembayaran
                
        [0] Kembali
                ''')
            pilihan = input('Masukan pilihan anda : ')
            match pilihan:
                case "1":
                    clear()
                    tambahTransaksi(id_admin)
                case "2":
                    clear()
                    editTransaksi(id_admin)
                case "3":
                    clear()
                    hapusTransaksi()
                case "4":
                    clear()
                    lihatDetailPembayaran()
                case "0":
                    break
                case _:
                    print(merah_terang+"\nPilihan tidak tersedia!")
                    input("Klik apapun untuk melanjutkan")
        except (Exception, pg.DatabaseError) as error:
            print(f'Error:{error}')
            input("Enter untuk kembali ") 
            break
        finally:
            if conn is not None:
                conn.close()

def lihatTransaksiSaja():
    params = config()
    conn = pg.connect(**params)
    cur =conn.cursor()

    cur.execute(
        """
        SELECT t.id_transaksi as ID,  t.tanggal_transaksi as Transaksi, c.nama as Customer, tipe_unit as unit,  t.tanggal_peminjaman as Pengambilan, t.tanggal_pengembalian as Pengembalian, t.status_peminjaman as "Status Peminjaman", t.status_pembayaran ||', '|| p.metode_pembayaran as Pembayaran,a.nama as Admin
        FROM transaksi t
        JOIN unit u on u.id_unit = t.id_unit
        JOIN customer c ON t.id_customer = c.id_customer
        JOIN admin a ON t.id_admin = a.id_admin
        JOIN pembayaran p ON t.id_pembayaran = p.id_pembayaran
        ORDER BY t.tanggal_transaksi DESC, t.id_transaksi DESC
        """
    )

    column_names = [desc[0].upper() for desc in cur.description]
    hasil = cur.fetchall()
    print(tabulate(hasil, headers=column_names, tablefmt="grid"))

def tambahTransaksi(id_admin, status_peminjaman="Dipesan", status_pembayaran="Menunggu Konfirmasi"):
    conn = None
    cur = None
    try:
        headerBonsa()
        print("Transaksi :")
        while True:
            confirm = input("Apakah customer memiliki akun ? (y/n): ")
            if confirm.lower() == 'y':
                clear()
                lihatCustomerSaja()
                id_customer = input("Masukkan ID customer : ")
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
                        INSERT INTO transaksi (tanggal_transaksi, tanggal_peminjaman, tanggal_pengembalian, status_peminjaman, status_pembayaran, id_pembayaran, id_unit, id_admin, id_customer, total_pembayaran)
                        VALUES (now(), %s, %s, %s, %s, %s, %s, %s, %s, %s)
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

                    conn.commit()
                    print(hijau_terang + "Data Transaksi berhasil ditambahkan!")
                    input("Tekan Enter untuk melanjutkan...")
                    break
                else:
                    print(merah_terang + "Harga Sewa tidak ditemukan")
                    input("Enter untuk kembali")
                    break
            else:
                print(merah_terang + "Tambahkan terlebih dahulu data customer!")
                input("Enter untuk menambah data customer baru ")
                clear()
                tambahCustomer()
                continue

    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk kembali ")
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def ambilHarga(id_unit):
    try:
        conn = None
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        sql = f'''
        SELECT harga_sewa
        FROM unit u
        WHERE id_unit = {id_unit}
        '''
        cur.execute(sql)
        harga_sewa = cur.fetchall()[0] 
        return harga_sewa 
    except (Exception, pg.DatabaseError) as error:
        input(error)
    finally:
        conn.close()
        cur.close()

def editCustomer():
    headerBonsa()
    try:
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        cur.execute("SELECT * from customer order by id_customer")
        customerdb = cur.fetchall()
        print("Daftar customer:")
        for customer in customerdb:
            print(f"\t[{customer[0]}] {customer[1]}".title())

        id_customer = int(input("Masukkan ID customer yang ingin diubah: "))

        print("""
Atribut yang dapat diubah:
        [1] Nama
        [2] NIK
        [3] No Telepon
        [4] Email
              """)
        
        pilihan = int(input("Pilih nomor atribut yang ingin diubah: "))
        nilai_baru = input("Masukkan nilai baru : ")

        if pilihan == 1:
            sql = "UPDATE customer SET nama = %s WHERE id_customer = %s"
        elif pilihan == 2:
            sql = "UPDATE customer SET NIK = %s WHERE id_customer = %s"
        elif pilihan == 3:
            sql = "UPDATE customer SET no_telepon = %s WHERE id_customer = %s"
            nilai_baru = int(nilai_baru)  
        elif pilihan == 4:
            sql = "UPDATE customer SET email = %s WHERE id_customer = %s"
        else:
            print(merah_terang+"Pilihan tidak valid.")
            input("Enter untuk melanjutkan ")

            return
        
        cur.execute(sql, (nilai_baru, id_customer))
        conn.commit()
        print(hijau_terang+"Data berhasil diubah !")
        input("Enter untuk kembali ")
    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk melanjutkan ")
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def hapusCustomer():
    headerBonsa()
    try:
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        cur.execute("SELECT * FROM customer")
        merkdb = cur.fetchall()
        print("Daftar customer:")
        for merk in merkdb:
            print(f"\t[{merk[0]}] {merk[1]}")

        id_customer = int(input("Masukkan ID customer yang ingin dihapus: "))
        if id_customer == 0:
            input("Penghapusan customer dibatalkan.")
        else:
            confirm = input(putih_terang+f"Apakah Anda yakin ingin menghapus unit dengan ID {id_customer} ? (y/n): ")
            if confirm.lower() == 'y':

                sql = "DELETE FROM customer WHERE id_customer = %s"
                cur.execute(sql, (id_customer,))
                conn.commit()
                print(hijau_terang+"Data Customer berhasil dihapus!")
                input("Tekan Enter untuk melanjutkan...")
            else:
                input("Penghapusan customer dibatalkan.")

    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk melanjutkan ")
    finally:
        if conn is not None:
            cur.close()
            conn.close()     

def editTransaksi(id_admin):
    conn = None
    cur = None
    try:
        headerBonsa()
        lihatTransaksiSaja()
        print("Edit Transaksi:")

        while True:
            try:
                id_transaksi = input("Masukkan ID transaksi yang akan diedit: ")
                id_transaksi = int(id_transaksi)
                if cekTransaksiAda(id_transaksi):
                    break
                else:
                    print(merah_terang + "ID transaksi tidak valid.")
            except ValueError:
                print(merah_terang + "ID transaksi harus berupa angka.")

        while True:
            konfirmasi = input("Apakah Anda yakin ingin mengedit transaksi ini? (y/n): ")
            if konfirmasi.lower() in ['y', 'n']:
                break
            else:
                print("Pilihan tidak valid. Silakan pilih y atau n.")

        if konfirmasi.lower() == 'n':
            return

        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        while True:
            print("\nKolom yang dapat diedit:")
            print("[1] Konfirmasi Admin")
            print("[2] Unit")
            print("[3] Tanggal Peminjaman")
            print("[4] Tanggal Pengembalian")
            print("[5] Status Peminjaman")
            print("[6] Status Pembayaran")
            print("[7] Metode Pembayaran")
            print("\n0. Kembali")
            pilihan = input("Pilih kolom yang akan diedit: ")

            if pilihan == "0":
                return
            elif pilihan in ["1","2","3","4", "5", "6"]:
                break
            else:
                print("Pilihan tidak valid.")

        cur.execute(
            """
            SELECT t.tanggal_peminjaman, t.tanggal_pengembalian, p.metode_pembayaran
            FROM transaksi t
            JOIN pembayaran p ON t.id_pembayaran = p.id_pembayaran
            WHERE t.id_transaksi = %s
            """,
            (id_transaksi,),
        )
        tanggal_peminjaman_lama, tanggal_pengembalian_lama,metode_pembayaran = cur.fetchone()

      
        if pilihan in ["3", "4"]: 
            try:
                nilai_baru = input("Masukkan nilai baru: ")
                nilai_baru = datetime.strptime(nilai_baru, "%Y-%m-%d").date()
                if pilihan == "3" and nilai_baru >= tanggal_pengembalian_lama:
                    raise ValueError("Tanggal peminjaman harus sebelum tanggal pengembalian.")
                elif pilihan == "4" and nilai_baru <= tanggal_peminjaman_lama:
                    raise ValueError("Tanggal pengembalian harus setelah tanggal peminjaman.")
            except ValueError as e:
                print(merah_terang + f"Error: {e}")
                input("Enter untuk melanjutkan")
        elif pilihan == "1":
            confirm = input("Apakah anda ingin mengkonfirmasi transaksi ini ? (y/n) : ") 
            if confirm == 'y':
                nilai_baru = id_admin
            else:
                print("Konfirmasi Dibatalkan")
                input("Enter untuk kembali")
                return
        elif pilihan == "2":
            try:
                clear()
                headerBonsa()
                lihatKatalogSaja()
                nilai_baru = input("Masukkan id unit baru: ")
                nilai_baru = int(nilai_baru) 
                if not cekUnitAda(nilai_baru):
                    raise ValueError("ID unit tidak valid.")
                else:
                    harga_sewa_baru = ambilHarga(nilai_baru)[0]
                    print(harga_sewa_baru)
                    input()
                    durasi_sewa = (tanggal_pengembalian_lama - tanggal_peminjaman_lama).days
                    total_harga_baru = harga_sewa_baru * durasi_sewa

                    cur.execute(
                        "UPDATE transaksi SET id_unit = %s, total_pembayaran = %s WHERE id_transaksi = %s",
                        (nilai_baru, total_harga_baru, id_transaksi),
                    )
                    cur.execute(
                            "UPDATE transaksi SET id_unit = %s WHERE id_transaksi = %s",
                            (nilai_baru, id_transaksi),
                        )
                    conn.commit()
            except ValueError as e:
                print(merah_terang + f"Error: {e}")
                return
        elif pilihan == "5": 
            nilai_baru = input("Masukkan status baru: ")
            nilai_baru = nilai_baru.capitalize()
        elif pilihan == "6": 
            nilai_baru = input("Masukkan status baru: ")
            nilai_baru = nilai_baru.capitalize()
        elif pilihan == "7":  
            print("Metode Pembayaran:\n[1] Tunai\n[2] Bank\n[3] QRIS")
            nilai_baru = input("Masukkan nilai baru: ")
            while True:
                if nilai_baru in ["1", "2", "3"]:
                    metode_pembayaran_mapping = {
                        "1": "Tunai",
                        "2": "Bank",
                        "3": "QRIS",
                    }
                    metode_pembayaran = metode_pembayaran_mapping[nilai_baru]
                    break
                else:
                    print("Pilihan tidak valid. Silakan pilih 1, 2, atau 3.")
                    return

        if pilihan == "7":
            cur.execute(
                "UPDATE pembayaran SET metode_pembayaran = %s WHERE id_pembayaran = (SELECT id_pembayaran FROM transaksi WHERE id_transaksi = %s)",
                (metode_pembayaran, id_transaksi),
            )
            conn.commit()

            cur.execute("DELETE FROM cash WHERE id_pembayaran = (SELECT id_pembayaran FROM transaksi WHERE id_transaksi = %s)", (id_transaksi,))
            cur.execute("DELETE FROM bank WHERE id_pembayaran = (SELECT id_pembayaran FROM transaksi WHERE id_transaksi = %s)", (id_transaksi,))
            cur.execute("DELETE FROM qris WHERE id_pembayaran = (SELECT id_pembayaran FROM transaksi WHERE id_transaksi = %s)", (id_transaksi,))

            cur.execute(
                "SELECT id_pembayaran FROM transaksi WHERE id_transaksi = %s", (id_transaksi,)
            )
            id_pembayaran = cur.fetchone()[0]
            if metode_pembayaran == "Tunai":
                cur.execute("INSERT INTO cash (id_pembayaran) VALUES (%s)", (id_pembayaran,))
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
            conn.commit()

        else:
            kolom_update = {
                "1": "id_admin",
                "2": "id_unit",
                "3": "tanggal_peminjaman",
                "4": "tanggal_pengembalian",
                "5": "status_peminjaman",
                "6": "status_pembayaran"

            }[pilihan]

            cur.execute(
                f"UPDATE transaksi SET {kolom_update} = %s WHERE id_transaksi = %s",
                (nilai_baru, id_transaksi),
            )
            conn.commit()

        print(hijau_terang + "Data transaksi berhasil diperbarui!")
        input("Tekan Enter untuk melanjutkan...")

    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk kembali")
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def cekUnitAda(id_unit):
    try:
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        cur.execute("SELECT * FROM unit WHERE id_unit = %s", (id_unit,))
        hasil = cur.fetchone()[0]

        return hasil > 0
    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        return False

    finally:
        if conn is not None:
            cur.close()
            conn.close()


def cekTransaksiAda(id_transaksi):
    try:
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM transaksi WHERE id_transaksi = %s", (id_transaksi,)
        )

        hasil = cur.fetchone()
        return hasil is not None 

    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        return False 

    finally:
        if conn is not None:
            cur.close()
            conn.close()
def hapusTransaksi():
    conn = None
    cur = None
    try:
        headerBonsa()
        lihatTransaksiSaja()
        print("Hapus Transaksi:")

        while True:
            try:
                id_transaksi = int(input("Masukkan ID transaksi yang akan dihapus: "))
                if cekTransaksiAda(id_transaksi):
                    break
                else:
                    print(merah_terang + "ID transaksi tidak valid.")
            except ValueError:
                print(merah_terang + "ID transaksi harus berupa angka.")
        while True:
            konfirmasi = input("Apakah Anda yakin ingin menghapus transaksi ini? (y/n): ")
            if konfirmasi.lower() in ['y', 'n']:
                break
            else:
                print("Pilihan tidak valid. Silakan pilih y atau n.")

        if konfirmasi.lower() == 'n':
            return

        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        cur.execute("SELECT id_pembayaran FROM transaksi WHERE id_transaksi = %s", (id_transaksi,))
        id_pembayaran = cur.fetchone()[0]


        cur.execute("DELETE FROM cash WHERE id_pembayaran = %s", (id_pembayaran,))
        cur.execute("DELETE FROM bank WHERE id_pembayaran = %s", (id_pembayaran,))
        cur.execute("DELETE FROM qris WHERE id_pembayaran = %s", (id_pembayaran,))

        cur.execute("DELETE FROM transaksi WHERE id_transaksi = %s", (id_transaksi,))

        cur.execute("DELETE FROM pembayaran WHERE id_pembayaran = %s", (id_pembayaran,))


        conn.commit()
        print(hijau_terang + "Transaksi berhasil dihapus!")
        input("Tekan Enter untuk melanjutkan...")
        clear()
    except (Exception, pg.DatabaseError) as error:
        print(f"Error: {error}")
        input("Enter untuk kembali")
    finally:
        if conn is not None:
            cur.close()
            conn.close()

def lihatDetailPembayaran():
    print(ungu_gelap+"="*128)
    print(putih_terang+"DETAIL PEMBAYARAN".center(128))
    print(putih_terang+"BONSA RENTAL PHOTOGRAPHY".center(128))
    print(ungu_gelap+ "="*128)
    try:
        lihatTransaksiSaja()
        params = config()
        conn = pg.connect(**params)
        cur = conn.cursor()

        id_transaksi = int(input("Masukkan ID transaksi: "))

        cur.execute(
            """
            SELECT t.id_transaksi as ID,t.tanggal_transaksi as "Tanggal Transaksi", c.nama as Customer,u.tipe_unit as unit, t.total_pembayaran as "Total Pembayaran", p.metode_pembayaran as Pembayaran, p.id_pembayaran, a.nama as Admin
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
            input("Enter untuk melanjutkan ")
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
