"""Tunnikontrolli ülesanded."""


def middle_way(first_list: list, second_list: list) -> list:
    """
    Make a list of the middle numbers from input lists.

    :param first_list: first list
    :param second_list: second list
    :return: new list with 2 arguments
    """
    return_list = [first_list[1], second_list[1]]
    return return_list


def sorta_sum(first_num: int, second_num: int) -> int:
    """
    Calculate the sum of input integers.

    Unless the sum is between 10-19, in which case return 20
    :param first_num: first number
    :param second_num: second number
    :return: the sum of the integers
    """
    final_sum = first_num + second_num
    if 9 < final_sum <= 19:
        return 20
    else:
        return final_sum


def combo_string(first_str: str, second_str: str) -> str:
    """
    Make a new string where the string with a smaller length is in twice.

    :param first_str: first string
    :param second_str: second string
    :return: new string
    """
    if len(first_str) > len(second_str):
        return second_str + first_str + second_str
    else:
        return first_str + second_str + first_str


def num_as_index(nums: list) -> int:
    """
    Return element which index is the value of the smaller of the first and the last element.

    If there is no such element (index is too high), return the smaller of the first and the last element.
    num_as_index([1, 2, 3]) => 2 (1 is smaller, use it as index)
    num_as_index([4, 5, 6]) => 4 (4 is smaller, but cannot be used as index)
    num_as_index([0, 1, 0]) => 0
    num_as_index([3, 5, 6, 1, 1]) => 5
    :param nums: list of non-negative integers.
    :return: element value in the specific index.
    """
    first_elem = nums[0]
    last_elem = nums[len(nums) - 1]
    if first_elem > last_elem:
        if len(nums) - 1 >= last_elem:
            return nums[last_elem]
        else:
            return last_elem
    elif last_elem > first_elem:
        if len(nums) - 1 >= first_elem:
            return nums[first_elem]
        else:
            return first_elem
    else:
        if len(nums) - 1 >= first_elem:
            return nums[first_elem]
        else:
            return first_elem


def count_clumps(nums: list) -> int:
    """
    Return the number of clumps in the given list.

    Say that a "clump" in a list is a series of 2 or more adjacent elements of the same value.
    count_clumps([1, 2, 2, 3, 4, 4]) → 2
    count_clumps([1, 1, 2, 1, 1]) → 2
    count_clumps([1, 1, 1, 1, 1]) → 1

    :param nums: List of integers.
    :return: Number of clumps.
    """
    last_number = ""
    groups_count = 0
    current_num_amt = 1
    for a in nums:
        if last_number == a:
            current_num_amt += 1
        else:
            last_number = a
            if current_num_amt > 1:
                groups_count += 1
                current_num_amt = 1
    if current_num_amt > 1:
        groups_count += 1
    return groups_count


if __name__ == '__main__':
    print(middle_way([1, 2, 3], [4, 5, 6]))
    print(sorta_sum(3, 4))
    print(combo_string('Hello', 'hi'))
    print(num_as_index([4, 2, 4]))
    print(count_clumps([1, 1]))
