import io
import pprint
import re
import textwrap
from collections import Counter
from contextlib import redirect_stdout

import pandas as pd

from . import pd_format

__all__ = ['compare', 'compare_lists', 'compare_dtypes']

_ = '''
TODO 2024-06-27:
  These should be computed manually with the other returned values.
- Add functions for where large code is done to keep code cleaner.
- Populate metadata while advancing, if a return is done, test metadata with pytest
- Check that all shown list are sorted lists and not sets or other data types
- Change printing level, 0=base
- Add doctrings.
- When using the original DataFrames, not the ones copied, be aware that the columns on the copies where sorted.
  Check if this is a problem somehow.
- Think if maybe a parameter should exist to do an ordered copy or not (columns and indexes) in `compare()`.
- Add documentation for all functions in README.md.
'''


def _print_title(
    level: int,
    title: str,
    subtitle: str = None,
    file: io.StringIO = None,
) -> None:
    print('————————————————————', file=file)
    print(
        textwrap.fill(f'{"#"*level} {title}', width=100),
        file=file,
    )
    if subtitle is not None:
        print(
            textwrap.fill(f'  ({subtitle})'),
            file=file,
        )


def _print_result(
    result: str,
    file: io.StringIO = None,
) -> None:
    print(
        textwrap.fill(f'<<< {result} >>>'),
        file=file,
    )


def _print_event(
    level: int,
    event: str,
    file: io.StringIO = None,
) -> None:
    level_str = '  ' * (level - 1)
    print(
        textwrap.fill(f'{level_str}-> {event}'),
        file=file,
    )


def _pprint(level: int, obj: object, stream: io.StringIO = None) -> None:
    level_str = '  ' * (level - 1)
    _stream = io.StringIO()
    pprint.pprint(obj, indent=1, width=100, compact=True, stream=_stream)
    to_print = level_str + _stream.getvalue()
    to_print = re.sub('\n.+', f'\n{level_str}', to_print)
    print(to_print, end='', file=stream)


