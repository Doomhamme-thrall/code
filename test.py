import struct
import time

import serial


def create_data_frame(
    left_stick_x,
    right_stick_y,
    right_trigger,
    left_trigger,
    bottom_x,
    bottom_y,
    bottom_a,
    bottom_b,
):
    frame_head = 0xAA
    frame_tail = 0xFF

    # 将浮点数和整数打包成二进制数据
    data = struct.pack(
        "<BffffBBBBB",
        frame_head,
        left_stick_x,
        right_stick_y,
        right_trigger,
        left_trigger,
        bottom_x,
        bottom_y,
        bottom_a,
        bottom_b,
        0,  # 校验和占位
    )

    # 计算校验和
    checksum = sum(data[:-2]) % 256

    # 将校验和和帧尾添加到数据帧中
    data = data[:-2] + struct.pack("BB", checksum, frame_tail)

    return data


# 初始化串口
ser = serial.Serial("COM6", 9600, timeout=1)

try:
    while True:
        # 固定非零常数数据
        left_stick_x = 0
        right_stick_y = 0
        right_trigger = 0
        left_trigger = 0
        bottom_x = 0
        bottom_y = 0
        bottom_a = 0
        bottom_b = 0

        # 创建数据帧
        data_frame = create_data_frame(
            left_stick_x,
            right_stick_y,
            right_trigger,
            left_trigger,
            bottom_x,
            bottom_y,
            bottom_a,
            bottom_b,
        )
    
        # 发送数据
        ser.write(data_frame)
        print("sended")

        # 接收数据
        if ser.in_waiting > 0:
            received_data = ser.read(ser.in_waiting)
            print("Received:", received_data)

        time.sleep(1)

except KeyboardInterrupt:
    print("end")
finally:
    ser.close()
