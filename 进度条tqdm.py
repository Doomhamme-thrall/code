import time

import tqdm

for i in tqdm.tqdm(range(100), desc="processing", total=100):
    time.sleep(0.1)  # 模拟处理时间
    pass
