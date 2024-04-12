# 用于创建模拟的随机数据
# 并将其写入data_dict.py或txt中
import os
import random
import time
from datetime import datetime
from column_map import column_map
from data_dict import data_dict
from format_time import format_elapsed_time
import argparse

# 设置初始时间点（这里以代码首次运行的时间为例）
start_time = datetime.now()


def gen_random_json_data(data_dict):
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
        "scdy": (110, 130), "scdl": (560, 640), "lcdy": (280, 350), "lcdl": (460, 500),
        "dqwd": (65, 65), "slcwd": (55, 55), "xlcwd": (55, 55), "sxwd": (23, 23),
        "slcsl": (45, 55), "dqsl": (95, 105), "xlcsl": (47, 57),
        "bgdl1": (90, 110), "bgdl2": (90, 110), "bgdl3": (95, 125), "bgdl4": (100.1, 100.1),
        "bgdl5": (98.9, 98.9), "bgdl6": (100.2, 100.2), "bgdl7": (80, 95), "bgdl8": (80, 95), "bgdl9": (80, 95),
        "d1wd": (20, 95), "d2wd": (20, 95), "d3wd": (15, 95), "d4wd": (0, 95)
    }

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


def gen_random_txt_data(output_path, data_dict_i, column_map_i):
    """
    生成随机数据并写入txt

    :param output_path: 输出文件的路径
    :param data_dict_i: 数据字典
    :param column_map_i: 列映射字典
    """

    # 检查输出文件是否存在，如果不存在则创建
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 确保输出文件存在
    with open(output_path, 'a') as f:
        pass

    while True:
        # 打开输出文件
        with open(output_path, 'a') as output_file:
            # 生成随机数据
            data_dict_i = gen_random_json_data(data_dict_i)
            # 创建一个列表，用于存储每一列的数据
            data_list = ['0'] * (max(column_map_i.keys()) + 1)
            for index, key in column_map_i.items():
                if index == 18:
                    print()
                data_list[index] = str(data_dict_i[key])
            # 创建时间戳
            timestamp = datetime.now().strftime('%H:%M:%S %B %d, %Y')
            # 创建要写入的行
            line = f"{timestamp} 40701: {' '.join(data_list)}\n"
            print(line)
            # 写入当前行到输出文件
            output_file.write(line)
            # 强制将数据写入到磁盘
            output_file.flush()
            os.fsync(output_file.fileno())
            # 暂停一秒
            time.sleep(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate random data and write it to a file.')
    parser.add_argument('output_path', default='data/data.txt', type=str, help='The path to the output file')
    args = parser.parse_args()
    if args.output_path:
        gen_random_txt_data(output_path=args.output_path, data_dict_i=data_dict, column_map_i=column_map)
    else:
        gen_random_txt_data(data_dict_i=data_dict, column_map_i=column_map)
