# -*- coding: utf-8 -*-
import random
import time
from datetime import datetime, timedelta
import requests
import json

# 设置初始时间点（这里以代码首次运行的时间为例）
start_time = datetime.now()

def format_elapsed_time(elapsed_time):
    # 获取总秒数
    seconds = int(elapsed_time.total_seconds())
    # 提取天数、小时数、分钟数和秒数
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    # 格式化为字符串
    return f"{days}天 {hours}小时 {minutes}分钟 {seconds}秒"
def update_data(data_dict):
    # 每个数据的更新频率（秒）
    update_frequency = {
        "scdy": 2, "scdl": 2, "lcdy": 10, "lcdl": 10,
        "yxsj": 1, "gzbj": 1, "sn": 1,
        "dqwd": 3, "slcwd": 3, "xlcwd": 3, "sxwd": 3,
        "slcsl": 1, "dqsl": 2, "xlcsl": 3,
        "bgdl1": 1, "bgdl2": 1, "bgdl3": 1, "bgdl4": 1,
        "bgdl5": 1, "bgdl6": 1, "bgdl7": 20, "bgdl8": 20, "bgdl9": 20,
        "d1wd": 1, "d2wd": 1, "d3wd": 1, "d4wd": 1
    }

    # 每个数据的变化范围
    change_range = {
        "scdy": (110,130), "scdl": (560, 640), "lcdy": (280, 350), "lcdl": (460, 500),
        "dqwd": (65, 65), "slcwd": (55, 55), "xlcwd": (55, 55), "sxwd": (23, 23),
        "slcsl": (45, 55), "dqsl": (95, 105), "xlcsl": (47, 57),
        "bgdl1": (90, 110), "bgdl2": (90, 110), "bgdl3": (95, 125), "bgdl4": (100.1, 100.1),
        "bgdl5": (98.9, 98.9), "bgdl6": (100.2, 100.2), "bgdl7": (80, 95), "bgdl8": (80, 95), "bgdl9": (80, 95),
        "d1wd": (20, 95), "d2wd": (20, 95), "d3wd": (15, 95), "d4wd": (0, 95)
    }
    # 设计图数据
    # change_range = {
    #     "yxsj": "0天 0小时 0分钟 0秒",
    #     "scdy": (110,110), "scdl": (800, 800), "lcdy": (280, 280), "lcdl": (460, 460),
    #     "dqwd": (0, 0), "slcwd": (0, 0), "xlcwd": (0, 0), "sxwd": (0, 0),
    #     "slcsl": (45, 45), "dqsl": (90, 90), "xlcsl": (40, 40),
    #     "bgdl1": (0, 0), "bgdl2": (0, 0), "bgdl3": (0, 0), "bgdl4": (0, 0),
    #     "bgdl5": (0, 0), "bgdl6": (0, 0), "bgdl7": (0, 0), "bgdl8": (0, 0), "bgdl9": (0, 0),
    #     "d1wd": (20, 95), "d2wd": (20, 95), "d3wd": (15, 95), "d4wd": (0, 95)
    # }

    # 当前时间
    current_time = datetime.now()

    for key in data_dict.keys():
        if key == "yxsj":
            # 计算运行时间
            elapsed_time = datetime.now() - start_time
            # 格式化运行时间
            data_dict[key] = format_elapsed_time(elapsed_time)
        elif key in ["gzbj", "sn"]:
            # 故障报警和使能的值为0或1
            if current_time.second % update_frequency[key] == 0:
                data_dict[key] = random.randint(0, 0)
        elif key in update_frequency:
            # 根据定义的频率更新其他数据
            if current_time.second % update_frequency[key] == 0:
                min_val, max_val = change_range[key]
                data_dict[key] = random.uniform(min_val, max_val)
                data_dict[key] = round(data_dict[key], 1)
    # data_dict["yxsj"] = '0天 0小时 0分钟 0秒'
    return data_dict


def send_data(data):
    url = "http://localhost:5000/send_data"
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response


# 初始数据
data_dict = {
    "scdy": 0, "scdl": 0, "lcdy": 0, "lcdl": 0,
    "yxsj": "1997-07-16T19:20+01:00", "gzbj": 0, "sn": 0,
    "dqwd": 0, "slcwd": 0, "xlcwd": 0, "sxwd": 0,
    "slcsl": 0, "dqsl": 0, "xlcsl": 0,
    "bgdl1": 0, "bgdl2": 0, "bgdl3": 0, "bgdl4": 0,
    "bgdl5": 0, "bgdl6": 0, "bgdl7": 0, "bgdl8": 0, "bgdl9": 0,
    "d1wd": 0, "d2wd": 0, "d3wd": 0, "d4wd": 0
}

# 演示数据更新
while True:
    updated_data = update_data(data_dict)
    print("开始发送")
    result = send_data(updated_data)
    print(updated_data)
    print(result.text)
    print("结束发送")
    time.sleep(1)  # 暂停1秒
