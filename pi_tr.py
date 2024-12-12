import serial
import socket
import threading
import time
import os
import signal
import fcntl

# 线程健康状态标志
thread_status = {"client_alive": True, "serial_alive": True}
# 文件路径
file_path = "/home/lyr/gxzl.txt"


def write_data(data):
    try:
        decoded_data = data.decode("utf-8")
    except UnicodeDecodeError:
        decoded_data = data.decode("latin-1")  # 或使用适当的编码
    with open(file_path, "a") as file:  # 追加模式
        # 获取文件锁
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write(decoded_data + "\n")
        # 释放文件锁
        fcntl.flock(file, fcntl.LOCK_UN)


def handle_client(client_socket, serial_port):
    global thread_status
    while True:
        try:
            # 从客户端接收数据
            data_from_client = client_socket.recv(1024)
            if not data_from_client:
                break
            print("接收到的消息(来自客户端): ", data_from_client.decode("utf-8"))
            # 将来自客户端的数据发送到串口
            serial_port.write(data_from_client)
            # 将数据写入文件
            write_data(data_from_client)
        except Exception as e:
            print(f"客户端处理异常: {e}")
            thread_status["client_alive"] = False
            break
    # 关闭客户端连接
    client_socket.close()


def handle_serial(serial_port, client_socket):
    global thread_status
    while True:
        try:
            # 从串口读取数据
            data_from_serial = serial_port.read(
                100
            )  # 读取 100 字节的数据，具体大小可以根据需要调整

            # 解码数据
            decoded_data = data_from_serial.decode("utf-8")
            print("接收到的消息(来自串口): ", decoded_data)

            # 将串口数据发送给客户端
            client_socket.sendall(data_from_serial)  # 发送数据到客户端
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}")
            decoded_data = data_from_serial.decode("latin-1")  # 或使用 errors='ignore'
            print("接收到的消息(来自串口) (Latin-1): ", decoded_data)
            client_socket.sendall(data_from_serial)  # 发送数据到客户端
        except Exception as e:
            print(f"其他异常: {e}")
            thread_status["serial_alive"] = False


def monitor_threads():
    while True:
        if not thread_status["client_alive"] or not thread_status["serial_alive"]:
            # 如果任意线程不再活跃，退出主进程以触发 systemd 重启
            os.kill(os.getpid(), signal.SIGTERM)
        time.sleep(60)  # 每60秒检查一次


def main():
    # 设置服务器IP地址和端口号
    host = "0.0.0.0"  # 监听所有网卡上的连接
    port = 5001  # 与C#代码中的RaspberryPiPort一致
    # 创建套接字对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 绑定地址和端口
    server_socket.bind((host, port))
    # 开始监听连接
    server_socket.listen(1)
    print("等待连接...")
    # 接受连接
    client_socket, addr = server_socket.accept()
    print("连接来自: ", addr)
    # 打开串口
    serial_port = serial.Serial("/dev/ttyAMA1", 9600)
    # 创建并启动处理客户端数据的线程
    client_thread = threading.Thread(
        target=handle_client, args=(client_socket, serial_port)
    )
    client_thread.start()
    # 创建并启动处理串口数据的线程
    serial_thread = threading.Thread(
        target=handle_serial, args=(serial_port, client_socket)
    )
    serial_thread.start()
    # 创建并启动监控线程
    monitor_thread = threading.Thread(target=monitor_threads)
    monitor_thread.start()
    # 等待线程完成
    client_thread.join()
    serial_thread.join()
    monitor_thread.join()
    # 关闭连接
    server_socket.close()
    serial_port.close()


if __name__ == "__main__":
    main()
