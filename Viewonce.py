import os
import time

class Viewonce:
    def __init__(self):
        self.opened_files = {}

    def open_file(self, file_path):
        try:
            print(f"Attempting to open file: {file_path}")

            # Check if the file exists
            if not os.path.isfile(file_path):
                raise FileNotFoundError("File not found.")

            if file_path in self.opened_files:
                raise ValueError("File has already been opened once.")

            # Open the file in binary mode
            file = open(file_path, 'rb')
            self.opened_files[file_path] = file
            print(f"File {file_path} opened successfully.")

            # Simulate some activity on the file
            time.sleep(2)  # Simulating file processing time

            return file

        except FileNotFoundError as e:
            print(f"Error: {e}")

        except ValueError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def close_file(self, file_path):
        try:
            if file_path not in self.opened_files:
                raise ValueError("File is not open or has already been closed.")

            # Close the file
            self.opened_files[file_path].close()
            print(f"File {file_path} closed successfully.")

            # Remove the file from the opened_files set
            del self.opened_files[file_path]

            # Delete the file from disk
            os.remove(file_path)
            print(f"File '{file_path}' has expired and has been deleted.")

        except ValueError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"Error while expiring file: {e}")

# Example usage:
file_expire = Viewonce()
file_path = "PS1_Setup_Guide (1).mp4"

# Create a test file if it doesn't exist
if not os.path.isfile(file_path):
    with open(file_path, 'wb') as f:
        f.write(os.urandom(1024))  # Creating a dummy binary file for testing

# Open the file for the first time
file = file_expire.open_file(file_path)

# Manually close the file and delete it
if file:
    file_expire.close_file(file_path)

# Try to open the same file again
file_expire.open_file(file_path)
