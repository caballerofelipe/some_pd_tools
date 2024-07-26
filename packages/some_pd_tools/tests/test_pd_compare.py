import io
import pprint
import re
from contextlib import redirect_stdout
from itertools import permutations
from typing import Callable

import pandas as pd
import pytest

from some_pd_tools import pd_compare

from .basedf import BaseDF


def _return_printed_title(level, title, subtitle=None):
    to_return = '————————————————————\n'
    to_return += f'{"#"*level} {title}\n'
    if subtitle is not None:
        to_return += f'  ({subtitle})\n'
    return to_return


def _return_printed_result(res):
    return f'<<< {res} >>>\n'


def _return_printed_event(level, res):
    level_str = '  ' * (level - 1)
    return f'{level_str}-> {res}\n'


def _return_pprinted(level: int, obj: object) -> None:
    level_str = '  ' * (level - 1)
    _stream = io.StringIO()
    pprint.pprint(obj, indent=1, width=100, compact=True, stream=_stream)
    to_print = level_str + _stream.getvalue()
    to_print = re.sub('\n.+', f'\n{level_str}', to_print)
    return to_print


def _fn_ret_and_output(fn: Callable, *args, **kwargs):
    stream = io.StringIO()
    with redirect_stdout(stream):
        returned = fn(*args, **kwargs)
    return returned, stream.getvalue()


def test__compare_lists__wrong_types():
    # list1 or list2 are not of type list
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('list1 and list2 must be of type list.'),
    ):
        pd_compare.compare_lists([1, 2, 3], {1, 2, 3})
    with pytest.raises(
        ValueError,
        match=re.escape('list1 and list2 must be of type list.'),
    ):
        pd_compare.compare_lists({1, 2, 3}, [1, 2, 3])

    # list1_name and list2_name must be of type str
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape(
            'list1_name, list2_name, type_name and type_name_plural must be of type str.'
        ),
    ):
        pd_compare.compare_lists([1, 2, 3], [1, 2, 3], list1_name=1)
    with pytest.raises(
        ValueError,
        match=re.escape(
            'list1_name, list2_name, type_name and type_name_plural must be of type str.'
        ),
    ):
        pd_compare.compare_lists([1, 2, 3], [1, 2, 3], list2_name=1)
    with pytest.raises(
        ValueError,
        match=re.escape(
            'list1_name, list2_name, type_name and type_name_plural must be of type str.'
        ),
    ):
        pd_compare.compare_lists([1, 2, 3], [1, 2, 3], type_name=1)
    with pytest.raises(
        ValueError,
        match=re.escape(
            'list1_name, list2_name, type_name and type_name_plural must be of type str.'
        ),
    ):
        pd_compare.compare_lists([1, 2, 3], [1, 2, 3], type_name_plural=1)


def test__compare_lists__equal_lists_no_dups():
    # With report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        [1, 2, 's'],
        [1, 2, 's'],
        type_name='someitem',
        type_name_plural='someitems',
        report=True,
    )
    (
        items_in_both,
        list1_exclusives,
        list2_exclusives,
        list1_dups,
        list2_dups,
    ) = returned
    assert items_in_both == {1, 2, 's'}
    assert list1_exclusives == set()
    assert list2_exclusives == set()
    assert list1_dups == {}
    assert list2_dups == {}
    io_predicted_str = _return_printed_title(1, 'Comparing someitems')
    io_predicted_str += _return_printed_event(1, '✅ Someitems equal')
    io_predicted_str += _return_printed_event(1, '✅ No duplicate someitems')
    assert io_predicted_str == io_out
    # No report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        [1, 2, 's'],
        [1, 2, 's'],
        type_name='someitem',
        type_name_plural='someitems',
        report=False,
    )
    (
        items_in_both,
        list1_exclusives,
        list2_exclusives,
        list1_dups,
        list2_dups,
    ) = returned
    assert items_in_both == {1, 2, 's'}
    assert list1_exclusives == set()
    assert list2_exclusives == set()
    assert list1_dups == {}
    assert list2_dups == {}
    io_predicted_str = ''
    assert io_predicted_str == io_out


