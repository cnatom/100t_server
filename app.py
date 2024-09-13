# -*- coding: utf-8 -*-
import flask
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import pymysql
import datetime
from utils.data_dict import data_dict
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json
from utils.config import getConfig, updateConfig

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins='*')
config = getConfig()

def init_db():
    db = pymysql.connect(host='localhost', user='root', password='')
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS 100t_data")
    cursor.execute("USE 100t_data")
    cursor.execute("CREATE TABLE IF NOT EXISTS data_dict (update_time DATETIME, data JSON)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), password VARCHAR(255))")

    # 检查users表是否为空
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    if count == 0:
        # 如果users表为空，添加一个默认的用户
        hashed_password = generate_password_hash('admin', method='pbkdf2:sha256')
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('admin', hashed_password))
        db.commit()

    cursor.close()
    db.close()


# 连接数据库
def connect_db():
    db = pymysql.connect(host='localhost', user='root', password='')
    cursor = db.cursor()
    cursor.execute("USE 100t_data")
    return db, cursor


@app.route('/send_data', methods=['POST'])
def send_data():
    global config
    incoming_data = request.json
    data_dict.update(incoming_data)  # 更新数据
    # 将data_dict数据赋给config
    charts = config['charts']
    for key, value in charts.items():
        items = value['items']
        for item in items:
            item['value'] = data_dict[item['id']] or 0
    # config['runningTime'] = data_dict['yxsj']
    socketio.emit('update_data', data_dict)  # 发送完整的数据到前端
    socketio.emit('update_config', config)
    # 连接数据库并存储数据
    db, cursor = connect_db()
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 将data_dict转换为JSON格式的字符串
    data_json = json.dumps(data_dict)
    cursor.execute("INSERT INTO data_dict (update_time, data) VALUES (%s, %s)", (update_time, data_json))
    db.commit()

    response = flask.jsonify({
        "update": incoming_data,
        "data": data_dict
    }), 200

    # 关闭数据库连接和游标
    cursor.close()
    db.close()

    return response


@app.route('/get_date_range', methods=['GET'])
def get_date_range():
    # 连接数据库
    db, cursor = connect_db()

    # 查询第一行和最后一行的更新时间
    cursor.execute("SELECT update_time FROM data_dict ORDER BY update_time ASC LIMIT 1")
    start_time = cursor.fetchone()[0]
    cursor.execute("SELECT update_time FROM data_dict ORDER BY update_time DESC LIMIT 1")
    end_time = cursor.fetchone()[0]

    # 关闭数据库连接和游标
    cursor.close()
    db.close()

    # 返回查询结果
    return flask.jsonify({"start_time": str(start_time), 'end_time': str(end_time)}), 200


@app.route('/get_data', methods=['GET'])
# @lru_cache(maxsize=128)
def get_data():
    # 获取当前时间
    now = datetime.now()
    # 获取一天前的时间
    one_day_ago = now - timedelta(days=1)
    # 将时间对象转换为字符串
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    one_day_ago_str = one_day_ago.strftime('%Y-%m-%d %H:%M:%S')
    # 获取请求参数
    start_time = request.args.get('start_time', default=one_day_ago_str)
    end_time = request.args.get('end_time', default=now_str)
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)

    # 连接数据库
    db, cursor = connect_db()

    # 构建SQL查询语句
    sql = "SELECT * FROM data_dict"
    count_sql = "SELECT COUNT(*) FROM data_dict"
    if start_time or end_time:
        sql += " WHERE"
        count_sql += " WHERE"
        if start_time:
            sql += f" update_time >= '{start_time}'"
            count_sql += f" update_time >= '{start_time}'"
            if end_time:
                sql += " AND"
                count_sql += " AND"
        if end_time:
            sql += f" update_time <= '{end_time}'"
            count_sql += f" update_time <= '{end_time}'"
    sql += " ORDER BY update_time DESC"
    sql += f" LIMIT {(page - 1) * page_size}, {page_size}"

    # 执行SQL查询
    cursor.execute(sql)

    # 获取查询结果
    results = cursor.fetchall()

    # 执行SQL查询获取总条数
    cursor.execute(count_sql)
    total = cursor.fetchone()[0]

    # 关闭数据库连接和游标
    cursor.close()
    db.close()

    # 将查询结果转换为JSON格式的字符串
    data_history = [{"update_time": str(result[0]), "data": json.loads(result[1])} for result in results]

    with open('data/alarm_rules.json', 'r') as f:
        alarm_rules = json.load(f)

    # 返回查询结果和总条数
    return flask.jsonify(
        {"total": total, "data_history": data_history, 'page_size': page_size, "alarm_rules": alarm_rules}), 200


@app.route('/change_password', methods=['POST'])
def change_password():
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')
    if not old_password or not new_password:
        return jsonify({"error": "Old and new password required", "status": 400}), 400

    db, cursor = connect_db()
    cursor.execute("SELECT * FROM users ORDER BY username ASC LIMIT 1")
    user = cursor.fetchone()
    if not user:
        return jsonify({"message": "没有找到用户", "status": 400}), 400

    if not check_password_hash(user[1], old_password):
        return jsonify({"message": "旧密码错误！", "status": 400}), 400

    hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')
    cursor.execute("UPDATE users SET password = %s WHERE username = %s", (hashed_password, user[0]))
    db.commit()
    cursor.close()
    db.close()

    return jsonify({"message": "密码更新成功", "status": 200}), 200


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password required", "status": 400}), 400

    db, cursor = connect_db()
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if not user or not check_password_hash(user[1], password):
        return jsonify({"error": "Invalid username or password", "status": 400}), 400

    return jsonify({"message": "Logged in successfully", "status": 200}), 200


@app.route('/get_config', methods=['GET'])
def get_config():
    return jsonify(config), 200

@app.route('/get_key_map', methods=['GET'])
def get_key_map():
    key_map = {}
    for chart in config['charts'].values():
        for item in chart['items']:
            key_map[item['id']] = item['name']
    return jsonify(key_map), 200


@app.route('/update_config', methods=['POST'])
def update_config():
    global config
    new_config = request.json
    updateConfig(new_config)
    config = getConfig()
    return jsonify(config), 200


@app.route('/recover_config', methods=['GET'])
def recover_config():
    global config
    with open('data/default_config.json', 'r', encoding='utf-8') as f:
        default_config = json.load(f)
    with open('data/config.json', 'w', encoding='utf-8') as f:
        json.dump(default_config, f,ensure_ascii=False)
    config = getConfig()
    return jsonify(config), 200


@app.route('/get_alarm_rules', methods=['GET'])
def get_alarm_rules():
    with open('data/alarm_rules.json', 'r') as f:
        alarm_rules = json.load(f)
    return jsonify(alarm_rules), 200


@app.route('/update_alarm_rules', methods=['POST'])
def update_alarm_rules():
    new_rules = request.json
    try:
        with open('data/alarm_rules.json', 'r') as f:
            current_rules = json.load(f)
        # 使用新规则更新当前规则
        current_rules.update(new_rules)
        with open('data/alarm_rules.json', 'w') as f:
            json.dump(current_rules, f)
        return jsonify({"status": 200, "message": "修改成功"}), 200
    except:
        return jsonify({"status": 501, "message": "修改失败，服务端错误"}), 501


if __name__ == '__main__':
    print("Before init_db")
    init_db()
    print("After init_db")
    socketio.run(app, port=5000, allow_unsafe_werkzeug=True)
