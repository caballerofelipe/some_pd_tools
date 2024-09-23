import math
import os
import random
import re
from datetime import datetime as dt

import pandas as pd
import pytest

from some_pd_tools import pd_compare

from ..basedf import BaseDF
from ..formatting import (
    _fn_ret_and_output,
    _return_pprint,
    _return_print_event,
    # _return_print_plain,
    _return_print_result,
    _return_print_title,
    # _sorted,
)


def test_df_exceptions():
    bdf = BaseDF()

    # df1 or df2 are not of type pd.DataFrame
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('df1 and df2 must be of type pd.DataFrame.'),
    ):
        pd_compare.compare(
            df1=[1, 2, 3],
            df2={1, 2, 3},
        )
    with pytest.raises(
        ValueError,
        match=re.escape('df1 and df2 must be of type pd.DataFrame.'),
    ):
        pd_compare.compare(
            df1='a',
            df2='b',
        )

    # df1_name or df2_name are not of type str
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('df1_name and df2_name must be of type str.'),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=1,
            df2_name=2,
        )
    with pytest.raises(
        ValueError,
        match=re.escape('df1_name and df2_name must be of type str.'),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=True,
            df2_name=False,
        )

    # df1_name or df2_name are not of type str
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('df1_name and df2_name must be different.'),
    ):
        pd_compare.compare(
            df1=bdf.df1,  # .
            df2=bdf.df2,  # .
            df1_name=bdf.df1_name,  # .
            df2_name=bdf.df1_name,  # .
        )


def test_report_file_exceptions():
    bdf = BaseDF()

    # report_file_path is not string
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('report_file_path must be of type None or str'),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to=None,
            report_print=True,
            report_file_path=12,
            show_common_cols=False,
            show_common_idxs=False,
            show_all_dtypes=False,
            xls_path=None,
            xls_overwrite=False,
            xls_compare_str_equal='',
            xls_compare_str_diff='*_diff_*',
            xls_fixed_cols=None,
            xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
        )

    # report_file_path is a directory
    # ************************************
    while True:
        dirname = (
            'tmpdir_'
            + dt.now().strftime('%Y-%m-%d_%H-%M-%S')
            + str(math.floor(random.random() * 1_000_000_000_000))
        )
        if not os.path.exists(dirname):
            break
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    else:
        raise ValueError('Directory exists.')
    with pytest.raises(
        ValueError,
        match=re.escape(f'report_file_path [{dirname}] cannot be a directory.'),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to=None,
            report_print=True,
            report_file_path=dirname,
            show_common_cols=False,
            show_common_idxs=False,
            show_all_dtypes=False,
            xls_path=None,
            xls_overwrite=False,
            xls_compare_str_equal='',
            xls_compare_str_diff='*_diff_*',
            xls_fixed_cols=None,
            xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
        )
    os.rmdir(dirname)

    # report_file_path exists but overwrite is False
    # ************************************
    while True:
        filename = (
            'tmpfile_'
            + dt.now().strftime('%Y-%m-%d_%H-%M-%S')
            + str(math.floor(random.random() * 1_000_000_000_000))
        )
        if not os.path.exists(filename):
            break
    if not os.path.exists(filename):
        open(filename, 'a', encoding='utf-8').close()
    else:
        raise ValueError('File exists.')
    with pytest.raises(
        ValueError,
        match=re.escape(
            f'report_file_path [{filename}] exists but report_file_overwrite is False.'
        ),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to=None,
            report_print=True,
            report_file_path=filename,
            report_file_overwrite=False,
            show_common_cols=False,
            show_common_idxs=False,
            show_all_dtypes=False,
            xls_path=None,
            xls_overwrite=False,
            xls_compare_str_equal='',
            xls_compare_str_diff='*_diff_*',
            xls_fixed_cols=None,
            xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
        )
    os.remove(filename)


def test_round_to_exceptions():
    bdf = BaseDF()

    # round_to wrong values
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape(
            "round_to must be None, a positive integer or a string (either 'floor' or 'ceil')."
        ),
    ):
        pd_compare.compare(
            df1=bdf.df1, df2=bdf.df2, df1_name=bdf.df1_name, df2_name=bdf.df2_name, round_to=True
        )
    with pytest.raises(
        ValueError,
        match=re.escape(
            "round_to must be None, a positive integer or a string (either 'floor' or 'ceil')."
        ),
    ):
        pd_compare.compare(
            df1=bdf.df1, df2=bdf.df2, df1_name=bdf.df1_name, df2_name=bdf.df2_name, round_to=-1
        )
    with pytest.raises(
        ValueError,
        match=re.escape(
            "round_to must be None, a positive integer or a string (either 'floor' or 'ceil')."
        ),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to='some string',
        )
    with pytest.raises(
        ValueError,
        match=re.escape(
            "round_to must be None, a positive integer or a string (either 'floor' or 'ceil')."
        ),
    ):
        pd_compare.compare(
            df1=bdf.df1, df2=bdf.df2, df1_name=bdf.df1_name, df2_name=bdf.df2_name, round_to=1.2
        )


