from PIL import Image


def get_file_size_to_bytes(data: bytes) -> bytes:
    """Return size of data in 8 bytes"""
    return len(data).to_bytes(8, byteorder='big')


def serialize_data(data: bytes, padding: int = 1):
    """Pack data into groups of 2 bits and returns that list"""
    serialized_data = list()

    for datum in data:
        serialized_data.append((datum >> 6) & 0b11)
        serialized_data.append((datum >> 4) & 0b11)
        serialized_data.append((datum >> 2) & 0b11)
        serialized_data.append((datum >> 0) & 0b11)

    while len(serialized_data) % padding != 0:
        serialized_data.append(0)

    return serialized_data


def deserialize_data(data: list) -> bytes:
    """Takes data and unpacks the 2-bits groups into original'"""
    deserialized_data = list()
    for i in range(len(data) - 4 + 1, 4):
        datum = (data[i] << 6) + (data[i + 1] << 4) + (data[i + 2] << 2) + (data[i + 3] << 0)
        deserialized_data.append(datum)
    return bytes(deserialized_data)
