import serial

frame_header = 0xAA  # 帧头


def frame_build(data):
    high_byte = (data >> 8) & 0xFF
    low_byte = data & 0xFF
    check = frame_header ^ high_byte ^ low_byte
    frame = bytes([frame_header, high_byte, low_byte, check])
    return frame


if __name__ == "__main__":
    off = 200
    frame = frame_build(off)

    ser = serial.Serial(
        port="COM3",
        baudrate=115200,
    )

    ser.write(frame)