def test_xls_exceptions():
    bdf = BaseDF()

    # xls_path is not string
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('xls_path must be of type str.'),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to=None,
            report_print=True,
            show_common_cols=False,
            show_common_idxs=False,
            show_all_dtypes=False,
            xls_path=12,
            xls_overwrite=False,
            xls_compare_str_equal='',
            xls_compare_str_diff='*_diff_*',
            xls_fixed_cols=None,
            xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
        )

    # xls_path is a directory
    # ************************************
    while True:
        dirname = (
            'tmpdir_'
            + dt.now().strftime('%Y-%m-%d_%H-%M-%S')
            + str(math.floor(random.random() * 1_000_000_000_000))
        )
        if not os.path.exists(dirname):
            break
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    else:
        raise ValueError('Directory exists.')
    with pytest.raises(
        ValueError,
        match=re.escape(f'xls_path [{dirname}] cannot be a directory.'),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to=None,
            report_print=True,
            show_common_cols=False,
            show_common_idxs=False,
            show_all_dtypes=False,
            xls_path=dirname,
            xls_overwrite=False,
            xls_compare_str_equal='',
            xls_compare_str_diff='*_diff_*',
            xls_fixed_cols=None,
            xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
        )
    os.rmdir(dirname)

    # overwriting a file but overwrite is False
    # ************************************
    while True:
        filename = (
            'tmpfile_'
            + dt.now().strftime('%Y-%m-%d_%H-%M-%S')
            + str(math.floor(random.random() * 1_000_000_000_000))
        )
        if not os.path.exists(filename):
            break
    if not os.path.exists(filename):
        open(filename, 'a', encoding='utf-8').close()
    else:
        raise ValueError('File exists.')
    with pytest.raises(
        ValueError,
        match=re.escape(f'xls_path [{filename}] exists but xls_overwrite is False.'),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to=None,
            report_print=True,
            show_common_cols=False,
            show_common_idxs=False,
            show_all_dtypes=False,
            xls_path=filename,
            xls_overwrite=False,
            xls_compare_str_equal='',
            xls_compare_str_diff='*_diff_*',
            xls_fixed_cols=None,
            xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
        )
    os.remove(filename)

    # xls_compare_str_equal is not string
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('xls_compare_str_equal must be of type str.'),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to=None,
            report_print=True,
            show_common_cols=False,
            show_common_idxs=False,
            show_all_dtypes=False,
            xls_path='__deleteme__.xlsx',
            xls_overwrite=False,
            xls_compare_str_equal=1,
            xls_compare_str_diff='*_diff_*',
            xls_fixed_cols=None,
            xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
        )

    # xls_compare_str_diff is not string
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('xls_compare_str_diff must be of type str.'),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to=None,
            report_print=True,
            show_common_cols=False,
            show_common_idxs=False,
            show_all_dtypes=False,
            xls_path='__deleteme__.xlsx',
            xls_overwrite=False,
            xls_compare_str_equal='',
            xls_compare_str_diff=1,
            xls_fixed_cols=None,
            xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
        )

    # Unexisting xls_fixed_cols column in df1
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape(
            f"The following fixed_cols are not present in df1(df1_name={bdf.df1_name}): ['not_existing_col', 'x_not_existing_col']."
        ),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to=None,
            report_print=True,
            show_common_cols=False,
            show_common_idxs=False,
            show_all_dtypes=False,
            xls_path='__deleteme__.xlsx',
            xls_overwrite=False,
            xls_compare_str_equal='',
            xls_compare_str_diff='*_diff_*',
            xls_fixed_cols=['x_not_existing_col', 'not_existing_col'],
            xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
        )

    # Unexisting xls_fixed_cols column in df2
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape(
            f"The following fixed_cols are not present in df2(df2_name={bdf.df2_name}): ['col_df1extra']."
        ),
    ):
        pd_compare.compare(
            df1=bdf.df1_extra_col,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to=None,
            report_print=True,
            show_common_cols=False,
            show_common_idxs=False,
            show_all_dtypes=False,
            xls_path='__deleteme__.xlsx',
            xls_overwrite=False,
            xls_compare_str_equal='',
            xls_compare_str_diff='*_diff_*',
            xls_fixed_cols=['col_df1extra'],
            xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
        )

    # xls_datetime_rpl is not string
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('xls_datetime_rpl must be of type str.'),
    ):
        pd_compare.compare(
            df1=bdf.df1,
            df2=bdf.df2,
            df1_name=bdf.df1_name,
            df2_name=bdf.df2_name,
            round_to=None,
            report_print=True,
            show_common_cols=False,
            show_common_idxs=False,
            show_all_dtypes=False,
            xls_path='__deleteme__.xlsx',
            xls_overwrite=False,
            xls_compare_str_equal='',
            xls_compare_str_diff='*_diff_*',
            xls_fixed_cols=None,
            xls_datetime_rpl=1,
        )


def test_equality_full() -> None:
    bdf = BaseDF()

    report_predicted = _return_print_title(1, 'Equality check', 'full')
    report_predicted += _return_print_result('🥳 Equal')
    report_predicted += _return_print_title(
        1, 'Returning', 'True[equality_full], False[equality_partial], dict[equality_metadata]'
    )

    # Equal DataFrames
    # ************************************
    # IMPORTANT: Using `df1 = bdf.df1` (same with df2) to use it later to reference the same object
    # because `bdf.df1` always creates a copy to avoid changing the internal `df1`
    df1 = bdf.df1
    df2 = bdf.df2
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=df1,
        df2=df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
    )
    equality_metadata_predicted = {
        'params': {
            'df1': df1,
            'df2': df2,
            'df1_name': bdf.df1_name,
            'df2_name': bdf.df2_name,
            'round_to': None,
            'report_print': True,
            'report_file_path': None,
            'report_file_overwrite': False,
            'show_common_cols': False,
            'show_common_idxs': False,
            'show_all_dtypes': False,
            'xls_path': None,
            'xls_overwrite': False,
            'xls_compare_str_equal': '',
            'xls_compare_str_diff': '*_diff_*',
            'xls_fixed_cols': None,
            'xls_datetime_rpl': '%Y-%m-%d %H:%M:%S',
        },
        'variables': {},
        'report': report_predicted,
    }
    assert returned[0] is True
    assert returned[1] is False
    print(returned[2])
    assert returned[2] == equality_metadata_predicted
    assert io_out == report_predicted

    bdf = BaseDF()

    # Equal Columns, equal DataFrames, all duplicated (two instances of each)
    # This only works because `df1_cp.equals(df2_cp)` is True in the beginning
    # ************************************
    df1 = bdf.df1[[*bdf.df1.columns, *bdf.df1.columns]]
    df2 = bdf.df2[[*bdf.df2.columns, *bdf.df2.columns]]
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=df1,
        df2=df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
    )
    equality_metadata_predicted = {
        'params': {
            'df1': df1,
            'df2': df2,
            'df1_name': bdf.df1_name,
            'df2_name': bdf.df2_name,
            'round_to': None,
            'report_print': True,
            'report_file_path': None,
            'report_file_overwrite': False,
            'show_common_cols': False,
            'show_common_idxs': False,
            'show_all_dtypes': False,
            'xls_path': None,
            'xls_overwrite': False,
            'xls_compare_str_equal': '',
            'xls_compare_str_diff': '*_diff_*',
            'xls_fixed_cols': None,
            'xls_datetime_rpl': '%Y-%m-%d %H:%M:%S',
        },
        'variables':{},
        'report': report_predicted,
    }
    assert returned[0] is True
    assert returned[1] is False
    assert returned[2] == equality_metadata_predicted
    assert io_out == report_predicted

    # Equal Indexes, equal DataFrames, all duplicated (two instances of each)
    # This only works because `df1_cp.equals(df2_cp)` is True in the beginning
    # This assumes there are no column duplicates (checked previously)
    # ************************************
    df1 = bdf.df1.loc[[*bdf.df1.index, *bdf.df1.index]]
    df2 = bdf.df2.loc[[*bdf.df2.index, *bdf.df2.index]]
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=df1,
        df2=df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
    )
    equality_metadata_predicted = {
        'params': {
            'df1': df1,
            'df2': df2,
            'df1_name': bdf.df1_name,
            'df2_name': bdf.df2_name,
            'round_to': None,
            'report_print': True,
            'report_file_path': None,
            'report_file_overwrite': False,
            'show_common_cols': False,
            'show_common_idxs': False,
            'show_all_dtypes': False,
            'xls_path': None,
            'xls_overwrite': False,
            'xls_compare_str_equal': '',
            'xls_compare_str_diff': '*_diff_*',
            'xls_fixed_cols': None,
            'xls_datetime_rpl': '%Y-%m-%d %H:%M:%S',
        },
        'variables':{},
        'report': report_predicted,
    }
    assert returned[0] is True
    assert returned[1] is False
    assert returned[2] == equality_metadata_predicted
    assert io_out == report_predicted


