# -*- coding: utf-8 -*-
import flask
from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS

from jsons.data_dict import data_dict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/socket.io/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins='*')

@app.route('/send_data', methods=['POST'])
def handle_data():
    incoming_data = request.json
    data_dict.update(incoming_data)  # 更新数据
    socketio.emit('update_data', data_dict)  # 发送完整的数据到前端
    return flask.jsonify({
        "update": incoming_data,
        "data": data_dict
    }), 200


if __name__ == '__main__':
    socketio.run(app, port=5000,allow_unsafe_werkzeug=True)
