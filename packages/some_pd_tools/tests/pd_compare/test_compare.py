import re

import pandas as pd
import pytest

from some_pd_tools import pd_compare

from ..basedf import BaseDF
from ..formatting import (
    _fn_ret_and_output,
    # _return_pprint,
    _return_print_event,
    # _return_print_plain,
    _return_print_result,
    _return_print_title,
    # _sorted,
)


def test_exceptions():
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


def test_equality_full() -> None:
    bdf = BaseDF()

    report_predicted = _return_print_title(1, 'Equality check', 'full')
    report_predicted += _return_print_result('🥳 Equal')

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
            'report': True,
            'show_common_cols': False,
            'show_common_idxs': False,
            'show_all_dtypes': False,
            'path': None,
            'fixed_cols': [],
        },
        'report': report_predicted,
    }
    assert returned[0] is True
    assert returned[1] is True
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
            'report': True,
            'show_common_cols': False,
            'show_common_idxs': False,
            'show_all_dtypes': False,
            'path': None,
            'fixed_cols': [],
        },
        'report': report_predicted,
    }
    assert returned[0] is True
    assert returned[1] is True
    assert returned[2] == equality_metadata_predicted
    assert io_out == report_predicted

    # Equal Indexes, equal DataFrames, all duplicated (two instances of each)
    # This only works because `df1_cp.equals(df2_cp)` is True in the beginning
    # This assumes there are no column duplicates (checked previously)
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
            'report': True,
            'show_common_cols': False,
            'show_common_idxs': False,
            'show_all_dtypes': False,
            'path': None,
            'fixed_cols': [],
        },
        'report': report_predicted,
    }
    assert returned[0] is True
    assert returned[1] is True
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
    assert equality_metadata.get('cols_common_set') == set(bdf.df1.columns)
    assert equality_metadata.get('cols_df1_excl_set') == set(bdf.df1_extra_col.columns) - set(
        bdf.df1.columns
    )
    assert equality_metadata.get('cols_df2_excl_set') == set(bdf.df2_extra_col.columns) - set(
        bdf.df2.columns
    )
    assert equality_metadata.get('cols_df1_dups_dict') == {
        col: 2 for col in bdf.df1_extra_col.columns
    }
    assert equality_metadata.get('cols_df2_dups_dict') == {
        col: 2 for col in bdf.df2_extra_col.columns
    }
    assert equality_metadata.get('cols_df1_dups_common_dict') == {col: 2 for col in bdf.df1.columns}
    assert equality_metadata.get('cols_df2_dups_common_dict') == {col: 2 for col in bdf.df2.columns}
    error = '🛑 Duplicate common columns found. Only common non duplicates columns allowed, stopping compare and returning. Either change the columns\' names or compare only one of the duplicates columns at a time. Review the returned metadata (indexes \'cols_df1_dups_common_dict\' and \'cols_df1_dups_common_dict\'.)'
    assert _return_print_event(1, error) in io_out
    assert equality_metadata.get('error') == _return_print_event(1, error)

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
    assert equality_metadata.get('cols_common_set') == set(bdf.df1.columns)
    assert equality_metadata.get('cols_df1_excl_set') == set(bdf.df1_extra_col.columns) - set(
        bdf.df1.columns
    )
    assert equality_metadata.get('cols_df2_excl_set') == set(bdf.df2_extra_col.columns) - set(
        bdf.df2.columns
    )
    assert equality_metadata.get('cols_df1_dups_dict') == {
        col: 2 for col in bdf.df1_extra_col.columns
    }
    assert equality_metadata.get('cols_df2_dups_dict') == {
        col: 3 for col in bdf.df2_extra_col.columns
    }
    assert equality_metadata.get('cols_df1_dups_common_dict') == {col: 2 for col in bdf.df1.columns}
    assert equality_metadata.get('cols_df2_dups_common_dict') == {col: 3 for col in bdf.df2.columns}
    error = '🛑 Duplicate common columns found. Only common non duplicates columns allowed, stopping compare and returning. Either change the columns\' names or compare only one of the duplicates columns at a time. Review the returned metadata (indexes \'cols_df1_dups_common_dict\' and \'cols_df1_dups_common_dict\'.)'
    assert equality_metadata.get('error') == _return_print_event(1, error)

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
    assert equality_metadata.get('cols_common_set') == set(bdf.df1.columns)
    assert equality_metadata.get('cols_df1_excl_set') == set()
    assert equality_metadata.get('cols_df2_excl_set') == set()
    assert equality_metadata.get('cols_df1_dups_dict') == {}
    assert equality_metadata.get('cols_df2_dups_dict') == {}
    assert equality_metadata.get('cols_df1_dups_common_dict') == {}
    assert equality_metadata.get('cols_df2_dups_common_dict') == {}
    assert equality_metadata.get('idxs_common_set') == set([1, 2])
    assert equality_metadata.get('idxs_df1_excl_set') == set([0])
    assert equality_metadata.get('idxs_df2_excl_set') == set([3])
    assert equality_metadata.get('idxs_df1_dups_dict') == {idx: 2 for idx in [0, 1, 2]}
    assert equality_metadata.get('idxs_df2_dups_dict') == {idx: 2 for idx in [1, 2, 3]}
    assert equality_metadata.get('idxs_df1_dups_common_dict') == {idx: 2 for idx in [1, 2]}
    assert equality_metadata.get('idxs_df2_dups_common_dict') == {idx: 2 for idx in [1, 2]}
    error = '🛑 Duplicate common indexes found. Only common non duplicates indexes allowed, stopping compare and returning. Either change the indexes\' names or compare only one of the duplicates indexes at a time. Review the returned metadata (indexes \'idxs_df1_dups_common_dict\' and \'idxs_df1_dups_common_dict\'.)'
    assert equality_metadata.get('error') == _return_print_event(1, error)

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
    assert equality_metadata.get('cols_common_set') == set(bdf.df1.columns)
    assert equality_metadata.get('cols_df1_excl_set') == set()
    assert equality_metadata.get('cols_df2_excl_set') == set()
    assert equality_metadata.get('cols_df1_dups_dict') == {}
    assert equality_metadata.get('cols_df2_dups_dict') == {}
    assert equality_metadata.get('cols_df1_dups_common_dict') == {}
    assert equality_metadata.get('cols_df2_dups_common_dict') == {}
    assert equality_metadata.get('idxs_common_set') == set([1, 2])
    assert equality_metadata.get('idxs_df1_excl_set') == set([0])
    assert equality_metadata.get('idxs_df2_excl_set') == set([3])
    assert equality_metadata.get('idxs_df1_dups_dict') == {idx: 2 for idx in [0, 1, 2]}
    assert equality_metadata.get('idxs_df2_dups_dict') == {idx: 3 for idx in [1, 2, 3]}
    assert equality_metadata.get('idxs_df1_dups_common_dict') == {idx: 2 for idx in [1, 2]}
    assert equality_metadata.get('idxs_df2_dups_common_dict') == {idx: 3 for idx in [1, 2]}
    error = '🛑 Duplicate common indexes found. Only common non duplicates indexes allowed, stopping compare and returning. Either change the indexes\' names or compare only one of the duplicates indexes at a time. Review the returned metadata (indexes \'idxs_df1_dups_common_dict\' and \'idxs_df1_dups_common_dict\'.)'
    assert equality_metadata.get('error') == _return_print_event(1, error)


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
        report=True,
    )
    io_predicted_printed_substr = compare_lists_ret_show_common[1]['report']
    equality_metadata = returned[2]
    assert returned[0] is False
    assert io_predicted_printed_substr in io_out
    assert io_predicted_printed_substr in equality_metadata.get('report')
    assert equality_metadata.get('cols_common_set') == cols_common_set
    assert equality_metadata.get('cols_df1_excl_set') == cols_df1_excl_set
    assert equality_metadata.get('cols_df2_excl_set') == cols_df2_excl_set
    assert equality_metadata.get('cols_df1_dups_dict') == {}
    assert equality_metadata.get('cols_df2_dups_dict') == {}
    assert equality_metadata.get('cols_df1_dups_common_dict') == {}
    assert equality_metadata.get('cols_df2_dups_common_dict') == {}

    # Column metadata returned NOT showing common columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col,
        show_common_cols=False,
        report=True,
    )
    equality_metadata = returned[2]
    assert returned[0] is False
    assert compare_lists_ret_show_common[1]['report'] not in io_out
    assert compare_lists_ret_no_show_common[1]['report'] in equality_metadata.get('report')
    assert compare_lists_ret_show_common[1]['report'] not in equality_metadata.get('report')
    assert equality_metadata.get('cols_common_set') == cols_common_set
    assert equality_metadata.get('cols_df1_excl_set') == cols_df1_excl_set
    assert equality_metadata.get('cols_df2_excl_set') == cols_df2_excl_set
    assert equality_metadata.get('cols_df1_dups_dict') == {}
    assert equality_metadata.get('cols_df2_dups_dict') == {}
    assert equality_metadata.get('cols_df1_dups_common_dict') == {}
    assert equality_metadata.get('cols_df2_dups_common_dict') == {}


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
        report=True,
    )
    io_predicted_printed_substr = compare_lists_ret_show_common[1]['report']
    equality_metadata = returned[2]
    assert returned[0] is False
    assert io_predicted_printed_substr in io_out
    assert io_predicted_printed_substr in equality_metadata.get('report')
    assert equality_metadata.get('idxs_common_set') == idxs_common_set
    assert equality_metadata.get('idxs_df1_excl_set') == idxs_df1_excl_set
    assert equality_metadata.get('idxs_df2_excl_set') == idxs_df2_excl_set
    assert equality_metadata.get('idxs_df1_dups_dict') == {}
    assert equality_metadata.get('idxs_df2_dups_dict') == {}
    assert equality_metadata.get('idxs_df1_dups_common_dict') == {}
    assert equality_metadata.get('idxs_df2_dups_common_dict') == {}

    # Index metadata returned NOT showing common indexes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_index_plus1,
        show_common_idxs=False,
        report=True,
    )
    equality_metadata = returned[2]
    assert returned[0] is False
    assert compare_lists_ret_show_common[1]['report'] not in io_out
    assert compare_lists_ret_no_show_common[1]['report'] in equality_metadata.get('report')
    assert compare_lists_ret_show_common[1]['report'] not in equality_metadata.get('report')
    assert equality_metadata.get('idxs_common_set') == idxs_common_set
    assert equality_metadata.get('idxs_df1_excl_set') == idxs_df1_excl_set
    assert equality_metadata.get('idxs_df2_excl_set') == idxs_df2_excl_set
    assert equality_metadata.get('idxs_df1_dups_dict') == {}
    assert equality_metadata.get('idxs_df2_dups_dict') == {}
    assert equality_metadata.get('idxs_df1_dups_common_dict') == {}
    assert equality_metadata.get('idxs_df2_dups_common_dict') == {}


