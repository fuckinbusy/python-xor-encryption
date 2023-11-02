from binascii import crc32


class Decoder:
    def __init__(self):
        self.__size_offset = 24

    def decode(self, key: str, file: str):
        with open(file, 'rb') as f:
            key_size = len(key.encode("utf-8"))
            split_filename = file.split("/")[-1].split(".")
            filename = f"{split_filename[0]}.{split_filename[1]}"

            f.seek(self.__size_offset, 1)
            data_size = int.from_bytes(f.read(4), "little")
            data = f.read(data_size)

        if key_size > data_size:
            key = key[:data_size].encode("utf-8")
        elif key_size < data_size:
            key = self.__resize_key(key, data_size).encode("utf-8")
        else:
            key.encode("utf-8")

        if not self.__crc_validation(file, key):
            print("⚠ Invalid key!")
            return

        xor_decoded_data = bytes([m ^ d for m, d in zip(key, data)])

        with open(f"Decoded/{filename}", 'wb') as f:
            f.write(xor_decoded_data)
        print(f"● Decoded successfully! [Decoded/{filename}]")

    def __resize_key(self, key: str, data_size: int) -> str:
        new_key = key * (data_size // len(key) + 1)
        return new_key[:data_size]

    def __crc_validation(self, file: str, key: bytes) -> bool:
        with open(file, 'rb') as f:
            f.seek(-8, 2)
            crc = f.read(4)
            crc_gen = crc32(key).to_bytes(4, byteorder="little")
            if crc_gen != crc:
                return False
            print("○ CRC validation completed")
        return True
