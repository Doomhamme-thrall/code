import serial

frame_header = 0xAA  # 帧头


def frame_build(*data):
    """
    数据帧生成

    依次传入所需的数据

    返回值直接用ser.write
    """
    frame = [frame_header]
    check = frame_header

    for value in data:
        high_byte = (value >> 8) & 0xFF
        low_byte = value & 0xFF
        frame.extend([high_byte, low_byte])
        check ^= high_byte ^ low_byte

    frame.append(check)
    return bytes(frame)


if __name__ == "__main__":
    off = 200
    frame = frame_build(off)

    ser = serial.Serial(
        port="COM3",
        baudrate=115200,
    )

    ser.write(frame)
