import threading
import time
from queue import Queue

import matplotlib.pyplot as plt
import numpy as np
import serial
from matplotlib.animation import FuncAnimation

offset_queue = Queue()

# 动态绘制
def visualize(range_x=3000, range_y=1.5, samples=1000, interval=10, scroll_step=1):
    fig, ax = plt.subplots()
    x = np.linspace(0, range_x, samples)
    y = np.zeros(samples)
    (line,) = ax.plot(x, y)
    ax.set_xlim(0, range_x)
    ax.set_ylim(-range_y, range_y)

    def update(frame):
        for _ in range(scroll_step):
            # 取最新值
            if not offset_queue.empty():
                new_val = offset_queue.get()
                if isinstance(new_val, (list, tuple, np.ndarray)):
                    new_val = new_val[-1]
                new_val = float(new_val)
            else:
                new_val = y[-1]
            # 左移并追加
            y[:-1] = y[1:]
            y[-1] = new_val
        line.set_ydata(y)
        return (line,)

    ani = FuncAnimation(fig, update, interval=interval, blit=True)
    plt.show()


# 外部串口输入
def external_input_from_serial(port, baudrate=115200):
    with serial.Serial(port, baudrate, timeout=1) as ser:
        while True:
            line = ser.readline().decode().strip()
            if line:
                # 将串口数据解析为偏移量数组
                new_offset = np.array([float(x) for x in line.split(",")])
                offset_queue.put(new_offset)


# 模拟随机输入
def external_input_from_random():
    while True:
        random_offset = np.random.uniform(-0.5, 0.5, 100)
        offset_queue.put(random_offset)
        time.sleep(0.001)


if __name__ == "__main__":
    sensor_thread = threading.Thread(target=external_input_from_random, daemon=True)
    sensor_thread.start()

    visualize(30)
