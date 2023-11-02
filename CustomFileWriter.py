class CustomFileWriter:
    """
    - signature - first 28 bytes
    - crc - 4 bytes before end
    - end - last 4 bytes
    """
    def __init__(self):
        self.__signature_len = 28
        self.__end_len = 4
        self.ATTRIBUTE_BYTES = b'author:fuckin_busy\x00size:'
        self.FILE_END_BYTES = b'\x00end'

    def write_file(self, file: str, data: bytes, crc: bytes):
        filename = file.split("/")[-1]
        data_size = len(data).to_bytes(length=4, byteorder='little')
        self.__create_file(filename, data_size)

        with open(f"Encoded/{filename}.rich", 'rb+') as f:
            f.seek(self.__signature_len, 1)
            f.write(bytearray(data + crc + self.FILE_END_BYTES))

    def __create_file(self, filename: str, data_size: bytes):
        with open(f"Encoded/{filename}.rich", 'wb') as f:
            f.write(bytearray(self.ATTRIBUTE_BYTES + data_size))
