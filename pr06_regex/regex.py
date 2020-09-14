"""Regex program."""
import re


def read_file(path: str) -> list:
    """
    Read file and return list of lines read.

    :param path: str
    :return: list
    """
    list_of_lines = []
    with open(path, 'r') as f:
        for line in f:
            list_of_lines.append(line.strip())
    return list_of_lines


def match_specific_string(input_data: list, keyword: str) -> int:
    """
    Check if given list of strings contains keyword.

    Return all keyword occurrences (case insensitive). If an element cointains the keyword several times, count all the
    occurrences.

    ["Python", "python", "PYTHON", "java"], "python" -> 3

    :param input_data: list
    :param keyword: str
    :return: int
    """
    number_of_words = 0
    for element in input_data:
        number_of_words += len(re.findall(keyword, element, re.IGNORECASE))
    return number_of_words


def detect_email_addresses(input_data: list) -> list:
    """
    Check if given list of strings contains valid email addresses.

    Return all unique valid email addresses in alphabetical order presented in the list.
    ["Test", "Add me test@test.ee", "ago.luberg@taltech.ee", "What?", "aaaaaa@.com", ";_:Ö<//test@test.au??>>>;;d,"] ->
    ["ago.luberg@taltech.ee", "test@test.au", "test@test.ee"]

    :param input_data: list
    :return: list
    """
    regex = r"[.0-9a-zA-Z+_-]+@[a-zA-Z]+[.a-zA-Z]+"
    email_list = []
    for line in input_data:
        email_list += re.findall(regex, line)
    email_list = list(set(email_list))
    email_list.sort()
    return email_list


if __name__ == '__main__':

    list_of_lines_emails = read_file("input_detect_email_addresses_example_1.txt")  # reading from file
    print(detect_email_addresses(list_of_lines_emails))

    list_of_lines_keywords = read_file("input_match_specific_string_example_1.txt")
    print(match_specific_string(list_of_lines_keywords, "job"))  # 9
