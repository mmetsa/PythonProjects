"""Encode and decode text using Rail-fence Cipher."""


def sik_sak(message, key):
    """
    Zig Zag through all the letters.

    :param message:
    :param key:
    :return:
    """
    down_move = True
    row = 0
    result = ""
    for i in range(len(message[0])):
        result += message[row][i]
        if row == 0:
            row += 1
            down_move = True
        elif row == key - 1:
            row -= 1
            down_move = False
        elif down_move:
            row += 1
        elif not down_move:
            row -= 1
    return result


def create_table(message: str, key: int, decoder: bool) -> []:
    """
    Create a table of dots and *'s.

    :param decoder:
    :param key:
    :param message:
    :return:
    """
    table = []  # The table where all the info goes
    for a in range(key):  # Create rows of dots
        row = []
        for a in range(len(message)):
            row.append(".")
        table.append(row)  # add the dots to the table
    row = 0
    increase = True
    for i in range(len(message)):  # i is the nth dot in the row
        if not decoder:
            table[row][i] = message[i]  # replace the dot with the letter from the message
        else:
            table[row][i] = '*'  # replace the dot with a '*'
        if increase:  # from 0 to key-1 rows, then back to 0
            if row == key - 1:
                increase = False
                row -= 1
            else:
                row += 1
        else:
            if row == 0:
                increase = True
                row += 1
            else:
                row -= 1
    return table


def encode(message: str, key: int) -> str:
    """
    Encode text using Rail-fence Cipher.

    Replace all spaces with '_'.

    :param message: Text to be encoded.
    :param key: Encryption key.
    :return: Decoded string.
    """
    message = message.replace(" ", "_")
    if key == 1:
        return message
    table = create_table(message, key, False)
    list_message = ""
    for row in table:
        for a in row:
            list_message += a
    list_message = list_message.replace(".", "")
    return list_message


def decode(message: str, key: int) -> str:
    """
    Decode text knowing it was encoded using Rail-fence Cipher.

    '_' have to be replaced with spaces.

    :param message: Text to be decoded.
    :param key: Decryption key.
    :return: Decoded string.
    """
    message_index = 0
    row_index = 0
    result = []
    message = message.replace("_", " ")
    if key == 1:
        return message
    table = create_table(message, key, True)
    for row in table:
        for a in row:
            if a == '*':
                row[row_index] = message[message_index]
                message_index += 1
            row_index += 1
        row_index = 0
    for row in table:
        result.append(row)
    result = sik_sak(result, key)
    return result


if __name__ == '__main__':
    print(encode("Mind on vaja krüpteerida", 3))  # => M_v_prido_aaküteiannjred
    print(encode("Mind on", 3))  # => M_idonn
    print(encode("hello", 1))  # => hello
    print(encode("hello", 8))  # => hello
    print(encode("kaks pead", 1))  # => kaks_pead

    print(decode("kaks_pead", 1))  # => kaks pead
    print(decode("M_idonn", 3))  # => Mind on
    print(decode("M_v_prido_aaküteiannjred", 3))  # => Mind on vaja krüpteerida
