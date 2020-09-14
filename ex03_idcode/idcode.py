# -*- coding: utf-8 -*-
"""Check if given ID code is valid."""


def is_valid_year_number(year_number: int) -> bool:
    """
    Check if given value is correct for year number in ID code.

    :param year_number: int
    :return: boolean
    """
    if 0 <= year_number < 100:
        return True
    else:
        return False


def is_valid_gender_number(gender_number: int) -> bool:
    """
    Check if given gender number is correct.

    :param gender_number:
    :return: boolean
    """
    if 0 < gender_number <= 6:
        return True
    else:
        return False


def is_leap_year(year_number: int) -> bool:
    """
    Check if given year is a leap year.

    :param year_number:
    :return: boolean
    """
    if year_number % 400 == 0:
        return True
    elif year_number % 100 == 0:
        return False
    elif year_number % 4 == 0:
        return True
    else:
        return False


def get_gender(gender_number: int) -> str:
    """
    Check if the idcode belongs to a male or female.

    :param gender_number:
    :return: str
    """
    if gender_number % 2 == 0:
        return "female"
    else:
        return "male"


def is_valid_month_number(month_number: int) -> bool:
    """
    Check if given value is correct for month number in ID code.

    :param month_number: int
    :return: boolean
    """
    return 0 < month_number <= 12


def is_valid_day_number(gender_number: int, year_number: int, month_number: int, day_number: int) -> bool:
    """
    Check if given value is correct for day number in ID code.

    Also, consider leap year and which month has 30 or 31 days.
    :param gender_number: int
    :param year_number: int
    :param month_number: int
    :param day_number: int
    :return: boolean
    """
    year_number = get_full_year(gender_number, year_number)
    if month_number == 2:
        if is_leap_year(year_number):
            if day_number <= 29:
                return True
            else:
                return False
        else:
            if day_number <= 28:
                return True
            else:
                return False
    else:
        if month_number < 8:
            if month_number % 2 == 0 and day_number <= 30:
                return True
            elif month_number % 2 != 0 and day_number <= 31:
                return True
            else:
                return False
        else:
            if month_number % 2 == 0 and day_number <= 31:
                return True
            elif month_number % 2 != 0 and day_number <= 30:
                return True
            else:
                return False


def is_valid_birth_number(birth_number: int):
    """
    Check if given value is correct for birth number in ID code.

    :param birth_number: int
    :return: boolean
    """
    if 0 < birth_number < 1000:
        return True
    else:
        return False


def is_valid_control_number(id_code: str) -> bool:
    """
    Check if given value is correct for control number in ID code.

    Use algorithm made for creating this number.
    :param id_code: string
    :return: boolean
    """
    list_1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1]
    list_2 = [3, 4, 5, 6, 7, 8, 9, 1, 2, 3]
    if len(id_code) != 11 or not id_code.isdigit():
        return False
    control_number = 0
    s = 0
    for a in list_1:
        control_number += a * int(id_code[s])
        s += 1
    control_number = control_number % 11
    if control_number == 10:
        control_number = 0
        s = 0
        for a in list_2:
            control_number += a * int(id_code[s])
            s += 1
        control_number = control_number % 11
        if control_number == 10:
            control_number = 0
    if control_number == int(id_code[10]):
        return True
    else:
        return False


def get_full_year(gender_number: int, year_number: int) -> int:
    """
    Define the 4-digit year when given person was born.

    Person gender and year numbers from ID code must help.
    Given year has only two last digits.
    :param gender_number: int
    :param year_number: int
    :return: int
    """
    if gender_number <= 2:
        return year_number + 1800
    elif gender_number <= 4:
        return year_number + 1900
    else:
        return year_number + 2000


def get_birth_place(birth_number: int) -> str:
    """
    Find the place where the person was born.

    Possible locations are following: Kuressaare, Tartu, Tallinn, Kohtla-Järve, Narva, Pärnu,
    Paide, Rakvere, Valga, Viljandi, Võru and undefined. Lastly if the number is incorrect the function must return
    the following 'Wrong input!'
    :param birth_number: int
    :return: str
    """
    if not is_valid_birth_number(birth_number):
        return "Wrong input!"
    iterator = 0
    list_of_place_names = ["Kuressaare", "Tartu", "Tallinn", "Kohtla-Järve", "Tartu", "Narva", "Pärnu", "Tallinn",
                           "Paide", "Rakvere", "Valga", "Viljandi", "Võru", "undefined"]
    list_of_place_codes = [10, 20, 220, 270, 370, 420, 470, 490, 520, 570, 600, 650, 710, 999]
    for a in list_of_place_codes:
        if birth_number == 0:
            return "Wrong input!"
        if birth_number > a:
            iterator += 1
            continue
        else:
            return list_of_place_names[iterator]


