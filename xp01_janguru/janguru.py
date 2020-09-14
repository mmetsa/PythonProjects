"""Jänguru ülesanne."""


def meet_me(pos1, jump_distance1, sleep1, pos2, jump_distance2, sleep2):
    """
    Check if the two rabbits ever meet.

    :param pos1: the position of the first rabbit
    :param pos2: the position of the second rabbit
    :param jump_distance1: the distance that the first rabbit jumps
    :param jump_distance2: the distance that the second rabbit jumps
    :param sleep1: the time that the first rabbit needs to rest
    :param sleep2: the time that the second rabbit needs to rest
    :return int: how far from the starting position the rabbits meet
    """
    sleep_timer_1 = 0
    sleep_timer_2 = 0
    rabbit1_jumps_done = 0
    rabbit2_jumps_done = 0
    default_pos_1 = pos1
    default_pos_2 = pos2
    pos1 += jump_distance1
    pos2 += jump_distance2
    rabbit1_jumps_done += 1
    rabbit2_jumps_done += 1
    while pos1 != pos2:
        if sleep_timer_1 + 1 != sleep1 and sleep_timer_2 + 1 != sleep2:
            amt_1 = sleep1 - sleep_timer_1 - 1
            amt_2 = sleep2 - sleep_timer_2 - 1
            if amt_1 > amt_2:
                amt_to_increase = amt_2
            else:
                amt_to_increase = amt_1

            sleep_timer_1 += amt_to_increase
            sleep_timer_2 += amt_to_increase
        elif sleep_timer_1 + 1 == sleep1 and sleep_timer_2 + 1 != sleep2:
            pos1 += jump_distance1
            rabbit1_jumps_done += 1
            sleep_timer_1 = 0
            sleep_timer_2 += 1
        elif sleep_timer_1 + 1 != sleep1 and sleep_timer_2 + 1 == sleep2:
            pos2 += jump_distance2
            rabbit2_jumps_done += 1
            sleep_timer_2 = 0
            sleep_timer_1 += 1
        else:
            pos1 += jump_distance1
            pos2 += jump_distance2
            rabbit1_jumps_done += 1
            rabbit2_jumps_done += 1
            sleep_timer_1 = 0
            sleep_timer_2 = 0
        if rabbit1_jumps_done > default_pos_1 and rabbit2_jumps_done > default_pos_2:
            return -1
    return pos1


if __name__ == "__main__":
    print(meet_me(100, 7, 4, 300, 8, 6))