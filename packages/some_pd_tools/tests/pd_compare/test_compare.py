import re

import pandas as pd

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


def test_equality_full() -> None:
    bdf = BaseDF()

    report_predicted = _return_print_title(1, 'Equality', 'complete')
    report_predicted += _return_print_result('🥳 Equal')

    # Equal DataFrames
    # ************************************
    # IMPORTANT: Using `df1 = bdf.df1` (same with df2) to use it later to reference the same object
    # because `bdf.df1` always creates a copy to avoid changing the internal `df1`
    df1 = bdf.df1
    df2 = bdf.df2
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1,
        df2,
        bdf.df1_name,
        bdf.df2_name,
    )
    equality_metadata_predicted = {
        'params': {
            'df1': df1,
            'df2': df2,
            'df1_name': bdf.df1_name,
            'df2_name': bdf.df2_name,
            'show_common_cols': False,
            'show_common_idxs': False,
            'int64_to_float64': False,
            'round_to_decimals': False,
            'astype_str': False,
            'path': None,
            'fixed_cols': [],
            'report': True,
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
        df1,
        df2,
        bdf.df1_name,
        bdf.df2_name,
    )
    equality_metadata_predicted = {
        'params': {
            'df1': df1,
            'df2': df2,
            'df1_name': bdf.df1_name,
            'df2_name': bdf.df2_name,
            'show_common_cols': False,
            'show_common_idxs': False,
            'int64_to_float64': False,
            'round_to_decimals': False,
            'astype_str': False,
            'path': None,
            'fixed_cols': [],
            'report': True,
        },
        'report': report_predicted,
    }
    assert returned[0] is True
    assert returned[1] is True
    assert returned[2] == equality_metadata_predicted
    assert io_out == report_predicted

    # Equal Indexes, equal Dataframes, all duplicated (two instances of each)
    # This only works because `df1_cp.equals(df2_cp)` is True in the beginning
    # This assumes there are no column duplicates (checked previously)
    # ************************************
    df1 = bdf.df1[[*bdf.df1.columns, *bdf.df1.columns]]
    df2 = bdf.df2[[*bdf.df2.columns, *bdf.df2.columns]]
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        df1,
        df2,
        bdf.df1_name,
        bdf.df2_name,
    )
    equality_metadata_predicted = {
        'params': {
            'df1': df1,
            'df2': df2,
            'df1_name': bdf.df1_name,
            'df2_name': bdf.df2_name,
            'show_common_cols': False,
            'show_common_idxs': False,
            'int64_to_float64': False,
            'round_to_decimals': False,
            'astype_str': False,
            'path': None,
            'fixed_cols': [],
            'report': True,
        },
        'report': report_predicted,
    }
    assert returned[0] is True
    assert returned[1] is True
    assert returned[2] == equality_metadata_predicted
    assert io_out == report_predicted


