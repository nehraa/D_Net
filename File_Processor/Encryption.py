from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# Function to generate a random symmetric AES key for CTR mode encryption
def generate_symmetric_key():
    '''
    Generates a 256-bit AES key for symmetric encryption.
    - No parameters are required.
    - Returns a random 256-bit key (32 bytes) to be used in AES encryption/decryption.
    '''
    # Generate a random 256-bit key (32 bytes) using os.urandom (ideal for cryptographic use)
    key = os.urandom(32)  # AES key size for AES-256
    return key  # Return the generated key


# Function to encrypt data using AES in CTR mode
def encrypt(data, key):
    '''
    Encrypts the provided data using AES in CTR mode.
    - Parameters:
      - data: A tuple (file_data, file_name, file_extension), where:
        - file_data (str): The content of the file to encrypt.
        - file_name (str): The name of the file.
        - file_extension (str): The file's extension.
      - key (bytes): The AES encryption key (256-bit).
      
    - Returns:
      - A tuple containing:
        1. nonce (bytes): A randomly generated 16-byte nonce for the CTR mode.
        2. encrypted_data (bytes): The encrypted data of the file.
        3. file_name (str): The original file name.
        4. file_extension (str): The original file extension.
    '''
    # Unpack the input data tuple into individual components.
    file_data, file_name, file_extension = data

    # Generate a random nonce (IV) for CTR mode (ensures unique encryption for each file)
    nonce = os.urandom(16)  # AES block size for CTR is 16 bytes (128-bit).

    # Create the AES cipher in CTR mode using the generated key and nonce
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    encryptor = cipher.encryptor()  # Create an encryptor object from the cipher.

    # Encrypt the file data (convert string data to bytes before encryption)
    encrypted_data = encryptor.update(file_data.encode('utf-8')) + encryptor.finalize()

    # Return the encrypted data as a tuple containing the nonce, encrypted data, file name, and extension.
    encrypted_tuple = (nonce, encrypted_data, file_name, file_extension)
    return encrypted_tuple


# Function to decrypt data using AES in CTR mode
def decrypt(encrypted_tuple, key):
    '''
    Decrypts the encrypted data using AES in CTR mode.
    - Parameters:
      - encrypted_tuple: A tuple (nonce, encrypted_data, file_name, file_extension), where:
        - nonce (bytes): The nonce used for encryption.
        - encrypted_data (bytes): The data to decrypt.
        - file_name (str): The name of the file.
        - file_extension (str): The file extension.
      - key (bytes): The AES key (256-bit) used for decryption.
      
    - Returns:
      - A tuple containing:
        1. decrypted_data (str): The decrypted data as a string.
        2. file_name (str): The name of the file.
        3. file_extension (str): The file's extension.
    '''
    # Unpack the input tuple into individual components.
    nonce, encrypted_data, file_name, file_extension = encrypted_tuple

    # Create the AES cipher in CTR mode using the nonce (IV) and the same key used for encryption.
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce), backend=default_backend())
    decryptor = cipher.decryptor()  # Create a decryptor object from the cipher.

    # Decrypt the encrypted data (the data is in bytes and will be decrypted back to the original data)
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Decode the decrypted data back into a string and return the decrypted content with the file name and extension.
    return decrypted_data.decode('utf-8'), file_name, file_extension
