import io
from collections import Counter

from .. import pd_format
from . import _module_report_formatting as f


def compare_lists(
    list_1: list,
    list_2: list,
    show_common_items: bool = False,
    list_1_name: str = 'list_1',
    list_2_name: str = 'list_2',
    type_name: str = 'item',
    type_name_plural: str = 'items',
    report_print: bool = False,
) -> tuple[bool, dict]:
    """Compares two lists, can show a report.

    The report does the following:
    - print "Comparing {type_name_plural}"
    - print if lists are equal
    - if lists are equal print duplicates
    - print if lists' length is equal
    - print if there are common items between both lists (if show_common_items==True shows common items)
    - print lists' exclusive items
    - print lists' duplicates

    Parameters
    ----------
    list_1 : list
        First list.
    list_2 : list
        Second list.
    show_common_items : bool, optional
        Wether to show common items in both lists in the report.
    list_1_name : str, optional
        First list name, by default 'list_1'.
    list_2_name : str, optional
        Second list name, by default 'list_2'.
    type_name : str, optional
        Type to show in the report, by default 'item'.
    type_name_plural : str, optional
        Plural of type to show in the report, by default 'items'.
    report_print : bool, optional
        Whether to show the report, by default False.

    Returns
    -------
    tuple[bool, dict]
        Explanation:
        - <b>tuple[0]</b>: True or False if lists are equal.
        - <b>tuple[1]</b>: Metadata dict. This contains:
            <ul>
                <li><b>'list_common_set'</b>: set. Items in both lists.</li>
                <li><b>'list_1_excl_set'</b>: set. Items only present in list_1.</li>
                <li><b>'list_2_excl_set'</b>: set. Items only present in list_2.</li>
                <li><b>'list_1_dups_dict'</b>: dict(item:count). Items duplicated in list_1 with their respective count.</li>
                <li><b>'list_2_dups_dict'</b>: dict(item:count). Items duplicated in list_2 with their respective count.</li>
                <li><b>'report'</b>: str. The generated report, this stores the report even if it wasn't shown when executing this function.</li>
            </ul>

    Raises
    ------
    ValueError
        Raised if either list_1 or list_2 are not of type list.
    ValueError
        Raised if either list_1_name, list_2_name, type_name or type_name_plural are not of type str.
    """
    # Type validation
    # ************************************
    if not isinstance(list_1, list) or not isinstance(list_2, list):
        raise ValueError('list_1 and list_2 must be of type list.')
    if (
        not isinstance(list_1_name, str)
        or not isinstance(list_2_name, str)
        or not isinstance(type_name, str)
        or not isinstance(type_name_plural, str)
    ):
        raise ValueError(
            'list_1_name, list_2_name, type_name and type_name_plural must be of type str.'
        )

    # Computations
    # ************************************
    list_1_set = set(list_1)
    list_2_set = set(list_2)
    # Items that exist only in either list
    list_1_excl_set = list_1_set - list_2_set
    list_2_excl_set = list_2_set - list_1_set
    list_common_set = set(list_1_set - list_1_excl_set)
    list_1_dups_dict = {i: q for i, q in Counter(list_1).items() if q > 1}
    list_2_dups_dict = {i: q for i, q in Counter(list_2).items() if q > 1}
    list_1_dups_set = set(list_1_dups_dict)
    list_2_dups_set = set(list_2_dups_dict)
    list_1_dups_exclusive_set = list_1_dups_set - list_common_set
    list_2_dups_exclusive_set = list_2_dups_set - list_common_set
    list_1_dups_common_set = list_1_dups_set.intersection(list_2_dups_set)
    list_2_dups_common_set = list_2_dups_set.intersection(list_1_dups_set)

    # Report
    # ************************************
    stream = io.StringIO()
    f.print_title(
        1, f'Comparing {type_name_plural} from [{list_1_name}] and [{list_2_name}]', file=stream
    )
    if list_1 == list_2:
        f.print_event(1, f'✅ {type_name_plural.capitalize()} equal', file=stream)

        if show_common_items is True:
            f.print_event(1, f'✅ {type_name_plural.capitalize()} in common:', file=stream)
            f.pprint_wrap(1, pd_format.obj_as_sorted_list(list_common_set), stream=stream)

        if len(list_1_dups_dict) == 0:
            f.print_event(1, f'✅ No duplicates {type_name_plural}', file=stream)
        else:
            f.print_event(1, f'😓 Duplicates {type_name_plural} (value,count):', file=stream)
            f.pprint_wrap(1, pd_format.obj_as_sorted_list(list_1_dups_dict), stream=stream)
    else:
        f.print_event(1, f'😓 {type_name_plural.capitalize()} not equal', file=stream)

        # Print length match
        if len(list_1) == len(list_2):
            f.print_event(
                1, f'✅ {type_name_plural.capitalize()} lengths match ({len(list_1)})', file=stream
            )
        else:
            f.print_event(
                1, f'😓 {type_name_plural.capitalize()} lengths don\'t match', file=stream
            )
            lgnd_maxlen = max(len(list_1_name), len(list_2_name))
            f.print_event(2, f'{list_1_name:<{lgnd_maxlen}}: {len(list_1)}', file=stream)
            f.print_event(2, f'{list_2_name:<{lgnd_maxlen}}: {len(list_2)}', file=stream)

        if len(list_common_set) > 0:
            if show_common_items is True:
                f.print_event(1, f'✅ {type_name_plural.capitalize()} in common:', file=stream)
                f.pprint_wrap(1, pd_format.obj_as_sorted_list(list_common_set), stream=stream)
            else:
                f.print_event(1, f'✅ Some {type_name_plural} in common (not shown)', file=stream)
        else:
            f.print_event(1, f'😓 No {type_name_plural} in common', file=stream)

        # Print specifics for each list
        for name, excl_items_set, dups_dict, dups_excl_set, dups_common_set in (
            (
                list_1_name,
                list_1_excl_set,
                list_1_dups_dict,
                list_1_dups_exclusive_set,
                list_1_dups_common_set,
            ),
            (
                list_2_name,
                list_2_excl_set,
                list_2_dups_dict,
                list_2_dups_exclusive_set,
                list_2_dups_common_set,
            ),
        ):
            f.print_event(1, f'{name}', file=stream)  # List name
            # Print exclusive items
            if len(excl_items_set) == 0:
                f.print_event(2, f'✅ No exclusive {type_name_plural}', file=stream)
            else:
                f.print_event(2, f'😓 Exclusive {type_name_plural}:', file=stream)
                f.pprint_wrap(2, pd_format.obj_as_sorted_list(excl_items_set), stream=stream)
            # Print duplicates
            if len(dups_dict) == 0:
                f.print_event(2, f'✅ No duplicates {type_name_plural}', file=stream)
            else:
                # Print value and the number of times duplicated
                f.print_event(2, f'😓 Duplicates {type_name_plural} (value,count):', file=stream)
                f.pprint_wrap(2, pd_format.obj_as_sorted_list(dups_dict), stream=stream)
                # Print duplicates exclusive items, value list only
                if len(dups_excl_set) == 0:
                    f.print_event(2, f'✅ No duplicates {type_name_plural} exclusive', file=stream)
                else:
                    f.print_event(2, f'😓 Duplicates {type_name_plural} exclusive:', file=stream)
                    f.pprint_wrap(2, pd_format.obj_as_sorted_list(dups_excl_set), stream=stream)
                # Print duplicates in common items, value list only
                if len(dups_common_set) == 0:
                    f.print_event(2, f'✅ No duplicates {type_name_plural} in common', file=stream)
                else:
                    f.print_event(2, f'😓 Duplicates {type_name_plural} in common:', file=stream)
                    f.pprint_wrap(2, pd_format.obj_as_sorted_list(dups_common_set), stream=stream)

    if report_print is True:
        print(stream.getvalue(), end='')

    # Return
    # ************************************
    return (list_1 == list_2), {
        'list_common_set': list_common_set,
        'list_1_excl_set': list_1_excl_set,
        'list_2_excl_set': list_2_excl_set,
        'list_1_dups_dict': list_1_dups_dict,
        'list_2_dups_dict': list_2_dups_dict,
        'report': stream.getvalue(),
    }
