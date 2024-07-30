import io
import pprint
import re
import textwrap
from contextlib import redirect_stdout
from itertools import permutations
from typing import Callable

import pandas as pd
import pytest

from some_pd_tools import pd_compare

from .basedf import BaseDF


def _sorted(obj):
    if isinstance(obj, dict):
        return sorted(obj.items(), key=lambda item: str(item[0]))
    if isinstance(obj, set) or isinstance(obj, list):
        return sorted(obj, key=lambda item: str(item))


def _fill(
    txt,
    initial_indent,
    subsequent_indent,
    width=100,
    expand_tabs=False,
    replace_whitespace=False,
    drop_whitespace=False,
):
    return textwrap.fill(
        txt,
        initial_indent=initial_indent,
        subsequent_indent=subsequent_indent,
        width=width,
        expand_tabs=expand_tabs,
        replace_whitespace=replace_whitespace,
        drop_whitespace=drop_whitespace,
    )


def _return_print_title(level: int, title: str, subtitle: str = None) -> None:
    to_return = '————————————————————' + '\n'
    title_ii = f'{"#" * level} '
    title_si = f'{" " * level} '
    to_return += _fill(title, initial_indent=title_ii, subsequent_indent=title_si) + '\n'
    if subtitle is not None:
        sub_ii = f'{" " * level} '
        subtitle_si = f'{" " * level} '
        to_return += (
            _fill(f'({subtitle})', initial_indent=sub_ii, subsequent_indent=subtitle_si) + '\n'
        )
    return to_return


def _return_print_result(result: str) -> None:
    return _fill(f'<<< {result} >>>', initial_indent='', subsequent_indent='    ') + '\n'


def _return_print_event(level: int, event: str) -> None:
    event_ii = f'{"  "*(level-1)}> '
    event_si = f'{"  "*(level-1)}  '
    return _fill(event, initial_indent=event_ii, subsequent_indent=event_si) + '\n'


def _return_print_plain(level: int, txt: str) -> None:
    level_str = '  ' * (level - 1)
    txt_ii = f'{level_str}  '
    txt_si = f'{level_str}  '
    return _fill(txt, initial_indent=txt_ii, subsequent_indent=txt_si) + '\n'


def _return_pprint(level: int, obj: object) -> None:
    level_str = f'{"  " * (level - 1)}  '
    _stream = io.StringIO()
    pprint.pprint(obj, indent=1, width=100 - len(level_str), compact=True, stream=_stream)
    to_print = level_str + _stream.getvalue()
    to_print = re.sub('\n.+', f'\n{level_str}', to_print)
    return to_print


def _fn_ret_and_output(fn: Callable, *args, **kwargs):
    stream = io.StringIO()
    with redirect_stdout(stream):
        returned = fn(*args, **kwargs)
    return returned, stream.getvalue()


