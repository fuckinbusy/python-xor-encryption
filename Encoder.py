from random import choice


class Encoder:
    def __init__(self):
        self.KEY_SYMBOLS = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890"
        self.KEY_SIZE = 8

    def encode(self, data: bytes) -> bytes:
        data_array = bytearray(data)
        key = self.__generate_key()
        data_size = len(data_array)
        key_size = len(key)

        if key_size > data_size:
            key = key[:data_size].encode("utf-8")
        elif key_size < data_size:
            key = self.__resize_key(key, data_size).encode("utf-8")
        else:
            key.encode("utf-8")

        xor_encoded_data = bytes([m ^ d for m, d in zip(key, data)])

        print(f"[Encoder.encode] Data size: {len(data_array)} bytes")
        return xor_encoded_data

    def __generate_key(self) -> str:
        key = ""
        for i in range(self.KEY_SIZE):
            s = choice(self.KEY_SYMBOLS)
            key += s
        print(f"Secret key generated: {key}")
        with open("keygen.txt", "w") as f:
            f.write(key)
        return key

    def __resize_key(self, key: str, data_size) -> str:
        new_key = key * (data_size // len(key) + 1)
        return new_key[:data_size]
