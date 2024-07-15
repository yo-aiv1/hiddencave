"""Encryption class"""
import random
import string
from Crypto.Cipher import AES
import json
import bz2
import base64


class CryptoCore:
    """class for handling cryptographic operations"""
    EncryptionKey = None
    IV = None

    def CheckParam(self) -> bool:
        """
        Check the required parameters for crypto.

        return:
            True if all the required are non NULL, otherwise False.
        """
        if self.EncryptionKey is None and self.IV is None:
            return False
        return True

    def CryptographicParam(self, EncryptionKey: str, IV: str) -> None:
        """Set or generate neccassry cryptographic parameters"""
        if EncryptionKey is None:
            self.EncryptionKey = self.RandomString(32).encode("utf-8")
            self.IV = self.RandomString(12).encode("utf-8")
        else:
            self.EncryptionKey = EncryptionKey.encode("utf-8")
            self.IV = IV.encode("utf-8")

    def EncryptBuffer(self, buffer) -> str:
        """
        Encrypte a given buffer.
        args:
            @buffer (Any): buffer that need to be encrypted.

        return:
            str: encrypted buffer.
        """
        cipher = AES.new(self.EncryptionKey, AES.MODE_GCM, nonce=self.IV)

        if isinstance(buffer, dict):
            buffer = json.dumps(buffer)
        else:
            buffer = str(buffer)

        buffer = buffer.encode("utf-8")
        buffer = bz2.compress(buffer)
        buffer = cipher.encrypt(buffer)
        buffer = base64.b64encode(buffer)

        return buffer.decode("utf-8")

    def DecryptBuffer(self, buffer) -> str:
        """
        Decrypte a given buffer.
        args:
            @buffer (bytes): buffer that need to be decrypted.

        return:
            bytes: decrypted buffer.
        """
        if not isinstance(buffer, bytes):
            buffer = buffer.encode("utf-8")

        cipher = AES.new(self.EncryptionKey, AES.MODE_GCM, nonce=self.IV)

        buffer = base64.b64decode(buffer)
        buffer = cipher.decrypt(buffer)
        buffer = bz2.decompress(buffer)

        return buffer

    def save(self, FileName: str) -> None:
        """
        Save Encryption Key and IV to a given file
        args:
            @FileName (str): file name
        return
            None
        """
        data = {"key": self.EncryptionKey.decode("utf-8"), "IV": self.IV.decode("utf-8")}
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

    def RandomString(self, length: int) -> str:
        """Generate a random string of given length"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
