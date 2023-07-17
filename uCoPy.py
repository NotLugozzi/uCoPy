import os
import shutil
import threading
import json
import hashlib
import argparse
import platform
import psutil
from tqdm import tqdm

def transfer_file(source, destination):
    shutil.copy2(source, destination)

def calculate_sha256(file):
    hash_obj = hashlib.sha256()
    with open(file, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def process_files(files, destination, num_parallel, target, verify_checksum):
    total_size_bytes = sum(get_file_size(file) for file in files)
    total_size_mb = total_size_bytes / (1024 * 1024)  # Convert bytes to megabytes
    progress_bar = tqdm(total=total_size_mb, unit='MB', desc='Progress')

    num_verification_errors = 0

    def transfer_wrapper(file):
        nonlocal num_verification_errors

        relative_path = os.path.relpath(file, start=target)
        destination_file = os.path.join(destination, relative_path)
        os.makedirs(os.path.dirname(destination_file), exist_ok=True)
        transfer_file(file, destination_file)
        progress_bar.update(get_file_size(file) / (1024 * 1024))  # Update progress by adding transferred file size in megabytes

        if verify_checksum:
            source_checksum = calculate_sha256(file)
            dest_checksum = calculate_sha256(destination_file)
            if source_checksum != dest_checksum:
                num_verification_errors += 1
                print(f"Checksum verification failed for file: {file}")

    threads = []
    for file in files:
        thread = threading.Thread(target=transfer_wrapper, args=(file,))
        thread.start()
        threads.append(thread)

        # Limit parallel transfers
        if len(threads) >= num_parallel:
            for t in threads:
                t.join()
            threads.clear()

    for thread in threads:
        thread.join()

    progress_bar.close()

    if verify_checksum and num_verification_errors == 0:
        print(f"Checksums verified successfully, 0 errors in {len(files)} items")

def get_files(target):
    files = []
    if os.path.isfile(target):
        files.append(target)
    elif os.path.isdir(target):
        for dirpath, _, filenames in os.walk(target):
            for filename in filenames:
                files.append(os.path.join(dirpath, filename))
    return files

def get_file_size(file):
    return os.path.getsize(file)

def calculate_progress(target, destination):
    target_size = sum(get_file_size(file) for file in target)
    destination_size = sum(get_file_size(file) for file in destination)
    target_size_mb = target_size / (1024 * 1024)  # Convert bytes to megabytes
    destination_size_mb = destination_size / (1024 * 1024)  # Convert bytes to megabytes
    return (destination_size_mb / target_size_mb) * 100

def print_system_info(version):
    cpu_info = platform.processor()
    ram_info = psutil.virtual_memory().total
    max_threads = psutil.cpu_count(logical=True)
    os_version = platform.platform()

    print(f"Program Version: {version}")
    print(f"OS: {os_version}")
    print(f"CPU: {cpu_info}")
    print(f"RAM: {ram_info/1024**3:.2f} GB")
    print(f"CPU Threads: {max_threads}")

    if ram_info <= 16 * 1024**3 and max_threads <= 8:
        max_thread = 200
    elif ram_info <= 15* 1024**3 and max_threads >= 8:
        max_thread = 450
    elif 16 * 1024**3 < ram_info <= 32 * 1024**3 and max_threads >= 8:
        max_thread = 600
    elif 32 * 1024**3 < ram_info <= 64 * 1024**3 and 8 < max_threads < 20:
        max_thread = 1000
    elif ram_info > 64 * 1024**3 and 16 < max_threads < 36:
        max_thread = 3000
    else:
        max_thread = "Unknown"
    return max_thread

def get_parallel(max_thread):
    while True:
        print(f"According to our tests, your PC can handle up to {max_thread} parallel threads")
        num_parallel = int(input("Enter the number of parallel copies (1 or greater): "))
        if num_parallel > 0 and num_parallel < max_thread:
            break
        else:
            print("Invalid number of parallel copies. Please try again.")
    return num_parallel

def main():
    parser = argparse.ArgumentParser(description='File Transfer Script')
    parser.add_argument('-s', '--source', help='Source file or directory')
    parser.add_argument('-d', '--destination', help='Destination directory')
    parser.add_argument('-C', '--cut', action='store_true', help='Delete the source file/folder after copying')
    parser.add_argument('-t', '--threads', type=int, default=0, help='Number of parallel copies')
    parser.add_argument('-ch', '--checksum', action='store_true', help='Verify checksums for each copied file')
    parser.add_argument('-v', '--version', default='1.0', help='Program version')

    args = parser.parse_args()

    if not args.source and not args.destination:
        source = input("Enter the path or file to copy: ")
        destination = input("Enter the destination path: ")
    else:
        source = args.source
        destination = args.destination

    num_parallel = args.threads
    delete_source = args.cut
    verify_checksum = args.checksum
    program_version = args.version

    if not verify_checksum:
        response = input("Do you want to verify checksums for each copied file? (yes/no, default is no): ").lower()
        if response == "yes":
            verify_checksum = True

    max_thread = print_system_info(program_version)
    num_parallel = get_parallel(max_thread)

    files = get_files(source)
    print(f"Number of files to be copied: {len(files)}")
    if len(files) == 0:
        print("No files in the source")
        return

    process_files(files, destination, num_parallel, source, verify_checksum)
    print("Files copied successfully!")

    if delete_source:
        if os.path.isfile(source):
            os.remove(source)
        elif os.path.isdir(source):
            shutil.rmtree(source)
        print("Source directory/file deleted.")

if __name__ == '__main__':
    main()
