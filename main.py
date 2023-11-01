from CustomFileWriter import CustomFileWriter
from Encoder import Encoder
from Decoder import Decoder
from tkinter.filedialog import askopenfilename


class Main:
    def __init__(self):
        self.writer = CustomFileWriter()
        self.encoder = Encoder()
        self.decoder = Decoder()

    def main(self):
        f = askopenfilename()
        print(f)
        with open(f, "rb") as file:
            data = file.read()
        encoded_data = self.encoder.encode(data)
        self.writer.write_file(f, encoded_data)
        f = askopenfilename(filetypes=[("RICH encryption file", "*.rich")])
        key = input("KEY: ")
        self.decoder.decode(key, f)


if __name__ == "__main__":
    m = Main()
    m.main()
