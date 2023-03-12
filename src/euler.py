def gen_prime_poly():
    """Generate prime numbers using polynomials

    Refs:
     - https://www.gaussianos.com/polinomios-generadores-de-numeros-primos-los-numeros-afortunados-de-euler-y-el-163/?utm_source=ReviveOldPost&utm_medium=social&utm_campaign=ReviveOldPost
    """
    euler_lucky_nums = [2, 3, 5, 11, 17, 41]
    lucky_one = euler_lucky_nums[-1]
    euler_poly = lambda x: x**2 + x + lucky_one
    for i in range(lucky_one - 1):
        yield euler_poly(i)
