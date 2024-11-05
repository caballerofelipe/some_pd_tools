import io
import os
import pathlib

import pandas as pd

from .. import pd_format
from . import _module_report_formatting as f
from ._module_compare_dtypes import compare_dtypes
from ._module_compare_lists import compare_lists
from ._module_compute_equality_df import compute_equality_df

__all__ = [
    'compare',
]


def _save_excel(
    df: pd.DataFrame,
    path: str,
    freeze_on_colindex: list,
    datetime_rpl_str: str,
):
    if datetime_rpl_str != '':
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.strftime(datetime_rpl_str)

    # If needed directly save to Excel from Pandas
    # df.to_excel(f'tmp_comparison_{now_str()}.xlsx', freeze_panes=(1, 6))

    # From https://xlsxwriter.readthedocs.io/example_pandas_autofilter.html

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(path, engine="xlsxwriter")

    show_index = True
    add_if_show_index = 1 if show_index is True else 0

    # Convert the DataFrame to an XlsxWriter Excel object. We also turn off the
    # index column at the left of the output DataFrame.
    df.to_excel(
        writer,
        sheet_name="Sheet1",
        index=show_index,
    )

    # Get the xlsxwriter workbook and worksheet objects.
    # workbook = writer.book
    worksheet = writer.sheets["Sheet1"]

    # Get the dimensions of the DataFrame.
    (max_row, max_col) = df.shape

    # # Make the columns wider for clarity.
    # worksheet.set_column(0, max_col, 12)

    # Set the autofilter.
    worksheet.autofilter(1, 1, max_row, max_col)

    # From https://xlsxwriter.readthedocs.io/example_panes.html
    worksheet.freeze_panes(2, freeze_on_colindex + add_if_show_index)

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

    dtypes_simplified = (
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
        report_print=False,  # No report if no dtypes changes were done
    )

    after_simp_equality = False

    if dtypes_simplified is False:
        f.print_event(1, '✅ No dtypes changed', file=str_io)
        # No report if no dtypes changes were done
    else:
        f.print_event(1, '😓 dtypes changed', file=str_io)
        # Show report if dtypes changed
        print(dtypes_metadata['report'], end='', file=str_io)

        # Equality testing
        if dtypes_equality is False:
            f.print_title(1, 'Skipping equality check', 'since dtypes are not equal', file=str_io)
        else:
            f.print_title(1, 'Equality check', 'since dtypes are now equal', file=str_io)

            if df1.equals(df2):  # Are the dfs equal?
                f.print_result('🥳 Equal', file=str_io)
                after_simp_equality = True
                # NOTE: After this point a return from compare() should be done
                # this must be done after the return from ↑↓ this function
            else:
                f.print_result('😡 Not equal', file=str_io)

    return (
        dtypes_simplified,
        after_simp_equality,
        df1,
        df2,
        dtypes_equality,
        dtypes_metadata['dtypes_df'],
    )


def _returner_for_compare(
    equality_full: bool,
    equality_partial: bool,
    equality_metadata: dict,
    str_io: io.StringIO,
    report_print: bool,
    report_file_path,
) -> tuple[bool, bool, dict]:

    # Important note:
    # No verification of report_file_path and report_file_overwrite params
    # this was done in `compare()` as this function is not meant to be called by itself

    # This is here to include the report of "saving the report to file"
    # but the actual report saving to file is done later.
    if report_file_path is not None:
        f.print_title(1, 'Saving report file', os.path.realpath(report_file_path), file=str_io)
        equality_metadata['variables'].update(
            {'report_file_path': os.path.realpath(report_file_path)}
        )

    # Adding "Returning" to report
    f.print_title(
        1,
        title='Returning',
        subtitle=f'{equality_full}[equality_full], {equality_partial}[equality_partial], dict[equality_metadata]',
        file=str_io,
    )

    # Adding the report to the equality_metadata
    report = str_io.getvalue()
    equality_metadata.update({'report': report})

    # Printing the report
    if report_print is True:
        print(report, end='')

    # Saving report to file (optionally)
    if report_file_path is not None:
        with open(report_file_path, 'w', encoding='utf-8') as report_file:
            report_file.write(report)

    # The actual return
    return [equality_full, equality_partial, equality_metadata]