def test__compare_lists__equal_lists_w_dups():
    # With report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        [1, 2, 's', 1, 2, 1, 2, 1, 's'],
        [1, 2, 's', 1, 2, 1, 2, 1, 's'],
        type_name='someitem',
        type_name_plural='someitems',
        report=True,
    )
    (
        items_in_both,
        list1_exclusives,
        list2_exclusives,
        list1_dups,
        list2_dups,
    ) = returned
    assert items_in_both == {1, 2, 's'}
    assert list1_exclusives == set()
    assert list2_exclusives == set()
    assert list1_dups == {1: 4, 2: 3, 's': 2}
    assert list2_dups == {1: 4, 2: 3, 's': 2}
    io_predicted_str = _return_printed_title(1, 'Comparing someitems')
    io_predicted_str += _return_printed_event(1, '✅ Someitems equal')
    io_predicted_str += _return_printed_event(1, '😓 Duplicate someitems (value:count):')
    io_predicted_str += _return_pprinted(1, list1_dups)
    assert io_predicted_str == io_out
    # No report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        [1, 2, 's', 1, 2, 1, 2, 1, 's'],
        [1, 2, 's', 1, 2, 1, 2, 1, 's'],
        type_name='someitem',
        type_name_plural='someitems',
        report=False,
    )
    (
        items_in_both,
        list1_exclusives,
        list2_exclusives,
        list1_dups,
        list2_dups,
    ) = returned
    assert items_in_both == {1, 2, 's'}
    assert list1_exclusives == set()
    assert list2_exclusives == set()
    assert list1_dups == {1: 4, 2: 3, 's': 2}
    assert list2_dups == {1: 4, 2: 3, 's': 2}
    io_predicted_str = ''
    assert io_predicted_str == io_out


def test__compare_lists__diff_lists_no_dups():
    # With report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        [1, 2, 's'],
        ['s', 3, 4, 5],
        type_name='someitem',
        type_name_plural='someitems',
        report=True,
    )
    (
        items_in_both,
        list1_exclusives,
        list2_exclusives,
        list1_dups,
        list2_dups,
    ) = returned
    assert items_in_both == {'s'}
    assert list1_exclusives == {1, 2}
    assert list2_exclusives == {3, 4, 5}
    assert list1_dups == {}
    assert list2_dups == {}
    io_predicted_str = _return_printed_title(1, 'Comparing someitems')
    io_predicted_str += _return_printed_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_printed_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_printed_event(2, 'list1: 3')
    io_predicted_str += _return_printed_event(2, 'list2: 4')
    io_predicted_str += _return_printed_event(1, '✅ Someitems in common:')
    io_predicted_str += _return_pprinted(1, {'s'})
    io_predicted_str += _return_printed_event(1, 'list1')
    io_predicted_str += _return_printed_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprinted(2, {1, 2})
    io_predicted_str += _return_printed_event(2, '✅ No duplicate someitems')
    io_predicted_str += _return_printed_event(1, 'list2')
    io_predicted_str += _return_printed_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprinted(2, {3, 4, 5})
    io_predicted_str += _return_printed_event(2, '✅ No duplicate someitems')
    assert io_predicted_str == io_out
    # No report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        [1, 2, 's'],
        ['s', 3, 4, 5],
        type_name='someitem',
        type_name_plural='someitems',
        report=False,
    )
    (
        items_in_both,
        list1_exclusives,
        list2_exclusives,
        list1_dups,
        list2_dups,
    ) = returned
    assert items_in_both == {'s'}
    assert list1_exclusives == {1, 2}
    assert list2_exclusives == {3, 4, 5}
    assert list1_dups == {}
    assert list2_dups == {}
    io_predicted_str = ''
    assert io_predicted_str == io_out


