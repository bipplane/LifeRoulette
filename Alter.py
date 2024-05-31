from cryptography.fernet import Fernet
from PIL import Image
import os
import cv2


class Alter:
    def __init__(self, key_file="key.key"):
        self.key_file = key_file
        self.fernet = None

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
            raise ValueError("Encryption key not loaded.")

        with open(image_path, "rb") as file:
            data = file.read()

        encrypted_data = self.fernet.encrypt(data)

        with open(encrypted_path, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

    def decrypt_image(self, encrypted_path, decrypted_path):
        if not self.fernet:
            raise ValueError("Encryption key not loaded.")

        with open(encrypted_path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()

        decrypted_data = self.fernet.decrypt(encrypted_data)

        with open(decrypted_path, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)

    def add_watermark(self, image_path, watermark_text, output_path):
        image = Image.open(image_path)
        watermark = Image.new("RGBA", image.size, (255, 255, 255, 0))
        watermark_draw = ImageDraw.Draw(watermark)
        watermark_draw.text((10, 10), watermark_text, fill=(255, 255, 255, 128))

        watermarked_image = Image.alpha_composite(image.convert("RGBA"), watermark)
        watermarked_image = watermarked_image.convert("RGB")

        watermarked_image.save(output_path)

    def obfuscate_video(self, video_path, obfuscated_path):
        cap = cv2.VideoCapture(video_path)
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(obfuscated_path, fourcc, 30.0, (640, 480))

        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Apply some obfuscation techniques here
                # For example, blurring the frame
                blurred_frame = cv2.GaussianBlur(frame, (15, 15), 0)
                out.write(blurred_frame)
            else:
                break

        cap.release()
        out.release()


# Example usage:
secure_file_manager = Alter()
secure_file_manager.generate_key()
secure_file_manager.load_key()

# Encrypt an image
secure_file_manager.encrypt_image("image.jpg", "encrypted_image.jpg")

# Decrypt the encrypted image
secure_file_manager.decrypt_image("encrypted_image.jpg", "decrypted_image.jpg")

# Add watermark to an image
secure_file_manager.add_watermark("image.jpg", "Confidential", "watermarked_image.jpg")

# Obfuscate a video
secure_file_manager.obfuscate_video("video.mp4", "obfuscated_video.mp4")