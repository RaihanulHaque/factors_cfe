import math
def printDivisors (n):
    factorL = []
    for i in range(1, int(math.sqrt(n))+1):
        if (n % i == 0):
            print(f"{i} {int(n/i)} ")
            factorL.append(i)
            factorL.append(int(n/i))

    return factorL
    # i = 1
    # while (i * i < n):
    #     if (n % i == 0):
    #         print(i, end = " ")
    #     i += 1
 
    # for i in range(int(math.sqrt(n)), 0, -1):
    #     if (n % i == 0):
    #         print(n // i, end = " ")

factor = printDivisors(1000)
