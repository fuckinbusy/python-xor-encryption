from CustomFileWriter import CustomFileWriter
from Encoder import Encoder
from Decoder import Decoder
from tkinter.filedialog import askopenfilename
from time import sleep


class Main:
    def __init__(self):
        self.writer = CustomFileWriter()
        self.encoder = Encoder()
        self.decoder = Decoder()

    def main(self):
        while True:
            choice = input("0.Quit; 1. Encode; 2. Decode\n_> ")
            if choice == "1" or choice.lower() == "encode":
                f = askopenfilename()
                print(f)
                with open(f, "rb") as file:
                    data = file.read()
                encoded_data, crc32 = self.encoder.encode(data, file.name)
                self.writer.write_file(f, encoded_data, crc32)
            elif choice == "2" or choice.lower() == "decode":
                f = askopenfilename(filetypes=[("RICH encryption file", "*.rich")])
                key = input("KEY: ")
                self.decoder.decode(key, f)
            elif choice == "0" or choice.lower() == "quit":
                print("(；′⌒`) Process finished. Bye-bye!")
                sleep(2)
                break


if __name__ == "__main__":
    m = Main()
    m.main()
