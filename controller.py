import pygame
import serial

# 初始化 Pygame
pygame.init()

# 初始化手柄
pygame.joystick.init()
# 检查是否有手柄连接
if pygame.joystick.get_count() == 0:
    print("没有检测到手柄")
    pygame.quit()
    exit()
# 获取第一个手柄
joystick = pygame.joystick.Joystick(0)
joystick.init()

# 初始化串口
ser = serial.Serial("COM6", 9600, timeout=0.1)  # 设置串口，timeout 避免阻塞

# 初始化上一次的输入状态
last_input_state = None

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 读取手柄输入并映射
    left_stick_x = int((joystick.get_axis(0) + 1) * 100)  # 映射到 0-200
    right_stick_y = int((joystick.get_axis(3) + 1) * 100)  # 映射到 0-200
    left_trigger = int((joystick.get_axis(4) + 1) * 50)  # 映射到 0-100
    right_trigger = int((joystick.get_axis(5) + 1) * 50)  # 映射到 0-100

    # 按键状态
    button_a = joystick.get_button(0)  # 0 或 1
    button_b = joystick.get_button(1)
    button_x = joystick.get_button(2)
    button_y = joystick.get_button(3)

    # 构建输入状态
    input_state = [
        left_stick_x,
        right_stick_y,
        left_trigger,
        right_trigger,
        button_a,
        button_b,
        button_x,
        button_y,
    ]

    # 发送数据
    if (1):
        # 计算校验和
        checksum = (sum(input_state)+170) % 256

        # 构建发送数据
        data_to_send = [0xAA] + input_state + [checksum, 0xFF]

        try:
            ser.write(bytearray(data_to_send))
            print(f"发送: {data_to_send}")
        except serial.SerialException as e:
            print(f"串口发送失败: {e}")

        # 更新上一次的输入状态
        last_input_state = input_state

    # 接收串口数据
    try:
        if ser.in_waiting > 0:  # 检查是否有数据可读
            received_data = ser.read(ser.in_waiting)  # 读取所有可用数据
            print(
                f"接收到的数据: {received_data.decode('utf-8', errors='ignore')}"
            )  # 尝试解码为字符串
    except serial.SerialException as e:
        print(f"串口接收失败: {e}")

    # 控制循环频率
    pygame.time.wait(100)




# 关闭串口
ser.close()

# 退出 Pygame
pygame.quit()