def test_not_equality_first_lines() -> None:
    bdf = BaseDF()

    report_predicted = _return_print_title(1, 'Equality', 'complete')
    report_predicted += _return_print_result('😡 Not equal')

    # Different columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col,
        bdf.df2_extra_col,
        bdf.df1_name,
        bdf.df2_name,
    )
    first_lines_not_equal = re.search('.*\n.*\n.*\n.*\n', io_out).group(0)
    assert returned[0] is False
    assert report_predicted == first_lines_not_equal

    # Different types
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_as_object,  # As object dtype
        bdf.df2,
        bdf.df1_name,
        bdf.df2_name,
    )
    first_lines_not_equal = re.search('.*\n.*\n.*\n.*\n', io_out).group(0)
    assert returned[0] is False
    assert report_predicted == first_lines_not_equal

    # Different indexes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2.drop(0),  # Drop first line
        bdf.df1_name,
        bdf.df2_name,
    )
    first_lines_not_equal = re.search('.*\n.*\n.*\n.*\n', io_out).group(0)
    assert returned[0] is False
    assert report_predicted == first_lines_not_equal

    # Different values
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        # Change the order and reset index
        bdf.df2.sort_index(ascending=False).reset_index(drop=True),
        bdf.df1_name,
        bdf.df2_name,
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
        bdf.df1_extra_col[[*bdf.df1_extra_col.columns, *bdf.df1_extra_col.columns]],
        bdf.df2_extra_col[[*bdf.df2_extra_col.columns, *bdf.df2_extra_col.columns]],
        bdf.df1_name,
        bdf.df2_name,
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
    assert equality_metadata.get('error') == _return_print_event(1, error)

    # Extra Columns, all duplicated (two instances df1, three instances of df2)
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col[[*bdf.df1_extra_col.columns, *bdf.df1_extra_col.columns]],
        bdf.df2_extra_col[
            [*bdf.df2_extra_col.columns, *bdf.df2_extra_col.columns, *bdf.df2_extra_col.columns]
        ],
        bdf.df1_name,
        bdf.df2_name,
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
        bdf.df1.loc[[0, 1, 2, 0, 1, 2]],
        bdf.df2.loc[[1, 2, 3, 1, 2, 3]],
        bdf.df1_name,
        bdf.df2_name,
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
        bdf.df1.loc[[0, 1, 2, 0, 1, 2]],
        bdf.df2.loc[[1, 2, 3, 1, 2, 3, 1, 2, 3]],
        bdf.df1_name,
        bdf.df2_name,
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
    df1_colset = set(bdf.df1_extra_col.columns)
    df2_colset = set(bdf.df2_extra_col.columns)
    cols_common_set = df1_colset.intersection(df2_colset)
    cols_common_list = sorted(list(cols_common_set))
    cols_df1_excl_set = df1_colset - cols_common_set
    cols_df2_excl_set = df2_colset - cols_common_set

    io_cols_common_title = _return_print_title(
        1,
        'Columns present in both DataFrames (intersection)',
    )

    # Column metadata returned showing common columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col,
        bdf.df2_extra_col,
        show_common_cols=True,
        report=True,
    )
    compare_lists_ret = pd_compare.compare_lists(
        list_1=list(bdf.df1_extra_col.columns),
        list_2=list(bdf.df2_extra_col.columns),
        list_1_name='df1',
        list_2_name='df2',
        type_name='column',
        type_name_plural='columns',
    )
    io_predicted_printed_substr = compare_lists_ret[1]['report']
    io_predicted_printed_substr += io_cols_common_title
    io_predicted_printed_substr += _return_pprint(1, cols_common_list)
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
        bdf.df1_extra_col,
        bdf.df2_extra_col,
        show_common_cols=False,
        report=True,
    )
    io_predicted_notprinted_substr = compare_lists_ret[1]['report']
    io_predicted_notprinted_substr += io_cols_common_title
    io_predicted_notprinted_substr += _return_pprint(1, cols_common_list)
    equality_metadata = returned[2]
    assert returned[0] is False
    assert io_predicted_notprinted_substr not in io_out
    assert compare_lists_ret[1]['report'] in equality_metadata.get('report')
    assert io_predicted_notprinted_substr not in equality_metadata.get('report')
    assert equality_metadata.get('cols_common_set') == cols_common_set
    assert equality_metadata.get('cols_df1_excl_set') == cols_df1_excl_set
    assert equality_metadata.get('cols_df2_excl_set') == cols_df2_excl_set
    assert equality_metadata.get('cols_df1_dups_dict') == {}
    assert equality_metadata.get('cols_df2_dups_dict') == {}
    assert equality_metadata.get('cols_df1_dups_common_dict') == {}
    assert equality_metadata.get('cols_df2_dups_common_dict') == {}


