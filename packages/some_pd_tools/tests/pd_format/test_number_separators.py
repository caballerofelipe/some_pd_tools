import re

import pandas as pd
import pytest

from some_pd_tools import pd_format

from ..basedf import BaseDF


def test__series_number_separators_exceptions():
    '''Testing _series_number_separators_exceptions, this function is used by `number_separators` and its exceptions differ, that's why only testing exceptions.'''

    bdf = BaseDF()

    # df of wrong type
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('`ser` must be of type pd.Series.'),
    ):
        pd_format._series_number_separators(1)

    # `thousands_sep` and `decimals_sep` equal
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('`thousands_sep` cannot be equal to `decimals_sep`.'),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], thousands_sep='a', decimals_sep='a')

    # `thousands_sep` and `decimals_sep`
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape("`thousands_sep` and `decimals_sep` cannot be bool."),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], thousands_sep=True)
    with pytest.raises(
        ValueError,
        match=re.escape("`thousands_sep` and `decimals_sep` cannot be bool."),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], decimals_sep=True)

    # `thousands_sep` and `decimals_sep` cannot be numbers
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape("`thousands_sep` and `decimals_sep` cannot be numbers."),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], thousands_sep=1.2)
    with pytest.raises(
        ValueError,
        match=re.escape("`thousands_sep` and `decimals_sep` cannot be numbers."),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], decimals_sep=1.2)

    # `thousands_sep` and `decimals_sep`  cannot include digits (0-9), '-', 'E' or 'e'
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape(
            "`thousands_sep` and `decimals_sep` cannot include the following: digits (0-9), '-', 'E' or 'e'; to avoid confusions."
        ),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], thousands_sep='0')
    with pytest.raises(
        ValueError,
        match=re.escape(
            "`thousands_sep` and `decimals_sep` cannot include the following: digits (0-9), '-', 'E' or 'e'; to avoid confusions."
        ),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], thousands_sep='-')
    with pytest.raises(
        ValueError,
        match=re.escape(
            "`thousands_sep` and `decimals_sep` cannot include the following: digits (0-9), '-', 'E' or 'e'; to avoid confusions."
        ),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], thousands_sep='E')
    with pytest.raises(
        ValueError,
        match=re.escape(
            "`thousands_sep` and `decimals_sep` cannot include the following: digits (0-9), '-', 'E' or 'e'; to avoid confusions."
        ),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], thousands_sep='e')
    with pytest.raises(
        ValueError,
        match=re.escape(
            "`thousands_sep` and `decimals_sep` cannot include the following: digits (0-9), '-', 'E' or 'e'; to avoid confusions."
        ),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], decimals_sep='0')
    with pytest.raises(
        ValueError,
        match=re.escape(
            "`thousands_sep` and `decimals_sep` cannot include the following: digits (0-9), '-', 'E' or 'e'; to avoid confusions."
        ),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], decimals_sep='-')
    with pytest.raises(
        ValueError,
        match=re.escape(
            "`thousands_sep` and `decimals_sep` cannot include the following: digits (0-9), '-', 'E' or 'e'; to avoid confusions."
        ),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], decimals_sep='E')
    with pytest.raises(
        ValueError,
        match=re.escape(
            "`thousands_sep` and `decimals_sep` cannot include the following: digits (0-9), '-', 'E' or 'e'; to avoid confusions."
        ),
    ):
        pd_format._series_number_separators(bdf.df1['col_int'], decimals_sep='e')


def test_number_separators_wrong_type():
    with pytest.raises(
        ValueError,
        match=re.escape('`df` must be of type pd.DataFrame or pd.Series.'),
    ):
        pd_format.number_separators([1, 2, 3])