def test_cols_idxs_report_and_compare() -> None:
    bdf = BaseDF()
    predicted_title = _return_print_title(1, 'Checking common columns and indexes')

    # All columns and indexes are common, checking report portion
    # ************************************
    report_portion_predicted = predicted_title
    report_portion_predicted += _return_print_event(
        1, '✅ Columns and indexes are equal in both DataFrames'
    )
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        show_common_idxs=False,
        report=True,
    )
    assert report_portion_predicted in io_out

    # Not all columns and indexes are common, common cols/idxs are equal
    # checking report portion and return
    # ************************************
    report_portion_predicted = predicted_title
    report_portion_predicted += _return_print_event(
        1, '😓 Columns and indexes are not equal in both DataFrames'
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
        report=True,
    )
    assert report_portion_predicted in io_out
    assert returned[0] is False
    assert returned[1] is True

    # Not all columns and indexes are common, common cols/idxs are different
    # checking report portion and return
    # ************************************
    report_portion_predicted = predicted_title
    report_portion_predicted += _return_print_event(
        1, '😓 Columns and indexes are not equal in both DataFrames'
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
        report=True,
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
        report=True,
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
    assert returned[2]['common_cols_dtypes_equality'] is True
    assert returned[2]['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Different columns, some common, different values
    # Equal dtypes, w report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col_diff_values,
        show_all_dtypes=False,
        report=True,
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
    assert returned[2]['common_cols_dtypes_equality'] is True
    assert returned[2]['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Different columns, some common, different values
    # Equal dtypes, no report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col_diff_values,
        show_all_dtypes=True,
        report=False,
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
    assert returned[2]['common_cols_dtypes_equality'] is True
    assert returned[2]['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Different columns, some common, different values
    # Equal dtypes, no report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1_extra_col,
        df2=bdf.df2_extra_col_diff_values,
        show_all_dtypes=False,
        report=False,
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
    assert returned[2]['common_cols_dtypes_equality'] is True
    assert returned[2]['common_cols_dtypes_df'].equals(predicted_dtypes_df)


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
        report=True,
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
    assert returned[2]['common_cols_dtypes_equality'] is False
    assert returned[2]['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Same columns, different dtypes, w report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        show_all_dtypes=False,
        report=True,
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
    assert returned[2]['common_cols_dtypes_equality'] is False
    assert returned[2]['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Same columns, different dtypes, no report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        show_all_dtypes=True,
        report=False,
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
    assert returned[2]['common_cols_dtypes_equality'] is False
    assert returned[2]['common_cols_dtypes_df'].equals(predicted_dtypes_df)

    # Same columns, different dtypes, no report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1=bdf.df1,
        df2=bdf.df2_as_object,
        show_all_dtypes=False,
        report=False,
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
    assert returned[2]['common_cols_dtypes_equality'] is False
    assert returned[2]['common_cols_dtypes_df'].equals(predicted_dtypes_df)


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
        report=True,
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
        report=False,
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
        report=False,
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
        report=True,
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
        report=False,
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
        report=True,
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
        report=False,
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
        report=False,
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
        report=False,
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
        report=False,
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
        report=False,
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
        report=True,
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
        report=False,
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
        report=True,
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
        report=False,
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
        report=False,
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
        report=False,
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
        report=False,
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
        report=True,
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
        report=True,
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
        report=True,
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
        report=False,
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
        report=False,
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
        report=False,
    )
    predicted_io = _return_print_title(1, 'Rounding [round_to=floor]')
    assert '' == io_out
    assert predicted_io in returned[2]['report']
