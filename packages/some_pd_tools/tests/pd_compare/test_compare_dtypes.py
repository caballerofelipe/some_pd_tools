import re

import pandas as pd
import pytest

from some_pd_tools import pd_compare

from ..basedf import BaseDF

from ..formatting import (
    _fn_ret_and_output,
    # _return_pprint,
    _return_print_event,
    _return_print_plain,
    # _return_print_result,
    _return_print_title,
    # _sorted,
)


def test_exceptions():
    bdf = BaseDF()

    # df1 or df2 are not of type pd.DataFrame error
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

    # df1_name and df2_name are not of type str error
    # ************************************
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

    # Different columns not allowed: different columns error
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('df1 (df1_name) and df2 (df2_name) must have the same columns.'),
    ):
        pd_compare.compare_dtypes(
            bdf.df1_extra_col, bdf.df2_extra_col, df1_name='df1_name', df2_name='df2_name'
        )

    # Duplicate columns, different columns: different columns error
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('df1 (df1_name) and df2 (df2_name) must have the same columns.'),
    ):
        pd_compare.compare_dtypes(
            bdf.df1_extra_col[[*bdf.df1_extra_col.columns, *bdf.df1_extra_col.columns]],
            bdf.df2_extra_col[[*bdf.df2_extra_col.columns, *bdf.df2_extra_col.columns]],
            df1_name='df1_name',
            df2_name='df2_name',
        )

    # Duplicate columns, equal columns: duplicates error
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('df1 (df1_name) and df2 (df2_name) cannot have duplicate columns.'),
    ):
        pd_compare.compare_dtypes(
            bdf.df1[[*bdf.df1.columns, *bdf.df1.columns]],
            bdf.df2[[*bdf.df2.columns, *bdf.df2.columns]],
            df1_name='df1_name',
            df2_name='df2_name',
        )


def test_equal_dtypes():
    bdf = BaseDF()

    predicted_dtypes_df = pd.DataFrame(
        {
            'different': [False, False, False, False, False],
            'thedf1': ['float64', 'int64', 'float64', 'object', 'object'],
            'thedf2': ['float64', 'int64', 'float64', 'object', 'object'],
        },
        index=['col_float', 'col_int', 'col_nan', 'col_str', 'col_strnan'],
    )

    # Equal columns, equal dtypes, w report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=True,
        report_print=True,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '✅ Columns have equal dtypes')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    io_predicted_str += _return_print_plain(1, '|column    |different|thedf1 |thedf2 |')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    io_predicted_str += _return_print_plain(1, '|col_float |         |float64|float64|')
    io_predicted_str += _return_print_plain(1, '|col_int   |         |int64  |int64  |')
    io_predicted_str += _return_print_plain(1, '|col_nan   |         |float64|float64|')
    io_predicted_str += _return_print_plain(1, '|col_str   |         |object |object |')
    io_predicted_str += _return_print_plain(1, '|col_strnan|         |object |object |')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    assert io_predicted_str == io_out
    assert returned[0] is True
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str

    # Equal columns, equal dtypes, w report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=False,
        report_print=True,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '✅ Columns have equal dtypes')
    assert io_predicted_str == io_out
    assert returned[0] is True
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str

    # Equal columns, equal dtypes, no report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=True,
        report_print=False,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '✅ Columns have equal dtypes')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    io_predicted_str += _return_print_plain(1, '|column    |different|thedf1 |thedf2 |')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    io_predicted_str += _return_print_plain(1, '|col_float |         |float64|float64|')
    io_predicted_str += _return_print_plain(1, '|col_int   |         |int64  |int64  |')
    io_predicted_str += _return_print_plain(1, '|col_nan   |         |float64|float64|')
    io_predicted_str += _return_print_plain(1, '|col_str   |         |object |object |')
    io_predicted_str += _return_print_plain(1, '|col_strnan|         |object |object |')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    assert '' == io_out
    assert returned[0] is True
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str

    # Equal columns, equal dtypes, no report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=False,
        report_print=False,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '✅ Columns have equal dtypes')
    assert '' == io_out
    assert returned[0] is True
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str


