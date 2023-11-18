# -*- coding: utf-8 -*-
from binascii import crc32
from os.path import getsize
from random import choice
from progress.bar import ShadyBar


class Encryptor:
    """
        - signature - first 28 bytes
        - crc - 4 bytes before end
        - end - last 4 bytes
    """

    def __init__(self):
        self.KEY_SYMBOLS = "abcdefghijklmnopqrstuvwxyz1234567890/?"
        self.KEY_SIZE = 16  # length of key in bytes
        self.__signature_len = 28
        self.__end_len = 4
        self.ATTRIBUTE_BYTES = b'author:fuckin_busy\x00size:'
        self.FILE_END_BYTES = b'\x00end'

    def encrypt(self, filename: str):
        if filename is None or filename == "":
            print("⚠ Wrong path!")
            return

        key = self.__generate_key(filename)
        print(f"○ Key generated: {key}")
        crc = self.__generate_crc(key.encode())
        filename_split = filename.split("/")[-1]

        with open(filename, "rb") as file:
            data_size = getsize(filename)

            if data_size == 0:
                print("⚠ Empty file!")
                return

            bytes_to_read = 8

            print(f"○ Data size: {data_size} bytes")
            with open(f"Encoded/{filename_split}.rich", "wb") as file2:

                file2.write(bytearray(self.ATTRIBUTE_BYTES + data_size.to_bytes(length=4, byteorder="little")))

                with ShadyBar("○ Encoding", max=data_size, fill="▮") as bar:
                    for c in range(0, data_size, 8):
                        data = file.read(bytes_to_read)
                        file2.write(self.__xor(data, key))
                        bar.next(8)

                file2.write(bytearray(crc + self.FILE_END_BYTES))

        print(f"● Encoded successfully! [Encoded/{filename.split('/')[-1]}]")

    def __generate_key(self, filename: str) -> str:
        key = ""
        for c in range(self.KEY_SIZE // 2):
            key += "".join(choice(self.KEY_SYMBOLS))
        key += "".join(":")
        for c in range(self.KEY_SIZE // 2):
            key += "".join(choice(self.KEY_SYMBOLS))

        with open("keygen.txt", "a") as file:
            file.write(f"{filename}: {key}\n")

        return key

    @staticmethod
    def __generate_crc(key: bytes) -> bytes:
        crc = crc32(key).to_bytes(4, byteorder="little")
        print(f"○ CRC generated")
        return crc

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
