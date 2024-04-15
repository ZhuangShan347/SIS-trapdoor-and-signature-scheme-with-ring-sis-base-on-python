def multiply_polynomials_mod(poly1, poly2, modulo_poly):
    # 计算结果多项式的次数
    degree = len(poly1) + len(poly2) - 2
    result = [0] * (degree + 1)

    # 逐项相乘并累加到结果多项式中
    for i in range(len(poly1)):
        for j in range(len(poly2)):
            result[i + j] += poly1[i] * poly2[j]

    # 模(x^n + 1)
  

    while len(result) >= len(modulo_poly):
        if result[-1] != 0:
            for j in range(len(modulo_poly)):
                result[-len(modulo_poly) + j] += result[-1] * modulo_poly[j]
        result.pop()

    return result


