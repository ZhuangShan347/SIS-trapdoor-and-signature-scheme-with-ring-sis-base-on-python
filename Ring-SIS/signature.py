from ploy import multiply_polynomials_mod
import numpy as np

# 示例使用
#poly1 = [1, 0]     # x + 1
#poly2 = [0, 0, 1,1]  # x^2 + 1
#modulo_poly = [-1, 0, 0, 1]  # x^3 + 1

#result = multiply_polynomials_mod(poly1, poly2, modulo_poly)
#print(result)  # 输出结果为 [1, 1, 1]，表示 (x + 1) * (x^2 + 1) % (x^3 + 1) = x^2 + x + 1
def add_lists(lists):
    # 获取列表中第一个列表的长度，假设所有列表的长度相同
    n = len(lists[0])
    
    # 创建一个长度为n的空列表，用于存放结果
    result = [0] * n
    
    # 对每个列表中的元素进行相加
    for lst in lists:
        for i in range(n):
            result[i] += lst[i]
    
    return result

def polynomial_to_vector(poly, message, m, n, modulo_poly):
    """
    将多项式映射到±1组成的向量
    
    参数:
    poly: list, 多项式的系数列表，其中poly[i]为x的i次项的系数
    m: int, 目标向量的维度
    
    返回值:
    vector: np.array, 由±1组成的向量
    """
    vector = [[0] * n for _ in range(m)]  # 初始化结果向量

    # 计算多项式在m个点的取值，并映射到±1
    for i in range(m):
        
        value = multiply_polynomials_mod(poly[i], message, modulo_poly)

        for j in value:

            if value[j] > 1:
                value[j] = 1

            elif value[j] < -1:
                value[j] = -1

            else:
                pass
        
        vector[i] = value
        
        #sum(poly[j] * ((message[j]+x) ** j) for j in range(n))  # 计算多项式在x处的值
        #print(value)
        

    return vector


def generate_matrix(m, n, q):
    matrix = []
    for i in range(m):
        row = []
        for j in range(m):
            vector = np.random.randint(0, q, size=n).tolist()  # 生成 n 维的随机正整数列表
            row.append(vector)
        matrix.append(row)
    return matrix


def Setup():

    with open('E:\\单壮\\sn-article-template\\Ring-SIS\\GenTrap.txt', 'r') as file:
        lines = file.readlines()

        # 读取 m
        m_index = lines.index("m:\n") + 1
        m = int(lines[m_index].strip())

        # 读取 n
        n_index = lines.index("n:\n") + 1
        n = int(lines[n_index].strip())

         # 读取 q
        q_index = lines.index("q:\n") + 1
        q = int(lines[q_index].strip())


        # 读取工具矩阵 G
        A_index = lines.index("公钥 A:\n") + 1
        A = np.loadtxt(lines[A_index:A_index + n], dtype=int)

        # 读取向量 u
        u_index = lines.index("向量 u:\n") + 1
        u = np.loadtxt(lines[u_index:u_index + n], dtype=int)

       
        

        # 读取 z
        sk_index = lines.index("sk:\n") + 1
        sk = np.loadtxt(lines[sk_index:sk_index + n**2+n], dtype=int)

    return A, u, sk, m, n, q # pk = (A,u), sk = sk


def Sign(A, sk, m, n, q, message, poly_coefficients, modulo_poly):

    
    HM = polynomial_to_vector(poly_coefficients, message, m, n, modulo_poly)

    A_f = generate_matrix(m, n, q)

    A_fS = [[0] * n for _ in range(m)]

    sigma1 = [[0] * n for _ in range(m)]

    for i in range(m):
        for j in range(m):
           
            A_fS0 = [x * sk[j] for x in A_f[i][j]]

            A_fS[i] = [x + y for x, y in zip(A_fS0, A_fS[i])]    

    #print(A_fS, HM, sk)

    for i in range(m):

        for j in range(n):

            sigma1[i][j] = HM[i][j] + A_fS[i][j]     
    
    for i in range(m):

        sigma1[i][0] = sigma1[i][0] + sk[i]


    sigma2 = [[0] * n for _ in range(m)]

    for i  in range(m):

        sigma2[i] = multiply_polynomials_mod(A.T[i], A_fS[i], modulo_poly)

    sigma2 = add_lists(sigma2)



    return A_fS, HM, sk, sigma1, sigma2


def mod_list_elements(lst, q):
    # 创建一个空列表，用于存放取模后的结果
    result = []
    
    # 遍历原始列表
    for num in lst:
        # 对每个元素执行取模操作，并将结果添加到结果列表中
        result.append(num % q)
    
    return result

def are_lists_equal(list1, list2, q):
    # 首先检查两个列表的长度是否相等
    list1 =  mod_list_elements(list1, q)

    list2 =  mod_list_elements(list1, q)
    # 遍历列表，逐个比较对应位置的元素
    for i in range(len(list1)):
        if list1[i] != list2[i]:
            return False
    
    # 如果循环结束都没有返回False，说明两个列表相等
    return True, list1, list2

def Verify(m, n, q, A, message, modulo_poly, sigma1, sigma2,sk):


    Fsigma1 = [[0] * n for _ in range(m)]

    #Fsigma1 = [0] * n 

    for i  in range(m):
        
        Fsigma1[i] = multiply_polynomials_mod(A.T[i], sigma1[i], modulo_poly)
        #Fsigma1[i] = multiply_polynomials_mod(A, sk[i], modulo_poly)
        
    Fsigma1 = add_lists(Fsigma1)
  
    FHM = [[0] * n for _ in range(m)]

    for i  in range(m):

        FHM[i] = multiply_polynomials_mod(A.T[i], HM[i], modulo_poly)

    FHM = add_lists(FHM)

    print(u,sigma2,FHM)

    sz = [0] * n

    for i in range(n):


        sz[i] = sigma2[i] +  FHM[i]  + u[i]

    
    return Fsigma1, sz



A, u, sk, m, n, q = Setup()

m = n**2 + n

modulo_poly = [-1]

for i in range(n-1):
    modulo_poly.append(0)

modulo_poly.append(1)

message = np.random.randint(0, 2, size=n).tolist()

poly_coefficients = np.random.randint(0, q, size=(m, n)) 

#print(poly_coefficients[2])

A_fS, HM, S, sigma1, sigma2 = Sign(A, sk, m, n, q, message, poly_coefficients, modulo_poly)

Fsigma1, sz = Verify(m, n, q, A, message, modulo_poly, sigma1, sigma2,sk)

zz, Fsigma1, sz = are_lists_equal(Fsigma1, sz, q) 

if zz == True:
    print('签名有效')
    

print("Fsigma1")
print(Fsigma1)

print("sz")
print(sz)