def compare_lists(
    list1: list,
    list2: list,
    list1_name: str = 'list1',
    list2_name: str = 'list2',
    type_name: str = 'item',
    type_name_plural: str = 'items',
    report: bool = False,
) -> tuple[set, set, set, dict, dict]:
    """Compares two lists, can show a report.

    The report does the following:
    - print "Comparing {type_name_plural}"
    - print if lists are equal
    - print if lists' length is equal
    - print lists' exclusive items
    - print lists' duplicated

    Parameters
    ----------
    list1 : list
        First list.
    list2 : list
        Second list.
    list1_name : str, optional
        First list name, by default 'list1'.
    list2_name : str, optional
        Second list name, by default 'list2'.
    type_name : str, optional
        Type to show in the report, by default 'item'.
    type_name_plural : str, optional
        Plural of type to show in the report, by default 'items'.
    report : bool, optional
        Whether to show the report, by default False.

    Returns
    -------
    tuple[set, set, set, dict, dict]
        items in both lists, items present only in list1, items present only in list2, duplicate items in list1, duplicate items in list2

    Raises
    ------
    ValueError
        Raised if either list1 or list2 are not of type list.
    ValueError
        Raised if either list1_name, list2_name, type_name or type_name_plural are not of type str.
    """
    # Type validation
    # ************************************
    if not isinstance(list1, list) or not isinstance(list2, list):
        raise ValueError('list1 and list2 must be of type list.')
    if (
        not isinstance(list1_name, str)
        or not isinstance(list2_name, str)
        or not isinstance(type_name, str)
        or not isinstance(type_name_plural, str)
    ):
        raise ValueError(
            'list1_name, list2_name, type_name and type_name_plural must be of type str.'
        )

    # Computations
    # ************************************
    list1_set = set(list1)
    list2_set = set(list2)
    # Items that exist only in either list
    list1_exclusives_set = list1_set - list2_set
    list2_exclusives_set = list2_set - list1_set
    items_in_both_set = set(list1_set - list1_exclusives_set)
    list1_dups_dict = {i: q for i, q in Counter(list1).items() if q > 1}
    list2_dups_dict = {i: q for i, q in Counter(list2).items() if q > 1}
    list1_dups_set = set(list1_dups_dict)
    list2_dups_set = set(list2_dups_dict)
    list1_dups_exclusive_set = list1_dups_set - items_in_both_set
    list2_dups_exclusive_set = list2_dups_set - items_in_both_set
    list1_dups_common_set = list1_dups_set.intersection(list2_dups_set)
    list2_dups_common_set = list2_dups_set.intersection(list1_dups_set)

    # Report
    # ************************************
    if report is True:
        _print_title(1, f'Comparing {type_name_plural}')
        if list1 == list2:
            _print_event(1, f'✅ {type_name_plural.capitalize()} equal')
            if len(list1_dups_dict) == 0:
                _print_event(1, f'✅ No duplicate {type_name_plural}')
            else:
                _print_event(1, f'😓 Duplicate {type_name_plural} (value:count):')
                _pprint(1, list1_dups_dict)
        else:
            _print_event(1, f'😓 {type_name_plural.capitalize()} not equal')

            # Print length match
            if len(list1) == len(list2):
                _print_event(1, f'✅ {type_name_plural.capitalize()} lengths match')
            else:
                _print_event(1, f'😓 {type_name_plural.capitalize()} lengths don\'t match')
                lgnd_maxlen = max(len(list1_name), len(list2_name))
                _print_event(2, f'{list1_name:>{lgnd_maxlen}}: {len(list1)}')
                _print_event(2, f'{list2_name:>{lgnd_maxlen}}: {len(list2)}')

            if len(items_in_both_set) > 0:
                _print_event(1, f'✅ {type_name_plural.capitalize()} in common:')
                _pprint(1, items_in_both_set)
            else:
                _print_event(1, f'😓 No {type_name_plural} in common')

            # Print specifics for each list
            for name, exclusive_items, dups, dups_exclusive, dups_common in (
                (
                    list1_name,
                    list1_exclusives_set,
                    list1_dups_dict,
                    list1_dups_exclusive_set,
                    list1_dups_common_set,
                ),
                (
                    list2_name,
                    list2_exclusives_set,
                    list2_dups_dict,
                    list2_dups_exclusive_set,
                    list2_dups_common_set,
                ),
            ):
                _print_event(1, f'{name}')  # List name
                # Print exclusive items
                if len(exclusive_items) == 0:
                    _print_event(2, f'✅ No exclusive {type_name_plural}')
                else:
                    _print_event(2, f'😓 Exclusive {type_name_plural}:')
                    _pprint(2, exclusive_items)
                # Print duplicates
                if len(dups) == 0:
                    _print_event(2, f'✅ No duplicate {type_name_plural}')
                else:
                    # Print value and the number of times duplicated
                    _print_event(2, f'😓 Duplicate {type_name_plural} (value:count):')
                    _pprint(2, dups)
                    # Print duplicates exclusive items, value list only
                    if len(dups_exclusive) == 0:
                        _print_event(2, f'✅ No duplicate {type_name_plural} exclusive')
                    else:
                        _print_event(2, f'😓 Duplicate {type_name_plural} exclusive:')
                        _pprint(2, dups_exclusive)
                    # Print duplicates in common items, value list only
                    if len(dups_common) == 0:
                        _print_event(2, f'✅ No duplicate {type_name_plural} in common')
                    else:
                        _print_event(2, f'😓 Duplicate {type_name_plural} in common:')
                        _pprint(2, dups_common)

    # Return
    # ************************************
    return (
        items_in_both_set,
        list1_exclusives_set,
        list2_exclusives_set,
        list1_dups_dict,
        list2_dups_dict,
    )


