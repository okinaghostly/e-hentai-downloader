import os
import re

def rename_images(folder):
    if not os.path.isdir(folder):
        print(f"Invalid path: {folder}")
        return

    files = os.listdir(folder)
    images = [file for file in files if file.lower().endswith(('.jpg', '.png', '.gif'))]

    for old_name in images:
        old_path = os.path.join(folder, old_name)

        # Regular expression to capture the number after the last "-"
        match = re.search(r'-([0-9]+)\.(jpg|png)$', old_name, re.IGNORECASE)
        if not match:
            print(f"Filename doesn't match expected pattern: {old_name}")
            continue

        final_number = match.group(1)
        extension = match.group(2).lower()

        new_name = f"{final_number}.{extension}"
        new_path = os.path.join(folder, new_name)

        # Avoid overwriting existing files
        if os.path.exists(new_path):
            print(f"Warning: {new_name} already exists, skipping.")
            continue

        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} → {new_name}")

# Example usage:
folder_input = input("Folder: ")
rename_images(folder_input)
