"""Encryption class"""
from Cryptodome.Cipher import AES
import json


class Encryption:
    """Class for handling encryption and decryption and data validation"""
    __DecryptionKey = None
    __ApiKey = None
    __iv = None

    def __init__(self) -> None:
        """Initialization of the base model"""
        file = open("settings.json", "r")
        settings = json.load(file)
        self.__DecryptionKey = settings["DecryptionKey"]
        self.__ApiKey = settings["ApiKey"]
        self.__iv = settings["IV"]

    def KeyChecker(self, key: bytes) -> bool:
        """Check if given Key is valid"""
        cipher = AES.new(self.__DecryptionKey, AES.MODE_GCM, nonce=self.__iv)
        plaintext = cipher.decrypt(key)
        plaintext = plaintext.decode()

        if plaintext == self.__ApiKey:
            return True

        return False
