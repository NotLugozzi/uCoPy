import os
import shutil
import threading
from tqdm import tqdm
import hashlib

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

def main():
    target = input("Enter the path or file to copy: ")
    destination = input("Enter the destination path: ")
    num_parallel = int(input("Enter the number of parallel copies (Recommended 20+ - Default Windows: 1): ") or 1)
    delete_target = input("Do you want to delete the source file? (yes/no, default is no): ").lower() == "yes"
    verify_checksum = input("Do you want to verify checksums for each copied file? (yes/no, default is no): ").lower() == "yes"

    files = get_files(target)
    print(f"Number of files to be copied: {len(files)}")
    if len(files) == 0:
        print("No files in the source")
        return

    process_files(files, destination, num_parallel, target, verify_checksum)
    print("Files copied successfully!")

    if delete_target:
        shutil.rmtree(target)
        print("Source directory/file deleted.")

if __name__ == '__main__':
    main()
