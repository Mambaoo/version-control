import os
import shutil
import logging
from datetime import datetime
import configparser

logging.basicConfig(filename='backup_log.txt', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def read_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config.read(config_file)

    source_folder = config.get('settings', 'source_folder')
    backup_location = config.get('settings', 'backup_location')
    
    file_extension_filter = config.get('settings', 'file_extension_filter', fallback="")
    if file_extension_filter:
        file_extension_filter = file_extension_filter.split(',')

    return source_folder, backup_location, file_extension_filter

def backup_folder(source_folder, backup_location, file_extension_filter=None):
    if not os.path.exists(source_folder):
        logging.error(f"Folder sumber '{source_folder}' tidak ditemukan.")
        print(f"Folder sumber '{source_folder}' tidak ditemukan.")
        return

    if not os.path.exists(backup_location):
        logging.error(f"Lokasi cadangan '{backup_location}' tidak ditemukan.")
        print(f"Lokasi cadangan '{backup_location}' tidak ditemukan.")
        return

    free_space = shutil.disk_usage(backup_location).free
    if free_space < 500 * 1024 * 1024:
        logging.error("Ruang penyimpanan tidak cukup untuk melakukan backup.")
        print("Ruang penyimpanan tidak cukup untuk melakukan backup.")
        return

    day_name = datetime.now().strftime("%A").lower()  
    day = datetime.now().strftime("%d")  
    month = datetime.now().strftime("%m")  
    year = datetime.now().strftime("%Y") 

    backup_folder_name = f"backup_{day_name}_{day}_{month}_{year}"
    backup_path = os.path.join(backup_location, backup_folder_name)

    try:
        os.makedirs(backup_path)

        total_files_copied = 0
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                if file_extension_filter:
                    if not file.lower().endswith(tuple(file_extension_filter)):
                        continue

                source_file = os.path.join(root, file)
                relative_path = os.path.relpath(root, source_folder)
                target_dir = os.path.join(backup_path, relative_path)

                os.makedirs(target_dir, exist_ok=True)
                shutil.copy2(source_file, target_dir)
                total_files_copied += 1

        if total_files_copied > 0:
            logging.info(f"Backup berhasil! {total_files_copied} file disalin ke folder cadangan: {backup_path}")
            print(f"Backup berhasil! {total_files_copied} file disalin ke folder cadangan: {backup_path}")
        else:
            logging.warning("Tidak ada file yang disalin. Mungkin tidak ada file yang cocok dengan filter ekstensi.")
            print("Tidak ada file yang disalin. Mungkin tidak ada file yang cocok dengan filter ekstensi.")

    except Exception as e:
        logging.error(f"Terjadi kesalahan saat backup: {e}")
        print(f"Terjadi kesalahan saat backup: {e}")

def main():
    source_folder, backup_location, file_extension_filter = read_config()
    backup_folder(source_folder, backup_location, file_extension_filter)

if __name__ == "__main__":
    main()
