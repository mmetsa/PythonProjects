"""Filtering."""


def remove_vowels(string: str) -> str:
    """
    Remove vowels (a, e, i, o, u).

    :param string: Input string
    :return string without vowels.
    """
    vowels = ['a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U']
    for a in string:
        if a in vowels:
            string = string.replace(a, '')
    return string


def longest_filtered_word(string_list: list) -> str:
    """
    Filter, find and return the longest string.

    Return None if list is empty.

    :param string_list: List of strings.
    :return: Longest string without vowels.
    """
    if len(string_list) == 0:
        return None
    longest_word = ""
    for a in string_list:
        a = remove_vowels(a)
        if len(longest_word) < len(a):
            longest_word = a
    return longest_word


def sort_list(string_list: list) -> list:
    """
    Filter vowels in strings and sort the list by the length.

    Longer strings come first.

    :param string_list: List of strings that need to be sorted.
    :return: Filtered list of strings sorted by the number of symbols in descending order.
    """
    if len(string_list) == 0:
        return []
    string_list_copy = []
    new_list = []
    for a in string_list:
        string_list_copy.append(remove_vowels(a))
    while len(string_list_copy) != 0:
        a = longest_filtered_word(string_list_copy)
        new_list.append(a)
        string_list_copy.remove(a)
    return new_list


if __name__ == '__main__':
    print(remove_vowels(""))  # => ""
    print(remove_vowels("hello"))  # => "hll"
    print(remove_vowels("Home"))  # => "Hm"
    print(longest_filtered_word(["Bunny", "Tiger", "Bear", "Snake"]))  # => "Bnny"
    print(sort_list(["Bunny", "Tiger", "Bear", "Snake"]))  # => ['Bnny', 'Tgr', 'Snk', 'Br']