def test__compare_lists__wrong_types():
    # list_1 or list_2 are not of type list
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape('list_1 and list_2 must be of type list.'),
    ):
        pd_compare.compare_lists([1, 2, 3], {1, 2, 3})
    with pytest.raises(
        ValueError,
        match=re.escape('list_1 and list_2 must be of type list.'),
    ):
        pd_compare.compare_lists({1, 2, 3}, [1, 2, 3])

    # list_1_name and list_2_name must be of type str
    # ************************************
    with pytest.raises(
        ValueError,
        match=re.escape(
            'list_1_name, list_2_name, type_name and type_name_plural must be of type str.'
        ),
    ):
        pd_compare.compare_lists([1, 2, 3], [1, 2, 3], list_1_name=1)
    with pytest.raises(
        ValueError,
        match=re.escape(
            'list_1_name, list_2_name, type_name and type_name_plural must be of type str.'
        ),
    ):
        pd_compare.compare_lists([1, 2, 3], [1, 2, 3], list_2_name=1)
    with pytest.raises(
        ValueError,
        match=re.escape(
            'list_1_name, list_2_name, type_name and type_name_plural must be of type str.'
        ),
    ):
        pd_compare.compare_lists([1, 2, 3], [1, 2, 3], type_name=1)
    with pytest.raises(
        ValueError,
        match=re.escape(
            'list_1_name, list_2_name, type_name and type_name_plural must be of type str.'
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
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp == True
    assert list_common_set == {1, 2, 's'}
    assert list_1_excl_set == set()
    assert list_2_excl_set == set()
    assert list_1_dups_dict == {}
    assert list_2_dups_dict == {}
    io_predicted_str = _return_print_title(1, 'Comparing someitems')
    io_predicted_str += _return_print_event(1, '✅ Someitems equal')
    io_predicted_str += _return_print_event(1, '✅ No duplicate someitems')
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
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp == True
    assert list_common_set == {1, 2, 's'}
    assert list_1_excl_set == set()
    assert list_2_excl_set == set()
    assert list_1_dups_dict == {}
    assert list_2_dups_dict == {}
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
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp == True
    assert list_common_set == {1, 2, 's'}
    assert list_1_excl_set == set()
    assert list_2_excl_set == set()
    assert list_1_dups_dict == {1: 4, 2: 3, 's': 2}
    assert list_2_dups_dict == {1: 4, 2: 3, 's': 2}
    io_predicted_str = _return_print_title(1, 'Comparing someitems')
    io_predicted_str += _return_print_event(1, '✅ Someitems equal')
    io_predicted_str += _return_print_event(1, '😓 Duplicate someitems (value,count):')
    io_predicted_str += _return_pprint(1, _sorted(list_1_dups_dict))
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
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp == True
    assert list_common_set == {1, 2, 's'}
    assert list_1_excl_set == set()
    assert list_2_excl_set == set()
    assert list_1_dups_dict == {1: 4, 2: 3, 's': 2}
    assert list_2_dups_dict == {1: 4, 2: 3, 's': 2}
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
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp == False
    assert list_common_set == {'s'}
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4, 5}
    assert list_1_dups_dict == {}
    assert list_2_dups_dict == {}
    io_predicted_str = _return_print_title(1, 'Comparing someitems')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list1: 3')
    io_predicted_str += _return_print_event(2, 'list2: 4')
    io_predicted_str += _return_print_event(1, '✅ Someitems in common:')
    io_predicted_str += _return_pprint(1, ['s'])
    io_predicted_str += _return_print_event(1, 'list1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '✅ No duplicate someitems')
    io_predicted_str += _return_print_event(1, 'list2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4, 5}))
    io_predicted_str += _return_print_event(2, '✅ No duplicate someitems')
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
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp == False
    assert list_common_set == {'s'}
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4, 5}
    assert list_1_dups_dict == {}
    assert list_2_dups_dict == {}
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
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp == False
    assert list_common_set == {'s'}
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4}
    assert list_1_dups_dict == {2: 3, 1: 4, 's': 2}
    assert list_2_dups_dict == {4: 2, 's': 3}
    io_predicted_str = _return_print_title(1, 'Comparing someitems')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list1: 9')
    io_predicted_str += _return_print_event(2, 'list2: 6')
    io_predicted_str += _return_print_event(1, '✅ Someitems in common:')
    io_predicted_str += _return_pprint(1, ['s'])
    io_predicted_str += _return_print_event(1, 'list1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicate someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({2: 3, 1: 4, 's': 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicate someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicate someitems in common:')
    io_predicted_str += _return_pprint(2, ['s'])
    io_predicted_str += _return_print_event(1, 'list2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4}))
    io_predicted_str += _return_print_event(2, '😓 Duplicate someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({4: 2, 's': 3}))
    io_predicted_str += _return_print_event(2, '😓 Duplicate someitems exclusive:')
    io_predicted_str += _return_pprint(2, [4])
    io_predicted_str += _return_print_event(2, '😓 Duplicate someitems in common:')
    io_predicted_str += _return_pprint(2, ['s'])
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
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp == False
    assert list_common_set == set()
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4, 's'}
    assert list_1_dups_dict == {2: 3, 1: 4}
    assert list_2_dups_dict == {4: 2, 's': 3}
    io_predicted_str = _return_print_title(1, 'Comparing someitems')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list1: 7')
    io_predicted_str += _return_print_event(2, 'list2: 6')
    io_predicted_str += _return_print_event(1, '😓 No someitems in common')
    io_predicted_str += _return_print_event(1, 'list1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicate someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({2: 3, 1: 4}))
    io_predicted_str += _return_print_event(2, '😓 Duplicate someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '✅ No duplicate someitems in common')
    io_predicted_str += _return_print_event(1, 'list2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4, 's'}))
    io_predicted_str += _return_print_event(2, '😓 Duplicate someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({4: 2, 's': 3}))
    io_predicted_str += _return_print_event(2, '😓 Duplicate someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({4, 's'}))
    io_predicted_str += _return_print_event(2, '✅ No duplicate someitems in common')
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


def test__compare_dtypes__equal_dtypes_no_dups():
    assert False  # TODO REMOVE


def test__compare_dtypes__equal_dtypes_w_dups():
    assert False  # TODO REMOVE


def test__compare_dtypes__diff_dtypes_no_dups():
    assert False  # TODO REMOVE


def test__compare_dtypes__diff_dtypes_w_dups():
    assert False  # TODO REMOVE


def test__compare__dtypes_equal_values_equal() -> None:
    '''Test output/return when dtypes are equal and values are equal.'''
    assert False  # TODO REMOVE


def test__compare__dtypes_not_equal_values_not_equal() -> None:
    '''Test output/return when dtypes are not equal and values are not equal.'''
    assert False  # TODO REMOVE


def test__compare__equality_full() -> None:
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
    assert _return_print_result('😓 Not fully equal') == first_line


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
    assert _return_print_result('😓 Not fully equal') == first_line


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
    assert _return_print_result('😓 Not fully equal') == first_line


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
    assert _return_print_result('😓 Not fully equal') == first_line


def test__compare__duplicates_abort() -> None:
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


def test__compare__io_out_cols_review() -> None:
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


def test__compare__io_out_idxs_review() -> None:
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
