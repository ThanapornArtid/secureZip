import gzip
from cryptography.fernet import Fernet
import os

KEY_FILE = "secret.key"

def generate_key():
    
    #Generates a new encryption key and save to 'secret.key'
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key() # create encrypt key
        with open(KEY_FILE, "wb") as key_file: #open file to store key
            key_file.write(key)
        print(f"Key generated and saved to {KEY_FILE}")
    else:
        print(f"{KEY_FILE} already exists. Not generating a new one.")

def load_key():
    
    #Loads the encryption key from 'secret.key'
    try:
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print(f"Error: {KEY_FILE} not found. Run generate_key() first.")
        return None

def save_secure(original_file_path, encrypted_output_path):

    #Compresses and encrypts file
    key = load_key()
    if not key:
        return

    fernet = Fernet(key)
    
    # Step 1 & 2: Read and Compress file
    print(f"Compressing {original_file_path}...")
    with open(original_file_path, "rb") as f_in:
        original_data = f_in.read()
    
    # compress directly in memory 
    compressed_data = gzip.compress(original_data)
    print("Successfully compressed data.")

    # Step 3: Encrypt file
    print(f"Encrypting data to {encrypted_output_path}...")
    encrypted = fernet.encrypt(compressed_data)
    with open(encrypted_output_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted)
    print("File encrypted and saved successfully!")

def open_secure(encrypted_input_path, decrypted_output_path):

    #Decrypts and decompresses file

    key = load_key()
    if not key:
        return

    fernet = Fernet(key)

    # Step 4: Decrypt file
    print(f"Decrypting {encrypted_input_path}...")
    with open(encrypted_input_path, "rb") as enc_file:
        encrypted_content = enc_file.read()
    
    try:
        decrypted_data = fernet.decrypt(encrypted_content)
        print("Decrypted data successfully.")
    except Exception as e:
        print(f"Error decrypting file: {e}. Check if the key is correct.")
        return

    # Step 5: Decompress file
    print(f"Decompressing data to {decrypted_output_path}...")
    # Decompress from the in-memory variable
    decompressed_data = gzip.decompress(decrypted_data)
    
    with open(decrypted_output_path, "wb") as f_out:
        f_out.write(decompressed_data)
    
    print("File decrypted and decompressed successfully.")


#TEST

with open("test2.txt", "w") as f:
    f.write("test ka")

generate_key()

print("SAVE")
save_secure(original_file_path="test2.txt", 
            encrypted_output_path="sample.txt.gz.enc")

print("OPEN")
open_secure(encrypted_input_path="sample.txt.gz.enc", 
            decrypted_output_path="final_sample.txt")

with open("final_sample.txt", "r") as f:
    print(f"\nContent of final file: '{f.read()}'")