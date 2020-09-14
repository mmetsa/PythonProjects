"""Create schedule from the given file."""
import re


def create_schedule_file(input_filename: str, output_filename: str) -> None:
    """Create schedule file from the given input file."""
    with open(input_filename, "r") as file:
        schedule_string = file.read()
    with open(output_filename, "w") as file:
        schedule_list = create_schedule_list(schedule_string)
        for line in schedule_list:
            file.write(line + "\n")


def create_schedule_string(input_string: str):
    """
    Create schedule string from the given input string.

    :param input_string: text string input
    :return: schedule string
    """
    schedule_dict = {}
    for match in re.finditer(r"([ \n])([0-9]{1,2})[^0-9]([0-9]{1,2})([ \n])+([a-zA-Z]+)", input_string):
        time_key = normalize(match.group(2), match.group(3), True)
        time_value = match.group(5).lower()
        if int(match.group(2)) > 23 or int(match.group(3)) > 59:  # Incorrect time, so take the next time
            continue
        if len(time_value) > 0:
            if time_key in schedule_dict:
                if " " + time_value not in schedule_dict[time_key]:
                    schedule_dict[time_key] += ", " + time_value
                    print(schedule_dict[time_key])
            else:
                schedule_dict[time_key] = " " + time_value
    schedule_dict = sorted(schedule_dict.items())
    return_string = ""
    for elem in create_table(schedule_dict):
        return_string += elem + "\n"
    return return_string


def create_schedule_list(input_string: str):
    """
    Create schedule string from the given input string.

    :param input_string: text string input
    :return: schedule string
    """
    schedule_dict = {}
    values_list = []
    for match in re.finditer(r"([ \n])([0-9]{1,2})[^0-9]([0-9]{1,2})([ \n])+([a-zA-Z]+)", input_string):
        time_key = normalize(match.group(2), match.group(3), True)
        time_value = match.group(5).lower()
        if int(match.group(2)) > 23 or int(match.group(3)) > 59:  # Incorrect time, so take the next time
            continue
        if len(time_value) > 0:
            if time_key in schedule_dict:
                if time_value not in values_list:
                    values_list.append(time_value)
                    schedule_dict[time_key] += ", " + time_value
                    print(schedule_dict[time_key])
            else:
                values_list.append(time_value)
                schedule_dict[time_key] = " " + time_value
    schedule_dict = sorted(schedule_dict.items())
    return create_table(schedule_dict)


def create_table(schedule_dict: list):
    """Create table."""
    table = []
    longest_activity = 0
    longest_time = 0
    for time, activity in schedule_dict:
        if int(len(activity)) > longest_activity:
            longest_activity = int(len(activity))
        if int(len(convert_time(time))) > longest_time:
            longest_time = int(len(convert_time(time)))
            print(longest_time)
    if longest_activity < 6:
        longest_activity = 6
    table.append("-" * (longest_time + longest_activity + 6))
    table.append("|" + " " * (longest_time - 3) + "time | items" + " " * (longest_activity - 5) + "|")
    table.append("-" * (longest_time + longest_activity + 6))
    if len(schedule_dict) == 0:
        return print_empty_table()
    for time, activity in schedule_dict:
        current_activity_len = int(len(activity))
        current_time_len = int(len(convert_time(time))) - 3  # -3 for " AM"
        table.append("|" + " " * (longest_time - current_time_len - 2) + convert_time(time) + " |" + activity
                     + " " * (longest_activity - current_activity_len) + " |")
    table.append("-" * (longest_time + longest_activity + 6))
    return table


def print_empty_table():
    """Print an empty table."""
    table = []
    times = 18
    table.append("-" * times)
    table.append("|  time | items  |")
    table.append("-" * times)
    table.append("| No items found |")
    table.append("-" * times)
    return table


def convert_time(time: str) -> str:
    """Convert 24hr time to 12hr time."""
    time = time.split(":")
    good_time = normalize(time[0], time[1], False)
    good_time = good_time.split(":")
    hours = good_time[0]
    minutes = good_time[1]
    time_text = "AM"
    if int(hours) == 0:
        hours = 12
    elif int(hours) == 12:
        time_text = "PM"
    if int(hours) > 12:
        time_text = "PM"
        hours = int(hours) - 12
    return str(hours) + ":" + minutes + " " + time_text


def normalize(hours: str, minutes: str, add_zero: bool) -> str:
    """Add missing 0's to the minutes and remove extra 0's from hours."""
    if add_zero and len(hours) == 1:
        hours = "0" + hours
    elif not add_zero and hours[0] == "0":
        hours = hours[1]
    if minutes == "0":
        minutes = "00"
    elif int(minutes) < 10 and minutes[0] != "0":
        minutes = "0" + minutes
    return hours + ":" + minutes


if __name__ == '__main__':
    print(create_schedule_string(""))
    create_schedule_file("schedule_input.txt", "schedule_output.txt")
