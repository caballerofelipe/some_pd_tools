import re

import pytest

from some_pd_tools import pd_compare

from ..formatting import (
    _fn_ret_and_output,
    _return_pprint,
    _return_print_event,
    # _return_print_plain,
    # _return_print_result,
    _return_print_title,
    _sorted,
)


def test_wrong_types():
    """Test if wrong parameters types raises Exception."""
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


def test_equal_lists_no_dups():
    # With report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's'],
        list_2=[1, 2, 's'],
        show_common_items=True,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=True,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is True
    assert list_common_set == {1, 2, 's'}
    assert list_1_excl_set == set()
    assert list_2_excl_set == set()
    assert list_1_dups_dict == {}
    assert list_2_dups_dict == {}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '✅ Someitems equal')
    io_predicted_str += _return_print_event(1, '✅ Someitems in common:')
    io_predicted_str += _return_pprint(1, _sorted({'s', 1, 2}))
    io_predicted_str += _return_print_event(1, '✅ No duplicates someitems')
    assert io_predicted_str == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # No report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's'],
        list_2=[1, 2, 's'],
        show_common_items=True,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=False,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is True
    assert list_common_set == {1, 2, 's'}
    assert list_1_excl_set == set()
    assert list_2_excl_set == set()
    assert list_1_dups_dict == {}
    assert list_2_dups_dict == {}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '✅ Someitems equal')
    io_predicted_str += _return_print_event(1, '✅ Someitems in common:')
    io_predicted_str += _return_pprint(1, _sorted({'s', 1, 2}))
    io_predicted_str += _return_print_event(1, '✅ No duplicates someitems')
    assert '' == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report


def test_equal_lists_w_dups():
    # With report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's', 1, 2, 1, 2, 1, 's'],
        list_2=[1, 2, 's', 1, 2, 1, 2, 1, 's'],
        show_common_items=False,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=True,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is True
    assert list_common_set == {1, 2, 's'}
    assert list_1_excl_set == set()
    assert list_2_excl_set == set()
    assert list_1_dups_dict == {1: 4, 2: 3, 's': 2}
    assert list_2_dups_dict == {1: 4, 2: 3, 's': 2}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '✅ Someitems equal')
    io_predicted_str += _return_print_event(1, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(1, _sorted(list_1_dups_dict))
    assert io_predicted_str == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # No report
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's', 1, 2, 1, 2, 1, 's'],
        list_2=[1, 2, 's', 1, 2, 1, 2, 1, 's'],
        show_common_items=False,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=False,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is True
    assert list_common_set == {1, 2, 's'}
    assert list_1_excl_set == set()
    assert list_2_excl_set == set()
    assert list_1_dups_dict == {1: 4, 2: 3, 's': 2}
    assert list_2_dups_dict == {1: 4, 2: 3, 's': 2}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '✅ Someitems equal')
    io_predicted_str += _return_print_event(1, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(1, _sorted(list_1_dups_dict))
    assert '' == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report


def test_diff_lists_no_dups():

    # With report, show_common_items=False
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's'],
        list_2=['s', 3, 4, 5],
        show_common_items=False,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=True,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == {'s'}
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4, 5}
    assert list_1_dups_dict == {}
    assert list_2_dups_dict == {}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 3')
    io_predicted_str += _return_print_event(2, 'list_2: 4')
    io_predicted_str += _return_print_event(1, '✅ Some someitems in common (not shown)')
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems')
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4, 5}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems')
    assert io_predicted_str == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # With report, show_common_items=True
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's'],
        list_2=['s', 3, 4, 5],
        show_common_items=True,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=True,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == {'s'}
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4, 5}
    assert list_1_dups_dict == {}
    assert list_2_dups_dict == {}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 3')
    io_predicted_str += _return_print_event(2, 'list_2: 4')
    io_predicted_str += _return_print_event(1, '✅ Someitems in common:')
    io_predicted_str += _return_pprint(1, ['s'])
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems')
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4, 5}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems')
    assert io_predicted_str == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # No report, show_common_items=False
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's'],
        list_2=['s', 3, 4, 5],
        show_common_items=False,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=False,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == {'s'}
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4, 5}
    assert list_1_dups_dict == {}
    assert list_2_dups_dict == {}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 3')
    io_predicted_str += _return_print_event(2, 'list_2: 4')
    io_predicted_str += _return_print_event(1, '✅ Some someitems in common (not shown)')
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems')
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4, 5}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems')
    assert '' == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # No report, show_common_items=True
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's'],
        list_2=['s', 3, 4, 5],
        show_common_items=True,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=False,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == {'s'}
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4, 5}
    assert list_1_dups_dict == {}
    assert list_2_dups_dict == {}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 3')
    io_predicted_str += _return_print_event(2, 'list_2: 4')
    io_predicted_str += _return_print_event(1, '✅ Someitems in common:')
    io_predicted_str += _return_pprint(1, ['s'])
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems')
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4, 5}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems')
    assert '' == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report