def get_data_from_id(id_code: str) -> str:
    """
    Get possible information about the person.

    Use given ID code and return a short message.
    Follow the template - This is a <gender> born on <DD.MM.YYYY> in <location>.
    :param id_code: str
    :return: str
    """
    if not is_id_valid(id_code):
        return "Given invalid ID code!"
    gender = get_gender(int(id_code[0]))
    birth_year = get_full_year(int(id_code[0]), int(id_code[1:3]))
    birth_month = id_code[3:5]
    birth_day = id_code[5:7]
    birth_location = get_birth_place(int(id_code[7:10]))
    return "This is a " + gender + " born on " + birth_day + "." + birth_month + "." + str(birth_year) + " in " + \
           birth_location + "."


def is_id_valid(id_code: str) -> bool:
    """
    Check if given ID code is valid and return the result (True or False).

    Complete other functions before starting to code this one.
    You should use the functions you wrote before in this function.
    :param id_code: str
    :return: boolean
    """
    if len(id_code) != 11 or not id_code.isdigit():
        return False
    elif not is_valid_gender_number(int(id_code[0])):
        return False
    elif not is_valid_birth_number(int(id_code[7:10])):
        return False
    elif not is_valid_control_number(id_code):
        return False
    elif not is_valid_day_number(int(id_code[0]), int(id_code[1:3]), int(id_code[3:5]), int(id_code[5:7])):
        return False
    elif not is_valid_month_number(int(id_code[3:5])):
        return False
    elif not is_valid_year_number(int(id_code[1:3])):
        return False
    else:
        return True


if __name__ == '__main__':
    print("\nGender number:")
    for i in range(9):
        print(f"{i} {is_valid_gender_number(i)}")
        # 0 -> False
        # 1...6 -> True
        # 7...8 -> False
    print("\nYear number:")
    print(is_valid_year_number(-5))  # -> False
    print(is_valid_year_number(50))  # -> true
    print("\nMonth number:")
    print(is_valid_month_number(2))  # -> True
    print(is_valid_month_number(15))  # -> False
    print("\nDay number:")
    print(is_valid_day_number(4, 5, 12, 25))  # -> True
    print(is_valid_day_number(3, 10, 8, 32))  # -> False
    print(is_leap_year(1804))  # -> True
    print(is_leap_year(1800))  # -> False
    print("\nFebruary check:")
    print(
        is_valid_day_number(4, 96, 2, 30))  # -> False (February cannot contain more than 29 days in any circumstances)
    print(is_valid_day_number(4, 99, 2, 29))  # -> False (February contains 29 days only during leap year)
    print(is_valid_day_number(4, 8, 2, 29))  # -> True
    print("\nMonth contains 30 or 31 days check:")
    print(is_valid_day_number(4, 22, 4, 31))  # -> False (April contains max 30 days)
    print(is_valid_day_number(4, 18, 10, 31))  # -> True
    print(is_valid_day_number(4, 15, 9, 31))  # -> False (September contains max 30 days)
    print("\nBorn order number:")
    print(is_valid_birth_number(0))  # -> False
    print(is_valid_birth_number(1))  # -> True
    print(is_valid_birth_number(850))  # -> True
    print("\nControl number:")
    print(is_valid_control_number("49808270244"))  # -> True
    print(is_valid_control_number("60109200187"))  # -> False, it must be 6

    print("\nFull message:")
    print(get_data_from_id("49808270244"))  # -> "This is a female born on 27.08.1998 in Tallinn."
    print(get_data_from_id("60109200187"))  # -> "Given invalid ID code!"
    print(get_full_year(1, 28))  # -> 1828
    print(get_full_year(4, 85))  # -> 1985
    print(get_full_year(5, 1))  # -> 2001
    print(get_gender(2))  # -> "female"
    print(get_gender(5))  # -> "male"

    # Comment these back in if you have completed other functions.
    print("\nChecking where the person was born")

    print(get_birth_place(0))  # -> "Wrong input!"
    print(get_birth_place(1))  # -> "Kuressaare"
    print(get_birth_place(273))  # -> "Tartu"
    print(get_birth_place(888))  # -> "Tallinn"

    print("\nOverall ID check::")
    print(is_id_valid("49808270244"))  # -> True
    print(is_id_valid("12345678901"))  # -> False
    print("\nTest now your own ID code:")
    personal_id = input()  # type your own id in command prompt
    print(get_data_from_id(personal_id))  # -> True
