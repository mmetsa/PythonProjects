"""Exam stuff."""
import copy


def swap_items(dic: dict) -> dict:
    """
    Given a dictionary return a new dictionary where keys and values are swapped.

    If duplicate keys in the new dictionary exist, leave the first one.
    {"a": 1, "b": 2, "c": 3} => {1: "a", 2: "b", 3: "c"}
    {"Morning": "Good", "Evening": "Good"} => {"Good": "Morning"}

    :param dic: original dictionary
    :return: dictionary where keys and values are swapped
    """
    new_dict = {}
    for key in dic:
        val = dic[key]
        if val not in new_dict:
            new_dict[val] = key
    return new_dict


def find_divisors(number) -> list:
    """
    The task is to find all the divisors for given number in range to the given number's value.

    Divisor - a number that divides evenly into another number.
    Return list of given number divisors in ascending order.
    NB! Numbers 1 and number itself must be excluded if there are more divisors
    than 1 and number itself!
    (138) > [2, 3, 6, 23, 46, 69]
    (3) > [1, 3]
    :param number: int
    :return: list of number divisors
    """
    list_of_divisors = []
    for numb in range(1, number + 1):
        if number % numb == 0:
            list_of_divisors.append(numb)
    if len(list_of_divisors) != 2 and len(list_of_divisors) != 1:
        list_of_divisors.remove(1)
        list_of_divisors.remove(list_of_divisors[len(list_of_divisors) - 1])
    return list_of_divisors


def sum_of_multiplies(first_num, second_num, limit) -> int:
    """
    The task is to find all the multiplies of each given of two numbers within the limit.

    Then, find the sum of those multiplies.
    (3, 5, 20) => 98 (3 + 6 + 9 + 12 + 15 + 18 + 5 + 10 + 20) 15 is included only once
    (3, 3, 10) => 18 (3 + 6 + 9)
    (3, 10, 2) => 0
    :param first_num: first number
    :param second_num: second number
    :param limit: limit
    :return: sum of multiplies
    """
    list_of_nums = []
    total = 0
    for numb in range(first_num, limit + 1, first_num):
        list_of_nums.append(numb)
    for numb in range(second_num, limit + 1, second_num):
        if numb not in list_of_nums:
            list_of_nums.append(numb)
    for elem in list_of_nums:
        total += elem
    return total


def count_odds_and_evens(numbers: list) -> str:
    r"""
    The task is to count how many odd and even numbers does the given list contain.

    Do not count zeros (0).
    Result should be displayed as string "ODDS: {number of odds}\nEVENS: {number of evens}"

    count_odds_and_events([1, 2, 3]) => "ODDS: 2\nEVENS: 1"
    count_odds_and_events([1, 0]) => "ODDS: 1\nEVENS: 0"

    :param numbers: list
    :return: str
    """
    odds = 0
    evens = 0
    for elem in numbers:
        if elem == 0:
            continue
        if elem % 2 == 0:
            evens += 1
        else:
            odds += 1
    return f"ODDS: {odds}\nEVENS: {evens}"


def sum_between_25(numbers: list) -> int:
    """
    Return the sum of the numbers in the array which are between 2 and 5.

    Summing starts from 2 (not included) and ends at 5 (not included).
    The section can contain 2 (but cannot 5 as this would end it).
    There can be several sections to be summed.

    sum_between_25([1, 3, 6, 7]) => 0
    sum_between_25([1, 2, 3, 4, 5, 6]) => 7
    sum_between_25([1, 2, 3, 4, 6, 6]) => 19
    sum_between_25([1, 3, 3, 4, 5, 6]) => 0
    sum_between_25([1, 2, 3, 4, 5, 6, 1, 2, 9, 5, 6]) => 16
    sum_between_25([1, 2, 3, 2, 5, 5, 3, 5]) => 5
    """
    sum = 0
    elems = []
    nums = copy.deepcopy(numbers)
    while 2 in nums:
        if 5 in nums:
            if nums.index(5) < numbers.index(2):
                nums.remove(5)
                continue
            for elem in nums[nums.index(2) + 1: nums.index(5)]:
                elems.append(elem)
                sum += elem
            for elem in elems:
                nums.remove(elem)
            elems.clear()
            elems.append(2)
            elems.append(5)
        else:
            for elem in nums[nums.index(2) + 1: len(nums)]:
                sum += elem
                elems.append(elem)
            for elem in elems:
                if elem in nums:
                    nums.remove(elem)
            elems.clear()
            elems.append(2)
    return sum


