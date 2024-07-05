"""CLI core class"""
from models.encryption import CLIEncryption
import base64
import os


class Core:
    """Core class for CLI"""
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
            if InputLength != 0:
                if len(InputData) == InputLength:
                    break
                print(f"{ErrorText} {len(InputData)}.")
            elif ExpectedInput is not None:
                if AllLower is True:
                    InputData = InputData.lower()
                if InputData in ExpectedInput:
                    break
                print(ErrorText)

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
            @FileName (str): file name of the file.

        return:
            None.
        """
        if os.path.isfile(FileName) is True:
            IsTrue = self.GetUserInput("File already exists. Do you want to overwrite the file? (Y/N): ", "Input must be either Y or N", 0, ["y", "n"], True)
            if IsTrue == "n":
                return
        self.__EncryptionOps.save(FileName)

    def GetData(self):
        """dummy function"""
        print(self.__EncryptionOps.get())
