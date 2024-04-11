# import subprocess
#
# def run_scripts(python_path="python3"):
#     # 启动 gen_random_data.py
#
#     p1 = subprocess.Popen([python_path, "utils/gen_random_data.py"], stdout=subprocess.PIPE)
#
#     # 启动 app.py
#     p2 = subprocess.Popen([python_path, "app.py"], stdout=subprocess.PIPE)
#
#     # 启动 update_data.py
#     p3 = subprocess.Popen([python_path, "utils/update_data.py"], stdout=subprocess.PIPE)
#
#     # 等待所有进程完成
#     p1.wait()
#     p2.wait()
#     p3.wait()
#
# if __name__ == "__main__":
#     run_scripts(python_path="usr/bin/python3")

import multiprocessing
import os

def worker(script):
    os.system(f'/usr/bin/python3 {script}')

if __name__ == "__main__":
    scripts = ['utils/gen_random_data.py', 'app.py', 'utils/update_data.py']

    processes = []

    for script in scripts:
        process = multiprocessing.Process(target=worker, args=(script,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()