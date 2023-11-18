# -*- coding: utf-8 -*-
from binascii import crc32
from progress.bar import ShadyBar


class Decryptor:
    def __init__(self):
        self.__size_offset = 24

    def decrypt(self, file: str):
        if file is None or file == "":
            print("⚠ Wrong path!")
            return

        key = input("KEY: ")
        with open(file, 'rb') as f:
            split_filename = file.split("/")[-1].split(".")
            filename = f"{split_filename[0]}.{split_filename[1]}"
            f.seek(self.__size_offset, 1)
            data_size = int.from_bytes(f.read(4), "little")

            if not self.__crc_validation(file, key.encode()):
                print("⚠ Invalid key!")
                return

            bytes_to_read = 8

            print(f"○ Data size: {data_size} bytes")
            with open(f"Decoded/{filename}", 'wb') as f2:
                with ShadyBar("○ Decoding", max=data_size, fill="▮") as bar:
                    for c in range(0, data_size, bytes_to_read):
                        data = f.read(bytes_to_read)
                        f2.write(bytearray(self.__xor(data, key)))
                        bar.next(8)

        print(f"● Decoded successfully! [Decoded/{filename}]")

    @staticmethod
    def __crc_validation(file: str, key: bytes) -> bool:
        with open(file, 'rb') as f:
            f.seek(-8, 2)
            crc = f.read(4)
        crc_gen = crc32(key).to_bytes(4, byteorder="little")
        if crc_gen != crc:
            return False
        print("○ CRC validation completed")
        return True

    @staticmethod
    def __xor(data: bytes, key: str) -> bytearray:
        xor_1, xor_2 = [], []
        key_split = key.split(":")
        key_1 = key_split[0].encode()
        key_2 = key_split[1].encode()

        for k, d in zip(key_1, data):
            xor_1.append(k ^ d)
        for k, d in zip(key_2, xor_1):
            xor_2.append(k ^ d)

        return bytearray(xor_2)
