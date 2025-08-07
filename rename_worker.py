import sys
import os

def change_file_name(file_path, new_name):
    """Change the file name to the new name."""
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return False
    
    directory = os.path.dirname(file_path)
    new_file_path = os.path.join(directory, new_name)
    try:
        os.rename(file_path, new_file_path)
        print(f"File renamed to {new_file_path}")
        return True
    except Exception as e:
        print(f"Error renaming file: {e}")
        return False

if __name__ == "__main__":
    print("This script is not meant to be run directly.")