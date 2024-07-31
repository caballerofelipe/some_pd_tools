import re


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
        'report': _return_print_result('🥳 Fully equal'),
    }
    assert returned == [True, False, equality_metadata_predicted]
    assert io_out == _return_print_result('🥳 Fully equal')

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
        'report': _return_print_result('🥳 Fully equal'),
    }
    assert returned == [True, False, equality_metadata_predicted]
    assert io_out == _return_print_result('🥳 Fully equal')

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
        'report': _return_print_result('🥳 Fully equal'),
    }
    assert returned == [True, False, equality_metadata_predicted]
    assert io_out == _return_print_result('🥳 Fully equal')


def test_not_equality_first_line_different_columns() -> None:
    # Test wether the first return line when not fully equal is the same.
    bdf = BaseDF()
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col,
        bdf.df2_extra_col,
        bdf.df1_name,
        bdf.df2_name,
    )
    first_line = re.search('.*\n', io_out).group(0)
    assert returned[0] == False
    assert _return_print_result('😓 Not fully equal') == first_line


def test_not_equality_first_line_different_types() -> None:
    # Test wether the first return line when not fully equal is the same.
    bdf = BaseDF()
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_as_object,  # As object dtype
        bdf.df2,
        bdf.df1_name,
        bdf.df2_name,
    )
    first_line = re.search('.*\n', io_out).group(0)
    assert returned[0] == False
    assert _return_print_result('😓 Not fully equal') == first_line


def test_not_equality_first_line_different_indexes() -> None:
    # Test wether the first return line when not fully equal is the same.
    bdf = BaseDF()
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2.drop(0),  # Drop first line
        bdf.df1_name,
        bdf.df2_name,
    )
    first_line = re.search('.*\n', io_out).group(0)
    assert returned[0] == False
    assert _return_print_result('😓 Not fully equal') == first_line


def test_not_equality_first_line_different_values() -> None:
    # Test wether the first return line when not fully equal is the same.
    bdf = BaseDF()
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        # Change the order and reset index
        bdf.df2.sort_index(ascending=False).reset_index(drop=True),
        bdf.df1_name,
        bdf.df2_name,
    )
    first_line = re.search('.*\n', io_out).group(0)
    assert returned[0] == False and returned[1] == False
    assert _return_print_result('😓 Not fully equal') == first_line


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


def test_io_out_cols_review() -> None:
    bdf = BaseDF()
    df1_colset = set(bdf.df1_extra_col.columns)
    df2_colset = set(bdf.df2_extra_col.columns)
    cols_common_set = df1_colset.intersection(df2_colset)
    cols_common_list = sorted(list(cols_common_set))
    cols_df1_excl_set = df1_colset - cols_common_set
    cols_df2_excl_set = df2_colset - cols_common_set

    io_predicted_str = _return_print_title(1, 'Columns present in both DataFrames (intersection)')

    # Testing showing common columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col,
        bdf.df2_extra_col,
        show_common_cols=True,
    )
    cols_common_ioret = _return_pprint(1, cols_common_list)
    io_predicted_full_str = io_predicted_str + cols_common_ioret
    assert io_predicted_full_str in io_out
    equality_metadata = returned[2]
    assert equality_metadata.get('cols_common_set') == cols_common_set
    assert equality_metadata.get('cols_df1_excl_set') == cols_df1_excl_set
    assert equality_metadata.get('cols_df2_excl_set') == cols_df2_excl_set
    assert equality_metadata.get('cols_df1_dups_dict') == {}
    assert equality_metadata.get('cols_df2_dups_dict') == {}
    assert equality_metadata.get('cols_df1_dups_common_dict') == {}
    assert equality_metadata.get('cols_df2_dups_common_dict') == {}

    # Testing NOT showing common columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col,
        bdf.df2_extra_col,
        show_common_cols=False,
    )
    cols_common_ioret = _return_pprint(1, cols_common_list)
    io_predicted_full_str = io_predicted_str + cols_common_ioret
    assert io_predicted_full_str not in io_out
    equality_metadata = returned[2]
    assert equality_metadata.get('cols_common_set') == cols_common_set
    assert equality_metadata.get('cols_df1_excl_set') == cols_df1_excl_set
    assert equality_metadata.get('cols_df2_excl_set') == cols_df2_excl_set
    assert equality_metadata.get('cols_df1_dups_dict') == {}
    assert equality_metadata.get('cols_df2_dups_dict') == {}
    assert equality_metadata.get('cols_df1_dups_common_dict') == {}
    assert equality_metadata.get('cols_df2_dups_common_dict') == {}


def test_io_out_idxs_review() -> None:
    bdf = BaseDF()
    df1_idxset = set(bdf.df1.index)
    df2_idxset = set(bdf.df2_index_plus1.index)
    idxs_common_set = df1_idxset.intersection(df2_idxset)
    idxs_common_list = sorted(list(idxs_common_set))
    idxs_df1_excl_set = df1_idxset - idxs_common_set
    idxs_df2_excl_set = df2_idxset - idxs_common_set

    io_predicted_str = _return_print_title(1, 'Indexes present in both DataFrames (intersection)')

    # Testing showing common indexes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2_index_plus1,
        show_common_idxs=True,
    )
    idxs_common_ioret = _return_pprint(1, idxs_common_list)
    io_predicted_full_str = io_predicted_str + idxs_common_ioret
    assert io_predicted_full_str in io_out
    equality_metadata = returned[2]
    assert equality_metadata.get('idxs_common_set') == idxs_common_set
    assert equality_metadata.get('idxs_df1_excl_set') == idxs_df1_excl_set
    assert equality_metadata.get('idxs_df2_excl_set') == idxs_df2_excl_set
    assert equality_metadata.get('idxs_df1_dups_dict') == {}
    assert equality_metadata.get('idxs_df2_dups_dict') == {}
    assert equality_metadata.get('idxs_df1_dups_common_dict') == {}
    assert equality_metadata.get('idxs_df2_dups_common_dict') == {}

    # Testing NOT showing common indexes
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2_index_plus1,
        show_common_idxs=False,
    )
    idxs_common_ioret = _return_pprint(1, idxs_common_list)
    io_predicted_full_str = io_predicted_str + idxs_common_ioret
    assert io_predicted_full_str not in io_out
    equality_metadata = returned[2]
    assert equality_metadata.get('idxs_common_set') == idxs_common_set
    assert equality_metadata.get('idxs_df1_excl_set') == idxs_df1_excl_set
    assert equality_metadata.get('idxs_df2_excl_set') == idxs_df2_excl_set
    assert equality_metadata.get('idxs_df1_dups_dict') == {}
    assert equality_metadata.get('idxs_df2_dups_dict') == {}
    assert equality_metadata.get('idxs_df1_dups_common_dict') == {}
    assert equality_metadata.get('idxs_df2_dups_common_dict') == {}