def test_idxs_review() -> None:
    bdf = BaseDF()
    df1_idxset = set(bdf.df1.index)
    df2_idxset = set(bdf.df2_index_plus1.index)
    idxs_common_set = df1_idxset.intersection(df2_idxset)
    idxs_common_list = sorted(list(idxs_common_set))
    idxs_df1_excl_set = df1_idxset - idxs_common_set
    idxs_df2_excl_set = df2_idxset - idxs_common_set

    io_idxs_common_title = _return_print_title(
        1,
        'Indexes present in both DataFrames (intersection)',
    )

    # Index metadata returned showing common indexes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2_index_plus1,
        show_common_idxs=True,
        report=True,
    )
    compare_lists_ret = pd_compare.compare_lists(
        list_1=list(bdf.df1.index),
        list_2=list(bdf.df2_index_plus1.index),
        list_1_name='df1',
        list_2_name='df2',
        type_name='index',
        type_name_plural='indexes',
    )
    io_predicted_printed_substr = compare_lists_ret[1]['report']
    io_predicted_printed_substr += io_idxs_common_title
    io_predicted_printed_substr += _return_pprint(1, idxs_common_list)
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
        bdf.df1,
        bdf.df2_index_plus1,
        show_common_idxs=False,
        report=True,
    )
    compare_lists_ret = pd_compare.compare_lists(
        list_1=list(bdf.df1.index),
        list_2=list(bdf.df2_index_plus1.index),
        list_1_name='df1',
        list_2_name='df2',
        type_name='index',
        type_name_plural='indexes',
    )
    io_predicted_notprinted_substr = compare_lists_ret[1]['report']
    io_predicted_notprinted_substr += io_idxs_common_title
    io_predicted_notprinted_substr += _return_pprint(1, idxs_common_list)
    equality_metadata = returned[2]
    assert returned[0] is False
    assert io_predicted_notprinted_substr not in io_out
    assert compare_lists_ret[1]['report'] in equality_metadata.get('report')
    assert io_predicted_notprinted_substr not in equality_metadata.get('report')
    assert equality_metadata.get('idxs_common_set') == idxs_common_set
    assert equality_metadata.get('idxs_df1_excl_set') == idxs_df1_excl_set
    assert equality_metadata.get('idxs_df2_excl_set') == idxs_df2_excl_set
    assert equality_metadata.get('idxs_df1_dups_dict') == {}
    assert equality_metadata.get('idxs_df2_dups_dict') == {}
    assert equality_metadata.get('idxs_df1_dups_common_dict') == {}
    assert equality_metadata.get('idxs_df2_dups_common_dict') == {}