def test_diff_dtypes():
    bdf = BaseDF()

    predicted_dtypes_df = pd.DataFrame(
        {
            'different': [True, True, True, False, False],
            'thedf1': ['float64', 'int64', 'float64', 'object', 'object'],
            'thedf2': ['object', 'object', 'object', 'object', 'object'],
        },
        index=['col_float', 'col_int', 'col_nan', 'col_str', 'col_strnan'],
    )

    # Different dtypes, w report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        bdf.df1,
        bdf.df2_as_object,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=True,
        report_print=True,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '😓 Columns have different dtypes')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|------|')
    io_predicted_str += _return_print_plain(1, '|column    |different|thedf1 |thedf2|')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|------|')
    io_predicted_str += _return_print_plain(1, '|col_float |    *    |float64|object|')
    io_predicted_str += _return_print_plain(1, '|col_int   |    *    |int64  |object|')
    io_predicted_str += _return_print_plain(1, '|col_nan   |    *    |float64|object|')
    io_predicted_str += _return_print_plain(1, '|col_str   |         |object |object|')
    io_predicted_str += _return_print_plain(1, '|col_strnan|         |object |object|')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|------|')
    assert io_predicted_str == io_out
    assert returned[0] is False
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str

    # Different dtypes, w report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        bdf.df1,
        bdf.df2_as_object,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=False,
        report_print=True,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '😓 Columns have different dtypes')
    io_predicted_str += _return_print_plain(1, '|---------|---------|-------|------|')
    io_predicted_str += _return_print_plain(1, '|column   |different|thedf1 |thedf2|')
    io_predicted_str += _return_print_plain(1, '|---------|---------|-------|------|')
    io_predicted_str += _return_print_plain(1, '|col_float|    *    |float64|object|')
    io_predicted_str += _return_print_plain(1, '|col_int  |    *    |int64  |object|')
    io_predicted_str += _return_print_plain(1, '|col_nan  |    *    |float64|object|')
    io_predicted_str += _return_print_plain(1, '|---------|---------|-------|------|')
    assert io_predicted_str == io_out
    assert returned[0] is False
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str

    # Different dtypes, no report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        bdf.df1,
        bdf.df2_as_object,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=True,
        report_print=False,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '😓 Columns have different dtypes')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|------|')
    io_predicted_str += _return_print_plain(1, '|column    |different|thedf1 |thedf2|')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|------|')
    io_predicted_str += _return_print_plain(1, '|col_float |    *    |float64|object|')
    io_predicted_str += _return_print_plain(1, '|col_int   |    *    |int64  |object|')
    io_predicted_str += _return_print_plain(1, '|col_nan   |    *    |float64|object|')
    io_predicted_str += _return_print_plain(1, '|col_str   |         |object |object|')
    io_predicted_str += _return_print_plain(1, '|col_strnan|         |object |object|')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|------|')
    assert '' == io_out
    assert returned[0] is False
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str

    # Different dtypes, no report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        bdf.df1,
        bdf.df2_as_object,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=False,
        report_print=False,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '😓 Columns have different dtypes')
    io_predicted_str += _return_print_plain(1, '|---------|---------|-------|------|')
    io_predicted_str += _return_print_plain(1, '|column   |different|thedf1 |thedf2|')
    io_predicted_str += _return_print_plain(1, '|---------|---------|-------|------|')
    io_predicted_str += _return_print_plain(1, '|col_float|    *    |float64|object|')
    io_predicted_str += _return_print_plain(1, '|col_int  |    *    |int64  |object|')
    io_predicted_str += _return_print_plain(1, '|col_nan  |    *    |float64|object|')
    io_predicted_str += _return_print_plain(1, '|---------|---------|-------|------|')
    assert '' == io_out
    assert returned[0] is False
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str


