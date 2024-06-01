import encryptor
import Alter
import Viewonce

def main():
    while True:
        print("\nSelect an operation:")
        print("1. Viewonce")
        print("2. Image Encryptor/Watermarker")
        print("3. Exit")

        choice = input("Enter the number corresponding to your choice: ")

        if choice == '1':
            viewonce_menu()
        elif choice == '2':
            encryptor_alter_menu()
        elif choice == '3':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please select a valid operation.")

def viewonce_menu():
    vo = Viewonce
    print("\nSelect an operation for ViewOnce:")
    print("1. Simulate Database Decryption")
    print("2. Simulate Database Encryption")
    print("3. Back to Main Menu")

    choice = input("Enter the number corresponding to your choice: ")

    if choice == '1':
        #vo.simulate_database_dec() - Function is not working as intended, thus commented out to show the workflow process instead.
        print("Database decryption simulated.")
    elif choice == '2':
        #vo.simulate_database_enc() - Function is not working as intended, thus commented out to show the workflow process instead.
        print("Database encryption simulated.")
    elif choice == '3':
        return
    else:
        print("Invalid choice. Please select a valid operation.")

def encryptor_alter_menu():
    enc = encryptor
    alt = Alter

    print("\nSelect an operation for Encryptor/Alter:")
    print("1. Encrypt an Image")
    print("2. Add Watermark to an Image")
    print("3. Back to Main Menu")

    choice = input("Enter the number corresponding to your choice: ")

    if choice == '1':
        img = input("Enter the image filename (e.g., '7.png'): ")
        output_file = 'encrypted_' + img
        enc.generate_key()
        enc.load_key()
        enc.encrypt_image(img, output_file)
        print(f"Image encrypted and saved to {output_file}")
    elif choice == '2':
        img = input("Enter the image filename (e.g., '7.png'): ")
        text = input("Enter the watermark text (e.g., 'Confidential'): ")
        output_file = 'watermarked_' + img
        alt.add_watermark(img, text, output_file)
        print(f"Watermarked image saved to {output_file}")
    elif choice == '3':
        return
    else:
        print("Invalid choice. Please select a valid operation.")

if __name__ == "__main__":
    main()
