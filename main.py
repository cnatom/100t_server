import argparse
import multiprocessing
import os

def worker(script, python_path):
    os.system(f'{python_path} {script}')

if __name__ == "__main__":
    # 创建解析器
    parser = argparse.ArgumentParser(description='Run scripts with specified Python path.')
    parser.add_argument('python_path', type=str, nargs='?', default='python', help='The path to the Python interpreter')

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