import re

import pandas as pd
import pytest

from some_pd_tools import pd_compare

from .basedf import BaseDF
from .formatting import (
    _fn_ret_and_output,
    _return_pprint,
    _return_print_event,
    _return_print_plain,
    _return_print_result,
    _return_print_title,
    _sorted,
)


def test__wrong_types():
    # df1 or df2 are not of type pd.DataFrame
    # ************************************
    # List and set
    with pytest.raises(
        ValueError,
        match=re.escape('df1 and df2 must be of type pd.DataFrame.'),
    ):
        pd_compare.compare_dtypes([1, 2, 3], {1, 2, 3})
    with pytest.raises(
        ValueError,
        match=re.escape('df1 and df2 must be of type pd.DataFrame.'),
    ):
        pd_compare.compare_dtypes({1, 2, 3}, [1, 2, 3])
    # Two series
    with pytest.raises(
        ValueError,
        match=re.escape('df1 and df2 must be of type pd.DataFrame.'),
    ):
        pd_compare.compare_dtypes(pd.Series([1, 2, 3]), pd.Series([1, 2, 3]))
    # One Series and one DataFrame
    with pytest.raises(
        ValueError,
        match=re.escape('df1 and df2 must be of type pd.DataFrame.'),
    ):
        pd_compare.compare_dtypes(pd.Series([1, 2, 3]), pd.DataFrame([1, 2, 3]))
    with pytest.raises(
        ValueError,
        match=re.escape('df1 and df2 must be of type pd.DataFrame.'),
    ):
        pd_compare.compare_dtypes(pd.DataFrame([1, 2, 3]), pd.Series([1, 2, 3]))

    # df1_name and df2_name must be of type str
    # ************************************
    bdf = BaseDF()
    with pytest.raises(
        ValueError,
        match=re.escape('df1_name and df2_name must be of type str.'),
    ):
        pd_compare.compare_dtypes(bdf.df1, bdf.df2, df1_name=1)
    with pytest.raises(
        ValueError,
        match=re.escape('df1_name and df2_name must be of type str.'),
    ):
        pd_compare.compare_dtypes(bdf.df1, bdf.df2, df2_name=1)


# def test__equal_dtypes_no_dups():
#     assert False  # TODO REMOVE


# def test__equal_dtypes_w_dups():
#     assert False  # TODO REMOVE


# def test__diff_dtypes_no_dups():
#     assert False  # TODO REMOVE


# def test__diff_dtypes_w_dups():
#     assert False  # TODO REMOVE


# def test__compare__dtypes_equal_values_equal() -> None:
#     '''Test output/return when dtypes are equal and values are equal.'''
#     assert False  # TODO REMOVE


# def test__compare__dtypes_not_equal_values_not_equal() -> None:
#     '''Test output/return when dtypes are not equal and values are not equal.'''
#     assert False  # TODO REMOVE
