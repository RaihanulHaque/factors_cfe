def primeFactors(n):
    c = 2
    step = 0
    str_primef = ""
    multi_primef = ""
    primef = []
    left = []
    while n > 1:
        step = step + 1
        if n % c == 0:
            # print(c, end=" ")
            primef.append(c)
            left.append(int(n))
            str_primef = str_primef+f"{c}, "
            multi_primef = multi_primef + f"{c} * "
            n = n / c
        else:
            c = c + 1
    left.append(1)
    # multi_primef = multi_primef[:-2]
    return primef, left, str_primef[:-2], multi_primef[:-2]


def primeFactors2(n):
    factors = {}
    c = 2
    while (n > 1):

        if (n % c == 0):
            factors[int(n)] = c
            n = n / c
        else:
            c = c + 1
    return factors

def isPrimeorComposite(n):
    primef, left, str_primef = primeFactors(n)
    if len(primef) > 1:
        return f"{n} is a composite number."
    else:
        return f"{n} is a prime number."


# n = 103650
arr = [32768, 33592, 604]
n = arr[0]
primef, left, str_primef, multi_primef = primeFactors(n)
# for i in range(0, len(primef)):
#     print(f"{left[i]}\n")
#     print(f"{primef[i]}      {left[i+1]}")
#     print("\n")
# print(len(primef))
# print(isPrimeorComposite(n))
print(primef)
print(primef)
print(primeFactors2(n))
# print(left)
# print(str_primef)
# print(multi_primef)