def test__compare_lists__diff_lists_w_dups():
    # With something in common
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        [1, 2, 's', 2, 2, 1, 1, 1, 's'],
        ['s', 3, 4, 4, 's', 's'],
        type_name='someitem',
        type_name_plural='someitems',
        report=True,
    )
    (
        items_in_both,
        list1_exclusives,
        list2_exclusives,
        list1_dups,
        list2_dups,
    ) = returned
    assert items_in_both == {'s'}
    assert list1_exclusives == {1, 2}
    assert list2_exclusives == {3, 4}
    assert list1_dups == {2: 3, 1: 4, 's': 2}
    assert list2_dups == {4: 2, 's': 3}
    io_predicted_str = _return_printed_title(1, 'Comparing someitems')
    io_predicted_str += _return_printed_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_printed_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_printed_event(2, 'list1: 9')
    io_predicted_str += _return_printed_event(2, 'list2: 6')
    io_predicted_str += _return_printed_event(1, '✅ Someitems in common:')
    io_predicted_str += _return_pprinted(1, {'s'})
    io_predicted_str += _return_printed_event(1, 'list1')
    io_predicted_str += _return_printed_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprinted(2, {1, 2})
    io_predicted_str += _return_printed_event(2, '😓 Duplicate someitems (value:count):')
    io_predicted_str += _return_pprinted(2, {2: 3, 1: 4, 's': 2})
    io_predicted_str += _return_printed_event(2, '😓 Duplicate someitems exclusive:')
    io_predicted_str += _return_pprinted(2, {1,2})
    io_predicted_str += _return_printed_event(2, '😓 Duplicate someitems in common:')
    io_predicted_str += _return_pprinted(2, {'s'})
    io_predicted_str += _return_printed_event(1, 'list2')
    io_predicted_str += _return_printed_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprinted(2, {3, 4})
    io_predicted_str += _return_printed_event(2, '😓 Duplicate someitems (value:count):')
    io_predicted_str += _return_pprinted(2, {4: 2, 's': 3})
    io_predicted_str += _return_printed_event(2, '😓 Duplicate someitems exclusive:')
    io_predicted_str += _return_pprinted(2, {4})
    io_predicted_str += _return_printed_event(2, '😓 Duplicate someitems in common:')
    io_predicted_str += _return_pprinted(2, {'s'})
    assert io_predicted_str == io_out
    # With nothing in common
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        [1, 2, 2, 2, 1, 1, 1],
        ['s', 3, 4, 4, 's', 's'],
        type_name='someitem',
        type_name_plural='someitems',
        report=True,
    )
    (
        items_in_both,
        list1_exclusives,
        list2_exclusives,
        list1_dups,
        list2_dups,
    ) = returned
    assert items_in_both == set()
    assert list1_exclusives == {1, 2}
    assert list2_exclusives == {3, 4, 's'}
    assert list1_dups == {2: 3, 1: 4}
    assert list2_dups == {4: 2, 's': 3}
    io_predicted_str = _return_printed_title(1, 'Comparing someitems')
    io_predicted_str += _return_printed_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_printed_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_printed_event(2, 'list1: 7')
    io_predicted_str += _return_printed_event(2, 'list2: 6')
    io_predicted_str += _return_printed_event(1, '😓 No someitems in common')
    io_predicted_str += _return_printed_event(1, 'list1')
    io_predicted_str += _return_printed_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprinted(2, {1, 2})
    io_predicted_str += _return_printed_event(2, '😓 Duplicate someitems (value:count):')
    io_predicted_str += _return_pprinted(2, {2: 3, 1: 4})
    io_predicted_str += _return_printed_event(2, '😓 Duplicate someitems exclusive:')
    io_predicted_str += _return_pprinted(2, {1,2})
    io_predicted_str += _return_printed_event(2, '✅ No duplicate someitems in common')
    io_predicted_str += _return_printed_event(1, 'list2')
    io_predicted_str += _return_printed_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprinted(2, {3, 4,'s'})
    io_predicted_str += _return_printed_event(2, '😓 Duplicate someitems (value:count):')
    io_predicted_str += _return_pprinted(2, {4: 2, 's': 3})
    io_predicted_str += _return_printed_event(2, '😓 Duplicate someitems exclusive:')
    io_predicted_str += _return_pprinted(2, {4, 's'})
    io_predicted_str += _return_printed_event(2, '✅ No duplicate someitems in common')
    assert io_predicted_str == io_out


