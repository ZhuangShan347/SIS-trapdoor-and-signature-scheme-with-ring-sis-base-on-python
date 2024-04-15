import numpy as np
from itertools import product


def kronecker_product(matrix1, matrix2):
    """
    计算两个矩阵的Kronecker product
    
    参数：
    matrix1: 第一个矩阵（numpy数组）
    matrix2: 第二个矩阵（numpy数组）
    
    返回：
    kronecker_product_matrix: Kronecker product的结果（numpy数组）
    """
    # 获取两个矩阵的形状
    m1, n1 = matrix1.shape
    m2, n2 = matrix2.shape
    
    # 初始化结果矩阵
    kronecker_product_matrix = np.zeros((m1*m2, n1*n2))
    
    # 计算Kronecker product
    for i in range(m1):
        for j in range(n1):
            kronecker_product_matrix[i*m2:(i+1)*m2, j*n2:(j+1)*n2] = matrix1[i, j] * matrix2
    
    return kronecker_product_matrix

# 测试示例
def G(n):
     a = []

     for i in range(0,n):

         a.append(2**i)

     A = np.array([a])
     B = np.eye(n)

     G = kronecker_product(B, A)

     return G


def solve_matrix_equation(G, u, q, m):
    """
    使用遍历法求解矩阵方程Az = u
    
    参数：
    A: 矩阵A（numpy数组）
    u: 向量u（numpy数组）
    q: 正整数
    
    返回：
    z: 满足方程Az = u的向量z，如果不存在则返回None
    """
        
    possible_values = [0, 1, -1]
    
    # 枚举z的所有可能值
    for z_values in product(possible_values, repeat=m):
        z = np.array(z_values)
        # 计算Az
        Az = np.dot(G, z.T) % q
        # 如果Az等于u，则找到满足条件的z
        if np.array_equal(Az, u.T):
            return z
    
    # 如果不存在满足条件的z，则返回None
    return None

