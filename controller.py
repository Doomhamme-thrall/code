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
ser = serial.Serial("COM6", 9600)  # 请根据实际情况修改串口号和波特率

# 初始化上一次的输入状态
last_input_state = None

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 读取手柄输入
    left_stick_x = int(joystick.get_axis(0) * 100)
    left_stick_y = int(joystick.get_axis(1) * 100)
    right_stick_x = int(joystick.get_axis(3) * 100)
    right_stick_y = int(joystick.get_axis(4) * 100)
    left_trigger = int((joystick.get_axis(2) + 1) * 50)
    right_trigger = int((joystick.get_axis(5) + 1) * 50)

    buttons = [joystick.get_button(i) for i in range(joystick.get_numbuttons())]

    # 将结果存储在数组中
    input_state = [
        left_stick_x,
        left_stick_y,
        right_stick_x,
        right_stick_y,
        left_trigger,
        right_trigger,
    ] + buttons

    # 如果输入状态发生变化，则通过串口发送数据
    ser.write(str(input_state).encode())
    print("seneded")

    # 接收串口数据
    if ser.in_waiting > 0:
        received_data = ser.readline().decode().strip()
        print(f"接收到的数据: {received_data}")

    # 控制循环频率
    pygame.time.wait(100)

# 关闭串口
ser.close()

# 退出 Pygame
pygame.quit()