def test__compare_dtypes__wrong_types():
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
        pd_compare.compare_dtypes(pd.Series([1,2,3]), pd.Series([1,2,3]))
    # One Series and one DataFrame
    with pytest.raises(
        ValueError,
        match=re.escape('df1 and df2 must be of type pd.DataFrame.'),
    ):
        pd_compare.compare_dtypes(pd.Series([1,2,3]), pd.DataFrame([1,2,3]))
    with pytest.raises(
        ValueError,
        match=re.escape('df1 and df2 must be of type pd.DataFrame.'),
    ):
        pd_compare.compare_dtypes(pd.DataFrame([1,2,3]), pd.Series([1,2,3]))

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


def test__compare_dtypes__equal_dtypes_no_dups():
    assert False  # TODO REMOVE


def test__compare_dtypes__equal_dtypes_w_dups():
    assert False  # TODO REMOVE


def test__compare_dtypes__diff_dtypes_no_dups():
    assert False  # TODO REMOVE


def test__compare_dtypes__diff_dtypes_w_dups():
    assert False  # TODO REMOVE


def test__compare__equality_full() -> None:
    bdf = BaseDF()
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
        'report': _return_printed_result('🥳 Fully equal'),
    }
    assert returned == [True, False, equality_metadata_predicted]
    assert io_out == _return_printed_result('🥳 Fully equal')


def test__compare__not_equality_first_line_different_columns() -> None:
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
    assert _return_printed_result('😓 Not fully equal') == first_line


def test__compare__not_equality_first_line_different_types() -> None:
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
    assert _return_printed_result('😓 Not fully equal') == first_line


def test__compare__not_equality_first_line_different_indexes() -> None:
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
    assert _return_printed_result('😓 Not fully equal') == first_line


def test__compare__not_equality_first_line_different_values() -> None:
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
    assert _return_printed_result('😓 Not fully equal') == first_line


def test__compare__columns_metadata_and_return() -> None:
    bdf = BaseDF()
    # Equal Columns, equal DataFrames
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2,
        bdf.df1_name,
        bdf.df2_name,
    )
    assert returned[0] == True
    assert returned[1] == False
    equality_metadata = returned[2]
    assert equality_metadata.get('common_cols_set') is None
    assert equality_metadata.get('df1_extra_cols_set') is None
    assert equality_metadata.get('df2_extra_cols_set') is None
    assert equality_metadata.get('df1_dups_cols_dict') is None
    assert equality_metadata.get('df2_dups_cols_dict') is None
    assert equality_metadata.get('df1_dups_cols_common_dict') is None
    assert equality_metadata.get('df2_dups_cols_common_dict') is None
    # Equal Columns, equal DataFrames, all duplicated (two instances of each)
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1[[*bdf.df1.columns, *bdf.df1.columns]],
        bdf.df2[[*bdf.df2.columns, *bdf.df2.columns]],
        bdf.df1_name,
        bdf.df2_name,
    )
    assert returned[0] is True
    assert returned[1] is False
    equality_metadata = returned[2]
    assert equality_metadata.get('common_cols_set') is None
    assert equality_metadata.get('df1_extra_cols_set') is None
    assert equality_metadata.get('df2_extra_cols_set') is None
    assert equality_metadata.get('df1_dups_cols_dict') is None
    assert equality_metadata.get('df2_dups_cols_dict') is None
    assert equality_metadata.get('df1_dups_cols_common_dict') is None
    assert equality_metadata.get('df2_dups_cols_common_dict') is None
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
    assert returned[1] is True
    equality_metadata = returned[2]
    assert equality_metadata.get('common_cols_set') == set(bdf.df1.columns)
    assert equality_metadata.get('df1_extra_cols_set') == set(bdf.df1_extra_col.columns) - set(
        bdf.df1.columns
    )
    assert equality_metadata.get('df2_extra_cols_set') == set(bdf.df2_extra_col.columns) - set(
        bdf.df2.columns
    )
    assert equality_metadata.get('df1_dups_cols_dict') == {
        col: 2 for col in bdf.df1_extra_col.columns
    }
    assert equality_metadata.get('df2_dups_cols_dict') == {
        col: 2 for col in bdf.df2_extra_col.columns
    }
    assert equality_metadata.get('df1_dups_cols_common_dict') == {col: 2 for col in bdf.df1.columns}
    assert equality_metadata.get('df2_dups_cols_common_dict') == {col: 2 for col in bdf.df2.columns}
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
    assert equality_metadata.get('common_cols_set') == set(bdf.df1.columns)
    assert equality_metadata.get('df1_extra_cols_set') == set(bdf.df1_extra_col.columns) - set(
        bdf.df1.columns
    )
    assert equality_metadata.get('df2_extra_cols_set') == set(bdf.df2_extra_col.columns) - set(
        bdf.df2.columns
    )
    assert equality_metadata.get('df1_dups_cols_dict') == {
        col: 2 for col in bdf.df1_extra_col.columns
    }
    assert equality_metadata.get('df2_dups_cols_dict') == {
        col: 3 for col in bdf.df2_extra_col.columns
    }
    assert equality_metadata.get('df1_dups_cols_common_dict') == {col: 2 for col in bdf.df1.columns}
    assert equality_metadata.get('df2_dups_cols_common_dict') == {col: 3 for col in bdf.df2.columns}
    assert (
        equality_metadata.get('error')
        == '🛑 Duplicate common columns found but duplicates don\'t match, aborting compare.'
    )


