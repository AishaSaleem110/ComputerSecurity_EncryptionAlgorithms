import random


def generate_prime_factors(n: int) -> dict:
    """
    this function generates prime factors for the given integer n
    :param n: the number for which primes factors are required
    :return: the prime factors in a dictionary
    """
    factors = {}

    while n % 2 == 0:
        check_if_value_in_factors(2, factors)
        n = n // 2

    for i in range(3, square_root(n) + 1, 2):
        while n % i == 0:
            check_if_value_in_factors(i, factors)
            n = n // i
    if n > 2:
        check_if_value_in_factors(n, factors)
    return factors


def check_if_value_in_factors(num: int, factors: dict) -> None:
    """
    This function checks if a base number already exists in the dictionary; if it does it increments its power by 1
     ;otherwise enter this new base in the prime factors.

    :param num: Base number to check if it exists in the dictionary representing prime factors
    :param factors: dictionary maintaining the prime factors as key value pairs; where key is a base and its power is the value
    :return: None
    """
    if num in factors:
        factors[num] += 1
    else:
        factors[num] = 1


def square_root(num: int) -> int:
    """
    This function calculates the square root of the number
    :param num: The value of the number for which square root needs to be computed
    :return: the square root of the number
    """
    return int(pow(num, 1 / 2))


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


def legendre_calculation(a: int, p: int) -> int:
    """
    This function calculates legendre symbol of the given integer a w.r.t. prime p

    :param a: the value of the number for which legendre symbol needs to be computed
    :param p: the value of prime number p
    :return: the legendre symbol of a w.r.t. prime p
    """
    power = int((p - 1) / 2)
    num = (exponential(a, power)) % p

    # (a/p) = ( a^((p-1)/2) ) mod p
    if num > 1 and ((num + 1) % p) == 0:
        return -1
    else:
        return num


def jacobi_calculation(a: int, q: int) -> int:
    """
    This function calculates Jacobi symbol of the given integer a w.r.t. composite q

    :param a: the value of the number for which legendre symbol needs to be computed
    :param q: the value of the composite number q
    :return: the jacobi symbol of an int 'a' w.r.t. composite number q
    """
    if a == 0:
        return 0
    if a == 1:
        return 1

    # first generate prime factors of a composite number q
    dic = generate_prime_factors(q)
    result = 1
    for key in dic:
        # calculate jacobi symbol
        result = result * exponential(legendre_calculation(a, key), dic[key])
    return result


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


def chinese_remainder_theorem(a: int, M: int, b: int, N: int) -> int:
    """
    This function finds the solution 'y' to two equations y = a mod M and y = b mod N using chinese remainder theorem
    :param a: the value of the divisor of the first equation
    :param M: the modulus value of first equation
    :param b: the value of the divisor of the second equation
    :param N: the modulus value of second equation
    :return: the solution of the two equations
    """
    d, x, y = extended_euclidean_algorithm(M, N)

    # chinese remainder theorem can only be applied if gcd of modulus of two equations is 1
    if d != 1:
        return 0
    if x < 0:
        t = get_negative_number_representation(x, N)
    else:
        t = x

    # applying chinese remainder theorem
    u: int = ((b - a) * t) % N

    return a + u * M


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


def check_if_valid_cipher(num: int, N: int) -> bool:
    """
    # This function checks if user has entered a valid ciphertext to be decrypted. GM is secure under the QUADRES assumption.
    If a ciphertext is generated correctly, it will be in J_N.

    :param num: ciphertext that needs to be checked if it is a valid cipher text
    :param N: The public parameter N
    :return: true if the ciphertext is a valid ciphertext i.e. it should belong to (Z/NZ)* and its Jacobi Symbol is 1
    """
    if get_gcd_by_euclidean(num, N) == 1 and jacobi_calculation(num, N) == 1:
        return True


def encrypt(bit, y, N) -> int:
    """
    The function encrypts a given plaintext message bit to a ciphertext using GoldWasser Micali scheme

    :param bit: the plain text message which needs to be encrypted
    :param y: the public key
    :param N: the public parameter N
    :return: the ciphertext obtained by encrypting the plaintext bit
    """

    mutually_prime_elements = get_mutually_prime_elements(N)
    index = random.randint(0, len(mutually_prime_elements))
    x = mutually_prime_elements[index]
    if bit == 0:
        c = exponential(x, 2) % N
        return c
    elif bit == 1:
        c = (y * exponential(x, 2)) % N
        return c


def decrypt(c: int, p: int) -> int:
    """
    The function decrypts a cipher text to plain text using GoldWasser Micali scheme.

    :param c: the ciphertext to be decrypted
    :param d: the private component
    :return: the plain text for the given cipher text
    """
    result = legendre_calculation(c, p)
    if result == 1:
        return 0
    elif result == -1:
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


# taking input the security paramter nu
nu = int(input(f"Please enter the security parameter `nu': "))
print_separators()
print('Setup:')
limit = nu // 2

# generating the first nu/2 bit prime number
p = generate_prime_number(int(limit))
print(f"The first prime generated by the Setup algorithm is p = {p}")

# generating the second nu/2 bit prime number
q = generate_prime_number(limit)
while p == q:
    q = generate_prime_number(limit)
print(f"The second prime generated by the Setup algorithm is q = {q}")

# generating the public parameter N
N = p * q
print(f"The integer N = pq = {N}")

# finding elements which are Quadratic Non Residues w.r.t primes p and q using legendre symbol
ya, yb = 0, 0

# if a legendre symbol of a ya is -1, it means the element y is a Quadratic Non Residue w.r.t. p
while legendre_calculation(ya, p) != -1:
    ya = random.randint(1, p)

# if a legendre symbol of a yb is -1, it means the element y is a Quadratic Non Residue w.r.t. q
while legendre_calculation(yb, q) != -1:
    yb = random.randint(1, q)

# finding solution to the following two equations using chinese remainder theorem
# y = ya mod p
# y = yb mod p
y: int = chinese_remainder_theorem(ya, p, yb, q)

# y is the public key for GoldWasser Micali system
print(f"The public key y = {y}")
print_separators()

play = True
while play:
    operation = int(input(f"Please enter an option: \n 1 to Encrypt \n 2 to Decrypt \n Any other number to quit "
                          f"\n Your option:"))

    # if a user wants to encrypt a plaintext
    if operation == 1:
        print('Encryption:')
        print('Your message space is the set: {0, 1}')
        m = int(input('Please enter a number from this set:'))
        c: int = encrypt(m, y, N)
        print(f"The ciphertext for your message {m} is {c}")
        print_separators()

    # if a user wants to decrypt a cipher text
    elif operation == 2:
        print('Decryption:')
        print(f'Your ciphertext space is the set J_{N}')
        m = int(input('Please enter a number from this set:'))

        # GM is secure under the QUADRES assumption. If a ciphertext is generated correctly, it will be in J_N. so we
        # check if user has entered a valid ciphertext to be decrypted
        while not check_if_valid_cipher(m, N):
            m = int(input('Please enter a number from this set:'))
        d = decrypt(m, p)
        print(f"The plaintext for your ciphertext {m} is {d}")
        print_separators()

    else:
        break
