# -*- coding: utf-8 -*-
import flask
from flask import Flask, request, logging
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/socket.io/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins='*')

# 全局数据字典
data_dict = {
    "scdy": 0,  # 输出电压
    "scdl": 0,  # 输出电流
    "lcdy": 0,  # 励磁电压
    "lcdl": 0,  # 励磁电流
    "yxsj": "1997-07-16T19:20+01:00",  # 运行时间
    "gzbj": 0,  # 故障报警
    "sn": 0,  # 使能
    "dqwd": 0,  # 动圈温度
    "slcwd": 0,  # 上励磁温度
    "xlcwd": 0,  # 下励磁温度
    "sxwd": 0,  # 水箱温度
    "slcsl": 0,  # 上励磁水流
    "dqsl": 0,  # 动圈水流
    "xlcsl": 0,  # 下励磁水流
    "bgdl1": 0,  # 边柜电流1
    "bgdl2": 0,  # 边柜电流2
    "bgdl3": 0,  # 边柜电流3
    "bgdl4": 0,  # 边柜电流4
    "bgdl5": 0,  # 边柜电流5
    "bgdl6": 0,  # 边柜电流6
    "bgdl7": 0,  # 边柜电流7
    "bgdl8": 0,  # 边柜电流8
    "bgdl9": 0,  # 边柜电流9
    "d1wd": 0,  # D1温度
    "d2wd": 0,  # D2温度
    "d3wd": 0,  # D3温度
    "d4wd": 0,  # D4温度
}


@app.route('/send_data', methods=['POST'])
def handle_data():
    global data_dict
    incoming_data = request.json
    data_dict.update(incoming_data)  # 更新数据
    socketio.emit('update_data', data_dict)  # 发送完整的数据到前端
    return flask.jsonify({
        "update": incoming_data,
        "data": data_dict
    }), 200


if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)