def test_not_equality_first_lines() -> None:
    bdf = BaseDF()

    report_predicted = _return_print_title(1, 'Equality check', 'full')
    report_predicted += _return_print_result('😡 Not equal')

    # Different columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
    )
    first_lines_not_equal = re.search('.*\n.*\n.*\n.*\n', io_out).group(0)
    assert returned[0] is False
    assert report_predicted == first_lines_not_equal

    # Different types
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_as_object,  # As object dtype
        df2=bdf.df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
    )
    first_lines_not_equal = re.search('.*\n.*\n.*\n.*\n', io_out).group(0)
    assert returned[0] is False
    assert report_predicted == first_lines_not_equal

    # Different indexes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2.drop(0),  # Drop first line
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
    )
    first_lines_not_equal = re.search('.*\n.*\n.*\n.*\n', io_out).group(0)
    assert returned[0] is False
    assert report_predicted == first_lines_not_equal

    # Different values
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        # Change the order and reset index
        df2=bdf.df2.sort_index(ascending=False).reset_index(drop=True),
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
    )
    first_lines_not_equal = re.search('.*\n.*\n.*\n.*\n', io_out).group(0)
    assert returned[0] is False
    assert report_predicted == first_lines_not_equal


def test_duplicates_abort() -> None:
    bdf = BaseDF()

    # Extra Columns, all duplicated (two instances of each)
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col[[*bdf.df1_extra_col.columns, *bdf.df1_extra_col.columns]],
        df2=bdf.df2_extra_col[[*bdf.df2_extra_col.columns, *bdf.df2_extra_col.columns]],
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
    )
    assert returned[0] is False
    assert returned[1] is False
    equality_metadata = returned[2]
    assert equality_metadata['variables'].get('cols_common_set') == set(bdf.df1.columns)
    assert equality_metadata['variables'].get('cols_df1_excl_set') == set(bdf.df1_extra_col.columns) - set(
        bdf.df1.columns
    )
    assert equality_metadata['variables'].get('cols_df2_excl_set') == set(bdf.df2_extra_col.columns) - set(
        bdf.df2.columns
    )
    assert equality_metadata['variables'].get('cols_df1_dups_dict') == {
        col: 2 for col in bdf.df1_extra_col.columns
    }
    assert equality_metadata['variables'].get('cols_df2_dups_dict') == {
        col: 2 for col in bdf.df2_extra_col.columns
    }
    assert equality_metadata['variables'].get('cols_df1_dups_common_dict') == {col: 2 for col in bdf.df1.columns}
    assert equality_metadata['variables'].get('cols_df2_dups_common_dict') == {col: 2 for col in bdf.df2.columns}
    error = '🛑 Duplicate common columns found. Only common non duplicates columns allowed, stopping compare and returning. Either change the columns\' names or compare only one of the duplicates columns at a time. Review the returned metadata (indexes \'cols_df1_dups_common_dict\' and \'cols_df1_dups_common_dict\'.)'
    assert _return_print_event(1, error) in io_out
    assert equality_metadata['variables'].get('error') == error

    # Extra Columns, all duplicated (two instances df1, three instances of df2)
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col[[*bdf.df1_extra_col.columns, *bdf.df1_extra_col.columns]],
        df2=bdf.df2_extra_col[
            [*bdf.df2_extra_col.columns, *bdf.df2_extra_col.columns, *bdf.df2_extra_col.columns]
        ],
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
    )
    assert returned[0] is False
    assert returned[1] is False
    equality_metadata = returned[2]
    assert equality_metadata['variables'].get('cols_common_set') == set(bdf.df1.columns)
    assert equality_metadata['variables'].get('cols_df1_excl_set') == set(bdf.df1_extra_col.columns) - set(
        bdf.df1.columns
    )
    assert equality_metadata['variables'].get('cols_df2_excl_set') == set(bdf.df2_extra_col.columns) - set(
        bdf.df2.columns
    )
    assert equality_metadata['variables'].get('cols_df1_dups_dict') == {
        col: 2 for col in bdf.df1_extra_col.columns
    }
    assert equality_metadata['variables'].get('cols_df2_dups_dict') == {
        col: 3 for col in bdf.df2_extra_col.columns
    }
    assert equality_metadata['variables'].get('cols_df1_dups_common_dict') == {col: 2 for col in bdf.df1.columns}
    assert equality_metadata['variables'].get('cols_df2_dups_common_dict') == {col: 3 for col in bdf.df2.columns}
    error = '🛑 Duplicate common columns found. Only common non duplicates columns allowed, stopping compare and returning. Either change the columns\' names or compare only one of the duplicates columns at a time. Review the returned metadata (indexes \'cols_df1_dups_common_dict\' and \'cols_df1_dups_common_dict\'.)'
    assert equality_metadata['variables'].get('error') == error

    # Extra Indexes, all duplicated (two instances of each)
    # df1 duplicated indexes are [0,1,2]
    # df2 duplicated indexes are [1,2,3]
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1.loc[[0, 1, 2, 0, 1, 2]],
        df2=bdf.df2.loc[[1, 2, 3, 1, 2, 3]],
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
    )
    assert returned[0] is False
    assert returned[1] is False
    equality_metadata = returned[2]
    assert equality_metadata['variables'].get('cols_common_set') == set(bdf.df1.columns)
    assert equality_metadata['variables'].get('cols_df1_excl_set') == set()
    assert equality_metadata['variables'].get('cols_df2_excl_set') == set()
    assert equality_metadata['variables'].get('cols_df1_dups_dict') == {}
    assert equality_metadata['variables'].get('cols_df2_dups_dict') == {}
    assert equality_metadata['variables'].get('cols_df1_dups_common_dict') == {}
    assert equality_metadata['variables'].get('cols_df2_dups_common_dict') == {}
    assert equality_metadata['variables'].get('idxs_common_set') == set([1, 2])
    assert equality_metadata['variables'].get('idxs_df1_excl_set') == set([0])
    assert equality_metadata['variables'].get('idxs_df2_excl_set') == set([3])
    assert equality_metadata['variables'].get('idxs_df1_dups_dict') == {idx: 2 for idx in [0, 1, 2]}
    assert equality_metadata['variables'].get('idxs_df2_dups_dict') == {idx: 2 for idx in [1, 2, 3]}
    assert equality_metadata['variables'].get('idxs_df1_dups_common_dict') == {idx: 2 for idx in [1, 2]}
    assert equality_metadata['variables'].get('idxs_df2_dups_common_dict') == {idx: 2 for idx in [1, 2]}
    error = '🛑 Duplicate common indexes found. Only common non duplicates indexes allowed, stopping compare and returning. Either change the indexes\' names or compare only one of the duplicates indexes at a time. Review the returned metadata (indexes \'idxs_df1_dups_common_dict\' and \'idxs_df1_dups_common_dict\'.)'
    assert equality_metadata['variables'].get('error') == error

    # Extra Indexes, all duplicated (two instances df1, three instances of df2)
    # df1 duplicated indexes are [0,1,2]
    # df2 duplicated indexes are [1,2,3]
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1.loc[[0, 1, 2, 0, 1, 2]],
        df2=bdf.df2.loc[[1, 2, 3, 1, 2, 3, 1, 2, 3]],
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
    )
    assert returned[0] is False
    assert returned[1] is False
    equality_metadata = returned[2]
    assert equality_metadata['variables'].get('cols_common_set') == set(bdf.df1.columns)
    assert equality_metadata['variables'].get('cols_df1_excl_set') == set()
    assert equality_metadata['variables'].get('cols_df2_excl_set') == set()
    assert equality_metadata['variables'].get('cols_df1_dups_dict') == {}
    assert equality_metadata['variables'].get('cols_df2_dups_dict') == {}
    assert equality_metadata['variables'].get('cols_df1_dups_common_dict') == {}
    assert equality_metadata['variables'].get('cols_df2_dups_common_dict') == {}
    assert equality_metadata['variables'].get('idxs_common_set') == set([1, 2])
    assert equality_metadata['variables'].get('idxs_df1_excl_set') == set([0])
    assert equality_metadata['variables'].get('idxs_df2_excl_set') == set([3])
    assert equality_metadata['variables'].get('idxs_df1_dups_dict') == {idx: 2 for idx in [0, 1, 2]}
    assert equality_metadata['variables'].get('idxs_df2_dups_dict') == {idx: 3 for idx in [1, 2, 3]}
    assert equality_metadata['variables'].get('idxs_df1_dups_common_dict') == {idx: 2 for idx in [1, 2]}
    assert equality_metadata['variables'].get('idxs_df2_dups_common_dict') == {idx: 3 for idx in [1, 2]}
    error = '🛑 Duplicate common indexes found. Only common non duplicates indexes allowed, stopping compare and returning. Either change the indexes\' names or compare only one of the duplicates indexes at a time. Review the returned metadata (indexes \'idxs_df1_dups_common_dict\' and \'idxs_df1_dups_common_dict\'.)'
    assert equality_metadata['variables'].get('error') == error


