import re

import pandas as pd
import pytest

from some_pd_tools import pd_compare

from ..basedf import BaseDF


def test_wrong_types():
    error = 'df1 and df2 must be of type pd.DataFrame.'
    # df1 or df2 are not of type pd.DataFrame
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape(error),
    ):
        pd_compare.compute_equality_df(
            df1=[1, 2, 3],
            df2={1, 2, 3},
        )
    with pytest.raises(
        ValueError,
        match=re.escape(error),
    ):
        pd_compare.compute_equality_df(
            df1='a',
            df2='b',
        )


def test_different_columns():
    bdf = BaseDF()
    with pytest.raises(
        ValueError,
        match=re.escape(
            'df1 and df2 must have equal columns and equal indexes. Select only the same columns and same indexes and run the function again.'
        ),
    ):
        pd_compare.compute_equality_df(
            df1=bdf.df1_extra_col,
            df2=bdf.df2_extra_col,
        )


def test_different_indexes():
    bdf = BaseDF()
    with pytest.raises(
        ValueError,
        match=re.escape(
            'df1 and df2 must have equal columns and equal indexes. Select only the same columns and same indexes and run the function again.'
        ),
    ):
        pd_compare.compute_equality_df(
            df1=bdf.df1,
            df2=bdf.df2_index_plus1,
        )


def test_duplicate_columns():
    bdf = BaseDF()
    with pytest.raises(
        ValueError,
        match=re.escape(
            'df1 and df2 cannot have duplicated columns or indexes. Select not duplicated columns and not duplicated indexes and run the function again.'
        ),
    ):
        pd_compare.compute_equality_df(
            df1=bdf.df1[[*bdf.df1.columns, *bdf.df1.columns]],
            df2=bdf.df1[[*bdf.df1.columns, *bdf.df1.columns]],
        )


def test_duplicate_indexes():
    bdf = BaseDF()
    with pytest.raises(
        ValueError,
        match=re.escape(
            'df1 and df2 cannot have duplicated columns or indexes. Select not duplicated columns and not duplicated indexes and run the function again.'
        ),
    ):
        pd_compare.compute_equality_df(
            df1=bdf.df1.loc[[*bdf.df1.index, *bdf.df1.index]],
            df2=bdf.df1.loc[[*bdf.df1.index, *bdf.df1.index]],
        )


def test_equal_values():
    bdf = BaseDF()
    expected_df = pd.DataFrame(
        {
            'col_int': [True, True, True, True],
            'col_float': [True, True, True, True],
            'col_str': [True, True, True, True],
            'col_nan': [True, True, True, True],
            'col_strnan': [True, True, True, True],
        }
    )

    # same dtypes and same values
    # ************************************
    equality_df = pd_compare.compute_equality_df(
        df1=bdf.df1,
        df2=bdf.df1,
    )
    assert str(expected_df[['col_int']]) == str(equality_df[['col_int']])
    assert str(expected_df[['col_float']]) == str(equality_df[['col_float']])
    assert str(expected_df[['col_str']]) == str(equality_df[['col_str']])
    assert str(expected_df[['col_nan']]) == str(equality_df[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(equality_df[['col_strnan']])
    assert expected_df.equals(equality_df)

    # different dtypes and same values
    # ************************************
    equality_df = pd_compare.compute_equality_df(
        df1=bdf.df1,
        df2=bdf.df1_as_object,
    )
    assert str(expected_df[['col_int']]) == str(equality_df[['col_int']])
    assert str(expected_df[['col_float']]) == str(equality_df[['col_float']])
    assert str(expected_df[['col_str']]) == str(equality_df[['col_str']])
    assert str(expected_df[['col_nan']]) == str(equality_df[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(equality_df[['col_strnan']])
    assert expected_df.equals(equality_df)


def test_diff_values():
    bdf = BaseDF()
    expected_df = pd.DataFrame(
        {
            'col_int': [False, False, False, True],
            'col_float': [False, False, False, True],
            'col_str': [False, False, False, True],
            'col_nan': [True, True, True, True],
            'col_strnan': [False, False, False, True],
        }
    )

    # same dtypes and same values
    # ************************************
    equality_df = pd_compare.compute_equality_df(
        df1=bdf.df1,
        df2=bdf.df2_diff_values,
    )
    assert str(expected_df[['col_int']]) == str(equality_df[['col_int']])
    assert str(expected_df[['col_float']]) == str(equality_df[['col_float']])
    assert str(expected_df[['col_str']]) == str(equality_df[['col_str']])
    assert str(expected_df[['col_nan']]) == str(equality_df[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(equality_df[['col_strnan']])
    assert expected_df.equals(equality_df)

    # different dtypes and same values
    # ************************************
    equality_df = pd_compare.compute_equality_df(
        df1=bdf.df1,
        df2=bdf.df1_as_object_diff_values,
    )
    assert str(expected_df[['col_int']]) == str(equality_df[['col_int']])
    assert str(expected_df[['col_float']]) == str(equality_df[['col_float']])
    assert str(expected_df[['col_str']]) == str(equality_df[['col_str']])
    assert str(expected_df[['col_nan']]) == str(equality_df[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(equality_df[['col_strnan']])
    assert expected_df.equals(equality_df)