def compare_dtypes(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    df1_name: str = 'df1',
    df2_name: str = 'df2',
    # type_name: str = 'item',
    # type_name_plural: str = 'items',
    report: bool = False,
) -> tuple[set, set, set, dict, dict]:
    # Type validation
    # ************************************
    if not isinstance(df1, pd.DataFrame) or not isinstance(df2, pd.DataFrame):
        raise ValueError('df1 and df2 must be of type pd.DataFrame.')
    if (
        not isinstance(df1_name, str)
        or not isinstance(df2_name, str)
        # or not isinstance(type_name, str)
        # or not isinstance(type_name_plural, str)
    ):
        raise ValueError('df1_name and df2_name must be of type str.')

    # Computations
    # ************************************
    (
        common_cols_set,
        df1_extra_cols_set,
        df2_extra_cols_set,
        df1_dups_cols_dict,
        df2_dups_cols_dict,
    ) = compare_lists(
        list1=list(df1.columns),
        list2=list(df2.columns),
        report=False,
    )
    # Duplicate columns dictionaries containing only common elements
    df1_dups_cols_common_dict = {
        val: count for val, count in df1_dups_cols_dict.items() if val in common_cols_set
    }
    df2_dups_cols_common_dict = {
        val: count for val, count in df2_dups_cols_dict.items() if val in common_cols_set
    }
    if df1_dups_cols_common_dict != df2_dups_cols_common_dict:
        raise ValueError('Duplicate common columns found but duplicates don\'t match.')

    common_cols_list = sorted(list(common_cols_set))
    common_cols_equal_dtypes_mask = (
        df1[common_cols_list].dtypes.sort_index() == df2[common_cols_list].dtypes.sort_index()
    )
    common_cols_equal_dtypes = df1[common_cols_list].dtypes.sort_index()[
        common_cols_equal_dtypes_mask
    ]
    common_cols_different_dtypes = df1[common_cols_list].dtypes.sort_index()[
        ~common_cols_equal_dtypes_mask
    ]

    # Report
    # ************************************
    if report is True:
        _print_title(1, 'Comparing dtypes for common columns')
        if common_cols_equal_dtypes_mask.all(axis=None):
            _print_event(1, '✅ No different dtypes')
        else:
            _print_event(1, '😓 Different dtypes')
            # <Formatting computations>
            legend = "col\\dataframe"
            lgnd_maxlen = max([len(i) for i in common_cols_different_dtypes.index])
            lgnd_maxlen = max(lgnd_maxlen, len(legend))
            diff_dtypes_cols = common_cols_different_dtypes.index
            df1types_col_len = [len(str(d)) for d in df1[diff_dtypes_cols].dtypes]
            df1types_col_len.append(len(df1_name))
            df1types_maxlen = max(df1types_col_len)
            df2types_col_len = [len(str(d)) for d in df2[diff_dtypes_cols].dtypes]
            df2types_col_len.append(len(df2_name))
            df2types_maxlen = max(df2types_col_len)
            # </Formatting computations>
            print(
                f'|{legend:<{lgnd_maxlen}}|{df1_name:<{df1types_maxlen}}|{df2_name:<{df2types_maxlen}}|'
            )
            print(f'|{"-"*lgnd_maxlen}|{"-"*df1types_maxlen}|{"-"*df2types_maxlen}|')
            for idx in common_cols_different_dtypes.index:
                print(
                    f'|{idx:<{lgnd_maxlen}}|{str(df1[idx].dtype):<{df1types_maxlen}}|{str(df2[idx].dtype):<{df2types_maxlen}}|',
                )

    # Return
    # ************************************
    return (
        common_cols_set,
        df1_extra_cols_set,
        df2_extra_cols_set,
        df1_dups_cols_dict,
        df2_dups_cols_dict,
    )


