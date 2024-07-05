import cmd
import os
from utils.asciiart import banner
from models.CORE import Core


class HiddenCave(cmd.Cmd):
    prompt = "$HiddenCave-> "
    doc_header = "Use help <command> for more information."
    core = Core()
    IsReady = False

    def default(self, arg):
        print("[*] Invalid command, use help for information.")

    def do_exit(self, arg):
        """exit the CLI.\n"""
        exit(0)

    def do_clear(self, arg):
        """clear the stdout.\n"""
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    def do_init(self, arg):
        """init command\n"""
        RandomParam = self.core.GetUserInput("Do you wanna generate random parameters? (Y/N) ", "Input must be either Y or N", 0, ["y", "n"], True)
        if RandomParam == "y":
            self.core.CryptoParam(None)
        else:
            print("Enter Key and IV, the key's length must be exactly 32 and the IV's length must be exactly 12.")
            data = {}
            data["key"] = self.core.GetUserInput("Key: ", "[-] Invalid key length. Expected 32 but got ", 32, None, False)
            data["IV"] = self.core.GetUserInput("IV: ", "[-] Invalid IV length. Expected 12 but got ", 12, None, False)
            self.core.CryptoParam(data)

        self.IsReady = True
        self.core.GetData()

    def do_save(self, arg):
        """save command\n"""
        if len(arg) == 0:
            print("[-] Invalid parameters.")
            return
        args = arg.split(" ")
        if args[0][-5:] != ".json":
            print("[-] Invalid file name, the file must have the json file extention \".json\".")
            return
        self.core.SaveCryptSettings(args[0])


if __name__ == '__main__':
    try:
        print(banner)
        HiddenCave().cmdloop()
    except KeyboardInterrupt:
        exit(0)
