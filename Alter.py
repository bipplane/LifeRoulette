import os
import time
from PIL import Image, ImageGrab


# Function to overlay an image with black
def overlay_with_black(image):
    width, height = image.size
    black = Image.new('RGBA', (width, height), (0, 0, 0, 255))
    return Image.alpha_composite(image.convert("RGBA"), black)


# Function to detect screenshot of the specified file and overlay with black
def detect_screenshot(file_path):
    # Load the original image
    original_image = Image.open(file_path)

    while True:
        # Capture screen
        screenshot = ImageGrab.grab()

        # Compare with original image
        if screenshot.tobytes() != original_image.tobytes():
            print("Screenshot detected!")

            # Overlay with black
            black_image = overlay_with_black(screenshot)

            # Show the black image (you can also save it if needed)
            black_image.show()

        time.sleep(1)  # Adjust the interval as needed


# Example usage
if __name__ == "__main__":
    file_path = "/Users/NgYinZi_1/All my stuff/Screenshots/Tester 2.png"  # Replace with the path to your file
    if os.path.exists(file_path):
        detect_screenshot(file_path)
    else:
        print("File not found!")