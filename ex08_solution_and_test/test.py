"""Test the solutions."""
import solution


def test_students_study_1():
    """Test if students study at 1 am."""
    assert solution.students_study(1, False) is False
    assert solution.students_study(1, True) is False


def test_students_study_4():
    """Test if students study at 4 am."""
    assert solution.students_study(4, False) is False
    assert solution.students_study(4, True) is False


def test_students_study_18():
    """Test if students study at 18 pm."""
    assert solution.students_study(18, True) is True
    assert solution.students_study(18, False) is True


def test_students_study_24():
    """Test if students study at 24 am."""
    assert solution.students_study(24, True) is True
    assert solution.students_study(24, False) is True


def test_students_study_5():
    """Test if students study at 5 am."""
    assert solution.students_study(5, True) is True
    assert solution.students_study(5, False) is False


def test_students_study_17():
    """Test if students study at 17 pm."""
    assert solution.students_study(17, True) is True
    assert solution.students_study(17, False) is False


def test_lottery_all_5():
    """Test if all lottery numbers are 5."""
    assert solution.lottery(5, 5, 5) == 10


def test_lottery_all_same_numbers():
    """Test if all lottery numbers are same."""
    assert solution.lottery(4, 4, 4) == 5
    assert solution.lottery(-5, -5, -5) == 5
    assert solution.lottery(0, 0, 0) == 5


def test_lottery_b_c_different_a():
    """Test if b and c are not equal to a."""
    assert solution.lottery(1, 5, 5) == 1
    assert solution.lottery(1, 5, 3) == 1


def test_lottery_a_same_b_or_c():
    """Test if a is equal to b or c."""
    assert solution.lottery(1, 5, 1) == 0
    assert solution.lottery(2, 2, 1) == 0


def test_fruit_order_order_all_0():
    """Test if there's 0 baskets and 0 need."""
    assert solution.fruit_order(0, 0, 0) == 0


def test_fruit_order_middle_0():
    """Test if there's 1 small basket, 0 big and 0 need."""
    assert solution.fruit_order(1, 0, 1) == 1


def test_fruit_order_first_0():
    """Test if there's no small baskets, 1 big and 1 need."""
    assert solution.fruit_order(0, 1, 1) == -1


def test_fruit_order_last_0():
    """Test if there's 1 small and 1 big basket, but 0 need."""
    assert solution.fruit_order(1, 1, 0) == 0


def test_fruit_order_last_1():
    """Test if there's no baskets but 1 need."""
    assert solution.fruit_order(0, 0, 1) == -1


def test_fruit_order_middle_1():
    """Test if there's 1 big basket, 0 small and 0 need."""
    assert solution.fruit_order(0, 1, 0) == 0


def test_fruit_order_first_1():
    """Test if there's 1 small basket, 0 big and 0 need."""
    assert solution.fruit_order(1, 0, 0) == 0


def test_fruit_order_all_1():
    """Test if there's 1 small and 1 big basket, and 1 need."""
    assert solution.fruit_order(1, 1, 1) == 1


def test_fruit_order_small_and_big_possible():
    """Test if big & small together work."""
    assert solution.fruit_order(10, 1, 10) == 5


def test_fruit_order_small_and_big_impossible():
    """Test if impossible returns -1."""
    assert solution.fruit_order(10, 1, 20) == -1


def test_fruit_order_large_first():
    """Test if only small baskets work."""
    assert solution.fruit_order(100, 0, 50) == 50


def test_fruit_order_large_first_complete():
    """Test if only small baskets work."""
    assert solution.fruit_order(100, 0, 100) == 100


def test_fruit_order_large_first_impossible():
    """Test if only small baskets work."""
    assert solution.fruit_order(100, 0, 101) == -1


def test_fruit_order_large_second():
    """Test if only big baskets work."""
    assert solution.fruit_order(0, 100, 495) == 0


def test_fruit_order_large_second_complete():
    """Test if only big baskets work."""
    assert solution.fruit_order(0, 200, 1000) == 0


def test_fruit_order_large_second_impossible():
    """Test if only big baskets work."""
    assert solution.fruit_order(0, 200, 1001) == -1


def test_fruit_order_large_third():
    """Test if only big baskets work."""
    assert solution.fruit_order(0, 20, 500) == -1


def test_fruit_order_large_third_possible():
    """Test if only big baskets work but large."""
    assert solution.fruit_order(0, 50, 250) == 0


def test_fruit_order_all_large_complete():
    """Test if small and big baskets work but large."""
    assert solution.fruit_order(100, 100, 600) == 100


def test_fruit_order_all_large_incomplete():
    """Test if small and big baskets work but large."""
    assert solution.fruit_order(100, 100, 550) == 50


def test_fruit_order_large_baskets_only_large():
    """Test if big baskets work but large."""
    assert solution.fruit_order(300, 200, 1000) == 0


def test_fruit_order_all_large_impossible():
    """Test if small and big baskets work but large."""
    assert solution.fruit_order(100, 100, 700) == -1


def test_fruit_order_all_large_more_baskets():
    """Test if small and big baskets work but large."""
    assert solution.fruit_order(100, 300, 250) == 0


def test_fruit_order_all_large_use_all():
    """Test if both small and big ones used."""
    assert solution.fruit_order(200, 200, 1200) == 200


def test_fruit_order_all_large_enough_bigs_not_enough_smalls():
    """Test if all there is not enough small baskets."""
    assert solution.fruit_order(2, 600, 1158) == -1
