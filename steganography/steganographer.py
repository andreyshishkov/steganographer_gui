from PIL import Image


def get_file_size_to_bytes(data: bytes) -> bytes:
    """Return size of data in 8 bytes"""
    return len(data).to_bytes(8, byteorder='big')
