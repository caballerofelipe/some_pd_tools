import re

import pandas as pd
import pytest

from some_pd_tools import pd_format

from ..basedf import BaseDF


def test_wrong_types():
    bdf = BaseDF()

    # df not pd.DataFrame
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('`df` must be of type pd.DataFrame.'),
    ):
        pd_format.approximate(1)

    # Wrong types for `round_to` parameter
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape(
            "round_to must be one of None, a positive integer or a string ('floor', 'ceil', 'trunc')."
        ),
    ):
        pd_format.approximate(bdf.df1, round_to=True)
    with pytest.raises(
        ValueError,
        match=re.escape(
            "round_to must be one of None, a positive integer or a string ('floor', 'ceil', 'trunc')."
        ),
    ):
        pd_format.approximate(bdf.df1, round_to=-1)
    with pytest.raises(
        ValueError,
        match=re.escape(
            "round_to must be one of None, a positive integer or a string ('floor', 'ceil', 'trunc')."
        ),
    ):
        pd_format.approximate(bdf.df1, round_to='a string')
    with pytest.raises(
        ValueError,
        match=re.escape(
            "round_to must be one of None, a positive integer or a string ('floor', 'ceil', 'trunc')."
        ),
    ):
        pd_format.approximate(bdf.df1, round_to=bdf)


def test_round_to_decimals():
    bdf = BaseDF()

    # 0 decimals
    # ************************************
    expected_df = pd.DataFrame(
        {
            'col_int': [1000, -2000, 3000, -4000000],
            'col_float': [-3333.0, 4444.0, -5556.0, 6667.0],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': [float('nan'), float('nan'), float('nan'), 8889.0],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.approximate(bdf.df1, round_to=0)
    assert str(expected_df[['col_int']]) == str(transformed[['col_int']])
    assert str(expected_df[['col_float']]) == str(transformed[['col_float']])
    assert str(expected_df[['col_str']]) == str(transformed[['col_str']])
    assert str(expected_df[['col_nan']]) == str(transformed[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(transformed[['col_strnan']])
    assert expected_df.equals(transformed)

    # 3 decimals
    # ************************************
    expected_df = pd.DataFrame(
        {
            'col_int': [1000, -2000, 3000, -4000000],
            'col_float': [-3333.333, 4444.444, -5555.556, 6666.667],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': [float('nan'), float('nan'), float('nan'), 8888.889],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.approximate(bdf.df1, round_to=3)
    assert str(expected_df[['col_int']]) == str(transformed[['col_int']])
    assert str(expected_df[['col_float']]) == str(transformed[['col_float']])
    assert str(expected_df[['col_str']]) == str(transformed[['col_str']])
    assert str(expected_df[['col_nan']]) == str(transformed[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(transformed[['col_strnan']])
    assert expected_df.equals(transformed)


def test_round_floor():
    bdf = BaseDF()

    expected_df = pd.DataFrame(
        {
            'col_int': [1000, -2000, 3000, -4000000],
            'col_float': [-3334.0, 4444.0, -5556.0, 6666.0],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': [float('nan'), float('nan'), float('nan'), 8888.0],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.approximate(bdf.df1, round_to='floor')
    assert str(expected_df[['col_int']]) == str(transformed[['col_int']])
    assert str(expected_df[['col_float']]) == str(transformed[['col_float']])
    assert str(expected_df[['col_str']]) == str(transformed[['col_str']])
    assert str(expected_df[['col_nan']]) == str(transformed[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(transformed[['col_strnan']])
    assert expected_df.equals(transformed)


def test_round_ceil():
    bdf = BaseDF()
    expected_df = pd.DataFrame(
        {
            'col_int': [1000, -2000, 3000, -4000000],
            'col_float': [-3333.0, 4445.0, -5555.0, 6667.0],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': [float('nan'), float('nan'), float('nan'), 8889.0],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.approximate(bdf.df1, round_to='ceil')
    assert str(expected_df[['col_int']]) == str(transformed[['col_int']])
    assert str(expected_df[['col_float']]) == str(transformed[['col_float']])
    assert str(expected_df[['col_str']]) == str(transformed[['col_str']])
    assert str(expected_df[['col_nan']]) == str(transformed[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(transformed[['col_strnan']])
    assert expected_df.equals(transformed)


def test_round_trunc():
    bdf = BaseDF()

    expected_df = pd.DataFrame(
        {
            'col_int': [1000, -2000, 3000, -4000000],
            'col_float': [-3333.0, 4444.0, -5555.0, 6666.0],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': [float('nan'), float('nan'), float('nan'), 8888.0],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.approximate(bdf.df1, round_to='trunc')
    assert str(expected_df[['col_int']]) == str(transformed[['col_int']])
    assert str(expected_df[['col_float']]) == str(transformed[['col_float']])
    assert str(expected_df[['col_str']]) == str(transformed[['col_str']])
    assert str(expected_df[['col_nan']]) == str(transformed[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(transformed[['col_strnan']])
    assert expected_df.equals(transformed)