def test_diff_lists_w_dups():

    # With report, with something in common, show_common_items=False
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's', 2, 2, 1, 1, 1, 's'],
        list_2=['s', 3, 4, 4, 's', 's'],
        show_common_items=False,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=True,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == {'s'}
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4}
    assert list_1_dups_dict == {2: 3, 1: 4, 's': 2}
    assert list_2_dups_dict == {4: 2, 's': 3}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 9')
    io_predicted_str += _return_print_event(2, 'list_2: 6')
    io_predicted_str += _return_print_event(1, '✅ Some someitems in common (not shown)')
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({2: 3, 1: 4, 's': 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems in common:')
    io_predicted_str += _return_pprint(2, ['s'])
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({4: 2, 's': 3}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, [4])
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems in common:')
    io_predicted_str += _return_pprint(2, ['s'])
    assert io_predicted_str == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # With report, with nothing in common, show_common_items=False
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 2, 2, 1, 1, 1],
        list_2=['s', 3, 4, 4, 's', 's'],
        show_common_items=False,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=True,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == set()
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4, 's'}
    assert list_1_dups_dict == {2: 3, 1: 4}
    assert list_2_dups_dict == {4: 2, 's': 3}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 7')
    io_predicted_str += _return_print_event(2, 'list_2: 6')
    io_predicted_str += _return_print_event(1, '😓 No someitems in common')
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({2: 3, 1: 4}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems in common')
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4, 's'}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({4: 2, 's': 3}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({4, 's'}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems in common')
    assert io_predicted_str == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # With report, with something in common, show_common_items=True
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's', 2, 2, 1, 1, 1, 's'],
        list_2=['s', 3, 4, 4, 's', 's'],
        show_common_items=True,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=True,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == {'s'}
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4}
    assert list_1_dups_dict == {2: 3, 1: 4, 's': 2}
    assert list_2_dups_dict == {4: 2, 's': 3}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 9')
    io_predicted_str += _return_print_event(2, 'list_2: 6')
    io_predicted_str += _return_print_event(1, '✅ Someitems in common:')
    io_predicted_str += _return_pprint(1, ['s'])
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({2: 3, 1: 4, 's': 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems in common:')
    io_predicted_str += _return_pprint(2, ['s'])
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({4: 2, 's': 3}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, [4])
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems in common:')
    io_predicted_str += _return_pprint(2, ['s'])
    assert io_predicted_str == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # With report, with nothing in common, show_common_items=True
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 2, 2, 1, 1, 1],
        list_2=['s', 3, 4, 4, 's', 's'],
        show_common_items=True,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=True,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == set()
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4, 's'}
    assert list_1_dups_dict == {2: 3, 1: 4}
    assert list_2_dups_dict == {4: 2, 's': 3}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 7')
    io_predicted_str += _return_print_event(2, 'list_2: 6')
    io_predicted_str += _return_print_event(1, '😓 No someitems in common')
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({2: 3, 1: 4}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems in common')
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4, 's'}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({4: 2, 's': 3}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({4, 's'}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems in common')
    assert io_predicted_str == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # No report, with something in common, show_common_items=False
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's', 2, 2, 1, 1, 1, 's'],
        list_2=['s', 3, 4, 4, 's', 's'],
        show_common_items=False,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=False,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == {'s'}
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4}
    assert list_1_dups_dict == {2: 3, 1: 4, 's': 2}
    assert list_2_dups_dict == {4: 2, 's': 3}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 9')
    io_predicted_str += _return_print_event(2, 'list_2: 6')
    io_predicted_str += _return_print_event(1, '✅ Some someitems in common (not shown)')
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({2: 3, 1: 4, 's': 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems in common:')
    io_predicted_str += _return_pprint(2, ['s'])
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({4: 2, 's': 3}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, [4])
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems in common:')
    io_predicted_str += _return_pprint(2, ['s'])
    assert '' == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # No report, with nothing in common, show_common_items=False
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 2, 2, 1, 1, 1],
        list_2=['s', 3, 4, 4, 's', 's'],
        show_common_items=False,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=False,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == set()
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4, 's'}
    assert list_1_dups_dict == {2: 3, 1: 4}
    assert list_2_dups_dict == {4: 2, 's': 3}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 7')
    io_predicted_str += _return_print_event(2, 'list_2: 6')
    io_predicted_str += _return_print_event(1, '😓 No someitems in common')
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({2: 3, 1: 4}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems in common')
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4, 's'}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({4: 2, 's': 3}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({4, 's'}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems in common')
    assert '' == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # No report, with something in common, show_common_items=True
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 's', 2, 2, 1, 1, 1, 's'],
        list_2=['s', 3, 4, 4, 's', 's'],
        show_common_items=True,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=False,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == {'s'}
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4}
    assert list_1_dups_dict == {2: 3, 1: 4, 's': 2}
    assert list_2_dups_dict == {4: 2, 's': 3}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 9')
    io_predicted_str += _return_print_event(2, 'list_2: 6')
    io_predicted_str += _return_print_event(1, '✅ Someitems in common:')
    io_predicted_str += _return_pprint(1, ['s'])
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({2: 3, 1: 4, 's': 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems in common:')
    io_predicted_str += _return_pprint(2, ['s'])
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({4: 2, 's': 3}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, [4])
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems in common:')
    io_predicted_str += _return_pprint(2, ['s'])
    assert '' == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report

    # No report, with nothing in common, show_common_items=True
    # ************************************
    returned, io_out = _fn_ret_and_output(
        pd_compare.compare_lists,
        list_1=[1, 2, 2, 2, 1, 1, 1],
        list_2=['s', 3, 4, 4, 's', 's'],
        show_common_items=True,
        type_name='someitem',
        type_name_plural='someitems',
        report_print=False,
    )
    lists_comp, lists_metadata = returned
    list_common_set = lists_metadata['list_common_set']
    list_1_excl_set = lists_metadata['list_1_excl_set']
    list_2_excl_set = lists_metadata['list_2_excl_set']
    list_1_dups_dict = lists_metadata['list_1_dups_dict']
    list_2_dups_dict = lists_metadata['list_2_dups_dict']
    assert lists_comp is False
    assert list_common_set == set()
    assert list_1_excl_set == {1, 2}
    assert list_2_excl_set == {3, 4, 's'}
    assert list_1_dups_dict == {2: 3, 1: 4}
    assert list_2_dups_dict == {4: 2, 's': 3}
    io_predicted_str = _return_print_title(1, 'Comparing someitems from [list_1] and [list_2]')
    io_predicted_str += _return_print_event(1, '😓 Someitems not equal')
    io_predicted_str += _return_print_event(1, '😓 Someitems lengths don\'t match')
    io_predicted_str += _return_print_event(2, 'list_1: 7')
    io_predicted_str += _return_print_event(2, 'list_2: 6')
    io_predicted_str += _return_print_event(1, '😓 No someitems in common')
    io_predicted_str += _return_print_event(1, 'list_1')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({2: 3, 1: 4}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({1, 2}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems in common')
    io_predicted_str += _return_print_event(1, 'list_2')
    io_predicted_str += _return_print_event(2, '😓 Exclusive someitems:')
    io_predicted_str += _return_pprint(2, _sorted({3, 4, 's'}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems (value,count):')
    io_predicted_str += _return_pprint(2, _sorted({4: 2, 's': 3}))
    io_predicted_str += _return_print_event(2, '😓 Duplicates someitems exclusive:')
    io_predicted_str += _return_pprint(2, _sorted({4, 's'}))
    io_predicted_str += _return_print_event(2, '✅ No duplicates someitems in common')
    assert '' == io_out
    metadata_report = lists_metadata['report']
    assert io_predicted_str == metadata_report