def test_cols_idxs_report_and_compare() -> None:
    bdf = BaseDF()
    predicted_title = _return_print_title(1, 'Common columns and indexes')

    # All columns and indexes are common, checking report portion
    # ************************************
    report_portion_predicted = predicted_title
    report_portion_predicted += _return_print_event(1, '✅ All columns and indexes are common')
    report_portion_predicted += _return_print_event(
        1, 'No equality check needed (same as "Equality, complete")'
    )
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2_as_object,
        show_common_idxs=False,
        report=True,
    )
    assert report_portion_predicted in io_out

    # Not all columns and indexes are common, common cols/idxs are equal
    # checking report portion and return
    # ************************************
    report_portion_predicted = predicted_title
    report_portion_predicted += _return_print_event(1, '😓 Not all columns and indexes are common')
    report_portion_predicted += _return_print_event(1, 'Equality check needed')
    report_portion_predicted += _return_print_title(
        1, 'Equality', 'comparing common columns and indexes'
    )
    report_portion_predicted += _return_print_result('🥳 Equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col,
        bdf.df2_extra_col,
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
    report_portion_predicted += _return_print_event(1, '😓 Not all columns and indexes are common')
    report_portion_predicted += _return_print_event(1, 'Equality check needed')
    report_portion_predicted += _return_print_title(
        1, 'Equality', 'comparing common columns and indexes'
    )
    report_portion_predicted += _return_print_result('😡 Not equal')
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2_extra_col_diff_values,
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
        bdf.df1_extra_col,
        bdf.df2_extra_col_diff_values,
        show_common_dtypes=True,
        report=True,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2,
        df1_name='df1',
        df2_name='df2',
        show_common_dtypes=True,
    )
    assert returned[0] is False
    assert compare_dtypes_ret[1]['report'] in io_out
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['dtypes_for_common_cols_equal'] is True
    assert returned[2]['dtypes_for_common_cols_df'].equals(predicted_dtypes_df)

    # Different columns, some common, different values
    # Equal dtypes, w report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col,
        bdf.df2_extra_col_diff_values,
        show_common_dtypes=False,
        report=True,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2,
        df1_name='df1',
        df2_name='df2',
        show_common_dtypes=False,
    )
    assert returned[0] is False
    assert compare_dtypes_ret[1]['report'] in io_out
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['dtypes_for_common_cols_equal'] is True
    assert returned[2]['dtypes_for_common_cols_df'].equals(predicted_dtypes_df)

    # Different columns, some common, different values
    # Equal dtypes, no report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col,
        bdf.df2_extra_col_diff_values,
        show_common_dtypes=True,
        report=False,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2,
        df1_name='df1',
        df2_name='df2',
        show_common_dtypes=True,
    )
    assert returned[0] is False
    assert io_out == ''
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['dtypes_for_common_cols_equal'] is True
    assert returned[2]['dtypes_for_common_cols_df'].equals(predicted_dtypes_df)

    # Different columns, some common, different values
    # Equal dtypes, no report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col,
        bdf.df2_extra_col_diff_values,
        show_common_dtypes=False,
        report=False,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2,
        df1_name='df1',
        df2_name='df2',
        show_common_dtypes=False,
    )
    assert returned[0] is False
    assert io_out == ''
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['dtypes_for_common_cols_equal'] is True
    assert returned[2]['dtypes_for_common_cols_df'].equals(predicted_dtypes_df)


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
        bdf.df1,
        bdf.df2_as_object,
        show_common_dtypes=True,
        report=True,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2_as_object,
        df1_name='df1',
        df2_name='df2',
        show_common_dtypes=True,
    )
    assert returned[0] is False
    assert compare_dtypes_ret[1]['report'] in io_out
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['dtypes_for_common_cols_equal'] is False
    assert returned[2]['dtypes_for_common_cols_df'].equals(predicted_dtypes_df)

    # Same columns, different dtypes, w report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2_as_object,
        show_common_dtypes=False,
        report=True,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2_as_object,
        df1_name='df1',
        df2_name='df2',
        show_common_dtypes=False,
    )
    assert returned[0] is False
    assert compare_dtypes_ret[1]['report'] in io_out
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['dtypes_for_common_cols_equal'] is False
    assert returned[2]['dtypes_for_common_cols_df'].equals(predicted_dtypes_df)

    # Same columns, different dtypes, no report, w show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2_as_object,
        show_common_dtypes=True,
        report=False,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2_as_object,
        df1_name='df1',
        df2_name='df2',
        show_common_dtypes=True,
    )
    assert returned[0] is False
    assert io_out == ''
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['dtypes_for_common_cols_equal'] is False
    assert returned[2]['dtypes_for_common_cols_df'].equals(predicted_dtypes_df)

    # Same columns, different dtypes, no report, no show common dtypes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2_as_object,
        show_common_dtypes=False,
        report=False,
    )
    compare_dtypes_ret = pd_compare.compare_dtypes(
        bdf.df1,
        bdf.df2_as_object,
        df1_name='df1',
        df2_name='df2',
        show_common_dtypes=False,
    )
    assert returned[0] is False
    assert io_out == ''
    assert compare_dtypes_ret[1]['report'] in returned[2]['report']
    assert returned[2]['dtypes_for_common_cols_equal'] is False
    assert returned[2]['dtypes_for_common_cols_df'].equals(predicted_dtypes_df)
