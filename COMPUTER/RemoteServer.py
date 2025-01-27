from flask import Flask, request
from flask_cors import CORS
from KeyPUT import PressKey

import os

app = Flask(__name__)
CORS(app)

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
    app.run(host='0.0.0.0', port=5000)  # 로컬 네트워크에서만 작동