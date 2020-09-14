"""Solutions to EX08."""


def students_study(time: int, coffee_needed: bool) -> bool:
    """
    Return True if students study in given circumstances.

    (19, False) -> True
    (1, True) -> False.
    """
    if 18 <= time <= 24:
        return True
    elif 5 <= time <= 17 and coffee_needed:
        return True
    else:
        return False


def lottery(a: int, b: int, c: int) -> int:
    """
    Return Lottery victory result 10, 5, 1, or 0 according to input values.

    (5, 5, 5) -> 10
    (2, 2, 1) -> 0
    (2, 3, 1) -> 1
    """
    if a == b == c == 5:
        return 10
    elif a == b == c:
        return 5
    elif a != b and a != c:
        return 1
    else:
        return 0


def fruit_order(small_baskets: int, big_baskets: int, ordered_amount: int) -> int:
    """
    Return number of small fruit baskets if it's possible to finish the order, otherwise return -1.

    (4, 1, 9) -> 4
    (3, 1, 10) -> -1
    """
    if ordered_amount == 0:
        return 0
    if 5 > ordered_amount == small_baskets:
        return small_baskets
    if big_baskets * 5 == ordered_amount:
        return 0
    if ordered_amount > big_baskets * 5 and ordered_amount - big_baskets * 5 > small_baskets:
        return -1
    elif ordered_amount < big_baskets * 5:
        ordered_amt = ordered_amount
        while ordered_amt >= 5:
            ordered_amt -= 5
        if ordered_amt == 0:
            return 0
        elif ordered_amt > small_baskets:
            return -1
    if ordered_amount % 5 == 0 and big_baskets * 5 >= ordered_amount:
        return 0
    if big_baskets * 5 + small_baskets == ordered_amount:
        return small_baskets
    if big_baskets * 5 + small_baskets > ordered_amount and small_baskets != 0:
        return ordered_amount - big_baskets * 5
    else:
        return -1


if __name__ == '__main__':
    print(fruit_order(0, 100, 495))