def transcribe(dna_strand: str):
    """
    Write a function that returns a transcribed RNA strand from the given DNA strand.

    that is formed by replacing each nucleotide(character) with its complement: G => C, C => G, T => A, A => U
    Return None if it is not possible to transcribe a DNA strand.
    Empty string should return empty string.

    "ACGTGGTCTTAA" => "UGCACCAGAAUU"
    "gcu" => None

    :param dna_strand: original DNA strand
    :return: transcribed RNA strand in the uppercase or None
    """
    rna_strand = ""
    if dna_strand == "":
        return ""
    dna_strand = dna_strand.upper()
    acceptable_chars = {'G': 'C', 'C': 'G', 'T': 'A', 'A': 'U'}
    for elem in dna_strand:
        if elem in acceptable_chars.keys():
            rna_strand += acceptable_chars[elem]
        else:
            return None
    return rna_strand


def union_of_dict(d1: dict, d2: dict):
    """
    Given two dictionaries return dictionary that has all the key-value pairs that are the same in given dictionaries.

    union_of_dict({"a": 1, "b": 2, "c":3}, {"a": 1, "b": 42}) ==> {"a": 1}
    union_of_dict({}, {"bar": "foo"}) => {}
    """
    result_dict = {}
    for elem in d1:
        if elem in d2:
            if d2[elem] == d1[elem]:
                result_dict[elem] = d1[elem]
    return result_dict


def reserve_list(input_strings: list) -> list:
    """
    Given list of strings, return new reversed list where each list element is.

    reversed too. Do not reverse strings followed after element "python". If element is "java" -
    reverse mode is on again.
    P.S - "python" and "java" are not being reversed

    ['apple', 'banana', 'onion'] -> ['noino', 'ananab', 'elppa']
    ['lollipop', 'python', 'candy'] -> ['candy', 'python', 'popillol']
    ['sky', 'python', 'candy', 'java', 'fly'] -> ['ylf', 'java', 'candy', 'python', 'yks']
    ['sky', 'python', 'java', 'candy'] -> ['ydnac', 'java', 'python', 'yks']

    :param input_strings: list of strings
    :return: reversed list
    """
    new_list = []
    reverse = True
    for elem in input_strings:
        if elem == "python":
            reverse = False
        elif elem == "java":
            reverse = True
        if reverse:
            if elem == "java":
                new_list.append(elem)
            else:
                new_list.append(elem[::-1])
        else:
            new_list.append(elem)
    new_list = new_list[::-1]
    return new_list


def convert_binary_to_decimal(binary_list: list):
    """
    Extract binary codes of given length from list and convert to decimal numbers.

    [0, 0, 0, 0] => 0.
    [0, 1, 0, 0] => 4.

    :param binary_list: list of 1 and 0 (binary code)
    :return: number converted into decimal system
    """
    binary = binary_list[::-1]
    pow_of_2 = 0
    total = 0
    for elem in binary:
        total += elem * 2 ** pow_of_2
        pow_of_2 += 1
    return total


def print_pages(pages: str) -> list:
    """
    Find pages to print in console.

    examples:
    print_pages("2,4,9") -> [2, 4, 9]
    print_pages("2,4-7") -> [2, 4, 5, 6, 7]
    print_pages("2-5,7,10-12,17") -> [2, 3, 4, 5, 7, 10, 11, 12, 17]
    print_pages("1,1") -> [1]
    print_pages("") -> []
    print_pages("2,1") -> [1, 2]

    :param pages: string containing page numbers and page ranges to print.
    :return: list of pages to print with no duplicates, sorted in increasing order.
    """
    all_pages = []
    page_nrs = pages.split(",")
    if pages == "":
        return []
    for elem in page_nrs:
        if "-" in elem:
            new_elems = elem.split("-")
            first = int(new_elems[0])
            last = int(new_elems[1])
            for other_elem in range(first, last + 1):
                if int(other_elem) not in all_pages:
                    all_pages.append(other_elem)
        else:
            if int(elem) not in all_pages:
                all_pages.append(int(elem))
    all_pages = sorted(all_pages)
    return all_pages


if __name__ == '__main__':
    print(transcribe("acgt"))
    print(sum_between_25([2, 25, 5]))
    print(sum_between_25([1, 2, 3, 4, 5, 6]))
    print(sum_between_25([1, 2, 3, 4, 6, 6]))
    print(sum_between_25([1, 3, 3, 4, 5, 6]))
    print(sum_between_25([1, 2, 3, 4, 5, 6, 1, 2, 9, 5, 6]))
    print(sum_between_25([1, 2, 3, 2, 5, 5, 3, 5]))
