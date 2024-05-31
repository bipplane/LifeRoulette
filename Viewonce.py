import os
import time

class Viewonce:
    def __init__(self):
        self.opened_files = set()

    def open_file(self, file_path):
        try:
            print(f"Attempting to open file: {file_path}")

            # Check if the file exists
            if not os.path.isfile(file_path):
                raise FileNotFoundError("File not found.")

            if file_path in self.opened_files:
                raise ValueError("File has already been opened once.")

            # Track the file as being opened
            self.opened_files.add(file_path)
            print(f"File {file_path} opened successfully.")

            # Simulate some activity on the file
            time.sleep(2)  # Simulating file processing time

            # After processing, mark the file for deletion
            self.expire_file(file_path)

        except FileNotFoundError as e:
            print(f"Error: {e}")

        except ValueError as e:
            print(f"Error: {e}")

    def expire_file(self, file_path):
        try:
            # Delete the file from disk
            os.remove(file_path)
            print(f"File '{file_path}' has expired and has been deleted.")
        except Exception as e:
            print(f"Error while expiring file: {e}")

# Example usage:
file_expire = Viewonce()
file_path = "msg-4282916410-45324.ogg"

# Create a test file
# with open(file_path, 'w') as f:
#    f.write("This is a test file.")

# Open the file for the first time
file_expire.open_file(file_path)

# Try to open the same file again
file_expire.open_file(file_path)
