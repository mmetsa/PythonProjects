"""Converter."""
import math


def dec_to_binary(dec: int) -> str:
    """
    Convert decimal number into binary.

    :param dec: decimal number to convert
    :return: number in binary
    """
    list_bin = []
    if dec == 0:
        list_bin.append(0)
    while dec != 0:
        list_bin.append(dec % 2)
        dec = math.floor(dec / 2)
    binary_values = ""
    for a in reversed(list_bin):
        binary_values = binary_values + str(a)
    return binary_values


def binary_to_dec(binary: str) -> int:
    """
    Convert binary number into decimal.

    :param binary: binary number to convert
    :return: number in decimal
    """
    current_position = len(binary)
    total_value = 0
    for number in binary:
        total_value += 2 ** (current_position - 1) * int(number)
        current_position -= 1
    return total_value


if __name__ == "__main__":
    print(dec_to_binary(0))  # -> 10010001
    print(dec_to_binary(245))  # -> 11110101
    print(dec_to_binary(255))  # -> 11111111

    print(binary_to_dec("1111"))  # -> 15
    print(binary_to_dec("10101"))  # -> 21
    print(binary_to_dec("10010"))  # -> 18