def test_cols_review() -> None:
    bdf = BaseDF()
    df1_col_set = set(bdf.df1_extra_col.columns)
    df2_col_set = set(bdf.df2_extra_col.columns)
    cols_common_set = df1_col_set.intersection(df2_col_set)
    cols_df1_excl_set = df1_col_set - cols_common_set
    cols_df2_excl_set = df2_col_set - cols_common_set

    compare_lists_ret_show_common = pd_compare.compare_lists(
        list_1=list(bdf.df1_extra_col.columns),
        list_2=list(bdf.df2_extra_col.columns),
        show_common_items=True,
        list_1_name='df1',
        list_2_name='df2',
        type_name='column',
        type_name_plural='columns',
    )
    compare_lists_ret_no_show_common = pd_compare.compare_lists(
        list_1=list(bdf.df1_extra_col.columns),
        list_2=list(bdf.df2_extra_col.columns),
        show_common_items=False,
        list_1_name='df1',
        list_2_name='df2',
        type_name='column',
        type_name_plural='columns',
    )

    # Column metadata returned showing common columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col,
        show_common_cols=True,
        report_print=True,
    )
    io_predicted_printed_substr = compare_lists_ret_show_common[1]['report']
    equality_metadata = returned[2]
    assert returned[0] is False
    assert io_predicted_printed_substr in io_out
    assert io_predicted_printed_substr in equality_metadata.get('report')
    assert equality_metadata['variables'].get('cols_common_set') == cols_common_set
    assert equality_metadata['variables'].get('cols_df1_excl_set') == cols_df1_excl_set
    assert equality_metadata['variables'].get('cols_df2_excl_set') == cols_df2_excl_set
    assert equality_metadata['variables'].get('cols_df1_dups_dict') == {}
    assert equality_metadata['variables'].get('cols_df2_dups_dict') == {}
    assert equality_metadata['variables'].get('cols_df1_dups_common_dict') == {}
    assert equality_metadata['variables'].get('cols_df2_dups_common_dict') == {}

    # Column metadata returned NOT showing common columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col,
        show_common_cols=False,
        report_print=True,
    )
    equality_metadata = returned[2]
    assert returned[0] is False
    assert compare_lists_ret_show_common[1]['report'] not in io_out
    assert compare_lists_ret_no_show_common[1]['report'] in equality_metadata.get('report')
    assert compare_lists_ret_show_common[1]['report'] not in equality_metadata.get('report')
    assert equality_metadata['variables'].get('cols_common_set') == cols_common_set
    assert equality_metadata['variables'].get('cols_df1_excl_set') == cols_df1_excl_set
    assert equality_metadata['variables'].get('cols_df2_excl_set') == cols_df2_excl_set
    assert equality_metadata['variables'].get('cols_df1_dups_dict') == {}
    assert equality_metadata['variables'].get('cols_df2_dups_dict') == {}
    assert equality_metadata['variables'].get('cols_df1_dups_common_dict') == {}
    assert equality_metadata['variables'].get('cols_df2_dups_common_dict') == {}


