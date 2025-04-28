import numpy as np


# 一阶低通滤波器
def lowpass_filter(input, alpha, state):
    state[0] = alpha * input + (1.0 - alpha) * state[0]
    return state[0]


# 一阶高通滤波器
def highpass_filter(input, alpha, state, prev_input):
    output = alpha * (state[0] + input - prev_input[0])
    prev_input[0] = input
    state[0] = output
    return output


# 滑动平均滤波器
# 用于平滑信号，适合处理周期性噪声。
# 参数：
# - input: 当前输入信号
# - buffer: 滤波器的缓冲区，用于存储最近的输入值
# - buffer_size: 缓冲区大小
# - index: 当前缓冲区的索引（列表形式，用于保持状态）
# - sum: 缓冲区中所有值的总和（列表形式，用于保持状态）
# 返回值：滤波后的信号
def moving_average_filter(input, buffer, buffer_size, index, sum):
    sum[0] -= buffer[index[0]]  # 从总和中减去旧值
    buffer[index[0]] = input  # 更新缓冲区
    sum[0] += input  # 将新值加到总和中
    index[0] = (index[0] + 1) % buffer_size  # 更新索引
    return sum[0] / buffer_size  # 返回平均值


# 加权平均滤波器
# 对输入数据赋予不同的权重。
# 参数：
# - inputs: 输入信号数组
# - weights: 权重数组，与输入信号一一对应
# 返回值：滤波后的信号
def weighted_average_filter(inputs, weights):
    sum = np.dot(inputs, weights)  # 计算加权和
    weight_sum = np.sum(weights)  # 计算权重总和
    return sum / weight_sum  # 返回加权平均值


# 中值滤波器
# 用于去除尖锐的噪声（如脉冲噪声）。
# 参数：
# - buffer: 输入信号数组
# 返回值：滤波后的信号（中值）
def median_filter(buffer):
    return np.median(buffer)  # 返回数组的中值


# 指数加权移动平均滤波器
# 用于实时数据流的平滑处理。
# 参数：
# - input: 当前输入信号
# - alpha: 滤波系数，范围为 0.0 到 1.0，越接近 1.0 响应越快
# - state: 滤波器的状态变量（列表形式，用于保持状态）
# 返回值：滤波后的信号
def exponential_moving_average(input, alpha, state):
    state[0] = alpha * input + (1.0 - alpha) * state[0]  # 更新状态
    return state[0]  # 返回滤波后的信号


# 卡尔曼滤波器
# 用于动态系统的状态估计。
# 参数：
# - input: 当前输入信号
# - estimate: 滤波器的状态估计值（列表形式，用于保持状态）
# - error_cov: 估计误差协方差（列表形式，用于保持状态）
# - process_noise: 过程噪声协方差
# - measurement_noise: 测量噪声协方差
# 返回值：滤波后的信号
def kalman_filter(input, estimate, error_cov, process_noise, measurement_noise):
    kalman_gain = error_cov[0] / (error_cov[0] + measurement_noise)  # 计算卡尔曼增益
    estimate[0] = estimate[0] + kalman_gain * (input - estimate[0])  # 更新估计值
    error_cov[0] = (1 - kalman_gain) * error_cov[0] + process_noise  # 更新误差协方差
    return estimate[0]  # 返回滤波后的信号


# 自适应滤波器
# 用于处理非平稳信号。
# 参数：
# - input: 当前输入信号
# - reference: 参考信号
# - weights: 滤波器的权重（列表形式，用于保持状态）
# - step_size: 步长，用于更新权重
# - num_taps: 滤波器的阶数
# 返回值：滤波后的信号
def adaptive_filter(input, reference, weights, step_size, num_taps):
    output = np.dot(weights, reference)  # 计算滤波器输出
    error = input - output  # 计算误差
    weights += step_size * error * reference  # 更新权重
    return output  # 返回滤波后的信号


if __name__ == "__main__":
    # 测试滤波器
    input_signal = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    alpha = 0.5
    state = [0.0]
    prev_input = [0.0]
    buffer_size = 3
    buffer = np.zeros(buffer_size)
    index = [0]
    sum = [0.0]
    weights = np.array([0.1, 0.3, 0.6])
    inputs = np.array([1.0, 2.0, 3.0])

    print("Lowpass Filter:", lowpass_filter(input_signal[0], alpha, state))
    print(
        "Highpass Filter:", highpass_filter(input_signal[1], alpha, state, prev_input)
    )
    print(
        "Moving Average Filter:",
        moving_average_filter(input_signal[2], buffer, buffer_size, index, sum),
    )
    print("Weighted Average Filter:", weighted_average_filter(inputs, weights))
    print("Median Filter:", median_filter(input_signal[:buffer_size]))
    print(
        "Exponential Moving Average Filter:",
        exponential_moving_average(input_signal[3], alpha, state),
    )
