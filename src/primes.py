"""Useful methods for prime numbers

Refs:
 - https://www.quora.com/Whats-the-best-algorithm-to-check-if-a-number-is-prime
"""
import math
import random
import logging

# https://en.wikipedia.org/wiki/List_of_prime_numbers
PRIMES_FERMAT = [3, 5, 17, 257, 65537]
PRIMES_EUCLID = [3, 7, 31, 211, 2311, 200560490131]
PRIMES_FIBONACCI = [
    2,
    3,
    5,
    13,
    89,
    233,
    1597,
    28657,
    514229,
    433494437,
    2971215073,
    99194853094755497,
    1066340417491710595814572169,
    19134702400093278081449423917,
]
PRIMES_FACTORIAL = [
    2,
    3,
    5,
    7,
    23,
    719,
    5039,
    39916801,
    479001599,
    87178291199,
    10888869450418352160768000001,
    265252859812191058636308479999999,
    263130836933693530167218012159999999,
    8683317618811886495518194401279999999,
]
PRIMES_CULLEN = [3, 393050634124102232869567034555427371542904833]
PRIMES_BELL = [
    2,
    5,
    877,
    27644437,
    35742549198872617291353508656626642567,
    359334085968622831041960188598043661065388726959079837,
]


def primes_famous():
    """Return list of famous primes."""
    return sorted(
        set(
            PRIMES_FERMAT
            + PRIMES_EUCLID
            + PRIMES_FIBONACCI
            + PRIMES_FACTORIAL
            + PRIMES_CULLEN
            + PRIMES_BELL
        )
    )


def gen_primes_eratosthenes(n):
    """Generate all primes up to provided n value using Sieve of Eratosthenes"""
    if n >= 10**8:
        logging.warning(
            "Provided n greater than 10^8 - 1. Universe could freeze before this execution ends."
        )
    prime = [True for i in range(n + 1)]
    p = 2
    while p * p <= n:
        if prime[p] == True:
            for i in range(p * p, n + 1, p):
                prime[i] = False
        p += 1

    # yield prime numbers
    for p in range(2, n + 1):
        if prime[p]:
            yield p


def test_primality_composite(p):
    """Test if a number p is prime by composite property.

    > Every composite number has at least one prime factor less than or equal to square root of itself.

    This property can be proved using counter statement. Let a and b be two factors of n such that a*b = n.
    If both are greater than sqrt(n), then a.b > sqrt(n), * sqrt(n),
    which contradicts the expression “a * b = n”.

    Time Complexity: O(sqrt(n))
    """
    for i in range(2, int(math.sqrt(p))):
        if p % i == 0:
            if i != p:
                return False
    # i == p
    return True


def test_primality_fermat(p, k=5):
    """Test if a number p is prime by statistical Fermat's primality test. Perform k tests.

    This is a statistical test, so it may fail in some cases. Use greater values of k
    to reduce the probability of failing. For values greater than 100 out of memory can happen.

    Test may fail due pseudo-primes, those little bastards...

    Refs:
     - https://en.wikipedia.org/wiki/Fermat_primality_test
     - https://math.stackexchange.com/questions/3363141/probability-that-a-number-passing-the-fermat-test-is-prime
    """
    """
    if p in (1, 2):
        return True

    if p % 2 == 0:
        return False
    """

    for _ in range(k):
        a = random.randint(1, p - 1)
        if math.pow(a, p - 1) % p != 1:
            # is Fermat witness, thus prime
            return False
    return True