def _save_compared_df(
    joined_df: pd.DataFrame, diff_rows, all_diff_cols, path: str, fixed_cols: list
):
    # Different columns with different rows
    df_tosave = joined_df.loc[
        diff_rows,
        [*fixed_cols, *all_diff_cols],
    ].copy()

    for col in joined_df.columns:
        if pd.api.types.is_datetime64_any_dtype(joined_df[col]):
            joined_df[col] = joined_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

    # df_tosave.to_excel(f'tmp_comparison_{now_str()}.xlsx', freeze_panes=(1, 6))

    # From https://xlsxwriter.readthedocs.io/example_pandas_autofilter.html

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(path, engine="xlsxwriter")

    show_index = True
    add_if_show_index = 1 if show_index is True else 0

    # Convert the dataframe to an XlsxWriter Excel object. We also turn off the
    # index column at the left of the output dataframe.
    df_tosave.to_excel(
        writer,
        sheet_name="Sheet1",
        index=show_index,
    )

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df_tosave.shape

    # # Make the columns wider for clarity.
    # worksheet.set_column(0, max_col, 12)

    # Set the autofilter.
    worksheet.autofilter(0, 0, max_row, max_col)

    # From https://xlsxwriter.readthedocs.io/example_panes.html
    worksheet.freeze_panes(1, len(fixed_cols) + add_if_show_index)

    # From https://stackoverflow.com/a/75120836/1071459
    worksheet.autofit()

    # Close the Pandas Excel writer and output the Excel file.
    writer.close()


def fnreturn(
    equality_full: bool,
    equality_partial: bool,
    equality_metadata: dict,
    str_io: io.StringIO,
    report: bool,
) -> tuple[bool, bool, dict]:
    equality_metadata = {**equality_metadata, 'report': str_io.getvalue()}
    if report is True:
        print(str_io.getvalue(), end='')
    return [equality_full, equality_partial, equality_metadata]


