import pandas as pd


def compute_equality_df(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
    """Compares the cell values of two DataFrames.

    Returns a DataFrame with the same columns and indexes, cells are boolean, either True or False. See Returns.

    This doesn't compute the DataFrames as a whole, only on a cell basis, which means that different dtypes don't matter. To compare DataFrames as a whole do `df1.equals(df2)` or use `pd_compare.compare()` for a thorough report.

    Parameters
    ----------
    df1 : pd.DataFrame
        First DataFrame to compare.
    df2 : pd.DataFrame
        Second DataFrame to compare.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the same columns and indexes as df1 and df2. Every cell is a boolean value, True if the cell is equal, False otherwise.

    Raises
    ------
    ValueError
        'df1 and df2 must be of type pd.DataFrame.'
    ValueError
        'df1 and df2 must have equal columns and equal indexes. Select only the same columns and same indexes and run the function again.'
    ValueError
        'df1 and df2 cannot have duplicated columns or indexes. Select not duplicated columns and not duplicated indexes and run the function again.'
    """
    if not isinstance(df1, pd.DataFrame) or not isinstance(df2, pd.DataFrame):
        raise ValueError('df1 and df2 must be of type pd.DataFrame.')
    if not df1.columns.equals(df2.columns) or not df1.index.equals(df2.index):
        raise ValueError(
            'df1 and df2 must have equal columns and equal indexes. Select only the same columns and same indexes and run the function again.'
        )
    if (
        len(df1.columns) != len(set(df1.columns))
        or len(df2.columns) != len(set(df2.columns))
        or len(df1.index) != len(set(df1.index))
        or len(df2.index) != len(set(df2.index))
    ):
        raise ValueError(
            'df1 and df2 cannot have duplicated columns or indexes. Select not duplicated columns and not duplicated indexes and run the function again.'
        )

    # The usual predictable equality BUT this outputs False when two 'nan' values are compared
    # (nan == nan) is False
    # So by itself, this equality is not enough,
    # we want a cell with a `True` value if a cell in both DataFrames is nan, check next part
    equality_df_normal = df1 == df2

    # There's a workaround to check if values in both DataFrames are 'nan':
    # (1) Compare each DataFrame to itself, if the result in a cell is different
    #   that means the cell's value is 'nan'
    # (2) If this happens in both DataFrame,
    #   that means both cells are 'nan' and their values are equal
    #
    #  see: # https://stackoverflow.com/a/19322739/1071459
    equality_df_true_where_nan = (df1 != df1) & (df2 != df2)

    # If either equality is True, we consider a cell's value to be True
    return equality_df_normal | equality_df_true_where_nan
