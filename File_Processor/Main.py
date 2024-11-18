import Encoder
import Encryption
import Sharding

'''
Uploads a file by compressing, encrypting, and sharding the data.

Parameters:
    - file_path (str): The path to the file that needs to be uploaded.

Returns:
    - Shards (list of bytes): A list of shards representing the encrypted, compressed data split into chunks.
'''
def Upload(file_path):
    # Step 1: Compress the file using the Encoder module.
    compressed_data = Encoder.compress_file(file_path)
    
    # Step 2: Generate a symmetric key for encryption.
    key = Encryption.generate_symmetric_key()
    
    # Step 3: Encrypt the compressed data using the generated symmetric key.
    encrypted_data = Encryption.encrypt(compressed_data, key)
    
    # Step 4: Shard the encrypted data into chunks of size 1024 bytes using the Sharding module.
    Shards = Sharding.shard_data(encrypted_data, 1024)
    
    # Return the list of shards for storage or transmission.
    return Shards

'''
Downloads a file by reconstructing, decrypting, and decompressing the data.

Parameters:
    - Shards (list of bytes): The list of shards representing the encrypted, compressed data.
    - key (bytes): The symmetric key used for decryption.

Returns:
    - decompressed_data (bytes): The original file data after decompression.
'''
def Download(Shards, key):
    # Step 1: Reconstruct the encrypted data from the shards using the Sharding module.
    encrypted_data = Sharding.reconstruct_data(Shards)
    
    # Step 2: Decrypt the reconstructed encrypted data using the provided symmetric key.
    compressed_data = Encryption.decrypt(encrypted_data, key)
    
    # Step 3: Decompress the decrypted data to restore the original file data.
    decompressed_data = Encoder.decompress_file(compressed_data)
    
    # Return the decompressed data, which is the original file content.
    return decompressed_data