def compare(
    df1: pd.DataFrame | pd.Series,
    df2: pd.DataFrame | pd.Series,
    df1_name: str = 'df1',
    df2_name: str = 'df2',
    show_common_cols: bool = False,
    show_common_idxs: bool = False,
    int64_to_float64: bool = False,
    round_to_decimals: int | bool = False,
    astype_str: bool = False,
    path: str = None,
    fixed_cols: list = None,
    report: bool = True,
):
    '''
    Some notes for documenting:
    - df1 and df2 are transformed into DataFrames before any comparing
    - The order of columns and indexes are not taken into account. Columns and indexes are sorted using
        `.sort_index(axis=0).sort_index(axis=1)`
    - Duplicate indexes and columns are allowed, but they must be duplicated equally in both DataFrames.
    '''
    if not isinstance(df1_name, str) or not isinstance(df2_name, str):
        raise ValueError('df1_name and df2_name must be of type str.')
    
    # Used to avoid dangerous default value
    # https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/dangerous-default-value.html
    if fixed_cols is None:
        fixed_cols = []

    # MARK: io.StringIO
    str_io = io.StringIO()
    # str_io = sys.stdout

    equality_metadata = {
        'params': {
            'df1': df1,
            'df2': df2,
            'df1_name': df1_name,
            'df2_name': df2_name,
            'show_common_cols': show_common_cols,
            'show_common_idxs': show_common_idxs,
            'int64_to_float64': int64_to_float64,
            'round_to_decimals': round_to_decimals,
            'astype_str': astype_str,
            'path': path,
            'fixed_cols': fixed_cols,
            'report': report,
        }
    }

    # MARK: COPY
    # Copy DataFrames to avoid making any changes to them
    # *************************************************************************
    df1_cp = pd.DataFrame(df1).sort_index(axis=0).sort_index(axis=1).copy()
    df2_cp = pd.DataFrame(df2).sort_index(axis=0).sort_index(axis=1).copy()

    # MARK: IS FULLY EQUAL
    # Check if both DataFrames are completely equal using Pandas function
    # *************************************************************************
    if df1_cp.equals(df2_cp):  # Are the dfs equal?
        _print_result('🥳 Fully equal', file=str_io)
        return fnreturn(True, False, equality_metadata, str_io, report)
    else:
        _print_result('😓 Not fully equal', file=str_io)

    # MARK: COMPARE COLUMNS
    # Compare columns, show report if `report==True`
    # and get common columns, extra columns for each DF
    # *************************************************************************
    with redirect_stdout(str_io):
        (
            common_cols_set,
            df1_extra_cols_set,
            df2_extra_cols_set,
            df1_dups_cols_dict,
            df2_dups_cols_dict,
        ) = compare_lists(
            list1=list(df1_cp.columns),
            list2=list(df2_cp.columns),
            list1_name=df1_name,
            list2_name=df2_name,
            type_name='column',
            type_name_plural='columns',
            report=report,
        )
    # Duplicate columns dictionaries containing only common elements
    df1_dups_cols_common_dict = {
        val: count for val, count in df1_dups_cols_dict.items() if val in common_cols_set
    }
    df2_dups_cols_common_dict = {
        val: count for val, count in df2_dups_cols_dict.items() if val in common_cols_set
    }
    equality_metadata = {
        **equality_metadata,
        'common_cols_set': common_cols_set,
        'df1_extra_cols_set': df1_extra_cols_set,
        'df2_extra_cols_set': df2_extra_cols_set,
        'df1_dups_cols_dict': df1_dups_cols_dict,
        'df2_dups_cols_dict': df2_dups_cols_dict,
        'df1_dups_cols_common_dict': df1_dups_cols_common_dict,
        'df2_dups_cols_common_dict': df2_dups_cols_common_dict,
    }
    common_cols_list = sorted(list(common_cols_set))
    if df1_dups_cols_common_dict != df2_dups_cols_common_dict:
        error = '🛑 Duplicate common columns found but duplicates don\'t match, aborting compare.'
        # IDEA: printing df1_dups_cols_dict and df2_dups_cols_dict but unit testing output isn't
        #       straightforward because dict might be unordered
        _print_event(1, error, file=str_io)
        equality_metadata = {**equality_metadata, 'error': error}
        return fnreturn(False, False, equality_metadata, str_io, report)

    # MARK: SHOW COMMON COLS
    # Show common columns if set in the options
    # *************************************************************************
    if show_common_cols is True:
        _print_title(1, 'Columns present in both DataFrames (intersection)', file=str_io)
        pprint.pprint(common_cols_list, indent=1, width=100, compact=True, stream=str_io)

    # MARK: COMPARE INDEXES
    # Compare indexes, show report if `report==True`
    # and get common indexes, extra indexes for each DF
    # *************************************************************************
    with redirect_stdout(str_io):
        (
            common_idxs_set,
            df1_extra_idxs_set,
            df2_extra_idxs_set,
            df1_dups_idxs_dict,
            df2_dups_idxs_dict,
        ) = compare_lists(
            list1=list(df1_cp.index),
            list2=list(df2_cp.index),
            list1_name=df1_name,
            list2_name=df2_name,
            type_name='index',
            type_name_plural='indexes',
            report=report,
        )
    # Duplicate indexes dictionaries containing only common elements
    df1_dups_idxs_common_dict = {
        val: count for val, count in df1_dups_idxs_dict.items() if val in common_idxs_set
    }
    df2_dups_idxs_common_dict = {
        val: count for val, count in df2_dups_idxs_dict.items() if val in common_idxs_set
    }
    equality_metadata = {
        **equality_metadata,
        'common_idxs_set': common_idxs_set,
        'df1_extra_idxs_set': df1_extra_idxs_set,
        'df2_extra_idxs_set': df2_extra_idxs_set,
        'df1_dups_idxs_dict': df1_dups_idxs_dict,
        'df2_dups_idxs_dict': df2_dups_idxs_dict,
        'df1_dups_idxs_common_dict': df1_dups_idxs_common_dict,
        'df2_dups_idxs_common_dict': df2_dups_idxs_common_dict,
    }
    common_idxs_list = sorted(list(common_idxs_set))
    if df1_dups_idxs_common_dict != df2_dups_idxs_common_dict:
        error = '🛑 Duplicate common indexes found but duplicates don\'t match, aborting compare.'
        # IDEA: printing df1_dups_idxs_dict and df2_dups_idxs_dict but unit testing output isn't
        #       straightforward because dict might be unordered
        _print_event(1, error, file=str_io)
        equality_metadata = {**equality_metadata, 'error': error}
        return fnreturn(False, False, equality_metadata, str_io, report)

    # MARK: SHOW COMMON IDXS
    # Show common indexes if set in the options
    # *************************************************************************
    if show_common_idxs is True:
        _print_title(1, 'Indexes present in both DataFrames (intersection)', file=str_io)
        pprint.pprint(common_idxs_list, indent=1, width=100, compact=True, stream=str_io)

    # MARK: COMPARE DTYPES
    # dtypes comparison
    # *************************************************************************
    with redirect_stdout(str_io):
        compare_dtypes(df1=df1_cp, df2=df2_cp, df1_name=df1_name, df2_name=df2_name, report=report)

    # MARK: SPECIAL SETTINGS
    # Special settings computations
    # *************************************************************************

    # TODO: review, might transform all numbers to float64
    # might use `is_numeric_dtype()`
    # importing: `from pandas.api.types import is_numeric_dtype`

    if int64_to_float64 is True:
        # Pass int64 to float64
        for tmp_df in (df1_cp, df2_cp):
            for col in tmp_df.columns:
                if str(tmp_df[col].dtype) in ('int64'):
                    tmp_df[col] = tmp_df[col].astype('float64')

    # Format as string with rounded decimals
    # TODO: review, might only round and in the next block transform to decimals
    if round_to_decimals is not False:
        df1_cp = df1_cp.apply(pd_format.format_nums, decimals=round_to_decimals)
        df2_cp = df2_cp.apply(pd_format.format_nums, decimals=round_to_decimals)

    if astype_str is True:
        df1_cp = df1_cp.astype(str)
        df2_cp = df2_cp.astype(str)

    # MARK: SPEC SETTINGS REPORT
    # Special settings report
    # *************************************************************************
    _print_title(1, 'Special settings used', file=str_io)
    if int64_to_float64 is True or round_to_decimals is not False or astype_str is True:
        if int64_to_float64 is True:
            _print_event(1, f'🧪 int64_to_float64[{int64_to_float64}]', file=str_io)
        if round_to_decimals is not False:
            _print_event(1, f'🧪 round_to_decimals[{round_to_decimals}]', file=str_io)
        if astype_str is True:
            _print_event(1, f'🧪 astype_str[{astype_str}]', file=str_io)
        # Equality with special settings
        _print_title(1, 'Equality with special settings', file=str_io)
        if df1_cp.equals(df2_cp):  # Are the dfs equal? (after Special Settings:)
            _print_result('🥸 Fully Equal (with special setting)', file=str_io)
            return fnreturn(False, True, equality_metadata, str_io, report)
        else:
            _print_result('😡 Not fully Equal (with special setting)', file=str_io)
    else:
        _print_event(1, 'No special settings.', file=str_io)

    # MARK: COMPARE VALUES
    # Comparing values
    # *************************************************************************
    _print_title(
        1,
        'Comparing values',
        'Only equal columns and equal indexes, see above non value differences',
        file=str_io,
    )

    df1_common_subset = df1_cp.loc[common_idxs_list, common_cols_list]
    df2_common_subset = df2_cp.loc[common_idxs_list, common_cols_list]

    # equal_mask_df = (
    #     df1_cp.loc[common_idxs_list, cols_in_both] == df2_cp.loc[common_idxs_list, cols_in_both]
    # )

    # The usual predictable equality BUT this outputs False when two 'nan' values are compared
    equal_mask_normal = df1_common_subset == df2_common_subset
    # There's a workaround to check if both values in each columns are 'nan'
    #  Compare each column to itself, if the result is different the value is 'nan'
    #  If this happens to both columns, that means both columns are 'nan' and their values are equal
    #   see: # https://stackoverflow.com/a/19322739/1071459
    equal_mask_for_nan = (df1_common_subset != df1_common_subset) & (
        df2_common_subset != df2_common_subset
    )
    # If either mask is True, we consider it to be True
    equal_mask_df = equal_mask_normal | equal_mask_for_nan

    if equal_mask_df.all(axis=None):
        _print_result('🥸 Equal values', file=str_io)
        return fnreturn(False, True, equality_metadata, str_io, report)

    diff_columns = equal_mask_df.columns[~(equal_mask_df.all(axis=0))].sort_values()
    _print_event(1, f'😓 Not equal columns (count[{len(diff_columns)}]):', file=str_io)
    pprint.pprint(list(diff_columns), indent=1, width=100, compact=True, stream=str_io)

    diff_rows = equal_mask_df.index[~equal_mask_df.all(axis=1)]
    _print_event(1, f'😓 Not equal rows (count[{len(diff_rows)}]):', file=str_io)
    pprint.pprint(list(diff_rows), indent=1, width=100, compact=True, stream=str_io)

    # MARK: JOINED DF
    # Creating joined_df
    # *************************************************************************
    joined_df = (
        df1_cp[common_cols_list]
        #
        .join(df2_cp[common_cols_list], lsuffix=f'_{df1_name}', rsuffix=f'_{df2_name}')
    )
    joined_df = df1_cp[[*fixed_cols]].join(joined_df)

    # Create a new column with suffix '_diff' to explicitly show if there's a difference
    new_diff_columns = [f'{col}_diff' for col in diff_columns]
    joined_df[new_diff_columns] = ''  # The new diff columns are empty

    # Add the word 'diff' where a difference exists
    for col in diff_columns:
        # TODO: This equality must check for nan equality
        diff_rows_for_col_mask = joined_df[f'{col}_{df1_name}'] != joined_df[f'{col}_{df2_name}']
        joined_df.loc[diff_rows_for_col_mask, f'{col}_diff'] = 'diff'

    # MARK: DF W/DIFF ROWS/COLS
    # Create a DataFrame containing the union of different rows and different columns,
    # including the diff columns.
    # *************************************************************************

    # TODO: review, might be able to remove `cols_diff = [*diff_columns]`

    cols_diff = [*diff_columns]
    df1_cols_diff = [f'{c}_{df1_name}' for c in cols_diff]
    df2_cols_diff = [f'{c}_{df2_name}' for c in cols_diff]
    show_diff_cols = [f'{c}_diff' for c in cols_diff]
    cols_diff_from_1_2_show_diff = zip(df1_cols_diff, df2_cols_diff, show_diff_cols)
    all_diff_cols = [item for tup in cols_diff_from_1_2_show_diff for item in tup]
    diff_df = joined_df.loc[diff_rows, all_diff_cols]

    # MARK: DIFF DF W/ORGN VALS
    # Creating a DataFrame where differences where found but with the original values
    # *************************************************************************

    # TODO: REVIEW

    diff_original_vals_df = pd.merge(
        df1_cp.loc[diff_rows, diff_columns],
        df2_cp.loc[diff_rows, diff_columns],
        left_index=True,
        right_index=True,
        suffixes=(f'_{df1_name}', f'_{df2_name}'),
    )

    # MARK: EXCEL
    # Saving to Excel
    # *************************************************************************
    if path != None:
        _save_compared_df(
            joined_df,
            diff_rows=diff_rows,
            all_diff_cols=all_diff_cols,
            path=path,
            fixed_cols=fixed_cols,
        )

    # MARK: RETURN
    equality_metadata = {
        **equality_metadata,
        'joined_df': joined_df,
        'equal_mask_df': equal_mask_df,
        'diff_df': diff_df,
        'diff_columns': diff_columns,
        'diff_rows': diff_rows,
        'diff_original_vals_df': diff_original_vals_df,
    }
    return fnreturn(False, False, equality_metadata, str_io, report)
