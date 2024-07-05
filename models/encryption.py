"""Encryption class"""
import random
import string
from Crypto.Cipher import AES
import json


class CLIEncryption:
    """class for handling cryptographic operations"""
    __EncryptionKey = None
    __IV = None

    def CheckParam(self) -> bool:
        """
        Check the required parameters for crypto.

        return:
            True if all the required are non NULL, otherwise False.
        """
        if self.__EncryptionKey is None and self.__IV is None:
            return False
        return True

    def CryptographicParam(self, EncryptionKey: str, IV: str) -> None:
        """Set or generate neccassry cryptographic parameters"""
        if EncryptionKey is None:
            self.__EncryptionKey = bytes(self.RandomString(32), "utf-8")
            self.__IV = bytes(self.RandomString(12), "utf-8")
        else:
            self.__EncryptionKey = bytes(EncryptionKey, "utf-8")
            self.__IV = bytes(IV, "utf-8")

    def EncryptBuffer(self, buffer: bytes) -> bytes:
        """
        Encrypte given buffer
        args:
            @buffer (bytes): buffer that need to be encrypted.

        return:
            bytes: encrypted buffer.
        """
        cipher = AES.new(self.__EncryptionKey, AES.MODE_GCM, nonce=self.__IV)
        ciphertext = cipher.encrypt(buffer)
        return ciphertext

    def save(self, FileName) -> None:
        """Save Encryption Key and IV to a given file"""
        data = {"key": self.__EncryptionKey.decode("utf-8"), "IV": self.__IV.decode("utf-8")}
        file = open(FileName, 'w')
        json.dump(data, file, indent=4)
        file.close()

    def RandomString(self, length: int) -> str:
        """Generate a random string of given length"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def get(self):
        return {"key": self.__EncryptionKey.decode("utf-8"), "IV": self.__IV.decode("utf-8")}