def test__compare__indexes_metadata_and_return() -> None:
    # This assumes there are no column duplicates (checked in `test__compare__columns_metadata_and_return()`)
    bdf = BaseDF()
    # Equal Indexes, equal DataFrames
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2,
        bdf.df1_name,
        bdf.df2_name,
    )
    assert returned[0] == True
    assert returned[1] == False
    equality_metadata = returned[2]
    assert equality_metadata.get('common_idxs_set') is None
    assert equality_metadata.get('df1_extra_idxs_set') is None
    assert equality_metadata.get('df2_extra_idxs_set') is None
    assert equality_metadata.get('df1_dups_idxs_dict') is None
    assert equality_metadata.get('df2_dups_idxs_dict') is None
    assert equality_metadata.get('df1_dups_idxs_common_dict') is None
    assert equality_metadata.get('df2_dups_idxs_common_dict') is None
    # Equal Indexes, equal Dataframes, all duplicated (two instances of each)
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1.loc[[*bdf.df1.index, *bdf.df1.index]],
        bdf.df2.loc[[*bdf.df2.index, *bdf.df2.index]],
        bdf.df1_name,
        bdf.df2_name,
    )
    assert returned[0] is True
    assert returned[1] is False
    equality_metadata = returned[2]
    assert equality_metadata.get('common_idxs_set') is None
    assert equality_metadata.get('df1_extra_idxs_set') is None
    assert equality_metadata.get('df2_extra_idxs_set') is None
    assert equality_metadata.get('df1_dups_idxs_dict') is None
    assert equality_metadata.get('df2_dups_idxs_dict') is None
    assert equality_metadata.get('df1_dups_idxs_common_dict') is None
    assert equality_metadata.get('df2_dups_idxs_common_dict') is None
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
    assert returned[1] is True
    equality_metadata = returned[2]
    assert equality_metadata.get('common_idxs_set') == set([1, 2])
    assert equality_metadata.get('df1_extra_idxs_set') == set([0])
    assert equality_metadata.get('df2_extra_idxs_set') == set([3])
    assert equality_metadata.get('df1_dups_idxs_dict') == {idx: 2 for idx in [0, 1, 2]}
    assert equality_metadata.get('df2_dups_idxs_dict') == {idx: 2 for idx in [1, 2, 3]}
    assert equality_metadata.get('df1_dups_idxs_common_dict') == {idx: 2 for idx in [1, 2]}
    assert equality_metadata.get('df2_dups_idxs_common_dict') == {idx: 2 for idx in [1, 2]}

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
    assert equality_metadata.get('common_idxs_set') == set([1, 2])
    assert equality_metadata.get('df1_extra_idxs_set') == set([0])
    assert equality_metadata.get('df2_extra_idxs_set') == set([3])
    assert equality_metadata.get('df1_dups_idxs_dict') == {idx: 2 for idx in [0, 1, 2]}
    assert equality_metadata.get('df2_dups_idxs_dict') == {idx: 3 for idx in [1, 2, 3]}
    assert equality_metadata.get('df1_dups_idxs_common_dict') == {idx: 2 for idx in [1, 2]}
    assert equality_metadata.get('df2_dups_idxs_common_dict') == {idx: 3 for idx in [1, 2]}
    assert (
        equality_metadata.get('error')
        == '🛑 Duplicate common indexes found but duplicates don\'t match, aborting compare.'
    )


