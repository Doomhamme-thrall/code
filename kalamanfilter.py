import numpy as np  # noqa: D100


class KalmanFilter:
    def __init__(self, A, B, H, Q, R, P, x):
        """初始化卡尔曼滤波

        :param A: 状态转移矩阵
        :param B: 控制输入矩阵
        :param H: 观测矩阵
        :param Q: 过程噪声协方差
        :param R: 测量噪声协方差
        :param P: 估计误差协方差
        :param x: 初始状态.
        """
        self.A = A  # 状态转移矩阵
        self.B = B  # 控制输入矩阵
        self.H = H  # 观测矩阵
        self.Q = Q  # 过程噪声协方差
        self.R = R  # 测量噪声协方差
        self.P = P  # 估计误差协方差
        self.x = x  # 初始状态

    def predict(self, u=0):
        """预测下一时刻的状态

        :param u: 控制输入
        """
        self.x = np.dot(self.A, self.x) + np.dot(self.B, u)
        self.P = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q

    def update(self, z):
        """更新状态估计

        :param z: 测量值
        """
        y = z - np.dot(self.H, self.x)  # 计算测量残差
        S = np.dot(self.H, np.dot(self.P, self.H.T)) + self.R  # 残差协方差
        K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))  # 卡尔曼增益
        self.x = self.x + np.dot(K, y)  # 更新状态估计
        I = np.eye(self.A.shape[0])  # 单位矩阵
        self.P = np.dot(I - np.dot(K, self.H), self.P)

    def get_state(self):
        """获取当前状态估计"""
        return self.x


if __name__ == "__main__":
    pass
