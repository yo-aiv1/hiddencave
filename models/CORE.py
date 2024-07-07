"""CLI core class"""
from models.encryption import CLIEncryption
import base64
import json
import os
import bz2
import requests


class Core:
    """Core class for CLI"""
    IsReady = False
    EndPoint = None

    def __init__(self) -> None:
        """Initialization of the Core class"""
        self.__EncryptionOps = CLIEncryption()

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

    def CryptoParamChecker(self) -> bool:
        """
        Check the required parameters for crypto.

        return:
            True if all the required are non NULL, otherwise False.
        """
        return self.__EncryptionOps.CheckParam()

    def CryptoParam(self, params: dict) -> None:
        """
        Set or generate random cryptographic parameters.

        args:
            @params (dict): a dictionary that has 2 keys "key" and "IV" or None.

        return:
            None.
        """
        if params is None:
            self.__EncryptionOps.CryptographicParam(None, None)
        else:
            self.__EncryptionOps.CryptographicParam(params["key"], params["IV"])

    def SaveCryptSettings(self, FileName: str) -> None:
        """
        Save the current cryptographic parameters.

        args:
            @FileName (str): file name.

        return:
            None.
        """
        if os.path.isfile(FileName) is True:
            IsTrue = self.GetUserInput("File already exists. Do you want to overwrite the file? (Y/N): ", "Input must be either Y or N", 0, ["y", "n"], True)
            if IsTrue == "n":
                return
        self.__EncryptionOps.save(FileName)

    def LoadCryptSettings(self, FileName: str) -> None:
        """
        Load cryptographic parameters.

        args:
            @FileName (str): file name.

        return:
            None.
        """
        if os.path.isfile(FileName) is False:
            print("[-] File does not exist.")
            return

        self.__EncryptionOps.load(FileName)
        self.GetData()

    def EncryptData(self, data) -> str:
        """
        Encrypt a given buffer after compressing it.
        args:
            @data (str): data that will be encrypted.

        return:
            str: encrypted string.
        """
        if isinstance(data, dict):
            data = json.dumps(data)
        else:
            data = str(data)

        data = data.encode("utf-8")
        data = bz2.compress(data)
        data = self.__EncryptionOps.EncryptBuffer(data)
        data = base64.b64encode(data)

        return data.decode("utf-8")

    def DecryptData(self, data) -> str:
        """
        Decrypte a given buffer then decompressing it.
        args:
            @data (str): data that will be decrypted.

        return:
            str: decrypted string.
        """
        if isinstance(data, dict):
            data = json.dumps(data)
        else:
            data = str(data)

        data = data.encode("utf-8")
        data = base64.b64decode(data)
        data = self.__EncryptionOps.DecryptBuffer(data)
        data = bz2.decompress(data)

        return data.decode("utf-8")

    def check(self) -> bool:
        """Check if the endpoint is reachable and validate the cryptographic parameters."""
        if self.CryptoParamChecker() is True:
            TestMessage = self.EncryptData("Are you ready?")
            header = {"cc": TestMessage}
            FullUrl = self.EndPoint + "/check"
            try:
                status = requests.get(url=FullUrl, headers=header, timeout=5)

                if status.status_code == 200:
                    self.IsReady = True
                else:
                    print("[-] Incorrect cryptographic parameters. Please verify that the used parameters are the same ones on the endpoint.")
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                print("[-] The endpoint is not reqponding, Please verify that the endpoint URL is correct.")
        else:
            print("[-] The cryptographic parameters are NULL, Please set them or load a setting file before checking endpoint.")

    def GetData(self):
        """dummy function"""
        print(self.__EncryptionOps.get())