def test_number_separators_DataFrame_no_separator_change():
    bdf = BaseDF()

    # Default precision
    # ************************************
    expected_df = pd.DataFrame(
        {
            'col_int': ['1,000', '-2,000', '3,000', '-4,000,000'],
            'col_float': ['-3,333.333333', '4,444.444444', '-5,555.555556', '6,666.666667'],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': ['nan', 'nan', 'nan', '8,888.888800'],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.number_separators(bdf.df1)
    assert expected_df.equals(transformed)

    # Custom precision
    # ************************************
    expected_df = pd.DataFrame(
        {
            'col_int': ['1,000', '-2,000', '3,000', '-4,000,000'],
            'col_float': ['-3,333.33', '4,444.44', '-5,555.56', '6,666.67'],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': ['nan', 'nan', 'nan', '8,888.89'],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.number_separators(bdf.df1, precision=2)
    assert expected_df.equals(transformed)


def test_number_separators_DataFrame_w_separator_change():
    bdf = BaseDF()

    # Default precision
    # ************************************
    expected_df = pd.DataFrame(
        {
            'col_int': ['1.000', '-2.000', '3.000', '-4.000.000'],
            'col_float': ['-3.333,333333', '4.444,444444', '-5.555,555556', '6.666,666667'],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': ['nan', 'nan', 'nan', '8.888,888800'],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.number_separators(bdf.df1, thousands_sep='.', decimals_sep=',')
    assert str(expected_df[['col_int']]) == str(transformed[['col_int']])
    assert str(expected_df[['col_float']]) == str(transformed[['col_float']])
    assert str(expected_df[['col_str']]) == str(transformed[['col_str']])
    assert str(expected_df[['col_nan']]) == str(transformed[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(transformed[['col_strnan']])
    assert expected_df.equals(transformed)

    # Custom precision
    # ************************************
    expected_df = pd.DataFrame(
        {
            'col_int': ['1.000', '-2.000', '3.000', '-4.000.000'],
            'col_float': ['-3.333,33', '4.444,44', '-5.555,56', '6.666,67'],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': ['nan', 'nan', 'nan', '8.888,89'],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.number_separators(
        bdf.df1, precision=2, thousands_sep='.', decimals_sep=','
    )
    assert str(expected_df[['col_int']]) == str(transformed[['col_int']])
    assert str(expected_df[['col_float']]) == str(transformed[['col_float']])
    assert str(expected_df[['col_str']]) == str(transformed[['col_str']])
    assert str(expected_df[['col_nan']]) == str(transformed[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(transformed[['col_strnan']])
    assert expected_df.equals(transformed)

    # Default precision, using '$'
    # ************************************
    expected_df = pd.DataFrame(
        {
            'col_int': ['1_000', '-2_000', '3_000', '-4_000_000'],
            'col_float': ['-3_333$333333', '4_444$444444', '-5_555$555556', '6_666$666667'],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': ['nan', 'nan', 'nan', '8_888$888800'],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.number_separators(bdf.df1, thousands_sep='_', decimals_sep='$')
    assert str(expected_df[['col_int']]) == str(transformed[['col_int']])
    assert str(expected_df[['col_float']]) == str(transformed[['col_float']])
    assert str(expected_df[['col_str']]) == str(transformed[['col_str']])
    assert str(expected_df[['col_nan']]) == str(transformed[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(transformed[['col_strnan']])
    assert expected_df.equals(transformed)
    expected_df = pd.DataFrame(
        {
            'col_int': ['1$000', '-2$000', '3$000', '-4$000$000'],
            'col_float': ['-3$333_333333', '4$444_444444', '-5$555_555556', '6$666_666667'],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': ['nan', 'nan', 'nan', '8$888_888800'],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.number_separators(bdf.df1, thousands_sep='$', decimals_sep='_')
    assert str(expected_df[['col_int']]) == str(transformed[['col_int']])
    assert str(expected_df[['col_float']]) == str(transformed[['col_float']])
    assert str(expected_df[['col_str']]) == str(transformed[['col_str']])
    assert str(expected_df[['col_nan']]) == str(transformed[['col_nan']])
    assert str(expected_df[['col_strnan']]) == str(transformed[['col_strnan']])
    assert expected_df.equals(transformed)


def test_number_separators_Series_no_separator_change():
    bdf = BaseDF()

    # Default precision
    # ************************************
    expected_df = pd.DataFrame(
        {
            'col_int': ['1,000', '-2,000', '3,000', '-4,000,000'],
            'col_float': ['-3,333.333333', '4,444.444444', '-5,555.555556', '6,666.666667'],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': ['nan', 'nan', 'nan', '8,888.888800'],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.number_separators(bdf.df1['col_int'])
    assert str(expected_df['col_int']) == str(transformed)
    assert expected_df['col_int'].equals(transformed)
    transformed = pd_format.number_separators(bdf.df1['col_float'])
    assert str(expected_df['col_float']) == str(transformed)
    assert expected_df['col_float'].equals(transformed)
    transformed = pd_format.number_separators(bdf.df1['col_str'])
    assert str(expected_df['col_str']) == str(transformed)
    assert expected_df['col_str'].equals(transformed)
    transformed = pd_format.number_separators(bdf.df1['col_nan'])
    assert str(expected_df['col_nan']) == str(transformed)
    assert expected_df['col_nan'].equals(transformed)
    transformed = pd_format.number_separators(bdf.df1['col_strnan'])
    assert str(expected_df['col_strnan']) == str(transformed)
    assert expected_df['col_strnan'].equals(transformed)

    # Custom precision
    # ************************************
    expected_df = pd.DataFrame(
        {
            'col_int': ['1,000', '-2,000', '3,000', '-4,000,000'],
            'col_float': ['-3,333.33', '4,444.44', '-5,555.56', '6,666.67'],
            'col_str': ['a', 'b', 'c', '4444.4444444444'],
            'col_nan': ['nan', 'nan', 'nan', '8,888.89'],
            'col_strnan': ['d', 'e', 'f', float('nan')],
        }
    )
    transformed = pd_format.number_separators(bdf.df1['col_int'], precision=2)
    assert str(expected_df['col_int']) == str(transformed)
    assert expected_df['col_int'].equals(transformed)
    transformed = pd_format.number_separators(bdf.df1['col_float'], precision=2)
    assert str(expected_df['col_float']) == str(transformed)
    assert expected_df['col_float'].equals(transformed)
    transformed = pd_format.number_separators(bdf.df1['col_str'], precision=2)
    assert str(expected_df['col_str']) == str(transformed)
    assert expected_df['col_str'].equals(transformed)
    transformed = pd_format.number_separators(bdf.df1['col_nan'], precision=2)
    assert str(expected_df['col_nan']) == str(transformed)
    assert expected_df['col_nan'].equals(transformed)
    transformed = pd_format.number_separators(bdf.df1['col_strnan'], precision=2)
    assert str(expected_df['col_strnan']) == str(transformed)
    assert expected_df['col_strnan'].equals(transformed)
