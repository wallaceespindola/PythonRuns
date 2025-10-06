import math


def calc_power():
    print("####### Testing python exponents calc x^y #######")

    # Assign values to x and n
    x = 2
    n = 3

    # Method 1
    power = x**n
    print("Method 1 [**]: %d to the power %d is %d" % (x, n, power))

    # Method 2
    power = pow(x, n)
    print("Method 2 [pow]: %d to the power %d is %d" % (x, n, power))

    # Method 3
    power = math.pow(x, x)
    print("Method 3 [math.pow]: %d to the power %d is %d" % (x, x, power))

    # Method 3 with decimal exponent
    i = 3
    j = 6.5
    power = math.pow(i, j)
    print("Method 3 [math.pow] (with decimal exponent): %d to the power %3.1f is %5.2f" % (i, j, power))


if __name__ == "__main__":
    calc_power()