def test__compare__io_out_show_common_cols() -> None:
    bdf = BaseDF()
    df1_colset = set(bdf.df1_extra_col.columns)
    df2_colset = set(bdf.df2_extra_col.columns)
    common_cols_set = df1_colset.intersection(df2_colset)
    common_cols_list = sorted(list(common_cols_set))

    io_predicted_str = _return_printed_title(1, 'Columns present in both DataFrames (intersection)')

    # Testing showing common columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col,
        bdf.df2_extra_col,
        show_common_cols=True,
    )
    stream = io.StringIO()
    pprint.pprint(common_cols_list, indent=1, width=100, compact=True, stream=stream)
    io_predicted_full_str = io_predicted_str + stream.getvalue()
    assert io_predicted_full_str in io_out
    equality_metadata = returned[2]
    assert equality_metadata.get('common_cols_set') == common_cols_set

    # Testing NOT showing common columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1_extra_col,
        bdf.df2_extra_col,
        show_common_cols=False,
    )
    stream = io.StringIO()
    pprint.pprint(common_cols_list, indent=1, width=100, compact=True, stream=stream)
    io_predicted_full_str = io_predicted_str + stream.getvalue()
    assert io_predicted_full_str not in io_out
    equality_metadata = returned[2]
    assert equality_metadata.get('common_cols_set') == common_cols_set


def test__compare__io_out_show_common_idxs() -> None:
    bdf = BaseDF()
    df1_idxset = set(bdf.df1.index)
    df2_idxset = set(bdf.df2_index_plus1.index)
    common_idxs_set = df1_idxset.intersection(df2_idxset)
    common_idxs_list = sorted(list(common_idxs_set))

    io_predicted_str = _return_printed_title(1, 'Indexes present in both DataFrames (intersection)')

    # Testing showing common columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2_index_plus1,
        show_common_idxs=True,
    )
    stream = io.StringIO()
    pprint.pprint(common_idxs_list, indent=1, width=100, compact=True, stream=stream)
    io_predicted_full_str = io_predicted_str + stream.getvalue()
    assert io_predicted_full_str in io_out
    equality_metadata = returned[2]
    assert equality_metadata.get('common_idxs_set') == common_idxs_set

    # Testing NOT showing common columns
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare,
        bdf.df1,
        bdf.df2_index_plus1,
        show_common_idxs=False,
    )
    stream = io.StringIO()
    pprint.pprint(common_idxs_list, indent=1, width=100, compact=True, stream=stream)
    io_predicted_full_str = io_predicted_str + stream.getvalue()
    assert io_predicted_full_str not in io_out
    equality_metadata = returned[2]
    assert equality_metadata.get('common_idxs_set') == common_idxs_set


def test__compare__dtypes_equal_values_equal() -> None:
    '''Test output/return when dtypes are equal and values are equal.'''
    assert False  # TODO REMOVE
    # bdf = BaseDF()
    # returned, io_out = compare_with_output(
    #     df1=bdf.df1,
    #     df1_name=bdf.df1_name,
    #     df2=bdf.df1_as_object,
    #     df2_name=bdf.df2_name,
    # )
    # io_predicted_str = _return_printed_result('😓 Not fully equal')
    # io_predicted_str += _return_printed_title(
    #     1, 'Comparing dtypes for common columns', 'Without special settings'
    # )
    # io_predicted_str += _return_printed_event('😓 Different dtypes')
    # io_predicted_str += '  col\\dataframe first_df second_df\n'
    # io_predicted_str += '  col_float     float64  object\n'
    # io_predicted_str += '  col_int       int64    object\n'
    # io_predicted_str += '  col_nan       float64  object\n'
    # assert io_out.startswith(io_predicted_str)
    # assert returned[0] == False and returned[1] == True


def test__compare__dtypes_not_equal_values_not_equal() -> None:
    '''Test output/return when dtypes are not equal and values are not equal.'''
    assert False  # TODO REMOVE
