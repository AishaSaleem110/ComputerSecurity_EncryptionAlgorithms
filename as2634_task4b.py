import random


def print_separators():
    print(20 * '-')


def exponential(base: int, power: int):
    if power == 0:
        return 1
    elif power == 1:
        return base
    elif power < 0:
        return exponential(1 / base, base * (-1))
    elif power % 2 == 0:
        return exponential(base * base, power / 2)
    else:
        return base * exponential(base * base, (power - 1) / 2)


def extended_euclidean_algorithm(a, b):
    r1, r = a, b
    s1, s = 1, 0
    t1, t = 0, 1

    while r != 0:
        q1 = int((r1 // r))
        r1, r = r, (r1 - (q1 * r))
        s1, s = s, (s1 - (q1 * s))
        t1, t = t, (t1 - (q1 * t))
        d = r1
        x = s1
        y = t1
        rr = r
        if rr == 0:
            return d, x, y


def get_gcd_by_euclidean(a: int, b: int):
    r: int = b
    while r != 0:
        r = a % b
        a = b
        b = r

    return a


def get_mutually_prime_elements(N: int) -> list:
    mutually_prime_list = []
    for i in range(1, N - 1):
        if get_gcd_by_euclidean(i, N) == 1:
            mutually_prime_list.append(i)
    return mutually_prime_list


def modify_cipher(c: int, N: int) -> int:
    mutually_prime_elements = get_mutually_prime_elements(N)
    index = random.randint(0, len(mutually_prime_elements))
    x = mutually_prime_elements[index]
    return (exponential(x, 2) * c) % N


def get_negative_number_representation(neg, n):
    neg = abs(neg)
    if neg > (n - 1):
        neg = neg % n
    neg = n - neg
    return neg


N = int(input(f"Please enter the public parameter N:"))
y = int(input(f"Please enter the encryption key:"))
print_separators()
c = int(input(f"Please enter the ciphertext c:"))
print_separators()
c1 = modify_cipher(c, N)
print(f"The modified ciphertext c` is = {c1}")
