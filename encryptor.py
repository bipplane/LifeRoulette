from cryptography.fernet import Fernet
from PIL import Image, ImageDraw
import io
import os
import cv2
import shelve
import numpy as np

class SecureFileManager:
    def __init__(self, key_file="key.txt"):
        self.key_file = key_file
        self.fernet = None

    def startmenu(self):
        print("Select an operation:")
        print("1. Encrypt an Image")
        print("2. Decrypt an Encrypted Image")
        print("3. Add Watermark to an Image")

        choice = input("Enter the number corresponding to your choice: ")

        if choice == '1':
            img = input("Enter the image filename (e.g., '7.png'): ")
            output_file = 'encrypted_' + img
            self.encrypt_image(img, output_file)
            print(f"Image encrypted and saved to {output_file}")
        elif choice == '2':
            input_file = input("Enter the encrypted image filename (e.g., 'encrypted_7.png'): ")
            output_file = input_file.replace('encrypted_', 'decrypted_')
            self.decrypt_image(input_file, output_file)
            print(f"Image decrypted and saved to {output_file}")
        elif choice == '3':
            img = input("Enter the image filename (e.g., '7.png'): ")
            text = input("Enter the watermark text (e.g., 'Confidential'): ")
            output_file = 'watermarked_' + img
            self.add_watermark(img, text, output_file)
            print(f"Watermarked image saved to {output_file}")
        else:
            print("Invalid choice. Please select a valid operation.")
    def persistent_storage(self):
        # Open an image file
        image = Image.open('C:/Users/limca/PycharmProjects/7.jpg')

    # Convert image to byte array
        #byte_arr = io.BytesIO()
        #image.save(byte_arr, format='JPEG')
        #image_bytes = byte_arr.getvalue()

    # Store byte array in shelve
        #with shelve.open('image_shelf.db') as db:
        #db['image'] = image_bytes

        #db.close() # always MANUALLY close the storage after usage,


    def generate_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)

    def load_key(self):
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as key_file:
                key = key_file.read()
                self.fernet = Fernet(key)
        else:
            raise FileNotFoundError("Key file not found.")

    def encrypt_image(self, image_path, encrypted_path):
        if not self.fernet:
            return "Encryption key not loaded. Cannot encrypt image for security reasons."

        with open(image_path, "rb") as file:
            data = file.read()

        encrypted_data = self.fernet.encrypt(data)

        with open(encrypted_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

    def decrypt_image(self, encrypted_path, decrypted_path, decryption_key=None):
        if not decryption_key:
            decryption_key = input("Enter decryption key: ").encode()

        # Read the stored key
        with open(self.key_file, "rb") as key_file:
            stored_key = key_file.read()

        if decryption_key != stored_key:
            print("Incorrect decryption key. Cannot decrypt image.")
            return

        fernet = Fernet(decryption_key)

        with open(encrypted_path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()

        decrypted_data = self.fernet.decrypt(encrypted_data)

        with open(decrypted_path, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)

    def add_watermark(self, image_path, watermark_text, output_path):
        if self.fernet:
            return "Image is encrypted. Cannot add watermark for security reasons."

        image = Image.open(image_path).convert("RGBA")
        watermark = Image.new("RGBA", image.size, (255, 255, 255, 0))
        watermark_draw = ImageDraw.Draw(watermark)
        watermark_draw.text((10, 10), watermark_text, fill=(255, 255, 255, 128))

        watermarked_image = Image.alpha_composite(image, watermark)
        watermarked_image = watermarked_image.convert("RGB")

        watermarked_image.save(output_path)
        return watermarked_image

    def obfuscate_video(self, video_path, obfuscated_path):
        cap = cv2.VideoCapture(video_path)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(obfuscated_path, fourcc, 30.0, (frame_width, frame_height))

        # Create watermark
        watermark_text = "Confidential"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        thickness = 3
        text_size = cv2.getTextSize(watermark_text, font, font_scale, thickness)[0]
        text_x = (frame_width - text_size[0]) // 2
        text_y = (frame_height + text_size[1]) // 2

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Apply blurring
                blurred_frame = cv2.GaussianBlur(frame, (51, 51), 0)

                # Apply watermark
                cv2.putText(blurred_frame, watermark_text, (text_x, text_y), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

                out.write(blurred_frame)
            else:
                break

        cap.release()
        out.release()

# Example usage:
secure_file_manager = SecureFileManager()
secure_file_manager.generate_key()
secure_file_manager.load_key()

secure_file_manager.startmenu()
# # Encrypt an image
# secure_file_manager.encrypt_image("7.png", "encrypted_7.png")
#
# # Decrypt the encrypted image
# secure_file_manager.decrypt_image("encrypted_7.png", "decrypted_7.png")
#
# # Add watermark to an image
# secure_file_manager.add_watermark("7.png", "Confidential", "watermarked_7.png")

# Create and obfuscate a sample video
def create_sample_video(video_path):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, 30.0, (640, 480))

    for i in range(100):
        frame = cv2.putText(
            np.zeros((480, 640, 3), dtype=np.uint8),
            f'Frame {i}',
            (100, 240),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )
        out.write(frame)

    out.release()

# create_sample_video("video.mp4")
# secure_file_manager.obfuscate_video("video.mp4", "obfuscated_video.mp4")
#
# # To check the result, you can play the obfuscated video using OpenCV or any media player
# cap = cv2.VideoCapture('obfuscated_video.mp4')
#
# while cap.isOpened():
#     ret, frame = cap.read()
#     if ret:
#         cv2.imshow('Obfuscated Video', frame)
#         if cv2.waitKey(30) & 0xFF == ord('q'):
#             break
#     else:
#         break
#
# cap.release()
# cv2.destroyAllWindows()