def compare(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    df1_name: str = 'df1',
    df2_name: str = 'df2',
    round_to: None | int | str = None,
    report_print: bool = True,
    report_file_path: None | str = None,
    report_file_overwrite: bool = False,
    show_common_cols: bool = False,
    show_common_idxs: bool = False,
    show_all_dtypes: bool = False,
    xls_path: None | str = None,
    xls_overwrite: bool = False,
    xls_compare_str_equal: str = '',
    xls_compare_str_diff: str = '*_diff_*',
    xls_fixed_cols: None | list = None,
    xls_datetime_rpl: str = '%Y-%m-%d %H:%M:%S',
) -> tuple[bool, bool, dict]:
    """Compares two DataFrames, creates a report and returns useful information (see the "Returns" section).

    **When is this function useful**: This function should be run when `df1.equals(df2)` is False, but if that returns True, there is no use for this function.

    **Columns and indexes are sorted initially**: The function's initial step is to sort the columns and rows of both DataFrames to do all further comparisons, it then internally does `df1.equals(df2)` with the sorted columns and rows. The sorting is done like `df.sort_index(axis=0).sort_index(axis=1)` which sorts by labels.

    **Important**: Duplicate indexes and columns are not allowed, UNLESS `df1_cp.equals(df2_cp)` is True, which means everything is equal.

    **Further reading**: This docstring contains documentation for this function but for an explanation of what is returned but see [this link](https://github.com/caballerofelipe/some_pd_tools/blob/main/Report\\%20and\\%20logic\\%20explanation\\%20for\\%20pd_compare.compare.md) to understand what the report shows, the logic behind it and what is returned.

    **Some notes**:
    - The whole goal of this function is to find differences in DataFrames, once they are found to be equal, the comparison stops. While looking for differences a report is created that will be printed (optionally), returned and saved to a file (optionally).
    - The report is the main focus of this function. The goal is to provide insight into how the DataFrames differ (if they do) the usage of the returned tuple might not be needed. However, if more information is needed or could be useful, the variables provided in the metadata might help.
    - This function is meant to be called interactively, possibly using Jupyter. It isn't meant to be run as a verification function, although it can be used like that, than might not be advised depending on the specific situation. The function will return a tuple of 3. In the returned tuple:
        - The first element will return True if everything is equal in the two DataFrame, this uses df1.equals(df2) but using the sorted columns and indexes.
        - The second element will return True if after some modification in the two DataFrames, everything is equal. This check happens after several points in the comparison process.
        - The third element will return metadata. This metadata depends on where in the function it was returned. The metadata is returned if the two DataFrames are equal, after some transformation. Or it is returned at the end of the function. The metadata values should be obtained with `.get()` since metadata is a dict and the key might not exist at a given point when returned.

    *A final note*: This functions is a little messy but I think: "doing something that works is better than not doing something perfect". There's room for improvement that might or might not be done in the future.

    Parameters
    ----------
    df1 : pd.DataFrame
        The first DataFrame to compare.
    df2 : pd.DataFrame
        The second DataFrame to compare.
    df1_name : str, optional
        The name to show in the report for the first DataFrame, by default 'df1'.
    df2_name : str, optional
        The name to show in the report for the second DataFrame, by default 'df2'.
    round_to : None | int | str, optional
        The way to approximate, by default None. Possible values and their meaning:
        - **None**: nothing is done.
        - **'int'**: rounds floating numbers to this decimal.
        - **'floor'**: does a floor operation on floats columns. Uses np.floor. From np.floor's documentation: "The floor of the scalar x is the largest integer i, such that i <= x."
        - **'ceil'**: does a ceil operation on floats columns. Uses np.ceil. From np.ceil's documentation: "The ceil of the scalar x is the smallest integer i, such that i >= x.".
        - **'trunc'**: removes decimals from floats columns. Uses np.trunc. From np.trunc's documentation: "The truncated value of the scalar x is the nearest integer i which is closer to zero than x is.".
    report_print : bool, optional
        Whether to print a report when the function ends, by default True.
    report_file_path : None | str, optional
        If set to a string, saves the report to the specified file, by default None.
    report_file_overwrite : bool, optional
        Whether to overwrite the specified path (when using report_file_path), by default False.
    show_common_cols : bool, optional
        Whether to show the common columns between the two compared DataFrames, by default False.
    show_common_idxs : bool, optional
        Whether to show the common indexes between the two compared DataFrames, by default False.
    show_all_dtypes : bool, optional
        For common columns, whether to show the columns that have the same dtype in the report, by default False.
    xls_path : None | str, optional
        If set to a string, creates an Excel file to the specified file, by default None.
    xls_overwrite : bool, optional
        Whether to overwrite the specified path (when using xls_overwrite), by default False.
    xls_compare_str_equal : str, optional
        A string to be placed inside a cell in the Excel file when both DataFrames contain the same value. Useful to know what cells are equal in the two DataFrames, by default empty. Can be used with the *find* function in Excel. By default ''.
    xls_compare_str_diff : str, optional
        A string to be placed inside a cell in the Excel file when the cell's value in the tow DataFrames is different. Useful to know what cells are different in the two DataFrames, by default "`*_diff_*`". Can be used with the *find* function in Excel. By default '*_diff_*'.
    xls_fixed_cols : None | list, optional
        A list of str containing columns that will be fixed in the generated Excel file. The columns in the list must exist in both DataFrames. By default None.
    xls_datetime_rpl : _type_, optional
        A string containing the format to be used for a column with a datetime64 dtype, useful to have a specific format for dates in Excel, by default '%Y-%m-%d %H:%M:%S'.

    Returns
    -------
    tuple[bool, bool, dict]
        Next is an explanation of what is returned but see [this link](https://github.com/caballerofelipe/some_pd_tools/blob/main/Report\\%20and\\%20logic\\%20explanation\\%20for\\%20pd_compare.compare.md) to understand what the report shows, the logic behind it and what is returned in the key 'variables' of the third tuple; this information was left out of this docstring to avoid too much information.
        - <b>tuple[0]</b>: bool. Checks for full equality for the two DataFrames **after** sorting columns and indexes.
            <ul>
                <li><b>True</b> if the two compared DataFrames are completely equal.</li>
                <li><b>False</b> otherwise.</li>
            </ul>
        - <b>tuple[1]</b>: bool. Checks for full equality for the two DataFrames **after** some operation done to them, see below for explanation of which operations are done.
            <ul>
                <li><b>True</b> if the two compared DataFrames are equal after some operation.</li>
                <li><b>False</b> otherwise.</li>
            </ul>
        - <b>tuple[2]</b>: dict. Metadata useful to keep track of what was done during the comparison:
            <ul>
                <li><b>['params']</b>: The list of parameters used in the function call.</li>
                <li><b>['variables']</b>: Some inner variables useful to keep track of what happened in the comparison and have information on what is different.</li>
                <li><b>['report']</b>: The same report, useful if the report wasn't printed (`report_print` == False) or to do something with it.</li>
            </ul>

    Raises
    ------
    ValueError
        Parameters are reviewed and an ValueError is raised if they don't have the specified values. No further documentation added to avoid too much information.
    """
    equality_metadata = {
        'params': {
            'df1': df1,
            'df2': df2,
            'df1_name': df1_name,
            'df2_name': df2_name,
            'round_to': round_to,
            'report_print': report_print,
            'report_file_path': report_file_path,
            'report_file_overwrite': report_file_overwrite,
            'show_common_cols': show_common_cols,
            'show_common_idxs': show_common_idxs,
            'show_all_dtypes': show_all_dtypes,
            'xls_path': xls_path,
            'xls_overwrite': xls_overwrite,
            'xls_compare_str_equal': xls_compare_str_equal,
            'xls_compare_str_diff': xls_compare_str_diff,
            'xls_fixed_cols': xls_fixed_cols,
            'xls_datetime_rpl': xls_datetime_rpl,
        },
        'variables': {},
    }

    if not isinstance(df1, pd.DataFrame) or not isinstance(df2, pd.DataFrame):
        raise ValueError('df1 and df2 must be of type pd.DataFrame.')

    if not isinstance(df1_name, str) or not isinstance(df2_name, str):
        raise ValueError('df1_name and df2_name must be of type str.')
    if df1_name == df2_name:
        raise ValueError('df1_name and df2_name must be different.')

    if round_to is not None and (
        isinstance(round_to, bool)
        or (isinstance(round_to, int) and round_to < 0)
        or (isinstance(round_to, str) and round_to not in ('floor', 'ceil', 'trunc'))
        or (not isinstance(round_to, int) and not isinstance(round_to, str))
    ):
        raise ValueError(
            "round_to must be None, a positive integer or a string (either 'floor' or 'ceil')."
        )

    if not isinstance(report_print, bool):
        raise ValueError('report_print must be of type bool.')

    if report_file_path is not None:
        if not isinstance(report_file_path, str):
            raise ValueError('report_file_path must be of type None or str')
        the_Path = pathlib.Path(report_file_path)
        if the_Path.is_dir():
            raise ValueError(f'report_file_path [{report_file_path}] cannot be a directory.')
        if report_file_overwrite is False and the_Path.is_file():
            raise ValueError(
                f'report_file_path [{report_file_path}] exists but report_file_overwrite is False.'
            )

    if xls_path is not None:
        if not isinstance(xls_path, str):
            raise ValueError('xls_path must be of type str.')
        the_Path = pathlib.Path(xls_path)
        if the_Path.is_dir():
            raise ValueError(f'xls_path [{xls_path}] cannot be a directory.')
        if xls_overwrite is False and the_Path.is_file():
            raise ValueError(f'xls_path [{xls_path}] exists but xls_overwrite is False.')

        if not isinstance(xls_compare_str_equal, str):
            raise ValueError('xls_compare_str_equal must be of type str.')
        if not isinstance(xls_compare_str_diff, str):
            raise ValueError('xls_compare_str_diff must be of type str.')

        # Used to avoid dangerous default value
        # https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/dangerous-default-value.html
        if xls_fixed_cols is None:
            xls_fixed_cols = []

        if not set(xls_fixed_cols) <= set(df1.columns):
            fixed_cols_not_present_sorted_list = pd_format.obj_as_sorted_list(
                set(xls_fixed_cols) - set(df1.columns)
            )
            raise ValueError(
                f'The following fixed_cols are not present in df1(df1_name={df1_name}): {fixed_cols_not_present_sorted_list}.'
            )
        if not set(xls_fixed_cols) <= set(df2.columns):
            fixed_cols_not_present_sorted_list = pd_format.obj_as_sorted_list(
                set(xls_fixed_cols) - set(df2.columns)
            )
            raise ValueError(
                f'The following fixed_cols are not present in df2(df2_name={df2_name}): {fixed_cols_not_present_sorted_list}.'
            )

        if not isinstance(xls_datetime_rpl, str):
            raise ValueError('xls_datetime_rpl must be of type str.')

    # MARK: io.StringIO
    str_io = io.StringIO()

    # MARK: COPY
    # Copy DataFrames to avoid making any changes to them
    # *************************************************************************
    df1_cp = pd.DataFrame(df1).sort_index(axis=0).sort_index(axis=1)
    df2_cp = pd.DataFrame(df2).sort_index(axis=0).sort_index(axis=1)

    # MARK: EQLTY FULL
    # Check if the two DataFrames are fully equal using Pandas' function
    # *************************************************************************
    f.print_title(1, 'Equality check', 'full', file=str_io)
    if df1_cp.equals(df2_cp):  # Are the dfs equal?
        f.print_result('🥳 Equal', file=str_io)
        return _returner_for_compare(
            equality_full=True,
            equality_partial=False,
            equality_metadata=equality_metadata,
            str_io=str_io,
            report_print=report_print,
            report_file_path=report_file_path,
        )
    else:
        f.print_result('😡 Not equal', file=str_io)

    # MARK: COMPARE COLUMNS
    # Compare columns and get common columns, extra columns for each DF
    # *************************************************************************
    cols_compare_equality, cols_compare_metadata = compare_lists(
        list_1=list(df1_cp.columns),
        list_2=list(df2_cp.columns),
        show_common_items=show_common_cols,
        list_1_name=df1_name,
        list_2_name=df2_name,
        type_name='column',
        type_name_plural='columns',
        report_print=False,
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

    cols_common_list_sorted = pd_format.obj_as_sorted_list(cols_common_set)

    equality_metadata['variables'].update(
        {
            'cols_compare_equality': cols_compare_equality,
            'cols_common_set': cols_common_set,
            'cols_common_list_sorted': cols_common_list_sorted,
            'cols_df1_excl_set': cols_df1_excl_set,
            'cols_df2_excl_set': cols_df2_excl_set,
            'cols_df1_dups_dict': cols_df1_dups_dict,
            'cols_df2_dups_dict': cols_df2_dups_dict,
            'cols_df1_dups_common_dict': cols_df1_dups_common_dict,
            'cols_df2_dups_common_dict': cols_df2_dups_common_dict,
        }
    )

    if len(cols_df1_dups_common_dict) > 0 or len(cols_df2_dups_common_dict) > 0:
        error = '🛑 Duplicate common columns found. Only common non duplicates columns allowed, stopping compare and returning. Either change the columns\' names or compare only one of the duplicates columns at a time. Review the returned metadata (indexes \'cols_df1_dups_common_dict\' and \'cols_df1_dups_common_dict\'.)'

        tmp_stream = io.StringIO()
        f.print_event(1, error, file=tmp_stream)  # Used to print and to store result in metadata
        print(tmp_stream.getvalue(), end='', file=str_io)

        equality_metadata['variables'].update({'error': error})

        return _returner_for_compare(
            equality_full=False,
            equality_partial=False,
            equality_metadata=equality_metadata,
            str_io=str_io,
            report_print=report_print,
            report_file_path=report_file_path,
        )

    # MARK: COMPARE INDEXES
    # Compare indexes and get common indexes, extra indexes for each DF
    # *************************************************************************
    idxs_compare_equality, idxs_compare_metadata = compare_lists(
        list_1=list(df1_cp.index),
        list_2=list(df2_cp.index),
        show_common_items=show_common_idxs,
        list_1_name=df1_name,
        list_2_name=df2_name,
        type_name='index',
        type_name_plural='indexes',
        report_print=False,
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

    idxs_common_list_sorted = pd_format.obj_as_sorted_list(idxs_common_set)

    equality_metadata['variables'].update(
        {
            'idxs_compare_equality': idxs_compare_equality,
            'idxs_common_set': idxs_common_set,
            'idxs_common_list_sorted': idxs_common_list_sorted,
            'idxs_df1_excl_set': idxs_df1_excl_set,
            'idxs_df2_excl_set': idxs_df2_excl_set,
            'idxs_df1_dups_dict': idxs_df1_dups_dict,
            'idxs_df2_dups_dict': idxs_df2_dups_dict,
            'idxs_df1_dups_common_dict': idxs_df1_dups_common_dict,
            'idxs_df2_dups_common_dict': idxs_df2_dups_common_dict,
        }
    )

    if len(idxs_df1_dups_common_dict) > 0 or len(idxs_df2_dups_common_dict) > 0:
        error = '🛑 Duplicate common indexes found. Only common non duplicates indexes allowed, stopping compare and returning. Either change the indexes\' names or compare only one of the duplicates indexes at a time. Review the returned metadata (indexes \'idxs_df1_dups_common_dict\' and \'idxs_df1_dups_common_dict\'.)'

        tmp_stream = io.StringIO()
        f.print_event(1, error, file=tmp_stream)  # Used to print and to store result in metadata
        print(tmp_stream.getvalue(), end='', file=str_io)

        equality_metadata['variables'].update({'error': error})

        return _returner_for_compare(
            equality_full=False,
            equality_partial=False,
            equality_metadata=equality_metadata,
            str_io=str_io,
            report_print=report_print,
            report_file_path=report_file_path,
        )

    # MARK: EQLTY 4 COMMON
    # Only taking into consideration common columns and indexes
    # Check if the two DataFrames are fully equal using Pandas' function
    # *************************************************************************
    f.print_title(1, 'Checking common columns and indexes', file=str_io)
    are_all_cols_and_idxs_common = (
        len(cols_df1_excl_set) == 0
        and len(cols_df2_excl_set) == 0
        and len(idxs_df1_excl_set) == 0
        and len(idxs_df2_excl_set) == 0
    )

    # If the two DataFrames have the same columns and indexes,
    # df{1,2}_common is indeed equal to df{1,2}_cp
    # but to avoid duplicating code, df{1,2}_common is used from this point on
    df1_common = df1_cp.loc[idxs_common_list_sorted, cols_common_list_sorted]
    df2_common = df2_cp.loc[idxs_common_list_sorted, cols_common_list_sorted]

    equality_metadata['variables'].update(
        {
            'df1_common': df1_common,
            'df2_common': df2_common,
        }
    )

    # Do the two DataFrames have no exclusive columns and indexes?
    if are_all_cols_and_idxs_common:
        f.print_event(1, '✅ Columns and indexes are equal in the two DataFrames', file=str_io)
    else:
        f.print_event(1, '😓 Columns and indexes are not equal in the two DataFrames', file=str_io)
        f.print_event(
            1, '😈 From this point on, comparing only common columns and indexes', file=str_io
        )

        # Equality check for common columns and indexes
        f.print_title(1, 'Equality check', 'for common columns and indexes', file=str_io)
        if df1_common.equals(df2_common):  # Are the dfs equal?
            f.print_result('🥳 Equal', file=str_io)
            return _returner_for_compare(
                equality_full=False,
                equality_partial=True,
                equality_metadata=equality_metadata,
                str_io=str_io,
                report_print=report_print,
                report_file_path=report_file_path,
            )
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
        report_print=False,
    )
    print(common_cols_dtypes_metadata['report'], end='', file=str_io)

    equality_metadata['variables'].update(
        {
            'common_cols_dtypes_equality': common_cols_dtypes_equality,
            'common_cols_dtypes_df': common_cols_dtypes_metadata['dtypes_df'],
        }
    )

    # MARK: DTYPES SIMP
    # dtypes simplification, dtypes comparison and testing equality afterwards
    # *************************************************************************
    if common_cols_dtypes_equality is False:
        f.print_title(1, 'Since dtypes are different, will try to simplify', file=str_io)

        (
            common_cols_dtypes_simplified,
            after_simp_equality,
            df1_common,
            df2_common,
            common_cols_dtypes_simplified_equality,
            common_cols_dtypes_simplified_df,
        ) = _dtypes_simp_and_eqlty_check(
            df1=df1_common,
            df2=df2_common,
            df1_name=df1_name,
            df2_name=df2_name,
            show_all_dtypes=show_all_dtypes,
            str_io=str_io,
        )

        equality_metadata['variables'].update(
            {'common_cols_dtypes_simplified': common_cols_dtypes_simplified}
        )

        if common_cols_dtypes_simplified is True:
            equality_metadata['variables'].update(
                {
                    'common_cols_dtypes_simplified_equality': common_cols_dtypes_simplified_equality,
                    'common_cols_dtypes_simplified_df': common_cols_dtypes_simplified_df,
                }
            )

            if after_simp_equality is True:
                return _returner_for_compare(
                    equality_full=False,
                    equality_partial=True,
                    equality_metadata=equality_metadata,
                    str_io=str_io,
                    report_print=report_print,
                    report_file_path=report_file_path,
                )
    else:
        f.print_title(
            1,
            'Skipping equality check',
            'since dtypes are equal, previous equality check is sufficient',
            file=str_io,
        )

    # MARK: ROUND_TO
    # Rounding numeric columns.
    # *************************************************************************
    if round_to is not None:
        f.print_title(1, f'Rounding [round_to={round_to}]', file=str_io)
        df1_common = pd_format.approximate(df1_common, round_to=round_to)
        df2_common = pd_format.approximate(df2_common, round_to=round_to)

        # Equality check for common columns and indexes, after rounding
        f.print_title(1, 'Equality check', 'after rounding', file=str_io)
        if df1_common.equals(df2_common):  # Are the dfs equal?
            f.print_result('🥳 Equal', file=str_io)
            return _returner_for_compare(
                equality_full=False,
                equality_partial=True,
                equality_metadata=equality_metadata,
                str_io=str_io,
                report_print=report_print,
                report_file_path=report_file_path,
            )
        else:
            f.print_result('😡 Not equal', file=str_io)

        # MARK: ROUND/DTYPES SIMP
        # if rounding was applied
        # dtypes simplification, dtypes comparison and testing equality afterwards
        # *************************************************************************
        (
            common_cols_post_round_dtypes_simplified,
            after_round_and_simp_equality,
            df1_common,
            df2_common,
            common_cols_post_round_dtypes_simplified_equality,
            common_cols_post_round_dtypes_simplified_df,
        ) = _dtypes_simp_and_eqlty_check(
            df1=df1_common,
            df2=df2_common,
            df1_name=df1_name,
            df2_name=df2_name,
            show_all_dtypes=show_all_dtypes,
            str_io=str_io,
        )

        equality_metadata['variables'].update(
            {
                'common_cols_post_round_dtypes_simplified': common_cols_post_round_dtypes_simplified,
            }
        )

        if common_cols_post_round_dtypes_simplified is True:

            equality_metadata['variables'].update(
                {
                    'common_cols_post_round_dtypes_simplified_equality': common_cols_post_round_dtypes_simplified_equality,
                    'common_cols_post_round_dtypes_simplified_df': common_cols_post_round_dtypes_simplified_df,
                }
            )

            if after_round_and_simp_equality is True:
                return _returner_for_compare(
                    equality_full=False,
                    equality_partial=True,
                    equality_metadata=equality_metadata,
                    str_io=str_io,
                    report_print=report_print,
                    report_file_path=report_file_path,
                )

    # MARK: COMPARE VALUES
    # Comparing values
    #
    # No equality check needed as one was done above when trying to simplify dtypes
    # and if no simplification was done, that means that dtypes are equal
    # and the previous equality check was sufficient
    # *************************************************************************
    f.print_title(
        1,
        'Comparing values',
        'from this point on, the DataFrames must have at least one different cell',
        file=str_io,
    )

    equality_df = compute_equality_df(df1_common, df2_common)

    cols_equal_list = list(equality_df.columns[(equality_df.all(axis=0))])
    cols_equal_list_sorted = pd_format.obj_as_sorted_list(cols_equal_list)
    rows_equal_list = list(equality_df.index[equality_df.all(axis=1)])
    rows_equal_list_sorted = pd_format.obj_as_sorted_list(rows_equal_list)

    cols_diff_list = list(equality_df.columns[~(equality_df.all(axis=0))])
    cols_diff_list_sorted = pd_format.obj_as_sorted_list(cols_diff_list)
    f.print_event(1, f'😓 Not equal columns (count={len(cols_diff_list_sorted)}):', file=str_io)
    f.pprint_wrap(1, pd_format.obj_as_sorted_list(cols_diff_list_sorted), stream=str_io)

    rows_diff_list = list(equality_df.index[~equality_df.all(axis=1)])
    rows_diff_list_sorted = pd_format.obj_as_sorted_list(rows_diff_list)
    f.print_event(1, f'😓 Not equal rows (count={len(rows_diff_list_sorted)}):', file=str_io)
    f.pprint_wrap(1, pd_format.obj_as_sorted_list(rows_diff_list_sorted), stream=str_io)

    equality_metadata['variables'].update(
        {
            'equality_df': equality_df,
            'cols_equal_list_sorted': cols_equal_list_sorted,
            'rows_equal_list_sorted': rows_equal_list_sorted,
            'cols_diff_list_sorted': cols_diff_list_sorted,
            'rows_diff_list_sorted': rows_diff_list_sorted,
        }
    )

    # MARK: JOINED DF
    # Creating joined_df
    # *************************************************************************
    with pd.option_context('future.no_silent_downcasting', True):
        only_diff_df = pd.DataFrame().reindex_like(equality_df).fillna(False).astype('bool')
    only_diff_df[~equality_df] = True

    # See https://stackoverflow.com/a/61105984/1071459
    joined_df = (
        pd.concat(
            (df1_common, df2_common, only_diff_df), axis=1, keys=(df1_name, df2_name, 'different')
        )
        .swaplevel(axis=1)
        .sort_index(axis=1, level=0, sort_remaining=False)
    )

    equality_metadata['variables'].update({'joined_df': joined_df})

    # MARK: EXCEL
    # Saving to Excel
    # *************************************************************************
    if xls_path is not None:
        # Add level to DataFrame, see https://datascientyst.com/add-level-index-pandas-dataframe/
        df1_fixed_cols_added_level = pd.concat(
            [df1_common.loc[idxs_common_list_sorted, xls_fixed_cols]],
            keys=[df1_name],
            axis=1,
        )
        df2_fixed_cols_added_level = pd.concat(
            [df2_common.loc[idxs_common_list_sorted, xls_fixed_cols]],
            keys=[df2_name],
            axis=1,
        )

        fixed_cols_df = (
            pd.merge(
                df1_fixed_cols_added_level,
                df2_fixed_cols_added_level,
                left_index=True,
                right_index=True,
            )
            .swaplevel(axis=1)[xls_fixed_cols]
            .rename(mapper=lambda x: f'{x} (fixed_cols)', axis='columns', level=0)
        )

        # Create a DataFrame with the equal (`xls_compare_str_equal`) or different (`xls_compare_str_diff`) string
        only_diff_for_excel_df = (
            pd.DataFrame().reindex_like(equality_df).fillna(xls_compare_str_equal)
        )
        only_diff_for_excel_df[~equality_df] = xls_compare_str_diff

        # See https://stackoverflow.com/a/61105984/1071459
        joined_for_excel_df = (
            pd.concat(
                (df1_common, df2_common, only_diff_for_excel_df),
                axis=1,
                keys=(df1_name, df2_name, 'different'),
            )
            .swaplevel(axis=1)
            .sort_index(axis=1, level=0, sort_remaining=False)
        )

        xls_df = pd.merge(fixed_cols_df, joined_for_excel_df, left_index=True, right_index=True)
        freeze_on_colindex = len(fixed_cols_df.columns)
        f.print_title(1, 'Creating Excel', os.path.realpath(xls_path), file=str_io)
        _save_excel(
            xls_df,
            path=os.path.realpath(xls_path),
            freeze_on_colindex=freeze_on_colindex,
            datetime_rpl_str=xls_datetime_rpl,
        )

        equality_metadata['variables'].update(
            {
                'xls_path': os.path.realpath(xls_path),
            }
        )

    # MARK: RETURN
    return _returner_for_compare(
        equality_full=False,
        equality_partial=False,
        equality_metadata=equality_metadata,
        str_io=str_io,
        report_print=report_print,
        report_file_path=report_file_path,
    )
