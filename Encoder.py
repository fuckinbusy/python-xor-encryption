from random import choice
from binascii import crc32


class Encoder:
    def __init__(self):
        self.KEY_SYMBOLS = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890"
        self.KEY_SIZE = 8

    def encode(self, data: bytes, filename: str) -> tuple[bytes, bytes]:
        data_array = bytearray(data)
        key = self.__generate_key(filename)
        data_size = len(data_array)
        key_size = len(key)

        if key_size > data_size:
            key = key[:data_size].encode("utf-8")
        elif key_size < data_size:
            key = self.__resize_key(key, data_size).encode("utf-8")
        else:
            key.encode("utf-8")

        xor_encoded_data = bytes([m ^ d for m, d in zip(key, data)])

        print(f"○ Data size: {len(data_array)} bytes")
        crc = self.__generate_crc(key)
        print(f"● Encoded successfully! [Encoded/{filename.split('/')[-1]}]")
        return xor_encoded_data, crc

    def __generate_key(self, filename: str) -> str:
        key = ""
        for i in range(self.KEY_SIZE):
            s = choice(self.KEY_SYMBOLS)
            key += s
        print(f"○ Secret key generated: {key}")
        with open("keygen.txt", "w+") as f:
            f.write(f"{filename.split('/')[-1]}: {key}")
        return key

    def __generate_crc(self, key: bytes) -> bytes:
        crc = crc32(key).to_bytes(4, byteorder="little")
        print(f"○ CRC generated")
        return crc

    def __resize_key(self, key: str, data_size) -> str:
        new_key = key * (data_size // len(key) + 1)
        return new_key[:data_size]
