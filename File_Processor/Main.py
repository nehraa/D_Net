import Encoder
import Encryption
import Sharding

def Upload(file_path):
    compressed_data = Encoder.compress_file(file_path)
    key = Encryption.generate_symmetric_key()
    encrypted_data = Encryption.encrypt(compressed_data, key)
    Shards = Sharding.shard_data(encrypted_data, 1024)
    return Shards,key

def Download(Shards,key):
    encrypted_data = Sharding.reconstruct_data(Shards)
    compressed_data = Encryption.decrypt(encrypted_data,key)
    decompressed_data = Encoder.decompress_file(compressed_data)
    return decompressed_data