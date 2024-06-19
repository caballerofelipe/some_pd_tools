import pprint
import textwrap

import pandas as pd

from . import pd_format

__all__ = ['compare']


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


def compare(
    df1: pd.DataFrame,
    df1_name: str,
    df2: pd.DataFrame,
    df2_name: str,
    show_common_cols=False,
    int64_to_float64: bool = False,
    round_to_decimals: int | bool = False,
    astype_str: bool = False,
    path: str = None,
    fixed_cols: list = [],
):
    if df1.equals(df2):  # Are the dfs equal?
        print('** 🥳 Fully equal')
        return [None] * 6
    else:
        print('** 😓 Not fully equal')

    df1_cp = df1.sort_index(axis=0).sort_index(axis=1).copy()
    df2_cp = df2.sort_index(axis=0).sort_index(axis=1).copy()

    # Columns sets
    df1_col_set = set(df1_cp.columns)
    df2_col_set = set(df2_cp.columns)
    df1_extra_cols = df1_col_set - df2_col_set
    df2_extra_cols = df2_col_set - df1_col_set
    cols_in_both = list(df1_col_set - df1_extra_cols)

    print('————————————————————')
    print('...Comparing dtypes for common columns...')
    print('(Without special settings)')
    common_cols_dtypes_mask = (
        df1_cp[cols_in_both].dtypes.sort_index() == df2_cp[cols_in_both].dtypes.sort_index()
    )
    diff_common_cols_dtypes = df1_cp[cols_in_both].dtypes.sort_index()[~common_cols_dtypes_mask]
    if common_cols_dtypes_mask.all(axis=None):
        print('* No different dtypes.')
    else:
        print('* 😓 Different dtypes:')
        legend = "col\dataframe"
        lgnd_maxlen = max([len(i) for i in diff_common_cols_dtypes.index])
        lgnd_maxlen = max(lgnd_maxlen, len(legend))
        # <Formatting computations>
        diff_dtypes_cols = diff_common_cols_dtypes.index
        df1types_col_len = [len(str(d)) for d in df1_cp[diff_dtypes_cols].dtypes]
        df1types_col_len.append(len(df1_name))
        df1types_maxlen = max(df1types_col_len)
        df2types_col_len = [len(str(d)) for d in df2_cp[diff_dtypes_cols].dtypes]
        df2types_col_len.append(len(df2_name))
        df2types_maxlen = max(df2types_col_len)
        # </Formatting computations>
        print(
            f'{legend:<{lgnd_maxlen}} {df1_name:<{df1types_maxlen}} {df2_name:<{df2types_maxlen}}'
        )
        for idx in diff_common_cols_dtypes.index:
            print(
                f'{idx:<{lgnd_maxlen}} {str(df1_cp[idx].dtype):<{df1types_maxlen}} {str(df2_cp[idx].dtype):<{df2types_maxlen}}'
            )

    # Special settings
    if int64_to_float64 is True:
        # Pass int64 to float64
        for tmp_df in (df1_cp, df2_cp):
            for col in tmp_df.columns:
                if str(tmp_df[col].dtype) in ('int64'):
                    tmp_df[col] = tmp_df[col].astype('float64')

    # Format as string with decimals
    if round_to_decimals is not False:
        df1_cp = df1_cp.apply(pd_format.format_nums, decimals=round_to_decimals)
        df2_cp = df2_cp.apply(pd_format.format_nums, decimals=round_to_decimals)

    if astype_str is True:
        df1_cp = df1_cp.astype(str)
        df2_cp = df2_cp.astype(str)

    print('————————————————————')
    print('🧪 Special settings:')
    if int64_to_float64 is True or round_to_decimals is not False or astype_str is True:
        if int64_to_float64 is True:
            print(f'* int64_to_float64[{int64_to_float64}]')
        if round_to_decimals is not False:
            print(f'* round_to_decimals[{round_to_decimals}]')
        if astype_str is True:
            print(f'* astype_str[{astype_str}]')
    else:
        print('* No special settings.')

    print('————————————————————')

    if df1_cp.equals(df2_cp):  # Are the dfs equal? (after setting equal decimals)
        print(f'** 🥸 Equal (with special settings).')
        return [None] * 6

    print('** 😡 Not equal')

    print('————————————————————')
    print('...Comparing columns...')
    if len(df1_cp.columns) == len(df2_cp.columns):
        print('* Column count matches')
    else:
        print('* 😓 Column count doesn\'t match:')
        lgnd_maxlen = max(len(df1_name), len(df2_name))
        print(f'  {df1_name:>{lgnd_maxlen}}: {len(df1_cp.columns)}')
        print(f'  {df2_name:>{lgnd_maxlen}}: {len(df2_cp.columns)}')

    print(f'* For {df1_name}:')
    if len(df1_extra_cols) > 0:
        print(f'  😓 The following columns are in {df1_name} but not in {df2_name}:')
        print(f'  {df1_extra_cols}')
    else:
        print('  No extra columns.')

    print(f'* For {df2_name}:')
    if len(df2_extra_cols) > 0:
        print(f'  😓 The following columns are in {df2_name} but not in {df1_name}:')
        print(f'  {df2_extra_cols}')
    else:
        print('  No extra columns.')

    if show_common_cols is True:
        print('————————————————————')
        print('Columns present in both DataFrames (a.k.a. intersection):')
        pprint.pprint(cols_in_both)

    print('————————————————————')
    print('...Comparing indexes...')
    if len(df1_cp.index) != len(df2_cp.index):
        print('* 😓 Indexes differ in length, no comparison done.')
        print(f'* {df1_name} index lenght: {len(df1_cp.index)}.')
        print(f'* {df2_name} index lenght: {len(df2_cp.index)}.')
        return [None] * 6
    index_equal_mask = df1_cp.index == df2_cp.index
    if index_equal_mask.all(axis=None):
        print('* All indexes equal.')
    else:
        df1_index_set = set(df1_cp.index)
        df2_index_set = set(df2_cp.index)
        df1_extra_index = df1_index_set - df2_index_set
        df2_extra_index = df2_index_set - df1_index_set

        print('* Different indexes:')

        print(f'* For {df1_name}:')
        if len(df1_extra_index) > 0:
            print(f'  😓 The following indexes are in {df1_name} but not in {df2_name}:')
            print(f'  {df1_extra_index}')
        else:
            print('  No extra indexes.')

        print(f'* For {df2_name}:')
        if len(df2_extra_index) > 0:
            print(f'  😓 The following indexes are in {df2_name} but not in {df1_name}:')
            print(f'  {df2_extra_index}')
        else:
            print('  No extra indexes.')

    print('————————————————————')
    print('...Comparing values...')
    print('(Only equal columns and equal indexes, see above non value differences)')

    df1_common_subset = df1_cp.loc[index_equal_mask, cols_in_both]
    df2_common_subset = df2_cp.loc[index_equal_mask, cols_in_both]

    # equal_mask_df = (
    #     df1_cp.loc[index_equal_mask, cols_in_both] == df2_cp.loc[index_equal_mask, cols_in_both]
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
        print('* 🥸 Compared DataFrames (using common indexes and columns).')
        return [None] * 6

    diff_columns = equal_mask_df.columns[~(equal_mask_df.all(axis=0))].sort_values()
    print(f'* 😓 Not equal columns (count[{len(diff_columns)}]):')
    print(textwrap.fill(str(list(diff_columns)), width=100))

    diff_rows = equal_mask_df.index[~equal_mask_df.all(axis=1)]
    print(f'* 😓 Not equal rows (count[{len(diff_rows)}]):')
    print(textwrap.fill(str(list(diff_rows)), width=100))

    # Creating joined_df
    joined_df = (
        df1_cp[cols_in_both]
        #
        .join(df2_cp[cols_in_both], lsuffix=f'_{df1_name}', rsuffix=f'_{df2_name}')
    )
    joined_df = df1_cp[[*fixed_cols]].join(joined_df)

    # Create a new column with suffix '_diff' to explicitly show if there's a difference
    new_diff_columns = [f'{col}_diff' for col in diff_columns]
    joined_df[new_diff_columns] = ''

    for col in diff_columns:
        diff_rows_for_col_mask = joined_df[f'{col}_{df1_name}'] != joined_df[f'{col}_{df2_name}']
        joined_df.loc[diff_rows_for_col_mask, f'{col}_diff'] = 'diff'

    cols_diff = [*diff_columns]
    df1_cols_diff = [f'{c}_{df1_name}' for c in cols_diff]
    df2_cols_diff = [f'{c}_{df2_name}' for c in cols_diff]
    show_diff_cols = [f'{c}_diff' for c in cols_diff]
    cols_diff_from_1_2_show_diff = zip(df1_cols_diff, df2_cols_diff, show_diff_cols)
    all_diff_cols = [item for tup in cols_diff_from_1_2_show_diff for item in tup]

    # Different columns with different rows
    diff_df = joined_df.loc[diff_rows, all_diff_cols]

    # Creating a DataFrame where differenes where found but with the original values
    diff_original_vals_df = pd.merge(
        df1.loc[diff_rows, diff_columns],
        df2.loc[diff_rows, diff_columns],
        left_index=True,
        right_index=True,
        suffixes=(f'_{df1_name}', f'_{df2_name}'),
    )

    if path != None:
        _save_compared_df(
            joined_df,
            diff_rows=diff_rows,
            all_diff_cols=all_diff_cols,
            path=path,
            fixed_cols=fixed_cols,
        )

    return joined_df, equal_mask_df, diff_df, diff_columns, diff_rows, diff_original_vals_df
