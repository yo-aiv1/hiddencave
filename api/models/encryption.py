"""Encryption class"""
from Crypto.Cipher import AES
import json


class Encryption:
    """class for handling cryptographic operations"""
    __CryptSettingsFile = "settings.json"
    __EncryptionKey = None
    __IV = None

    def __init__(self) -> None:
        file = open(self.__CryptSettingsFile, 'r')
        data = json.loads(file.read())
        file.close()

        self.__EncryptionKey = bytes(data["key"], "utf-8")
        self.__IV = bytes(data["IV"], "utf-8")

    def EncryptBuffer(self, buffer) -> bytes:
        """
        Encrypte given buffer.
        args:
            @buffer (bytes): buffer that need to be encrypted.

        return:
            bytes: encrypted buffer.
        """

        cipher = AES.new(self.__EncryptionKey, AES.MODE_GCM, nonce=self.__IV)
        ciphertext = cipher.encrypt(buffer)
        return ciphertext

    def get(self):
        return {"key": self.__EncryptionKey.decode("utf-8"), "IV": self.__IV.decode("utf-8")}
