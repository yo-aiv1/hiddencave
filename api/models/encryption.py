"""Encryption class"""
from Crypto.Cipher import AES
import json
import bz2
import base64


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

    def EncryptBuffer(self, buffer) -> str:
        """
        Compresse then encrypte a given buffer.
        args:
            @buffer (Any): buffer that need to be encrypted.

        return:
            str: encrypted buffer encoded with base64.
        """
        if isinstance(buffer, dict):
            buffer = json.dumps(buffer)
        else:
            buffer = str(buffer)

        cipher = AES.new(self.__EncryptionKey, AES.MODE_GCM, nonce=self.__IV)

        buffer = buffer.encode("utf-8")
        buffer = bz2.compress(buffer)
        buffer = cipher.encrypt(buffer)
        buffer = base64.b64encode(buffer)

        return buffer.decode("utf-8")

    def DecryptBuffer(self, buffer) -> str:
        """
        Decompresse then decrypte a given buffer.
        args:
            @buffer (Any): buffer that need will be decrypted.

        return:
            str: decrypted buffer.
        """
        if isinstance(buffer, dict):
            buffer = json.dumps(buffer)
        else:
            buffer = str(buffer)

        cipher = AES.new(self.__EncryptionKey, AES.MODE_GCM, nonce=self.__IV)

        buffer = buffer.encode("utf-8")
        buffer = base64.b64decode(buffer)
        buffer = cipher.decrypt(buffer)

        try:
            buffer = bz2.decompress(buffer)
        except OSError:
            return ""

        return buffer.decode("utf-8")

    def get(self):
        return {"key": self.__EncryptionKey.decode("utf-8"), "IV": self.__IV.decode("utf-8")}
