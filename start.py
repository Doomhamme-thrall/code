import subprocess
import time
from datetime import datetime

import psutil


def process_exists(process_name):
    for proc in psutil.process_iter():
        if proc.name() == process_name:
            return True
    return False


# Steam 可执行文件路径
steam_path = r"C:\Program Files (x86)\Steam\steam.exe"
# 游戏的 appid
appids = {"dollar": "3069470", "banana": "2923300"}


while True:
    current_time = datetime.now()
    if current_time.hour >= 23:
        if process_exists("Dollar.exe") and process_exists("Banana.exe"):
            print("已经在运行，跳过")
            break
        else:
            # 启动所有游戏
            for game_name, appid in appids.items():
                subprocess.Popen([steam_path, "-applaunch", appid], shell=True)
                print(
                    f"游戏 {game_name} 已在 {current_time.strftime('%Y-%m-%d %H:%M:%S')} 启动。"
                )
                time.sleep(5)
    time.sleep(60)