def test_idxs_review() -> None:
    bdf = BaseDF()
    df1_idx_set = set(bdf.df1.index)
    df2_idx_set = set(bdf.df2_index_plus1.index)
    idxs_common_set = df1_idx_set.intersection(df2_idx_set)
    idxs_df1_excl_set = df1_idx_set - idxs_common_set
    idxs_df2_excl_set = df2_idx_set - idxs_common_set

    compare_lists_ret_show_common = pd_compare.compare_lists(
        list_1=list(bdf.df1.index),
        list_2=list(bdf.df2_index_plus1.index),
        show_common_items=True,
        list_1_name='df1',
        list_2_name='df2',
        type_name='index',
        type_name_plural='indexes',
    )
    compare_lists_ret_no_show_common = pd_compare.compare_lists(
        list_1=list(bdf.df1.index),
        list_2=list(bdf.df2_index_plus1.index),
        show_common_items=False,
        list_1_name='df1',
        list_2_name='df2',
        type_name='index',
        type_name_plural='indexes',
    )

    # Index metadata returned showing common indexes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_index_plus1,
        show_common_idxs=True,
        report_print=True,
    )
    io_predicted_printed_substr = compare_lists_ret_show_common[1]['report']
    equality_metadata = returned[2]
    assert returned[0] is False
    assert io_predicted_printed_substr in io_out
    assert io_predicted_printed_substr in equality_metadata.get('report')
    assert equality_metadata['variables'].get('idxs_common_set') == idxs_common_set
    assert equality_metadata['variables'].get('idxs_df1_excl_set') == idxs_df1_excl_set
    assert equality_metadata['variables'].get('idxs_df2_excl_set') == idxs_df2_excl_set
    assert equality_metadata['variables'].get('idxs_df1_dups_dict') == {}
    assert equality_metadata['variables'].get('idxs_df2_dups_dict') == {}
    assert equality_metadata['variables'].get('idxs_df1_dups_common_dict') == {}
    assert equality_metadata['variables'].get('idxs_df2_dups_common_dict') == {}

    # Index metadata returned NOT showing common indexes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_index_plus1,
        show_common_idxs=False,
        report_print=True,
    )
    equality_metadata = returned[2]
    assert returned[0] is False
    assert compare_lists_ret_show_common[1]['report'] not in io_out
    assert compare_lists_ret_no_show_common[1]['report'] in equality_metadata.get('report')
    assert compare_lists_ret_show_common[1]['report'] not in equality_metadata.get('report')
    assert equality_metadata['variables'].get('idxs_common_set') == idxs_common_set
    assert equality_metadata['variables'].get('idxs_df1_excl_set') == idxs_df1_excl_set
    assert equality_metadata['variables'].get('idxs_df2_excl_set') == idxs_df2_excl_set
    assert equality_metadata['variables'].get('idxs_df1_dups_dict') == {}
    assert equality_metadata['variables'].get('idxs_df2_dups_dict') == {}
    assert equality_metadata['variables'].get('idxs_df1_dups_common_dict') == {}
    assert equality_metadata['variables'].get('idxs_df2_dups_common_dict') == {}


def test_cols_idxs_report_and_compare() -> None:
    bdf = BaseDF()
    predicted_title = _return_print_title(1, 'Checking common columns and indexes')

    # All columns and indexes are common, checking report portion
    # ************************************
    report_portion_predicted = predicted_title
    report_portion_predicted += _return_print_event(
        1, '✅ Columns and indexes are equal in the two DataFrames'
    )
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        show_common_idxs=False,
        report_print=True,
    )
    assert report_portion_predicted in io_out

    # Not all columns and indexes are common, common cols/idxs are equal
    # checking report portion and return
    # ************************************
    report_portion_predicted = predicted_title
    report_portion_predicted += _return_print_event(
        1, '😓 Columns and indexes are not equal in the two DataFrames'
    )
    report_portion_predicted += _return_print_event(
        1, '😈 From this point on, comparing only common columns and indexes'
    )
    report_portion_predicted += _return_print_title(
        1, 'Equality check', 'for common columns and indexes'
    )
    report_portion_predicted += _return_print_result('🥳 Equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col,
        show_common_idxs=False,
        report_print=True,
    )
    assert report_portion_predicted in io_out
    assert returned[0] is False
    assert returned[1] is True

    # Not all columns and indexes are common, common cols/idxs are different
    # checking report portion and return
    # ************************************
    report_portion_predicted = predicted_title
    report_portion_predicted += _return_print_event(
        1, '😓 Columns and indexes are not equal in the two DataFrames'
    )
    report_portion_predicted += _return_print_event(
        1, '😈 From this point on, comparing only common columns and indexes'
    )
    report_portion_predicted += _return_print_title(
        1, 'Equality check', 'for common columns and indexes'
    )
    report_portion_predicted += _return_print_result('😡 Not equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_extra_col_diff_values,
        show_common_idxs=False,
        report_print=True,
    )
    assert report_portion_predicted in io_out
    assert returned[0] is False


