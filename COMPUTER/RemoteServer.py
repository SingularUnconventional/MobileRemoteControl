from flask import Flask, request
from flask import render_template
from flask_cors import CORS
from KeyPUT import PressKey

import socket
import sys
import os

app = Flask(__name__)
CORS(app)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("www.google.com", 443))
IP = sock.getsockname()[0]

@app.route('/mobil')
def mobil(MyIP=None):
    return render_template('index.html', MyIP=IP)#나중에 ip를 입력받게.
# def hello(name=None):
#     return render_template('hello.html', name=name)

@app.route('/command', methods=['POST'])
def command():
    data = request.json  # JSON 데이터를 받음
    if not data:  # JSON이 없을 경우
        return {"status": "Invalid request: No JSON data"}, 400

    command = data.get('command')  # "command" 키의 값을 읽음
    if not command:  # 명령어가 비어있을 경우
        return {"status": "Invalid command"}, 400

    print(f"Received command: {command}")

    # 받은 명령에 따라 작업 수행
    if  command == "powerOff":      
        os.system("shutdown -s -t 2")
        return {"status": "powerOff"}, 200
    elif command == "playpause":   
        PressKey(0x22)
        return {"status": "playpause"}, 200
    elif command == "volumeUp":     
        PressKey(0x30)
        return {"status": "volumeUp"}, 200
    elif command == "volumeDown":   
        PressKey(0x2E)
        return {"status": "volumeDown"}, 200
    else:
        return {"status": "Unknown command"}, 400

if __name__ == '__main__':
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)

    app.run(host='0.0.0.0', port=5000)  # 로컬 네트워크에서만 작동