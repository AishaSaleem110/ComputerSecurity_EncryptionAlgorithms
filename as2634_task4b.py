import random

"""
Write a program to demonstrate that Goldwasser-Micali encryption scheme is insecure with respect to an
IND-CCA adversary. The program will take as input a public key (N; y) and a ciphertext c created by the
program written for Task 2. It will then output the modied ciphertext c' = c . z^2 (mod N) for a random
z belongs (Z=NZ)*. This modifed ciphertext c' = c . z^2 (mod N) can be decrypted using the program you have
written for Task 2 to check if the decryption is correct.

"""
# To show GoldWasser Micali encryption scheme is not IND-CCA secure

def print_separators() -> None:
    """
    The function prints the separators on console

    :return: None
    """
    print(20 * '-')


def exponential(base: int, power: int) -> int:
    """
    This is the function to calculate exponential

    :param base: the value to want to raise to a power
    :param power: the value of the power
    :return: the value of the base raised to the given power
    """
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


def extended_euclidean_algorithm(a: int, b: int) -> tuple[int, int, int]:
    """
    This is the function to get the greatest common divisor between two numbers and also returns inverses for the numbers

    :param a: the value of the first number
    :param b: the value of the second number
    :return: a tuple containing gcd of two params, multiplicative inverse of the first param and multiplicative inverse
    of the second param respectively
    """
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


def get_gcd_by_euclidean(a: int, b: int) -> int:
    """
    This function calculates greatest common divisor of two integers using Euclidean Algorithm
    :param a: the value of the first number
    :param b: the value of the second number
    :return: the greatest common divisor of two input params
    """
    r: int = b
    while r != 0:
        r = a % b
        a = b
        b = r

    return a


def get_mutually_prime_elements(N: int) -> list:
    """
    This function generates the elements of the set (Z/NZ)* i.e. the elements that are mutually prime to N
    :param N: The value of N for the set (Z/NZ) for which mutually prime elements needs to be generated
    :return: the list of mutually prime elements to N
    """
    mutually_prime_list = []
    for i in range(1, N - 1):
        # if an element is mutually prime to N ; it's gcd will be 1 w.r.t N
        # calculating gcd by Euclidean algorithm
        if get_gcd_by_euclidean(i, N) == 1:
            mutually_prime_list.append(i)
    return mutually_prime_list


def modify_cipher(c: int, N: int) -> int:
    """
    This function modifies the cipher text using Homomorphism property by multiplying it to another cipher text 2^e
    :param c: initial ciphertext that needs to be modified
    :param N: the public parameter N
    :return: the modified ciphertext
    """
    # calculating a new ciphertext with a random number z which belongs to the set (Z/NZ)* and then multiplying it
    # with given ciphertext to generate a new modified cipher text

    mutually_prime_elements = get_mutually_prime_elements(N)
    index = random.randint(0, len(mutually_prime_elements))
    x = mutually_prime_elements[index]
    return (exponential(x, 2) * c) % N


def get_negative_number_representation(neg: int, n: int) -> int:
    """
    This function maps a negative number to find its representation within the set Z/nZ

    :param neg: The negative number to be mapped to Z/nZ
    :param n: The value of n to generate the set Z/nZ
    :return: the representation of the negative number from the set Z/nZ
    """
    neg = abs(neg)

    # if the number is out of the set of Z/nZ we first find its representation within the set
    if neg > (n - 1):
        neg = neg % n

    # we then find the inverse of the negative number which is a positive number and from within the set Z/nZ
    neg = n - neg
    return neg


# taking input the public key paramters N and y
N = int(input(f"Please enter the public parameter N:"))
y = int(input(f"Please enter the encryption key:"))
print_separators()

# taking ciphertext as input
c = int(input(f"Please enter the ciphertext c:"))
print_separators()

# calculating a new ciphertext with a random number z which belongs to the set (Z/NZ)* and then multiplying it
# with given ciphertext to generate a new modified cipher text c1
c1 = modify_cipher(c, N)
print(f"The modified ciphertext c` is = {c1}")

# if we decrypt this modified cipher text c` using our task 2 (GM decryption), we can recover the original plaintext
# which shows GM Scheme is not IND-CCA secure
