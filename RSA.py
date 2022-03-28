import random
 """
    Naive RSA encryption system implementation.

    The program will take as input the security parameter nu. It will then generate the two nu/2-bit primes, and the
    integers N; e and d. It will then prompt the user to choose one of the two options - encryption and decryption.
    If the user chooses encryption, the program will prompt the user to enter an element from the plaintext space
    Z=NZ and provide its encryption. If the user chooses decryption, the program will prompt the user to enter an
    element from the ciphertext space Z=NZ and provide its decryption.
    """

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

    # until remainder is not zero this loop continues
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


def generate_prime_number(limit: int) -> int:
    """
    This function randomly generates a prime number of the bit size specified in the param
    and also tests its primality by partial trial division method and fermat's test

    :param limit: the bit size to generate a random prime number of bits between limit -1 and the limit
    :return: a prime number
    """
    p = 0
    is_prime = False

    # setting up the range of the bit size for the prime number
    init_range = exponential(2, limit - 1)
    val_range = exponential(2, limit)

    while not is_prime:

        # randomly generating a prime number between the bits specified
        p = random.randint(init_range, val_range)

        # checking the primality of the prime number
        if p > 2 and check_prime_by_partial_trial_division_method(p) == 1:
            if check_by_fermat_test_method(p, 50) == 1:
                break
    return p


def check_prime_by_partial_trial_division_method(n: int) -> int:
    """
    This function checks if a given number is a prime by using a partial trial division method with a bound till 100

    :param n: The number to check if it is a prime or not
    :return: 1 if the number is prime otherwise return its certificate of compositeness
    """
    for x in range(2, 101):

        # checking if the number is divisible by any number between 2 and 100
        if x != n and n % x == 0:
            return x
        # returns 1 if number is a prime
    return 1


def check_by_fermat_test_method(num: int, k: int) -> int:
    """
    The function checks if the given number is a probable prime using Fermat's little theorem in specified number of
    iterations.

    :param num: the number to be checked if it is a prime
    :param k: the number of iterations to check for a number to be probable prime
    :return: 1 if the number is not found to be a prime in k iterations; otherwise returns the certificate of compositeness
    """
    for i in range(k):
        a = random.randint(2, num - 1)

        # by fermat's little theorem b == 1 if n is a prime
        b = exponential(a, num - 1) % num

        if b != 1:
            return a
    return 1


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


def print_separators() -> None:
    """
    The function prints the separators on console

    :return: None
    """
    print(20 * '-')


def encrypt(m: int, e: int, N: int) -> int:
    """
    The function encrypts a given plaintext message m to a ciphertext using RSA scheme

    :param m: the plain text message which needs to be encrypted
    :param e: the public key
    :param N: the public parameter N
    :return: the ciphertext obtained by encrypting the plaintext m
    """
    return int(exponential(m, e)) % N


def decrypt(c: int, d: int, N: int) -> int:
    """
    The function decrypts a cipher text to plain text using RSA scheme.

    :param c: the ciphertext to be decrypted
    :param d: the private key
    :param N: the public parameter N
    :return: the plain text for the given cipher text
    """
    return int((exponential(c, int(d))) % int(N))


# taking input the security paramter nu
nu = int(input(f"Please enter the security parameter `nu': "))
print_separators()
print('Setup:')
limit = int(nu // 2)

# generating the first nu/2 bit prime number
p = generate_prime_number(limit)
print(f"The first prime generated by the Setup algorithm is p = {p}")

# generating the second nu/2 bit prime number
q = generate_prime_number(limit)
while p == q:
    q = generate_prime_number(limit)
print(f"The second prime generated by the Setup algorithm is q = {q}")

# generating the public parameter N
N = p * q
print(f"The integer N = pq = {N}")
M = (p - 1) * (q - 1)

# generating a random integer e such that gcd(e;M) = 1:
while True:
    i = exponential(2, ((nu // 2) - 1))
    e = random.randint(i, M)

    # checking if gcd (e,M) == 1 and also generating its inverse d
    gcd, inverse, y = extended_euclidean_algorithm(e, M)
    if gcd == 1:
        break

if inverse < 0:
    # if the multiplicative inverse is not from the set Z/MZ; we find its equivalent representation within Z/MZ
    d = get_negative_number_representation(inverse, M)
else:
    d = inverse

print(f'The encryption exponent is e = {e}')
print(f'The decryption exponent is d = {d}')
print_separators()

play = True
while play:
    operation = int(input(f"Please enter an option: \n 1 to Encrypt \n 2 to Decrypt \n Any other number to quit "
                          f"\n Your option:"))

    # if a user wants to encrypt a plaintext
    if operation == 1:
        print('Encryption:')
        print("Your message space is the set {Z/NZ} = {0,1,......,", N - 1, '}')
        m = int(input('Please enter a number from this set:'))
        encrypted_text = encrypt(m, e, N)
        print(f"The ciphertext for your message {m} is {encrypted_text}")
        print_separators()

    # if a user wants to decrypt a cipher text
    elif operation == 2:
        print('Decryption:')
        print("Your ciphertext space is the set {Z/NZ} = {0,1,......,", N - 1, '}')
        cipher = int(input('Please enter a number from this set:'))
        decrypted_text = decrypt(cipher, d, N)
        print(f"The plaintext for your ciphertext {cipher} is {decrypted_text}")
        print_separators()

    # if a user wants to quit
    else:
        break
