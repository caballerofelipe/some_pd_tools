import io
from collections import Counter
from contextlib import redirect_stdout

import pandas as pd

from . import pd_format
from . import _report_formatting as f

__all__ = [
    'compare',
    'compare_lists',
    'compare_dtypes',
]

# TODO: review TODO.md


def compare_lists(
    list_1: list,
    list_2: list,
    show_common_items: bool = False,
    list_1_name: str = 'list_1',
    list_2_name: str = 'list_2',
    type_name: str = 'item',
    type_name_plural: str = 'items',
    report: bool = False,
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
    report : bool, optional
        Whether to show the report, by default False.

    Returns
    -------
    tuple[bool, dict]
        - tuple[0]: True or False if lists are equal.
        - tuple[1]: Metadata dict. This contains:
          - 'list_common_set': items in both lists.
          - 'list_1_excl_set': items only present in list_1.
          - 'list_2_excl_set': items only present in list_2.
          - 'list_1_dups_dict': items duplicated in list_1.
          - 'list_2_dups_dict': items duplicated in list_2.
          - 'report': The generated report, this stores the report even if it wasn't shown when executing this function.

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

    if report is True:
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


def compare_dtypes(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    df1_name: str = 'df1',
    df2_name: str = 'df2',
    report: bool = False,
    show_all_dtypes=False,
) -> tuple[bool, dict]:
    """Compare dtypes for columns in two DataFrames.

    Some clarifications:
    - The order of the columns is irrelevant, they will be sorted alphabetically to do the dtype
      comparison.
    - The columns from both DataFrames must be equal, if they're not an Exception will be raised.
    - If columns are different and/or an Exception is raised, you can use the function `compare_lists()`
      to review the differences. If using `compare_lists()`, the result can be used to compare the
      DataFrames specifying only the common columns.
    - Duplicate columns are forbidden. If a comparison of duplicated columns is needed, rename them
      manually by index before calling this function. Example:

      ```python
      df.columns.values[0] = "same_name_0"
      df.columns.values[1] = "same_name_1"
      ```

      For a fuller example, see https://www.geeksforgeeks.org/rename-column-by-index-in-pandas/.

    Parameters
    ----------
    df1 : pd.DataFrame
        The first DataFrame to compare.
    df2 : pd.DataFrame
        The second DataFrame to compare.
    df1_name : str, optional
        The name to show for the first DataFrame, by default 'df1'.
    df2_name : str, optional
        The name to show for the second DataFrame, by default 'df2'.
    report : bool, optional
        Whether to show the comparison report, by default False
    show_all_dtypes : bool, optional
        Whether to show the columns that have the same dtype in the report, by default False.

    Returns
    -------
    tuple[bool, dict]
        - tuple[0]: True if all dtypes equal, False if not.
        - tuple[1]: Metadata dict. This contains:
          - 'dtypes_df': A DataFrame where the index the analyzed column and 3 columns:
            1. 'different' representing wether the column is different or not in both input DataFrames (True means different, False means equal).
            2. {df1_name} (stated name for first DataFrame): the dtype for the given column in df1.
            3. {df2_name} (stated name for second DataFrame): the dtype for the given column in df2.
          - 'report': The report, useful in case the param `report` is False.

    Raises
    ------
    ValueError
        If df1 or df2 are not of type DataFrame.
    ValueError
        If df1_name or df2_name are not of type str.
    ValueError
        If df1 and df2 columns are not equal (disregarding the order).
    ValueError
        If df1 and/or df2 have duplicate columns.
    """
    # Type validation
    # ************************************
    if not isinstance(df1, pd.DataFrame) or not isinstance(df2, pd.DataFrame):
        raise ValueError('df1 and df2 must be of type pd.DataFrame.')
    if not isinstance(df1_name, str) or not isinstance(df2_name, str):
        raise ValueError('df1_name and df2_name must be of type str.')

    stream_compare = io.StringIO()
    with redirect_stdout(stream_compare):
        lists_equal, lists_metadata = compare_lists(
            list(df1.columns),
            list(df2.columns),
            list_1_name=df1_name,
            list_2_name=df2_name,
            type_name='column',
            type_name_plural='columns',
            report=True,
        )
    # Lists aren't equal, raise Exception with the report using `compare_lists()`
    if not lists_equal:
        raise ValueError(
            f'df1 ({df1_name}) and df2 ({df2_name}) must have the same columns.'
            + f'\n{stream_compare.getvalue()}'
        )
    if len(lists_metadata['list_1_dups_dict']) > 0 or len(lists_metadata['list_2_dups_dict']) > 0:
        raise ValueError(
            f'df1 ({df1_name}) and df2 ({df2_name}) cannot have duplicate columns.'
            + f'\n{stream_compare.getvalue()}'
        )

    # Computations
    # ************************************
    df1_dtypes = df1.dtypes.sort_index().rename(df1_name)
    df2_dtypes = df2.dtypes.sort_index().rename(df2_name)
    cols_equal_dtypes_mask = df1_dtypes == df2_dtypes

    # Report
    # ************************************
    stream = io.StringIO()
    f.print_title(1, 'Comparing column dtypes', file=stream)
    if cols_equal_dtypes_mask.all(axis=None):
        f.print_event(1, '✅ Columns have equal dtypes', file=stream)
    else:
        f.print_event(1, '😓 Columns have different dtypes', file=stream)
    if not cols_equal_dtypes_mask.all(axis=None) or show_all_dtypes is True:
        # <Formatting computations>
        if show_all_dtypes is True:
            # Show all columns dtypes
            cols_to_show = list(cols_equal_dtypes_mask.index)
            cols_equality = list(cols_equal_dtypes_mask.values)
        else:
            # Filter only by not equal dtypes
            cols_to_show = list(cols_equal_dtypes_mask[~cols_equal_dtypes_mask].index)
            cols_equality = list(cols_equal_dtypes_mask[~cols_equal_dtypes_mask].values)
        legend = "column"
        equal_title = 'different'
        equal_tit_maxlen = len(equal_title)
        lgnd_maxlen = max([len(i) for i in cols_to_show])
        lgnd_maxlen = max(lgnd_maxlen, len(legend))
        df1types_col_len = [len(str(d)) for d in df1[cols_to_show].dtypes]
        df1types_col_len.append(len(df1_name))
        df1types_maxlen = max(df1types_col_len)
        df2types_col_len = [len(str(d)) for d in df2[cols_to_show].dtypes]
        df2types_col_len.append(len(df2_name))
        df2types_maxlen = max(df2types_col_len)
        # </Formatting computations>
        # Initial bar
        f.print_plain(
            1,
            f'|{"-"*lgnd_maxlen}|{"-"*equal_tit_maxlen}|{"-"*df1types_maxlen}'
            + f'|{"-"*df2types_maxlen}|',
            file=stream,
        )
        # Legend
        f.print_plain(
            1,
            f'|{legend:<{lgnd_maxlen}}|{equal_title}|{df1_name:<{df1types_maxlen}}'
            + f'|{df2_name:<{df2types_maxlen}}|',
            file=stream,
        )
        # Middle bar
        f.print_plain(
            1,
            f'|{"-"*lgnd_maxlen}|{"-"*equal_tit_maxlen}|{"-"*df1types_maxlen}'
            + f'|{"-"*df2types_maxlen}|',
            file=stream,
        )
        # Data
        for col_idx, col_name in enumerate(cols_to_show):
            f.print_plain(
                1,
                f'|{col_name:<{lgnd_maxlen}}'
                + f'|{"" if cols_equality[col_idx] else "*":^{equal_tit_maxlen}}'
                + f'|{str(df1_dtypes[col_name]):<{df1types_maxlen}}'
                + f'|{str(df2_dtypes[col_name]):<{df2types_maxlen}}'
                + '|',
                file=stream,
            )
        # Final bar
        f.print_plain(
            1,
            f'|{"-"*lgnd_maxlen}|{"-"*equal_tit_maxlen}|{"-"*df1types_maxlen}'
            + f'|{"-"*df2types_maxlen}|',
            file=stream,
        )

    if report is True:
        print(stream.getvalue(), end='')

    # Return
    # ************************************
    # Merge `df1_types` and `df2_types`
    dtypes_df = pd.merge(
        df1_dtypes,
        df2_dtypes,
        left_index=True,
        right_index=True,
        how='inner',
    )
    # Add `cols_equal_dtypes_mask`
    dtypes_df = pd.merge(
        pd.DataFrame(~cols_equal_dtypes_mask, columns=['different']),
        dtypes_df,
        left_index=True,
        right_index=True,
        how='inner',
    )
    return bool(cols_equal_dtypes_mask.all(axis=None)), {
        'dtypes_df': dtypes_df,
        'report': stream.getvalue(),
    }


def _save_compared_df(
    joined_df: pd.DataFrame, diff_rows, all_diff_cols, path: str, fixed_cols: list
):
    # Different columns with different rows
    df_to_save = joined_df.loc[
        diff_rows,
        [*fixed_cols, *all_diff_cols],
    ].copy()

    for col in joined_df.columns:
        if pd.api.types.is_datetime64_any_dtype(joined_df[col]):
            joined_df[col] = joined_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

    # df_to_save.to_excel(f'tmp_comparison_{now_str()}.xlsx', freeze_panes=(1, 6))

    # From https://xlsxwriter.readthedocs.io/example_pandas_autofilter.html

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(path, engine="xlsxwriter")

    show_index = True
    add_if_show_index = 1 if show_index is True else 0

    # Convert the DataFrame to an XlsxWriter Excel object. We also turn off the
    # index column at the left of the output DataFrame.
    df_to_save.to_excel(
        writer,
        sheet_name="Sheet1",
        index=show_index,
    )

    # Get the xlsxwriter workbook and worksheet objects.
    # workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    # Get the dimensions of the DataFrame.
    (max_row, max_col) = df_to_save.shape

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


def _dtypes_simp_and_eqlty_check(
    df1,
    df2,
    df1_name,
    df2_name,
    show_all_dtypes,
    str_io,
):
    '''This does:
    - Simplifies dtype for both DataFrames
    - Compares dtypes (and shows report if changed)
    - Does an equality check.
    - Then returns, the returned information is used in the `compare()` flow.

    This was originally part of `compare()` but since it was done more than once, was exported as a function.
    '''
    # dtypes simplification
    f.print_title(1, 'Trying to simplify dtypes', file=str_io)
    df1_original_dtypes = df1.dtypes
    df2_original_dtypes = df2.dtypes
    df1 = pd_format.simplify_dtypes(df1)
    df2 = pd_format.simplify_dtypes(df2)
    if df1.dtypes.equals(df1_original_dtypes):
        f.print_event(1, f'✅ {df1_name}... already simplified', file=str_io)
    else:
        f.print_event(1, f'😓 {df1_name}... simplified', file=str_io)
    if df2.dtypes.equals(df2_original_dtypes):
        f.print_event(1, f'✅ {df2_name}... already simplified', file=str_io)
    else:
        f.print_event(1, f'😓 {df2_name}... simplified', file=str_io)

    changed_dtypes = (
        df1.dtypes.equals(df1_original_dtypes) is False
        or df2.dtypes.equals(df2_original_dtypes) is False
    )

    # dtypes comparison, values needed even if no dtype change happened
    dtypes_equality, dtypes_metadata = compare_dtypes(
        df1=df1,
        df2=df2,
        df1_name=df1_name,
        df2_name=df2_name,
        show_all_dtypes=show_all_dtypes,
        report=False,  # No report if no dtypes changes were done
    )

    if changed_dtypes is True:
        f.print_event(1, '😓 dtypes changed', file=str_io)
        # Show report if dtypes changed
        print(dtypes_metadata['report'], end='', file=str_io)
    else:
        f.print_event(1, '✅ No dtypes changed', file=str_io)
        # No report if no dtypes changes were done

    # Equality testing
    after_simp_equality = False
    if changed_dtypes:
        if dtypes_equality is True:
            f.print_title(1, 'Equality check', 'since dtypes are now equal', file=str_io)
            if df1.equals(df2):  # Are the dfs equal?
                f.print_result('🥳 Equal', file=str_io)
                after_simp_equality = True
                # NOTE: After this point a return should be done
                # This must be done after calling this function
            else:
                f.print_result('😡 Not equal', file=str_io)
                after_simp_equality = False
        else:
            f.print_title(1, 'Skipping equality check', 'since dtypes are not equal', file=str_io)
            after_simp_equality = False

    return (
        after_simp_equality,
        df1,
        df2,
        dtypes_equality,
        dtypes_metadata,
    )


def _returner_for_compare(
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
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    df1_name: str = 'df1',
    df2_name: str = 'df2',
    round_to: None | int | str = None,
    report: bool = True,
    show_common_cols: bool = False,
    show_common_idxs: bool = False,
    show_all_dtypes: bool = False,
    path: str = None,
    fixed_cols: list = None,
):
    '''
    Some notes for documenting:
    - The whole goal of this function is to find differences in DataFrames, once they are found to be equal, the comparison stops.
    - df1 and df2 are transformed into DataFrames before any comparing
    - The order of columns and indexes are not taken into account. Columns and indexes are sorted using
        `.sort_index(axis=0).sort_index(axis=1)`
    - Duplicate indexes and columns are not allowed, UNLESS `if df1_cp.equals(df2_cp)` is True, which means everything is equal.
    - When returning, if an equality is returned, use the functions to get to the point where equality was obtained.
    '''
    if not isinstance(df1, pd.DataFrame) or not isinstance(df2, pd.DataFrame):
        raise ValueError('df1 and df2 must be of type pd.DataFrame.')
    if not isinstance(df1_name, str) or not isinstance(df2_name, str):
        raise ValueError('df1_name and df2_name must be of type str.')
    if round_to is not None and (
        isinstance(round_to, bool)
        or (isinstance(round_to, int) and round_to < 0)
        or (isinstance(round_to, str) and round_to not in ('floor', 'ceil', 'trunc'))
        or (not isinstance(round_to, int) and not isinstance(round_to, str))
    ):
        raise ValueError(
            "round_to must be None, a positive integer or a string (either 'floor' or 'ceil')."
        )

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
            'round_to': round_to,
            'report': report,
            'show_common_cols': show_common_cols,
            'show_common_idxs': show_common_idxs,
            'show_all_dtypes': show_all_dtypes,
            'path': path,
            'fixed_cols': fixed_cols,
        }
    }

    # MARK: COPY
    # Copy DataFrames to avoid making any changes to them
    # *************************************************************************
    df1_cp = pd.DataFrame(df1).sort_index(axis=0).sort_index(axis=1).copy()
    df2_cp = pd.DataFrame(df2).sort_index(axis=0).sort_index(axis=1).copy()

    # MARK: EQLTY FULL
    # Check if both DataFrames are fully equal using Pandas function
    # *************************************************************************
    f.print_title(1, 'Equality check', 'full', file=str_io)
    if df1_cp.equals(df2_cp):  # Are the dfs equal?
        f.print_result('🥳 Equal', file=str_io)
        return _returner_for_compare(True, True, equality_metadata, str_io, report)
    else:
        f.print_result('😡 Not equal', file=str_io)

    # MARK: COMPARE COLUMNS
    # Compare columns, show report if `report==True`
    # and get common columns, extra columns for each DF
    # *************************************************************************
    cols_compare_equality, cols_compare_metadata = compare_lists(
        list_1=list(df1_cp.columns),
        list_2=list(df2_cp.columns),
        show_common_items=show_common_cols,
        list_1_name=df1_name,
        list_2_name=df2_name,
        type_name='column',
        type_name_plural='columns',
        report=False,
    )

    print(cols_compare_metadata['report'], end='', file=str_io)

    cols_common_set = cols_compare_metadata['list_common_set']
    cols_df1_excl_set = cols_compare_metadata['list_1_excl_set']
    cols_df2_excl_set = cols_compare_metadata['list_2_excl_set']
    cols_df1_dups_dict = cols_compare_metadata['list_1_dups_dict']
    cols_df2_dups_dict = cols_compare_metadata['list_2_dups_dict']

    # Duplicate columns dictionaries containing only common elements
    cols_df1_dups_common_dict = {
        val: count for val, count in cols_df1_dups_dict.items() if val in cols_common_set
    }
    cols_df2_dups_common_dict = {
        val: count for val, count in cols_df2_dups_dict.items() if val in cols_common_set
    }

    equality_metadata = {
        **equality_metadata,
        'cols_compare_equality': cols_compare_equality,
        'cols_common_set': cols_common_set,
        'cols_df1_excl_set': cols_df1_excl_set,
        'cols_df2_excl_set': cols_df2_excl_set,
        'cols_df1_dups_dict': cols_df1_dups_dict,
        'cols_df2_dups_dict': cols_df2_dups_dict,
        'cols_df1_dups_common_dict': cols_df1_dups_common_dict,
        'cols_df2_dups_common_dict': cols_df2_dups_common_dict,
    }
    cols_common_list = pd_format.obj_as_sorted_list(cols_common_set)
    if len(cols_df1_dups_common_dict) > 0 or len(cols_df2_dups_common_dict) > 0:
        error = '🛑 Duplicate common columns found. Only common non duplicates columns allowed, stopping compare and returning. Either change the columns\' names or compare only one of the duplicates columns at a time. Review the returned metadata (indexes \'cols_df1_dups_common_dict\' and \'cols_df1_dups_common_dict\'.)'
        tmp_stream = io.StringIO()
        f.print_event(1, error, file=tmp_stream)  # Used to print and to store result in metadata
        print(tmp_stream.getvalue(), end='', file=str_io)
        equality_metadata = {**equality_metadata, 'error': tmp_stream.getvalue()}
        return _returner_for_compare(False, False, equality_metadata, str_io, report)

    # MARK: COMPARE INDEXES
    # Compare indexes, show report if `report==True`
    # and get common indexes, extra indexes for each DF
    # *************************************************************************
    idxs_compare_equality, idxs_compare_metadata = compare_lists(
        list_1=list(df1_cp.index),
        list_2=list(df2_cp.index),
        show_common_items=show_common_idxs,
        list_1_name=df1_name,
        list_2_name=df2_name,
        type_name='index',
        type_name_plural='indexes',
        report=False,
    )

    print(idxs_compare_metadata['report'], end='', file=str_io)

    idxs_common_set = idxs_compare_metadata['list_common_set']
    idxs_df1_excl_set = idxs_compare_metadata['list_1_excl_set']
    idxs_df2_excl_set = idxs_compare_metadata['list_2_excl_set']
    idxs_df1_dups_dict = idxs_compare_metadata['list_1_dups_dict']
    idxs_df2_dups_dict = idxs_compare_metadata['list_2_dups_dict']

    # Duplicate indexes dictionaries containing only common elements
    idxs_df1_dups_common_dict = {
        val: count for val, count in idxs_df1_dups_dict.items() if val in idxs_common_set
    }
    idxs_df2_dups_common_dict = {
        val: count for val, count in idxs_df2_dups_dict.items() if val in idxs_common_set
    }

    equality_metadata = {
        **equality_metadata,
        'idxs_compare_equality': idxs_compare_equality,
        'idxs_common_set': idxs_common_set,
        'idxs_df1_excl_set': idxs_df1_excl_set,
        'idxs_df2_excl_set': idxs_df2_excl_set,
        'idxs_df1_dups_dict': idxs_df1_dups_dict,
        'idxs_df2_dups_dict': idxs_df2_dups_dict,
        'idxs_df1_dups_common_dict': idxs_df1_dups_common_dict,
        'idxs_df2_dups_common_dict': idxs_df2_dups_common_dict,
    }
    idxs_common_list = pd_format.obj_as_sorted_list(idxs_common_set)
    if len(idxs_df1_dups_common_dict) > 0 or len(idxs_df2_dups_common_dict) > 0:
        error = '🛑 Duplicate common indexes found. Only common non duplicates indexes allowed, stopping compare and returning. Either change the indexes\' names or compare only one of the duplicates indexes at a time. Review the returned metadata (indexes \'idxs_df1_dups_common_dict\' and \'idxs_df1_dups_common_dict\'.)'
        tmp_stream = io.StringIO()
        f.print_event(1, error, file=tmp_stream)  # Used to print and to store result in metadata
        print(tmp_stream.getvalue(), end='', file=str_io)
        equality_metadata = {**equality_metadata, 'error': tmp_stream.getvalue()}
        return _returner_for_compare(False, False, equality_metadata, str_io, report)

    # MARK: EQLTY 4COMMON
    # Only taking into consideration common columns and indexes
    # Check if both DataFrames are fully equal using Pandas function
    # *************************************************************************
    f.print_title(1, 'Checking common columns and indexes', file=str_io)
    are_all_cols_and_idxs_common = (
        len(cols_df1_excl_set) == 0
        and len(cols_df2_excl_set) == 0
        and len(idxs_df1_excl_set) == 0
        and len(idxs_df2_excl_set) == 0
    )

    # If both DataFrames have the same columns and indexes,
    # df{1,2}_common is indeed equal to df{1,2}_cp
    # but to avoid duplicating code, df{1,2}_common is used from this point on
    df1_common = df1_cp.loc[idxs_common_list, cols_common_list]
    df2_common = df2_cp.loc[idxs_common_list, cols_common_list]

    # Do both DataFrames have no exclusive columns and indexes?
    if are_all_cols_and_idxs_common:
        f.print_event(1, '✅ Columns and indexes are equal in both DataFrames', file=str_io)
    else:
        f.print_event(1, '😓 Columns and indexes are not equal in both DataFrames', file=str_io)
        f.print_event(
            1, '😈 From this point on, comparing only common columns and indexes', file=str_io
        )

        # Equality check for common columns and indexes
        f.print_title(1, 'Equality check', 'for common columns and indexes', file=str_io)
        if df1_common.equals(df2_common):  # Are the dfs equal?
            f.print_result('🥳 Equal', file=str_io)
            return _returner_for_compare(False, True, equality_metadata, str_io, report)
        else:
            f.print_result('😡 Not equal', file=str_io)

    # MARK: DTYPES COMP
    # dtypes comparison
    # *************************************************************************
    common_cols_dtypes_equality, common_cols_dtypes_metadata = compare_dtypes(
        df1=df1_common,
        df2=df2_common,
        df1_name=df1_name,
        df2_name=df2_name,
        show_all_dtypes=show_all_dtypes,
        report=False,
    )
    print(common_cols_dtypes_metadata['report'], end='', file=str_io)
    equality_metadata = {
        **equality_metadata,
        'common_cols_dtypes_equality': common_cols_dtypes_equality,
        'common_cols_dtypes_df': common_cols_dtypes_metadata['dtypes_df'],
    }

    # MARK: DTYPES SIMP
    # dtypes simplification, dtypes comparison and testing equality afterwards
    # *************************************************************************
    if common_cols_dtypes_equality is False:
        f.print_title(1, 'Since dtypes are different, will try to simplify', file=str_io)
        (
            after_simp_equality,
            df1_common,
            df2_common,
            common_cols_dtypes_simplified_equality,
            common_cols_dtypes_simplified_metadata,
        ) = _dtypes_simp_and_eqlty_check(
            df1=df1_common,
            df2=df2_common,
            df1_name=df1_name,
            df2_name=df2_name,
            show_all_dtypes=show_all_dtypes,
            str_io=str_io,
        )

        equality_metadata = {
            **equality_metadata,
            'common_cols_dtypes_simplified_equality': common_cols_dtypes_simplified_equality,
            'common_cols_dtypes_simplified_df': common_cols_dtypes_simplified_metadata['dtypes_df'],
        }

        if after_simp_equality is True:
            return _returner_for_compare(False, True, equality_metadata, str_io, report)

    # MARK: ROUND_TO
    # Rounding numeric columns.
    # *************************************************************************
    if round_to is not None:
        f.print_title(1, f'Rounding [round_to={round_to}]', file=str_io)
        df1_common = pd_format.approximate(df1_common, round_to=round_to)
        df2_common = pd_format.approximate(df2_common, round_to=round_to)

        # MARK: ROUND/DTYPES SIMP
        # if rounding was applied
        # dtypes simplification, dtypes comparison and testing equality afterwards
        # *************************************************************************
        (
            after_round_and_simp_equality,
            df1_common,
            df2_common,
            common_cols_dtypes_simplified_post_round_equality,
            common_cols_dtypes_simplified_post_round_metadata,
        ) = _dtypes_simp_and_eqlty_check(
            df1=df1_common,
            df2=df2_common,
            df1_name=df1_name,
            df2_name=df2_name,
            show_all_dtypes=show_all_dtypes,
            str_io=str_io,
        )

        equality_metadata = {
            **equality_metadata,
            'common_cols_dtypes_simplified_post_round_equality': common_cols_dtypes_simplified_post_round_equality,
            'common_cols_dtypes_simplified_post_round_df': common_cols_dtypes_simplified_post_round_metadata[
                'dtypes_df'
            ],
        }

        if after_round_and_simp_equality is True:
            return _returner_for_compare(False, True, equality_metadata, str_io, report)

    # MARK: COMPARE VALUES
    # Comparing values
    # *************************************************************************
    f.print_title(1, 'Comparing values', file=str_io)

    # The usual predictable equality BUT this outputs False when two 'nan' values are compared
    equal_mask_normal = df1_common == df2_common
    # There's a workaround to check if both values in each columns are 'nan'
    #  Compare each column to itself, if the result is different the value is 'nan'
    #  If this happens to both columns, that means both columns are 'nan' and their values are equal
    #   see: # https://stackoverflow.com/a/19322739/1071459
    equal_mask_for_nan = (df1_common != df1_common) & (df2_common != df2_common)
    # If either mask is True, we consider it to be True
    equal_mask_df = equal_mask_normal | equal_mask_for_nan

    if equal_mask_df.all(axis=None):
        f.print_result('🥸 Equal values', file=str_io)
        return _returner_for_compare(False, True, equality_metadata, str_io, report)

    diff_columns_list = list(equal_mask_df.columns[~(equal_mask_df.all(axis=0))].sort_values())
    f.print_event(1, f'😓 Not equal columns (count[{len(diff_columns_list)}]):', file=str_io)
    f.pprint_wrap(1, pd_format.obj_as_sorted_list(diff_columns_list), stream=str_io)

    diff_rows_list = list(equal_mask_df.index[~equal_mask_df.all(axis=1)].sort_values())
    f.print_event(1, f'😓 Not equal rows (count[{len(diff_rows_list)}]):', file=str_io)
    f.pprint_wrap(1, pd_format.obj_as_sorted_list(diff_rows_list), stream=str_io)

    # MARK: JOINED DF
    # Creating joined_df
    # *************************************************************************
    joined_df = (
        df1_cp[cols_common_list]
        #
        .join(df2_cp[cols_common_list], lsuffix=f'_{df1_name}', rsuffix=f'_{df2_name}')
    )
    joined_df = df1_cp[[*fixed_cols]].join(joined_df)

    # Create a new column with suffix '_diff' to explicitly show if there's a difference
    new_diff_columns = [f'{col}_diff' for col in diff_columns_list]
    joined_df[new_diff_columns] = ''  # The new diff columns are empty

    # Add the word 'diff' where a difference exists
    for col in diff_columns_list:
        # TODO: This equality must check for nan equality
        diff_rows_for_col_mask = joined_df[f'{col}_{df1_name}'] != joined_df[f'{col}_{df2_name}']
        joined_df.loc[diff_rows_for_col_mask, f'{col}_diff'] = 'diff'

    # MARK: DF W/DIFF ROWS/COLS
    # Create a DataFrame containing the union of different rows and different columns,
    # including the diff columns.
    # *************************************************************************

    # TODO: review, might be able to remove `cols_diff = [*diff_columns]`

    cols_diff = [*diff_columns_list]
    df1_cols_diff = [f'{c}_{df1_name}' for c in cols_diff]
    df2_cols_diff = [f'{c}_{df2_name}' for c in cols_diff]
    show_diff_cols = [f'{c}_diff' for c in cols_diff]
    cols_diff_from_1_2_show_diff = zip(df1_cols_diff, df2_cols_diff, show_diff_cols)
    all_diff_cols = [item for tup in cols_diff_from_1_2_show_diff for item in tup]
    diff_df = joined_df.loc[diff_rows_list, all_diff_cols]

    # MARK: EXCEL
    # Saving to Excel
    # *************************************************************************
    if path is not None:
        _save_compared_df(
            joined_df,
            diff_rows=diff_rows_list,
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
        'diff_columns': diff_columns_list,
        'diff_rows': diff_rows_list,
    }
    return _returner_for_compare(False, False, equality_metadata, str_io, report)