def test_dtypes_equal_review() -> None:
    bdf = BaseDF()

    predicted_dtypes_df = pd.DataFrame(
        {
            'different': [False, False, False, False, False],
            'df1': ['float64', 'int64', 'float64', 'object', 'object'],
            'df2': ['float64', 'int64', 'float64', 'object', 'object'],
        },
        index=['col_float', 'col_int', 'col_nan', 'col_str', 'col_strnan'],
    )

    # Different columns, some common, different values
    # Equal dtypes, w report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col_diff_values,
        show_all_dtypes=True,
        report_print=True,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2,
        df1_name='df1',
        df2_name='df2',
        show_all_dtypes=True,
    )
    assert returned[0] is False
    assert compare_dtypes_ret[1]['report'] in io_out
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['variables']['common_cols_dtypes_equality'] is True
    assert returned[2]['variables']['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Different columns, some common, different values
    # Equal dtypes, w report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col_diff_values,
        show_all_dtypes=False,
        report_print=True,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2,
        df1_name='df1',
        df2_name='df2',
        show_all_dtypes=False,
    )
    assert returned[0] is False
    assert compare_dtypes_ret[1]['report'] in io_out
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['variables']['common_cols_dtypes_equality'] is True
    assert returned[2]['variables']['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Different columns, some common, different values
    # Equal dtypes, no report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col_diff_values,
        show_all_dtypes=True,
        report_print=False,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2,
        df1_name='df1',
        df2_name='df2',
        show_all_dtypes=True,
    )
    assert returned[0] is False
    assert io_out == ''
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['variables']['common_cols_dtypes_equality'] is True
    assert returned[2]['variables']['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Different columns, some common, different values
    # Equal dtypes, no report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col_diff_values,
        show_all_dtypes=False,
        report_print=False,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2,
        df1_name='df1',
        df2_name='df2',
        show_all_dtypes=False,
    )
    assert returned[0] is False
    assert io_out == ''
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['variables']['common_cols_dtypes_equality'] is True
    assert returned[2]['variables']['common_cols_dtypes_df'].equals(predicted_dtypes_df)


def test_dtypes_diff_review() -> None:
    bdf = BaseDF()

    predicted_dtypes_df = pd.DataFrame(
        {
            'different': [True, True, True, False, False],
            'df1': ['float64', 'int64', 'float64', 'object', 'object'],
            'df2': ['object', 'object', 'object', 'object', 'object'],
        },
        index=['col_float', 'col_int', 'col_nan', 'col_str', 'col_strnan'],
    )

    # Same columns, different dtypes, w report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        show_all_dtypes=True,
        report_print=True,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2_as_object,
        df1_name='df1',
        df2_name='df2',
        show_all_dtypes=True,
    )
    assert returned[0] is False
    assert compare_dtypes_ret[1]['report'] in io_out
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['variables']['common_cols_dtypes_equality'] is False
    assert returned[2]['variables']['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Same columns, different dtypes, w report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        show_all_dtypes=False,
        report_print=True,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2_as_object,
        df1_name='df1',
        df2_name='df2',
        show_all_dtypes=False,
    )
    assert returned[0] is False
    assert compare_dtypes_ret[1]['report'] in io_out
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['variables']['common_cols_dtypes_equality'] is False
    assert returned[2]['variables']['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Same columns, different dtypes, no report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        show_all_dtypes=True,
        report_print=False,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2_as_object,
        df1_name='df1',
        df2_name='df2',
        show_all_dtypes=True,
    )
    assert returned[0] is False
    assert io_out == ''
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['variables']['common_cols_dtypes_equality'] is False
    assert returned[2]['variables']['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Same columns, different dtypes, no report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        show_all_dtypes=False,
        report_print=False,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2_as_object,
        df1_name='df1',
        df2_name='df2',
        show_all_dtypes=False,
    )
    assert returned[0] is False
    assert io_out == ''
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['variables']['common_cols_dtypes_equality'] is False
    assert returned[2]['variables']['common_cols_dtypes_df'].equals(predicted_dtypes_df)