def test_diff_dtypes_second_only():
    bdf = BaseDF()

    predicted_dtypes_df = pd.DataFrame(
        {
            'different': [False, True, False, False, False],
            'thedf1': ['float64', 'int64', 'float64', 'object', 'object'],
            'thedf2': ['float64', 'object', 'float64', 'object', 'object'],
        },
        index=['col_float', 'col_int', 'col_nan', 'col_str', 'col_strnan'],
    )

    # Different dtypes, w report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        bdf.df1,
        bdf.df2_diff_values_col_int_made_str,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=True,
        report_print=True,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '😓 Columns have different dtypes')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    io_predicted_str += _return_print_plain(1, '|column    |different|thedf1 |thedf2 |')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    io_predicted_str += _return_print_plain(1, '|col_float |         |float64|float64|')
    io_predicted_str += _return_print_plain(1, '|col_int   |    *    |int64  |object |')
    io_predicted_str += _return_print_plain(1, '|col_nan   |         |float64|float64|')
    io_predicted_str += _return_print_plain(1, '|col_str   |         |object |object |')
    io_predicted_str += _return_print_plain(1, '|col_strnan|         |object |object |')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    assert io_predicted_str == io_out
    assert returned[0] is False
    assert str(returned[1]['dtypes_df']) == str(predicted_dtypes_df)
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str

    # Different dtypes, w report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        bdf.df1,
        bdf.df2_diff_values_col_int_made_str,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=False,
        report_print=True,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '😓 Columns have different dtypes')
    io_predicted_str += _return_print_plain(1, '|-------|---------|------|------|')
    io_predicted_str += _return_print_plain(1, '|column |different|thedf1|thedf2|')
    io_predicted_str += _return_print_plain(1, '|-------|---------|------|------|')
    io_predicted_str += _return_print_plain(1, '|col_int|    *    |int64 |object|')
    io_predicted_str += _return_print_plain(1, '|-------|---------|------|------|')
    assert io_predicted_str == io_out
    assert returned[0] is False
    assert str(returned[1]['dtypes_df']) == str(predicted_dtypes_df)
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str

    # Different dtypes, no report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        bdf.df1,
        bdf.df2_diff_values_col_int_made_str,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=True,
        report_print=False,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '😓 Columns have different dtypes')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    io_predicted_str += _return_print_plain(1, '|column    |different|thedf1 |thedf2 |')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    io_predicted_str += _return_print_plain(1, '|col_float |         |float64|float64|')
    io_predicted_str += _return_print_plain(1, '|col_int   |    *    |int64  |object |')
    io_predicted_str += _return_print_plain(1, '|col_nan   |         |float64|float64|')
    io_predicted_str += _return_print_plain(1, '|col_str   |         |object |object |')
    io_predicted_str += _return_print_plain(1, '|col_strnan|         |object |object |')
    io_predicted_str += _return_print_plain(1, '|----------|---------|-------|-------|')
    assert '' == io_out
    assert returned[0] is False
    assert str(returned[1]['dtypes_df']) == str(predicted_dtypes_df)
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str

    # Different dtypes, no report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_dtypes,
        bdf.df1,
        bdf.df2_diff_values_col_int_made_str,
        df1_name='thedf1',
        df2_name='thedf2',
        show_all_dtypes=False,
        report_print=False,
    )
    io_predicted_str = _return_print_title(1, 'Comparing column dtypes')
    io_predicted_str += _return_print_event(1, '😓 Columns have different dtypes')
    io_predicted_str += _return_print_plain(1, '|-------|---------|------|------|')
    io_predicted_str += _return_print_plain(1, '|column |different|thedf1|thedf2|')
    io_predicted_str += _return_print_plain(1, '|-------|---------|------|------|')
    io_predicted_str += _return_print_plain(1, '|col_int|    *    |int64 |object|')
    io_predicted_str += _return_print_plain(1, '|-------|---------|------|------|')
    assert '' == io_out
    assert returned[0] is False
    assert str(returned[1]['dtypes_df']) == str(predicted_dtypes_df)
    assert returned[1]['dtypes_df'].equals(predicted_dtypes_df)
    assert returned[1]['report'] == io_predicted_str
