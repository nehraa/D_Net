import lzo
import os

def compress_file(file_path):
    """
    Compresses a file using LZO and saves it with a .lzo extension.

    Args:
        file_path (str): The full path to the file to be compressed.

    Returns:
        tuple: A tuple containing the compressed file path, original file name, and file extension.
    """
    try:
        # Open the file in binary read mode
        with open(file_path, 'rb') as f:
            data = f.read()

        # Compress the data using LZO
        compressed_data = lzo.compress(data)

        # Save the compressed data to a new file with a .lzo extension
        compressed_file_path = file_path + ".lzo"
        with open(compressed_file_path, 'wb') as f:
            f.write(compressed_data)

        # Extract file name and extension for metadata
        # Extract file name with extension
        file_name_with_extension = os.path.basename(file_path)

        # Extract file name without extension
        file_name = os.path.splitext(file_name_with_extension)[0]

        # Extract file extension
        file_extension = os.path.splitext(file_name_with_extension)[1]

        print(f"File '{file_path}' compressed and saved to '{compressed_file_path}'")
        return compressed_file_path, file_name, file_extension
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"Error: {e}")

def decompress_file(compressed_file_path, file_name, file_extension):
    """
    Decompresses a file using LZO and writes the output to a file with the original name and extension.

    Args:
        compressed_file_path (str): The full path to the compressed file.
        file_name (str): The original name of the file (without extension).
        file_extension (str): The original file's extension.

    Returns:
        str: The path to the decompressed file.
    """
    try:
        # Open the compressed file in binary read mode
        with open(compressed_file_path, 'rb') as f:
            compressed_data = f.read()

        # Decompress the data using LZO
        decompressed_data = lzo.decompress(compressed_data)

        # Construct the original file path using the provided metadata
        original_file_path = f"{file_name}{file_extension}"

        # Write the decompressed data to a new file
        with open(original_file_path, 'wb') as f:
            f.write(decompressed_data)

        print(f"File '{compressed_file_path}' decompressed and saved to '{original_file_path}'")
        return original_file_path
    except FileNotFoundError:
        print(f"Error: The file '{compressed_file_path}' was not found.")
    except Exception as e:
        print(f"Error: {e}")