def test_dtypes_simplification():
    bdf = BaseDF()

    # Same columns, same dtypes, report, no simplification tried
    # ************************************
    wrong_predicted_io = _return_print_title(1, 'Since dtypes are different, will try to simplify')
    wrong_predicted_io += _return_print_title(1, 'Trying to simplify dtypes')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_diff_values,
        show_all_dtypes=False,
        report_print=True,
    )
    assert wrong_predicted_io not in io_out
    assert wrong_predicted_io not in returned[2]['report']

    # Same columns, same dtypes, no report, no simplification tried
    # ************************************
    wrong_predicted_io = _return_print_title(1, 'Since dtypes are different, will try to simplify')
    wrong_predicted_io += _return_print_title(1, 'Trying to simplify dtypes')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_diff_values,
        show_all_dtypes=False,
        report_print=False,
    )
    assert '' == io_out
    assert wrong_predicted_io not in returned[2]['report']

    # Same columns, different dtypes, report, not show_all_dtypes, simplification tried, equality
    # ************************************
    predicted_io = _return_print_title(1, 'Since dtypes are different, will try to simplify')
    predicted_io += _return_print_title(1, 'Trying to simplify dtypes')
    predicted_io += _return_print_event(1, '✅ first_df... already simplified')
    predicted_io += _return_print_event(1, '😓 second_df... simplified')
    predicted_io += _return_print_event(1, '😓 dtypes changed')

    _, dtypes_metadata = pd_compare.compare_dtypes(
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=False,
    )

    predicted_io += dtypes_metadata['report']
    predicted_io += _return_print_title(1, 'Equality check', 'since dtypes are now equal')
    predicted_io += _return_print_result('🥳 Equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=True,
    )
    assert returned[0] is False
    assert returned[1] is True
    assert predicted_io in io_out
    assert predicted_io in returned[2]['report']

    # Same columns, different dtypes, report, show_all_dtypes, simplification tried, equality
    # ************************************
    predicted_io = _return_print_title(1, 'Since dtypes are different, will try to simplify')
    predicted_io += _return_print_title(1, 'Trying to simplify dtypes')
    predicted_io += _return_print_event(1, '✅ first_df... already simplified')
    predicted_io += _return_print_event(1, '😓 second_df... simplified')
    predicted_io += _return_print_event(1, '😓 dtypes changed')

    _, dtypes_metadata = pd_compare.compare_dtypes(
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=True,
        report_print=False,
    )

    predicted_io += dtypes_metadata['report']
    predicted_io += _return_print_title(1, 'Equality check', 'since dtypes are now equal')
    predicted_io += _return_print_result('🥳 Equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=True,
        report_print=True,
    )
    assert returned[0] is False
    assert returned[1] is True
    assert predicted_io in io_out
    assert predicted_io in returned[2]['report']

    # Same columns, different dtypes, no report, not show_all_dtypes, simplification tried, equality
    # ************************************
    predicted_io = _return_print_title(1, 'Since dtypes are different, will try to simplify')
    predicted_io += _return_print_title(1, 'Trying to simplify dtypes')
    predicted_io += _return_print_event(1, '✅ first_df... already simplified')
    predicted_io += _return_print_event(1, '😓 second_df... simplified')
    predicted_io += _return_print_event(1, '😓 dtypes changed')

    _, dtypes_metadata = pd_compare.compare_dtypes(
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=False,
    )

    predicted_io += dtypes_metadata['report']
    predicted_io += _return_print_title(1, 'Equality check', 'since dtypes are now equal')
    predicted_io += _return_print_result('🥳 Equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=False,
    )
    assert returned[0] is False
    assert returned[1] is True
    assert '' == io_out
    assert predicted_io in returned[2]['report']

    # Same columns, different dtypes, no report, show_all_dtypes, simplification tried, equality
    # ************************************
    predicted_io = _return_print_title(1, 'Since dtypes are different, will try to simplify')
    predicted_io += _return_print_title(1, 'Trying to simplify dtypes')
    predicted_io += _return_print_event(1, '✅ first_df... already simplified')
    predicted_io += _return_print_event(1, '😓 second_df... simplified')
    predicted_io += _return_print_event(1, '😓 dtypes changed')

    _, dtypes_metadata = pd_compare.compare_dtypes(
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=True,
        report_print=False,
    )

    predicted_io += dtypes_metadata['report']
    predicted_io += _return_print_title(1, 'Equality check', 'since dtypes are now equal')
    predicted_io += _return_print_result('🥳 Equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=True,
        report_print=False,
    )
    assert returned[0] is False
    assert returned[1] is True
    assert '' == io_out
    assert predicted_io in returned[2]['report']

    # Same columns, different dtypes, report, not show_all_dtypes, simplification tried, not equality
    # ************************************
    predicted_io = _return_print_title(1, 'Since dtypes are different, will try to simplify')
    predicted_io += _return_print_title(1, 'Trying to simplify dtypes')
    predicted_io += _return_print_event(1, '✅ first_df... already simplified')
    predicted_io += _return_print_event(1, '😓 second_df... simplified')
    predicted_io += _return_print_event(1, '😓 dtypes changed')

    _, dtypes_metadata = pd_compare.compare_dtypes(
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=False,
    )

    predicted_io += dtypes_metadata['report']
    predicted_io += _return_print_title(1, 'Equality check', 'since dtypes are now equal')
    predicted_io += _return_print_result('😡 Not equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=True,
    )
    assert returned[0] is False
    assert predicted_io in io_out
    assert predicted_io in returned[2]['report']

    # Same columns, different dtypes, report, show_all_dtypes, simplification tried, not equality
    # ************************************
    predicted_io = _return_print_title(1, 'Since dtypes are different, will try to simplify')
    predicted_io += _return_print_title(1, 'Trying to simplify dtypes')
    predicted_io += _return_print_event(1, '✅ first_df... already simplified')
    predicted_io += _return_print_event(1, '😓 second_df... simplified')
    predicted_io += _return_print_event(1, '😓 dtypes changed')

    _, dtypes_metadata = pd_compare.compare_dtypes(
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=False,
    )

    predicted_io += dtypes_metadata['report']
    predicted_io += _return_print_title(1, 'Equality check', 'since dtypes are now equal')
    predicted_io += _return_print_result('😡 Not equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=True,
    )
    assert returned[0] is False
    assert predicted_io in io_out
    assert predicted_io in returned[2]['report']

    # Same columns, different dtypes, no report, not show_all_dtypes, simplification tried, not equality
    # ************************************
    predicted_io = _return_print_title(1, 'Since dtypes are different, will try to simplify')
    predicted_io += _return_print_title(1, 'Trying to simplify dtypes')
    predicted_io += _return_print_event(1, '✅ first_df... already simplified')
    predicted_io += _return_print_event(1, '😓 second_df... simplified')
    predicted_io += _return_print_event(1, '😓 dtypes changed')

    _, dtypes_metadata = pd_compare.compare_dtypes(
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=False,
    )

    predicted_io += dtypes_metadata['report']
    predicted_io += _return_print_title(1, 'Equality check', 'since dtypes are now equal')
    predicted_io += _return_print_result('😡 Not equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=False,
    )
    assert returned[0] is False
    assert '' == io_out
    assert predicted_io in returned[2]['report']

    # Same columns, different dtypes, no report, show_all_dtypes, simplification tried, not equality
    # ************************************
    predicted_io = _return_print_title(1, 'Since dtypes are different, will try to simplify')
    predicted_io += _return_print_title(1, 'Trying to simplify dtypes')
    predicted_io += _return_print_event(1, '✅ first_df... already simplified')
    predicted_io += _return_print_event(1, '😓 second_df... simplified')
    predicted_io += _return_print_event(1, '😓 dtypes changed')

    _, dtypes_metadata = pd_compare.compare_dtypes(
        df1=bdf.df1,
        df2=bdf.df2,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=False,
    )

    predicted_io += dtypes_metadata['report']
    predicted_io += _return_print_title(1, 'Equality check', 'since dtypes are now equal')
    predicted_io += _return_print_result('😡 Not equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        show_all_dtypes=False,
        report_print=False,
    )
    assert returned[0] is False
    assert '' == io_out
    assert predicted_io in returned[2]['report']


