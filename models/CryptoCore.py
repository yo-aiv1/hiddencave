"""Encryption class"""
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
        Check the required parameters are available.

        return:
            True if all the required are non NULL, otherwise False.
        """
        if self.EncryptionKey is None and self.IV is None:
            return False
        return True

    def GetRandomParam(self, EncryptionKey: str, IV: str) -> None:
        """Set or generate neccassry cryptographic parameters"""
        self.EncryptionKey = self.RandomString(32).encode("utf-8")
        self.IV = self.RandomString(12).encode("utf-8")

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
