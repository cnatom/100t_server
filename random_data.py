import random
import time
from datetime import datetime, timedelta
import requests
import json


def update_data(data_dict):
    # 每个数据的更新频率（秒）
    update_frequency = {
        "scdy": 5, "scdl": 5, "lcdy": 10, "lcdl": 10,
        "yxsj": 1, "gzbj": 1, "sn": 1,
        "dqwd": 3, "slcwd": 3, "xlcwd": 3, "sxwd": 3,
        "slcsl": 1, "dqsl": 2, "xlcsl": 3,
        "bgdl1": 1, "bgdl2": 1, "bgdl3": 1, "bgdl4": 1,
        "bgdl5": 20, "bgdl6": 20, "bgdl7": 20, "bgdl8": 20, "bgdl9": 20,
        "d1wd": 1, "d2wd": 1, "d3wd": 1, "d4wd": 1
    }

    # 每个数据的变化范围
    change_range = {
        "scdy": (95, 105), "scdl": (30, 35), "lcdy": (10, 15), "lcdl": (28, 33),
        "dqwd": (80, 90), "slcwd": (60, 65), "xlcwd": (85, 90), "sxwd": (95, 100),
        "slcsl": (30, 40), "dqsl": (50, 60), "xlcsl": (80, 90),
        "bgdl1": (80, 95), "bgdl2": (80, 95), "bgdl3": (80, 95), "bgdl4": (80, 95),
        "bgdl5": (80, 95), "bgdl6": (80, 95), "bgdl7": (80, 95), "bgdl8": (80, 95), "bgdl9": (80, 95),
        "d1wd": (20, 95), "d2wd": (20, 95), "d3wd": (15, 95), "d4wd": (0, 95)
    }

    # 当前时间
    current_time = datetime.now()

    for key in data_dict.keys():
        if key == "yxsj":
            # 运行时间每秒更新
            data_dict[key] = current_time.isoformat()
        elif key in ["gzbj", "sn"]:
            # 故障报警和使能的值为0或1
            if current_time.second % update_frequency[key] == 0:
                data_dict[key] = random.randint(0, 1)
        elif key in update_frequency:
            # 根据定义的频率更新其他数据
            if current_time.second % update_frequency[key] == 0:
                min_val, max_val = change_range[key]
                data_dict[key] = random.uniform(min_val, max_val)
                data_dict[key] = round(data_dict[key], 1)

    return data_dict


def send_data(data):
    url = "http://localhost:5000/send_data"
    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)


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
    send_data(updated_data)
    print(updated_data)
    print("结束发送")
    time.sleep(1)  # 暂停1秒
