import math

# Function to shard data into smaller chunks
def shard_data(data, shard_size=1024):
    """
    Shards the data into smaller chunks.

    Parameters:
        - data (bytes): The original data to be split into shards.
        - shard_size (int): The size of each shard in bytes (default is 1024 bytes).
        
    Returns:
        - List of shards, each a byte string representing a chunk of the original data.
    """
    # Calculate the total number of shards required
    total_size = len(data)
    num_shards = math.ceil(total_size / shard_size)

    # Use a list comprehension to split the data into shards efficiently
    shards = [data[i * shard_size: (i + 1) * shard_size] for i in range(num_shards)]
    return shards


# Function to reconstruct data from shards
def reconstruct_data(shards):
    """
    Reconstructs the original data from the shards.

    Parameters:
        - shards (list of bytes): The list of byte strings representing the shards.
        
    Returns:
        - The original data as bytes after reconstructing from the shards.
    """
    # Join the shards back into the original data using a single operation for efficiency
    return b''.join(shards)
