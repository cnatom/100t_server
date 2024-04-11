import argparse
import multiprocessing
import os
import sys


# 获取当前文件的绝对路径
current_path = os.path.dirname(os.path.abspath(__file__))
# 获取map_data模块的路径
module_path = os.path.join(current_path, 'map_data')

# 将map_data模块的路径添加到sys.path中
sys.path.append(module_path)
def worker(script, python_path):
    os.system(f'{python_path} {script}')

if __name__ == "__main__":
    # 创建解析器
    parser = argparse.ArgumentParser(description='Run scripts with specified Python path.')
    parser.add_argument('python_path', type=str, nargs='?', default='/usr/bin/python3', help='The path to the Python interpreter')

    # 解析参数
    args = parser.parse_args()

    scripts = ['utils/gen_random_data.py', 'app.py', 'utils/update_data.py']
    processes = []

    for script in scripts:
        process = multiprocessing.Process(target=worker, args=(script, args.python_path))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()