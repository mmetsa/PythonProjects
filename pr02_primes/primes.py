"""Primes identifier."""


def is_prime_number(number: int) -> bool:
    """
    Check if number (given in function parameter) is prime.

    If number is prime -> return True
    If number is not prime -> return False

    :param number: number for check.
    :return: boolean True if number is prime or False if number is not prime.
    """
    if number > 1:
        if number == 2:
            return True
        for i in range(2, number):
            if number % i == 0:
                return False
        return True


if __name__ == '__main__':
    print(is_prime_number(9))  # -> True
    print(is_prime_number(89))  # -> True
    print(is_prime_number(23))  # -> True
    print(is_prime_number(4))  # -> False
    print(is_prime_number(7))  # -> True
    print(is_prime_number(88))  # -> False
