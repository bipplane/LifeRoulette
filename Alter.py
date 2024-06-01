import pygetwindow as gw
import time
import os
from PIL import Image, ImageDraw
import mimetypes


# Function to overlay an image with black
def overlay_with_black(image_path):
    img = Image.open(image_path)
    width, height = img.size
    black = Image.new('RGBA', (width, height), (0, 0, 0, 255))
    img.paste(black, (0, 0), black)
    img.save(image_path)


# Function to detect file type and overlay with black accordingly
def protect_file(file_path):
    file_type, _ = mimetypes.guess_type(file_path)
    if file_type:
        file_type = file_type.split('/')[0]  # Get the general type (e.g., image, video, application)

        if file_type == 'image':
            overlay_with_black(file_path)
        elif file_type == 'video':
            overlay_with_black(file_path)
        elif file_type == 'application':
            # For documents, convert them to images first, then overlay with black
            # You'll need to use appropriate libraries for document conversion (e.g., PyMuPDF for PDF)
            # Here, I'll simply treat unknown application files as images
            overlay_with_black(file_path)
        else:
            print(f"Unsupported file type: {file_type}")
    else:
        print("Unknown file type")


# Function to periodically check for screenshot
def detect_screenshot(file_path):
    prev_screenshot = None
    while True:
        # Capture screen
        screenshot = gw.getWindowsWithTitle('Screen')[0].screenshot()

        # Compare with previous screenshot
        if prev_screenshot is not None and prev_screenshot.tobytes() != screenshot.tobytes():
            print("Screenshot detected!")
            protect_file(file_path)

        prev_screenshot = screenshot
        time.sleep(1)  # Adjust the interval as needed


# Example usage
if __name__ == "__main__":
    file_path = "your_file_path"  # Replace "your_file_path" with the path to your file
    if os.path.exists(file_path):
        detect_screenshot(file_path)
    else:
        print("File not found!")