def test_round_to_report():
    bdf = BaseDF()

    # round_to=0, report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        round_to=0,
        show_all_dtypes=False,
        report_print=True,
    )
    predicted_io = _return_print_title(1, 'Rounding [round_to=0]')
    assert predicted_io in io_out
    assert predicted_io in returned[2]['report']

    # round_to='ceil', report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        round_to='ceil',
        show_all_dtypes=False,
        report_print=True,
    )
    predicted_io = _return_print_title(1, 'Rounding [round_to=ceil]')
    assert predicted_io in io_out
    assert predicted_io in returned[2]['report']

    # round_to='floor', report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        round_to='floor',
        show_all_dtypes=False,
        report_print=True,
    )
    predicted_io = _return_print_title(1, 'Rounding [round_to=floor]')
    assert predicted_io in io_out
    assert predicted_io in returned[2]['report']

    # round_to=0, report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        round_to=0,
        show_all_dtypes=False,
        report_print=False,
    )
    predicted_io = _return_print_title(1, 'Rounding [round_to=0]')
    assert '' == io_out
    assert predicted_io in returned[2]['report']

    # round_to='ceil', report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        round_to='ceil',
        show_all_dtypes=False,
        report_print=False,
    )
    predicted_io = _return_print_title(1, 'Rounding [round_to=ceil]')
    assert '' == io_out
    assert predicted_io in returned[2]['report']

    # round_to='floor', report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        round_to='floor',
        show_all_dtypes=False,
        report_print=False,
    )
    predicted_io = _return_print_title(1, 'Rounding [round_to=floor]')
    assert '' == io_out
    assert predicted_io in returned[2]['report']


def test_compare_values_report():
    bdf = BaseDF()

    predicted_io = _return_print_title(
        1,
        'Comparing values',
        'from this point on, the DataFrames must have at least one different cell',
    )
    predicted_io += _return_print_event(1, '😓 Not equal columns (count=4):')
    predicted_io += _return_pprint(1, ['col_float', 'col_int', 'col_str', 'col_strnan'])
    predicted_io += _return_print_event(1, '😓 Not equal rows (count=3):')
    predicted_io += _return_pprint(1, [0, 1, 2])

    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        round_to=None,
        report_print=True,
        show_common_cols=False,
        show_common_idxs=False,
        show_all_dtypes=False,
        xls_path=None,
        xls_overwrite=False,
        xls_compare_str_equal='',
        xls_compare_str_diff='*_diff_*',
        xls_fixed_cols=None,
        xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
    )
    assert predicted_io in io_out
    assert predicted_io in returned[2]['report']


def test_after_compare_values_metadata():
    bdf = BaseDF()
    expected_eqlty_df = pd.DataFrame(
        {
            'col_float': [False, False, False, True],
            'col_int': [False, False, False, True],
            'col_nan': [True, True, True, True],
            'col_str': [False, False, False, True],
            'col_strnan': [False, False, False, True],
        }
    )
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_diff_values,
        df1_name=bdf.df1_name,
        df2_name=bdf.df2_name,
        round_to=None,
        report_print=True,
        show_common_cols=False,
        show_common_idxs=False,
        show_all_dtypes=False,
        xls_path=None,
        xls_overwrite=False,
        xls_compare_str_equal='',
        xls_compare_str_diff='*_diff_*',
        xls_fixed_cols=None,
        xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
    )
    metadata = returned[2]
    # Equality check
    assert str(expected_eqlty_df) == str(metadata['variables']['equality_df'])
    assert expected_eqlty_df.equals(metadata['variables']['equality_df'])

    # Equal columns/rows check
    assert ['col_nan'] == metadata['variables']['cols_equal_list_sorted']
    assert [3] == metadata['variables']['rows_equal_list_sorted']

    # Different columns/rows check
    assert ['col_float', 'col_int', 'col_str', 'col_strnan'] == metadata['variables']['cols_diff_list_sorted']
    assert [0, 1, 2] == metadata['variables']['rows_diff_list_sorted']

    # Expected joined_df
    _df1 = bdf.df1
    _df2 = bdf.df2_diff_values
    tuples = list(
        zip(
            [
                *(['col_float'] * 3),
                *(['col_int'] * 3),
                *(['col_nan'] * 3),
                *(['col_str'] * 3),
                *(['col_strnan'] * 3),
            ],
            ['first_df', 'second_df', 'different'] * 5,
        )
    )
    multi_index = pd.MultiIndex.from_tuples(tuples)

    data = []
    for i in range(4):
        data_row = []
        for col_name in ['col_float', 'col_int', 'col_nan', 'col_str', 'col_strnan']:
            data_row.append(_df1.loc[i, col_name])
            data_row.append(_df2.loc[i, col_name])
            data_row.append(~expected_eqlty_df.loc[i, col_name])  # Toggle bools with '~' (tilde)
        data.append(data_row)
    expected_joined_df = pd.DataFrame(data, columns=multi_index)

    assert str(expected_joined_df) == str(metadata['variables']['joined_df'])
    assert expected_joined_df.equals(metadata['variables']['joined_df'])
