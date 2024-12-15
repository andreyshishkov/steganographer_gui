from PIL import Image
import crypto
from exceptions import MaxFileSizeException


magic_bytes = {
    "encryptedLSB": 0x1337c0de,
    "unencryptedLSB": 0xdeadc0de,
}


def get_file_size_to_bytes(data: bytes) -> bytes:
    """Return size of data in 8 bytes"""
    return len(data).to_bytes(8, byteorder='big')


def change_last_two_bits(orig_byte: int, new_bits: int) -> int:
    """Change last two bits of original byte by new bits"""
    return (orig_byte >> 2) << 2 | new_bits


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


def hide_data_to_image(
        input_image_path: str,
        file_to_hide_path: str,
        output_image_path: str = None,
        password: str = None,
) -> None:
    with open(file_to_hide_path, 'rb') as file:
        data = file.read()

    image = Image.open(input_image_path).convert('RGB')
    pixels = image.load()

    if password:
        data = crypto.encrypt_data(data, password)
        data = (magic_bytes['encryptedLSB']).to_bytes(4, byteorder='big') \
               + get_file_size_to_bytes(data) + data

    else:
        data = (magic_bytes['unencryptedLSB']).to_bytes(4, byteorder='big') \
               + get_file_size_to_bytes(data) + data

    if len(data) > (image.size[0] * image.size[1] * 6) // 8:
        raise MaxFileSizeException(
            'Maximum hidden file size exceeded, to hide this file, choose a bigger resolution'
        )

    data = serialize_data(data, padding=3)
    data.reverse()

    image_x, image_y = 0, 0
    while data:
        pixel_val = pixels[image_x, image_y]

        pixel_val = (
            change_last_two_bits(pixel_val[0], data.pop()),
            change_last_two_bits(pixel_val[1], data.pop()),
            change_last_two_bits(pixel_val[2], data.pop())
        )

        pixels[image_x, image_y] = pixel_val

        if image_x == image.size[0] - 1:
            image_x = 0
            image_y += 1
        else:
            image_x += 1

    if not output_image_path:
        output_image_path = '.'.join(input_image_path.split('.')[:-1]) + '_with_hidden' \
                            + '.' + input_image_path.split('.')[-1]

        image.save(output_image_path)
