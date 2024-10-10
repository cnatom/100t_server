import argparse
import multiprocessing
import os
import time

if __name__ == "__main__":
    # 创建解析器
    parser = argparse.ArgumentParser(description='Run scripts with specified Python path.')
    parser.add_argument('-env', type=str, nargs='?', default='python', help='The path to the Python interpreter')
    parser.add_argument('-path', type=str, default='data/data.txt', help='The input file path')
    parser.add_argument('-demo', type=str, default='False', help='Run the demo')
    # 解析参数
    args = parser.parse_args()
    if args.demo == 'True':
        multiprocessing.Process(target=os.system, args=(f'{args.env} utils/gen_random_data.py {args.path}',)).start()
    multiprocessing.Process(target=os.system, args=(f'{args.env} app.py',)).start()
    time.sleep(2)
    multiprocessing.Process(target=os.system, args=(f'{args.env} utils/update_data.py {args.path}',)).start()
