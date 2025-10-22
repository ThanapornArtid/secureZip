import gzip
import shutil
from cryptography.fernet import Fernet

# Step1 create sample text file
with open("/Users/thanapornartidtayamontol/Documents/SecureZip/test.txt", "w") as f:
    f.write("Test Ngab")
#Step 2 Compress file using Gzip
with open("/Users/thanapornartidtayamontol/Documents/SecureZip/test.txt","rb") as f_in: # ใส้่path original file
      with gzip.open("sample.txt.gz","wb") as f_out:
          shutil.copyfileobj(f_in,f_out)
print("Successfully compressed file")

# step3 Generate key for encryption
key = Fernet.generate_key() # create encrypt key
with open("secret.key", "wb") as key_file: #open file to store key
    key_file.write(key) 

    print("Key generated and saved to secret.key")
    
# step4 Encrypt the compressed file
fernet =Fernet(key)  
with open("sample.txt.gz","rb") as file:
    original = file.read() #read
encrypted = fernet.encrypt(original) #encrypt
with open("sample.txt.gz.enc","wb") as encrypted_file:
    encrypted_file.write(encrypted) #write
print("File encrypted and saved ja!!")

# Step 5 Decrypt the file
with open("sample.txt.gz.enc", "rb") as enc_file:
    encrypted_content = enc_file.read()
decrypted_data = fernet.decrypt(encrypted_content)

with open("decrypted_sample.txt.gz", "wb") as dec_file:
    dec_file.write(decrypted_data)
print("Decrypted file successfully")


# Step 6 Decompress the file
with gzip.open("decrypted_sample.txt.gz", "rb") as f_in: 
    with open("final_sample.txt", "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

print("File decrypted and decompressed successfully.")