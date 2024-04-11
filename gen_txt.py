import time
import os

def copy_file_with_delay(input_path, output_path):
    """
    将输入文件的内容复制到输出文件中，每读取一行暂停一秒。

    :param input_path: 输入文件的路径
    :param output_path: 输出文件的路径
    """
    # 确保输出文件存在
    with open(output_path, 'w') as f:
        pass

    # 打开输入文件和输出文件
    with open(input_path, 'r') as input_file, open(output_path, 'a') as output_file:
        for line in input_file:
            print(line)
            # 写入当前行到输出文件
            output_file.write(line)
            # 强制将数据写入到磁盘
            output_file.flush()
            os.fsync(output_file.fileno())
            # 暂停一秒
            time.sleep(1)

if __name__ == '__main__':
    copy_file_with_delay('/Users/atom/Desktop/123.txt', '123.txt')