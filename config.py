import configparser
def config():
    config = configparser.ConfigParser()
    try:
        with open("D:/Kuliah/SBD/Bonsa Rental/repository/database_bonsa.ini", 'r') as config_file:
            config.read_file(config_file)
        return {
            'database': config['postgresql']['database'],
            'user': config['postgresql']['user'],
            'password': config['postgresql']['password'],
            'host': config['postgresql']['host']
        }

    except (configparser.NoSectionError, KeyError, FileNotFoundError) as e:
        print(f"Error membaca konfigurasi database: {e}")
        return None  