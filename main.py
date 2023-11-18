# -*- coding: utf-8 -*-
from Encryptor import Encryptor
from Decryptor import Decryptor
from tkinter.filedialog import askopenfilename
from tkinter import Tk
from time import sleep


class Main:
    def __init__(self):
        self.window = Tk()
        self.Encryptor = Encryptor()
        self.Decryptor = Decryptor()
        self.window.attributes('-topmost', 1)
        self.window.withdraw()

    def main(self):
        while True:
            choice = input("0.Quit; 1. Encode; 2. Decode\n_> ")
            if choice == "1" or choice.lower() == "encode":
                f = askopenfilename(title="Choose file to encode")
                print(f)
                self.Encryptor.encrypt(f)
            elif choice == "2" or choice.lower() == "decode":
                f = askopenfilename(filetypes=[("RICH encryption file", "*.rich")],
                                    title="Choose file to decode",
                                    initialdir="Encoded")
                print(f)
                self.Decryptor.decrypt(f)
            elif choice == "0" or choice.lower() == "quit":
                print("(；′⌒`) Process finished. Bye-bye!")
                sleep(1)
                break
                

if __name__ == "__main__":
    m = Main()
    m.main()
