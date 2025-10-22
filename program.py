import gzip
import shutil
from cryptography.fernet import Fernet
import os # Added for checking if key file exists

KEY_FILE = "secret.key"

def generate_key():
    """
    Generates a new encryption key and saves it to 'secret.key'.
    You only need to run this function ONCE.
    """
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key() # create encrypt key
        with open(KEY_FILE, "wb") as key_file: #open file to store key
            key_file.write(key)
        print(f"Key generated and saved to {KEY_FILE}")
    else:
        print(f"{KEY_FILE} already exists. Not generating a new one.")

def load_key():
    """
    Loads the encryption key from 'secret.key'.
    """
    try:
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        print(f"Error: {KEY_FILE} not found. Run generate_key() first.")
        return None

def save_secure(original_file_path, encrypted_output_path):
    """
    Automatically compresses and encrypts a file.
    This is your "save" function.
    """
    key = load_key()
    if not key:
        return

    fernet = Fernet(key)
    
    # --- Step 1 & 2: Read and Compress (in memory) ---
    print(f"Compressing {original_file_path}...")
    with open(original_file_path, "rb") as f_in:
        original_data = f_in.read()
    
    # We can compress directly in memory instead of making a temp .gz file
    compressed_data = gzip.compress(original_data)
    print("Successfully compressed data.")

    # --- Step 3: Encrypt ---
    print(f"Encrypting data to {encrypted_output_path}...")
    encrypted = fernet.encrypt(compressed_data)
    with open(encrypted_output_path, "wb") as encrypted_file:
        encrypted_file.write(encrypted)
    print("File encrypted and saved successfully!")

def open_secure(encrypted_input_path, decrypted_output_path):
    """
    Automatically decrypts and decompresses a file.
    This is your "open" function.
    """
    key = load_key()
    if not key:
        return

    fernet = Fernet(key)

    # --- Step 4: Decrypt ---
    print(f"Decrypting {encrypted_input_path}...")
    with open(encrypted_input_path, "rb") as enc_file:
        encrypted_content = enc_file.read()
    
    try:
        decrypted_data = fernet.decrypt(encrypted_content)
        print("Decrypted data successfully.")
    except Exception as e:
        print(f"Error decrypting file: {e}. Check if the key is correct.")
        return

    # --- Step 5: Decompress ---
    print(f"Decompressing data to {decrypted_output_path}...")
    # We decompress from the in-memory variable
    decompressed_data = gzip.decompress(decrypted_data)
    
    with open(decrypted_output_path, "wb") as f_out:
        f_out.write(decompressed_data)
    
    print("File decrypted and decompressed successfully.")


# --- HOW TO USE YOUR NEW PROGRAM ---

# 1. First, create your test file (like your step 1)
with open("test.txt", "w") as f:
    f.write("testttttttt toooooooooo")

# 2. IMPORTANT: Run this one time to create your key
generate_key()

print("\n--- Testing SAVE function ---")
# 3. This is your "save" command
# It automatically compresses and encrypts "test.txt"
save_secure(original_file_path="test.txt", 
            encrypted_output_path="sample.txt.gz.enc")

print("\n--- Testing OPEN function ---")
# 4. This is your "open" command
# It automatically decrypts and decompresses "sample.txt.gz.enc"
open_secure(encrypted_input_path="sample.txt.gz.enc", 
            decrypted_output_path="final_sample.txt")

# 5. Check the result
with open("final_sample.txt", "r") as f:
    print(f"\nContent of final file: '{f.read()}'")