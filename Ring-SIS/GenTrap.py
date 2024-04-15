import numpy as np

from Tool import G, solve_matrix_equation
from error import select_random_vector


def generate_random_matrix(rows, cols, q):
    return np.random.randint(0, q, size=(rows, cols))  # 生成随机整数矩阵

def compute_A(G, n, q):
    B = generate_random_matrix(n, n, q)
    R = generate_random_matrix(n, n**2, q)

    BR = np.dot(B, R)

    A = np.concatenate((B, G - BR), axis=1)%q
    return A, B, R

def compute_sk(R, z, q, n, p):

    I = np.eye(n**2)

    RI = np.concatenate((R.T, I), axis=1)%q

    sk = np.dot(RI.T, z.T)+p
    return sk


def panduan(A, sk, u, q):

    u1 = np.dot(A, sk.T)%q

    if np.array_equal(u1, u):

        return print("陷门值合理"), u, u1


# 示例输入
n = 3

m = n*n

q = 3

u = np.random.randint(0, q, size=n)

G = G(n)

A, B, R = compute_A(G, n, q)

# 参数设置
sigma_squared = 1.0  # 方差

# 在（σ²I - RR^T）中随机选取一个整数系数向量
p = select_random_vector(R, sigma_squared)

print("随机选取的整数系数向量：", p)

p1 = np.concatenate((np.zeros(n), p), axis=0)

# 求解方程Az = u
z = solve_matrix_equation(G, (u - np.dot(A, p1.T))%q, q, m)

if z is not None:
    print("\n找到满足条件的 z:")
    print(z)
else:
    print("\n未找到满足条件的 z.")

sk = compute_sk(R, z, q, n, p1)%q


aa, u, u1 = panduan(A, sk, u, q)



#file_path = 'E:\\单壮\\sn-article-template\\Ring-SIS\\Tool.txt'
#print("\n工具矩阵 G:")
#print(G)
#print("\nq:")
#print(q)
#print("\nm:")
#print(m)
#print("\nn:")
#print(n)
#print("\n解 z:")
#print(z)
# 给定的维度
# 生成随机矩阵 B 和 R
# 计算 A
#print("随机矩阵 B:")
#print(B)

print(aa, u, u1)

print("\n随机矩阵 R:")
print(R)

print("\n计算得到的矩阵 A:")
print(A)


print("\n向量 u:")
print(u)

print("\n计算得到的 sk:")
print(sk)



with open('E:\\单壮\\sn-article-template\\Ring-SIS\\GenTrap.txt', 'w') as file:
    file.write("公钥 A:\n")
    np.savetxt(file, A, fmt='%d')
    file.write("\n\n向量 u:\n")
    np.savetxt(file, u, fmt='%d')
    file.write("\n\nq:\n")
    file.write(str(q))
    file.write("\n\nm:\n")
    file.write(str(m))
    file.write("\n\nn:\n")
    file.write(str(n))
    file.write("\n\nsk:\n")

    np.savetxt(file, sk, fmt='%d')

print("密钥已经存储到文件 'GenTrap.txt' 中。")