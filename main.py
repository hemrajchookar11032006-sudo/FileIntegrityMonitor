import os
import json
import hashlib
from datetime import datetime

BASELINE_FILE = "baseline.json"
LOG_FILE = "activity.log"


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while True:
                data = file.read(4096)
                if not data:
                    break
                sha256.update(data)

        return sha256.hexdigest()

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def log_activity(message):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write(f"[{time}] {message}\n")


def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        return {}

    try:
        with open(BASELINE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return {}


def save_baseline(baseline):
    with open(BASELINE_FILE, "w", encoding="utf-8") as file:
        json.dump(baseline, file, indent=4)


def create_baseline(folder):
    baseline = {}

    if not os.path.exists(folder):
        print("Folder does not exist.")
        return

    for root, directories, files in os.walk(folder):

        for filename in files:
            file_path = os.path.abspath(os.path.join(root, filename))

            try:
                file_hash = calculate_hash(file_path)

                if file_hash:
                    baseline[file_path] = file_hash

            except Exception as e:
                print(f"Could not process {file_path}: {e}")

    save_baseline(baseline)

    log_activity(f"Baseline created for folder: {folder}")

    print("\nBaseline created successfully.")
    print(f"Files recorded: {len(baseline)}")


def check_integrity(folder):
    baseline = load_baseline()

    if not baseline:
        print("No baseline found.")
        print("Create a baseline first.")
        return

    current_files = {}

    for root, directories, files in os.walk(folder):

        for filename in files:
            file_path = os.path.abspath(os.path.join(root, filename))

            # Ignore project files
            if file_path.endswith(BASELINE_FILE) or file_path.endswith(LOG_FILE):
                continue

            file_hash = calculate_hash(file_path)

            if file_hash:
                current_files[file_path] = file_hash

    modified = []
    deleted = []
    new_files = []

    # Check modified and deleted files
    for file_path, old_hash in baseline.items():

        if file_path not in current_files:
            deleted.append(file_path)

        elif current_files[file_path] != old_hash:
            modified.append(file_path)

    # Check new files
    for file_path in current_files:

        if file_path not in baseline:
            new_files.append(file_path)

    print("\n========================================")
    print("        FILE INTEGRITY CHECK")
    print("========================================")

    if not modified and not deleted and not new_files:
        print("\nSTATUS: SAFE")
        print("No changes detected.")

        log_activity("Integrity check completed - No changes detected.")

    else:
        print("\nSTATUS: WARNING - CHANGES DETECTED")

        if modified:
            print("\n[MODIFIED FILES]")
            for file_path in modified:
                print("-", file_path)
                log_activity(f"MODIFIED: {file_path}")

        if deleted:
            print("\n[DELETED FILES]")
            for file_path in deleted:
                print("-", file_path)
                log_activity(f"DELETED: {file_path}")

        if new_files:
            print("\n[NEW FILES]")
            for file_path in new_files:
                print("-", file_path)
                log_activity(f"NEW FILE: {file_path}")

    print("\n========================================")


def main():

    print("========================================")
    print("      FILE INTEGRITY MONITOR")
    print("========================================")

    while True:

        print("\n1. Create Baseline")
        print("2. Check File Integrity")
        print("3. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":

            folder = input("Enter folder path to monitor: ").strip()

            folder = folder.strip('"')

            create_baseline(folder)

        elif choice == "2":

            folder = input("Enter folder path to check: ").strip()

            folder = folder.strip('"')

            check_integrity(folder)

        elif choice == "3":

            print("\nExiting...")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()