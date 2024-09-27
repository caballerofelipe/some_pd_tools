import io
from contextlib import redirect_stdout

import pandas as pd

from . import _module_report_formatting as f
from ._module_compare_lists import compare_lists


def compare_dtypes(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    df1_name: str = 'df1',
    df2_name: str = 'df2',
    report_print: bool = False,
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
    report_print : bool, optional
        Whether to show the comparison report, by default False
    show_all_dtypes : bool, optional
        Whether to show the columns that have the same dtype in the report, by default False.

    Returns
    -------
    tuple[bool, dict]
        Explanation:
        - <b>tuple[0]</b>: True if all dtypes equal, False if not.
        - <b>tuple[1]</b>: Metadata dict. This contains:
            <ul>
                <li><b>'dtypes_df'</b>: DataFrame. A DataFrame where the index is the analyzed column and the following 3 columns:
                    <ol>
                        <li><b>'different'</b> representing wether the column is different or not in both input DataFrames (True means different, False means equal).</li>
                        <li><b>{df1_name}</b> (stated name for first DataFrame): the dtype for the given column in df1.</li>
                        <li><b>{df2_name}</b> (stated name for second DataFrame): the dtype for the given column in df2.</li>
                    </ol>
                </li>
                <li><b>'report'</b>: str. The report, useful in case the param `report` is False.</li>
            </ul>

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
            report_print=True,
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

    if report_print is True:
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
