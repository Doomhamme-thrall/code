frame_header = 0xAA  # 帧头
frame_tail = 0xFF  # 帧尾


def frame_build(*data):
    """
    数据帧生成

    依次传入所需的数据

    返回值可直接用ser.write
    """
    frame = [frame_header]
    # check = frame_header

    for value in data:
        if value < 0:
            value = -value
            frame.append(0x00)
        else:
            frame.append(0x01)
        high_byte = (value >> 8) & 0xFF
        low_byte = value & 0xFF
        frame.extend([high_byte, low_byte])
        # check ^= high_byte ^ low_byte

    # frame.append(check)
    frame.append(frame_tail)
    return bytes(frame)


if __name__ == "__main__":
    off = 200
    frame = frame_build(128)

    print(frame)
