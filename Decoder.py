class Decoder:
    def __init__(self):
        self.__size_offset = 24

    def decode(self, key: str, file: str):
        key_size = len(key)
        split_filename = file.split("/")[-1].split(".")
        filename = f"{split_filename[0]}.{split_filename[1]}"
        with open(file, 'rb') as f:
            f.seek(self.__size_offset, 1)
            data_size = int.from_bytes(f.read(4), "little")
            data = f.read(data_size)

        if key_size > data_size:
            key = key[:data_size].encode("utf-8")
        elif key_size < data_size:
            key = self.__resize_key(key, data_size).encode("utf-8")
        else:
            key.encode("utf-8")

        xor_decoded_data = bytes([m ^ d for m, d in zip(key, data)])

        with open(f"Decoded/{filename}", 'wb') as f:
            f.write(xor_decoded_data)

    def __resize_key(self, key: str, data_size) -> str:
        new_key = key * (data_size // len(key) + 1)
        return new_key[:data_size]
