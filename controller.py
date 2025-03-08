import pygame
import serial

pygame.init()
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("none")
    pygame.quit()
    exit()
joystick = pygame.joystick.Joystick(0)
joystick.init()
ser = serial.Serial("COM5", 9600, timeout=0.1)  # 设置串口，timeout 避免阻塞

last_input_state = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 摇杆状态
    left_stick_x = int((joystick.get_axis(0) + 1) * 100)  # 映射到 0-200
    right_stick_y = int((joystick.get_axis(3) + 1) * 100)
    # 扳机状态
    left_trigger = int((joystick.get_axis(4) + 1) * 50)  # 映射到 0-100
    right_trigger = int((joystick.get_axis(5) + 1) * 50)
    # 按键状态
    button_a = int(joystick.get_button(0))  # 映射到1，2
    button_b = int(joystick.get_button(1))
    button_x = int(joystick.get_button(2))
    button_y = int(joystick.get_button(3))

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

    # 发送
    if 1:
        # 计算校验和
        checksum = (sum(input_state) + 170) % 256

        # 数据帧
        data_to_send = [0xAA] + input_state + [checksum, 0xFF]

        try:
            ser.write(bytearray(data_to_send))
            # print(f"sended: {data_to_send}")
        except serial.SerialException as e:
            print(f"send failed: {e}")

        last_input_state = input_state

    try:
        if ser.in_waiting > 0:
            received_data = ser.read(ser.in_waiting)
            print(f"received: {received_data.decode('utf-8', errors='ignore')}")
    except serial.SerialException as e:
        print(f"receive failed {e}")

    pygame.time.wait(500)  # 100hz

ser.close()

pygame.quit()
