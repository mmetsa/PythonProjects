"""Let's count calories."""
import math


def x_sum_loop(nums, x) -> int:
    """
    Given a list of integers and a number called x. Iteratively return sum of every x'th number in the list.

    :param nums: list of integer
    :param x: number indicating every which num to add to sum
    :return: sum of every x'th number in the list
    """
    answer = 0
    if nums == [] or x == 0:
        return 0
    elif abs(x) > len(nums):
        return 0
    else:
        if x > 0:
            for elem_i in range(x, len(nums) + 1, x):
                answer += nums[elem_i - 1]
        else:
            x = abs(x)
            nums = nums[::-1]
            for elem_i in range(x, len(nums) + 1, x):
                answer += nums[elem_i - 1]
        return answer


def x_sum_recursion(nums, x) -> int:
    """
    Given a list of integers and a number called x. Recursively return sum of every x'th number in the list.

    :param nums: list of integer
    :param x: number indicating every which num to add to sum
    :return: sum of every x'th number in the list
    """
    if nums == [] or x == 0:
        return 0
    elif abs(x) > len(nums):
        return 0
    else:
        if 0 > x:
            return x_sum_recursion(nums[::-1], -x)
        else:
            return nums[x - 1] + x_sum_recursion(nums[x:], x)


def lets_count_calories(salad: float, chocolate_pieces: int, fridge_visits: int) -> int:
    """
    Count Kadri's calories.

    :param fridge_visits:
    :param salad: salad in the fridge, given in kilograms (1.2kg == 1200g).
    :param chocolate_pieces: pieces of chocolate in the fridge.
    :return: calories eaten while visiting fridge.
    """
    if fridge_visits == 0:
        return 0
    if salad == 0 and chocolate_pieces == 0:
        return 0
    if salad != 0 and chocolate_pieces != 0:
        return 120 + 34 + lets_count_calories(round(salad - 0.1, 1), chocolate_pieces - 1, fridge_visits - 1)
    elif salad != 0 and chocolate_pieces == 0:
        return 120 + lets_count_calories(round(salad - 0.1, 1), chocolate_pieces, fridge_visits - 1)
    elif salad == 0 and chocolate_pieces >= 2:
        return 68 + lets_count_calories(0, chocolate_pieces - 2, fridge_visits - 1)
    elif salad == 0 and chocolate_pieces == 1:
        return 34


def cycle(cyclists: list, distance: float, time: int = 0, index: int = 0) -> str:
    """
    Given cyclists and distance in kilometers, find out who crosses the finish line first.

    :param cyclists: list on tuples, containing cyclist's name, distance it cycles first and time in minutes how long
    :param distance: distance to be cycled overall
    :param time: time in minutes indicating how long it has taken cyclists so far
    :param index: index to know which cyclist's turn it is to be first
    :return: string indicating the last cyclist to carry the others
    """
    if not cyclists or distance <= 0:
        return "Everyone fails."
    else:
        cycle(cyclists, round(distance - cyclists[index][1], 1), time + cyclists[index][2],
              get_next_index(cyclists, index))
        return cyclists[index][0] + " is the last leader. Total time:" + str(math.floor(time / 60)) + "h " + \
            str(time - math.floor(time / 60)) + "min."


def get_next_index(cyclists: list, index: int) -> int:
    """Get the next index.

    :return int
    """
    if index + 1 >= len(cyclists):
        return 0
    else:
        return index + 1


def count_strings(data: list, pos=None, result: dict = None) -> dict:
    """
    You are given a list of strings and lists, which may also contain strings and lists etc.

    print(count_strings([[], ["J", "*", "W", "f"], ["j", "g", "*"], ["j", "8", "5", "6", "*"], ["*", "*", "A", "8"]]))
    # {'J': 1, '*': 5, 'W': 1, 'f': 1, 'j': 2, 'g': 1, '8': 2, '5': 1, '6': 1, 'A': 1}
    print(count_strings([[], [], [], [], ["h", "h", "m"], [], ["m", "m", "M", "m"]]))  # {'h': 2, 'm': 4, 'M': 1}
    print(count_strings([]))  # {}
    print(count_strings([['a'], 'b', ['a', ['b']]]))  # {'a': 2, 'b': 2}

    :param data: given list of lists
    :param pos: figure out how to use it
    :param result: figure out how to use it
    :return: dict of given symbols and their count
    """
    pass


if __name__ == '__main__':
    print(cycle([("First", 0.1, 9), ("Second", 0.1, 8)], 0.3))  # "First is the last leader. Total time: 0h 26min."
    # print(cycle([], 0))  # "Everyone fails."
    print(cycle([("Fernando", 19.8, 42), ("Patricio", 12, 28), ("Daniel", 7.8, 11), ("Robert", 15.4, 49)],
                50))  # "Robert is the last leader. Total time: 2h 10min."
    print(cycle([("Loner", 0.1, 1)], 60))  # "Loner is the last leader. Total time: 10h 0min."
