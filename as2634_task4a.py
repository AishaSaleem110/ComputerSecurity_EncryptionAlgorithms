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


def modify_cipher(c: int, e: int, N: int) -> int:
    return (exponential(2, e) * c) % N


def get_negative_number_representation(neg, n):
    neg = abs(neg)
    if neg > (n - 1):
        neg = neg % n
    neg = n - neg
    return neg


N = int(input(f"Please enter the public parameter N:"))
e = int(input(f"Please enter the encryption exponent e:"))
print_separators()
c = int(input(f"Please enter the ciphertext c:"))
print_separators()
c1 = modify_cipher(c, e, N)
print(f"The modified ciphertext c` is = {c1}")
gcd, inverse, y = extended_euclidean_algorithm(2, N)
if inverse < 0:
    inverse = get_negative_number_representation(inverse, N)

print(f"The inverse of 2 mod {N} is {inverse}")
print("Please decrypt the modified ciphertext c` using your program from Task 1.")
m1 = int(input("Please input the plaintext m` decrypted from c`:"))
m = (m1 * inverse) % N
print(f"The original plaintext message m computed from m` is: {m}")
