import numpy as np

def generate_random_matrix(n, m, q):
    # 生成随机矩阵
    return np.random.randint(q, size=(n, m))

def select_random_vector(R, sigma_squared):
    # 计算协方差矩阵C = RR^T
    C = np.dot(R.T, R)
    
    # 计算扰动矩阵D = σ²I - C
    D = sigma_squared * np.eye(C.shape[0]) - C
    
    # 对D进行特征值分解
    eigenvalues, eigenvectors = np.linalg.eig(D)
    
    # 随机生成一个服从标准正态分布的向量
    x = np.random.randn(len(eigenvalues))
    
    # 计算扰动向量y = E(D⁰·x)
    D_sqrt = np.diag(np.sqrt(np.abs(eigenvalues)))
    y = np.dot(eigenvectors, np.dot(D_sqrt, x))
    
    # 最终的随机向量v = y + μ，其中μ是RRᵀ的均值向量
    mean_vector = np.mean(C, axis=1)
    v = y + mean_vector
    
    # 将浮点数向量四舍五入为整数向量
    rounded_vector = np.rint(v).astype(int)
    
    return rounded_vector

