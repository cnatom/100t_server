# -*- coding: utf-8 -*-
# 读取txt文件，保留txt文件中最新的100行数据，数据清洗后发送到Flask后端
import argparse
import time
import requests
import json
from column_map import column_map
from data_dict import data_dict
from format_time import format_elapsed_time
from datetime import datetime


def send_data(data):
    """发送数据到Flask后端"""
    url = "http://localhost:5000/send_data"
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


def update_data(input_path='data/data.txt'):
    start_time = None
    while True:
        with open(input_path, 'r+') as file:
            lines = file.readlines()
            # 如果行数超过100行，只保留最新的100行
            if len(lines) > 100:
                lines = lines[-100:]
                file.seek(0)
                file.truncate()
                file.writelines(lines)
            # 读取最新的一行数据
            last_line = lines[-1] if lines else ''
            # 将数据转换为字典格式
            data_list = last_line.strip().split()[5:]
            for i, data in enumerate(data_list):
                if i in column_map:
                    data_dict[column_map[i]] = format(float(data_list[i])/10, '.1f')
            # 获取开始时间和当前时间
            if start_time is None and lines:
                start_time = datetime.strptime(lines[0].split()[0], '%H:%M:%S')
            if lines:
                current_time = datetime.strptime(lines[-1].split()[0], '%H:%M:%S')
                elapsed_time = current_time - start_time
                # 使用format_elapsed_time函数格式化运行时间
                data_dict['yxsj'] = format_elapsed_time(elapsed_time)
            # 发送数据到服务器
            result = send_data(data_dict)
            print(result.text)
        # 暂停一秒
        time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update data from a text file.')
    parser.add_argument('input_path', default='data/data.txt', type=str, help='The path to the input file')
    args = parser.parse_args()
    if args.input_path:
        update_data(input_path=args.input_path)
    else:
        update_data()
