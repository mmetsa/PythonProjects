"""Minesweeper has to swipe the mines."""
import copy


def create_minefield(height: int, width: int) -> list:
    """
    Create and return minefield.

    Minefield must be height high and width wide. Each position must contain single dot (`.`).
    :param height: int
    :param width: int
    :return: list
    """
    minefield = [["." for _ in range(width)] for _ in range(height)]
    return minefield


def add_mines(minefield: list, mines: list) -> list:
    """
    Add mines to a minefield and return minefield.

    This function cannot modify the original minefield list.
    Minefield must be length long and width wide. Each non-mine position must contain single dot.
    If a position is empty ("."), then a small mine is added ("x").
    If a position contains small mine ("x"), a large mine is added ("X").
    Mines are in a list.
    Mine is a list. Each mine has 4 integer parameters in the format [N, S, E, W].
        - N is the distance between area of mines and top of the minefield.
        - S ... area of mines and bottom of the minefield.
        - E ... area of mines and right of the minefield.
        - W ... area of mines and left of the minefield.
    :param minefield: list
    :param mines: list
    :return: list
    """
    new_minefield = copy.deepcopy(minefield)
    for mine in mines:
        for row_i in range(mine[0], len(new_minefield) - mine[1]):
            for col_i in range(mine[3], len(new_minefield[row_i]) - mine[2]):
                if new_minefield[row_i][col_i] == ".":
                    new_minefield[row_i][col_i] = "x"
                else:
                    new_minefield[row_i][col_i] = "X"
    return new_minefield


def get_minefield_string(minefield: list) -> str:
    """
    Return minefield's string representation.

    .....
    .....
    x....
    Xx...

    :param minefield:
    :return:
    """
    minefield_str = ""
    for row in minefield:
        for col in row:
            minefield_str += col
        minefield_str += "\n"
    return minefield_str


def calculate_mine_count(minefield: list) -> list:
    """
    For each cell in minefield, calculate how many mines are nearby.

    This function cannot modify the original list.
    So, the result should be a new list (or copy of original).

    ....
    ..x.
    X.X.
    x..X

    =>

    0111
    13x2
    X4X3
    x32X

    :param minefield:
    :return:
    """
    new_minefield = copy.deepcopy(minefield)
    for row_i in range(len(new_minefield)):
        for elem_i in range(len(new_minefield[row_i])):
            if new_minefield[row_i][elem_i] == ".":
                new_minefield[row_i][elem_i] = str(calculate_bomb_count(new_minefield, row_i, elem_i))
    return new_minefield


def calculate_bomb_count(minefield: list, row: int, col: int) -> int:
    """Calculate the nearby bomb count for each cell.

    :return: int
    """
    bomb_count = 0
    elems = ["x", "X"]
    for row_i in range(row - 1, row + 2):
        if row_i == -1 or row_i == len(minefield):
            continue
        for col_i in range(col - 1, col + 2):
            if col_i == -1 or col_i == len(minefield[row_i]):
                continue
            if minefield[row_i][col_i] in elems:
                bomb_count += 1
    return bomb_count


def walk(minefield, moves, lives) -> list:
    """
    Make moves on the minefield.

    This function cannot modify the original minefield list.
    Starting position is marked by #.
    There is always exactly one # on the field.
    The position you start is an empty cell (".").

    Moves is a list of move "orders":
    N - up,
    S - down,
    E - right,
    W - left.

    Example: "NWWES"

    If the position you have to move contains "x" (small mine),
    then the mine is cleared (position becomes "."),
    but you cannot move there.
    In case of clearing a small mine, ff the position where the minesweeper is, has 5 or more mines nearby
    (see the previous function), minesweeper also loses a life.
    If it has 0 lives left, then clearing is not done and moving stops.

    Example:
    #x
    ..
    moves: ESS

    =>

    1st step ("E"):
    #.
    ..

    2nd step ("S"):
    ..
    #.

    3rd step ("S"):
    ..
    #.

    Example #2
    XXX
    x.x
    .#X
    moves: NWES, lives = 1

    1) "N"
    XXX
    x#x
    ..X

    2) "W". the small mine is cleared, but with the cost of one life :'(
    XXX
    .#x
    ..X
    lives = 0

    3) "E"
    XXX
    .#x
    ..X
    As clearing the mine on the right, he would lose a life (because minesweeper has 5 or more mines nearby).
    But as he has no lives left, he stops there. No more moves will be carried out.

    If the position you have to move contains "X" (huge mine),
    then you move there and lose a life.

    #X
    ..
    moves: ESS

    1) (lives = lives - 1)
    .#
    ..
    2)
    ..
    .#
    3)
    ..
    .#

    If you have to move into a position with a huge mine "X"
    but you don't have any more lives, then you finish your moves.

    lives: 2

    #XXXX
    .....
    moves: EEES

    1) lives = 1
    .#XXX
    .....
    2) lives = 0
    ..#XX
    .....
    3) stop, because you would die
    final result:
    ..#XX
    .....

    :param minefield:
    :param moves:
    :param lives:
    :return:
    """
    moves_dict = {
        "N": (-1, 0),
        "E": (0, 1),
        "S": (1, 0),
        "W": (0, -1)
    }
    new_minefield = copy.deepcopy(minefield)
    minesweeper_pos_row = find_minesweeper(minefield)[0]
    minesweeper_pos_col = find_minesweeper(minefield)[1]
    new_minefield[minesweeper_pos_row][minesweeper_pos_col] = "."
    for move in moves:
        new_pos_row = minesweeper_pos_row + moves_dict[move][0]
        new_pos_col = minesweeper_pos_col + moves_dict[move][1]
        if new_pos_row < 0 or new_pos_row == len(new_minefield)\
                or new_pos_col < 0 or new_pos_col == len(new_minefield[minesweeper_pos_row]):
            continue
        if new_minefield[new_pos_row][new_pos_col] == "x":
            if calculate_bomb_count(new_minefield, minesweeper_pos_row, minesweeper_pos_col) >= 5:
                if lives == 0:
                    break
                else:
                    lives -= 1
            new_minefield[new_pos_row][new_pos_col] = "."
        elif new_minefield[new_pos_row][new_pos_col] == "X":
            if lives == 0:
                break
            else:
                new_minefield[new_pos_row][new_pos_col] = "."
                lives -= 1
                minesweeper_pos_row = new_pos_row
                minesweeper_pos_col = new_pos_col
        else:
            minesweeper_pos_row = new_pos_row
            minesweeper_pos_col = new_pos_col
    new_minefield[minesweeper_pos_row][minesweeper_pos_col] = "#"
    return new_minefield


def find_minesweeper(minefield: list) -> tuple:
    """Find the position of the minesweeper(#).

    :return tuple
    """
    for row_i in range(len(minefield)):
        for col_i in range(len(minefield[row_i])):
            if minefield[row_i][col_i] == "#":
                return row_i, col_i


if __name__ == '__main__':
    minefield_a = create_minefield(4, 3)
    print(minefield_a)  # ->
    """
    [
        ['.', '.', '.'],
        ['.', '.', '.'],
        ['.', '.', '.'],
        ['.', '.', '.']
    ]
    """

    minefield_a = add_mines(minefield_a, [[0, 3, 2, 0], [2, 1, 0, 1]])
    print(minefield_a)  # ->
    """
    [
        ['x', '.', '.'],
        ['.', '.', '.'],
        ['.', 'x', 'x'],
        ['.', '.', '.']
    ]
    """

    minefield_ac = calculate_mine_count(minefield_a)
    print(minefield_ac)
