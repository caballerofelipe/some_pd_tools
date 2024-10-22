from some_pd_tools import pd_format


def test_obj_is_dict() -> None:
    # Including non int
    assert (
        [
            (1, 123),
            (12, 345),
            (2, 234),
            (23, 456),
            (234, 567),
            (3, 345),
            ('a', 'abc'),
            ('b', 'bcd'),
            ('c', 'cde'),
        ]
    ) == pd_format.obj_as_sorted_list(
        {'c': 'cde', 'a': 'abc', 3: 345, 1: 123, 2: 234, 'b': 'bcd', 12: 345, 23: 456, 234: 567}
    )
    # Only int
    assert (
        [
            (1, 123),
            (2, 234),
            (3, 345),
            (12, 345),
            (23, 456),
            (234, 567),
        ]
    ) == pd_format.obj_as_sorted_list({3: 345, 1: 123, 2: 234, 12: 345, 23: 456, 234: 567})
    # Only int, force str classification
    assert (
        [
            (1, 123),
            (12, 345),
            (2, 234),
            (23, 456),
            (234, 567),
            (3, 345),
        ]
    ) == pd_format.obj_as_sorted_list(
        {3: 345, 1: 123, 2: 234, 12: 345, 23: 456, 234: 567}, force_str=True
    )


def test_obj_is_set() -> None:
    # Including non int
    assert [1, 12, 2, 23, 234, 3, 'a', 'b', 'c'] == pd_format.obj_as_sorted_list(
        set(['c', 'a', 3, 1, 2, 'b', 1, 2, 2, 12, 23, 234])
    )
    # Only int
    assert [1, 2, 3, 12, 23, 234] == pd_format.obj_as_sorted_list(
        set([3, 1, 2, 1, 2, 2, 12, 23, 234])
    )
    # Only int, force str classification
    assert [1, 12, 2, 23, 234, 3] == pd_format.obj_as_sorted_list(
        set([3, 1, 2, 1, 2, 2, 12, 23, 234]), force_str=True
    )


def test_obj_is_list() -> None:
    # Including non int
    assert [1, 1, 12, 2, 2, 2, 23, 234, 3, 'a', 'b', 'c'] == pd_format.obj_as_sorted_list(
        ['c', 'a', 3, 1, 2, 'b', 1, 2, 2, 12, 23, 234]
    )
    # Only int
    assert [1, 1, 2, 2, 2, 3, 12, 23, 234] == pd_format.obj_as_sorted_list(
        [3, 1, 2, 1, 2, 2, 12, 23, 234]
    )
    # Only int, force str classification
    assert [1, 1, 12, 2, 2, 2, 23, 234, 3] == pd_format.obj_as_sorted_list(
        [3, 1, 2, 1, 2, 2, 12, 23, 234], force_str=True
    )


def test_obj_is_tuple() -> None:
    # Including non int
    assert [1, 1, 12, 2, 2, 2, 23, 234, 3, 'a', 'b', 'c'] == pd_format.obj_as_sorted_list(
        ('c', 'a', 3, 1, 2, 'b', 1, 2, 2, 12, 23, 234)
    )
    # Only int
    assert [1, 1, 2, 2, 2, 3, 12, 23, 234] == pd_format.obj_as_sorted_list(
        (3, 1, 2, 1, 2, 2, 12, 23, 234)
    )
    # Only int, force str classification
    assert [1, 1, 12, 2, 2, 2, 23, 234, 3] == pd_format.obj_as_sorted_list(
        (3, 1, 2, 1, 2, 2, 12, 23, 234), force_str=True
    )
