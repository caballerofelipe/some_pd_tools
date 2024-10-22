import re

import numpy as np
import pandas as pd

__all__ = [
    'number_separators',
    'approximate',
    'ceil',
    'floor',
    'trunc',
    'simplify_dtypes',
]


def obj_as_sorted_list(obj: object, force_str=False) -> list:
    """Return an object as a sorted list.
    
    If ints are found inside the obj or in its keys, the sorting will be done using int [1,2,12] will be sorted as [1,2,12]. If there is something else than ints, the sorting will be done parsing the value or the key to str, so for instance sorting ("1",2,12) will sort to: (1,12,2).

    The function can be forced to sort using str with the param force_str.

    Note: Not implemented for "every" object, only the ones needed in this project: dict, set, tuple and list. Raises exception if none of these types of objects are tried to be transformed.

    Parameters
    ----------
    obj : object
        The object.
    force_str : bool, optional
        Forces the function to use string classification, even if the obj is filled with int or if the obj keys are all int (depending on the type for obj). By default False.

    Returns
    -------
    list
        The sorted object as a list.

    Raises
    ------
    ValueError
        Function not implemented for type:{type(obj)}.
    """
    if isinstance(obj, dict):
        if force_str is True:
            return sorted(obj.items(), key=lambda item: str(item[0]))
        
        all_ints = True
        for v in obj.keys():
            if not isinstance(v, int):
                all_ints = False
                break
        if all_ints:
            return sorted(obj.items())
        else:
            return sorted(obj.items(), key=lambda item: str(item[0]))
    
    if isinstance(obj, set) or isinstance(obj, list) or isinstance(obj, tuple):
        if force_str is True:
            return sorted(obj, key=lambda item: str(item))
        
        all_ints = True
        for v in obj:
            if not isinstance(v, int):
                all_ints = False
                break
        if all_ints:
            return sorted(obj)
        else:
            return sorted(obj, key=lambda item: str(item))

    raise ValueError(f'Function not implemented for type: {type(obj)}.')


def _series_number_separators(
    ser: pd.Series,
    precision: int = 6,
    thousands_sep: str = ',',
    decimals_sep: str = '.',
) -> pd.Series:
    """Transform a Series adding a thousands separator. Optionally modifies the thousands and decimals separator.

    **Important (1)**: This transforms a numeric series to dtype 'object' and each cell is a string.

    **Important (2)**: For floats, this uses String Formatting Operations. The formatting is like this: `f'{x:,f}'` and from the documentation: "The precision determines the number of significant digits before and after the decimal point and defaults to 6." So keep in mind that this will round to 6 digits. If you need a different precision use the precision parameter.
    See: https://docs.python.org/2/library/stdtypes.html#string-formatting-operations .

    See https://stackoverflow.com/a/69190425/1071459 .

    Parameters
    ----------
    ser : pd.Series
        The Series where the numbers are to be changed.
    precision : int
        The rounding precision.
    thousands_sep : str, optional
        Thousands separator, by default ','.
    decimals_sep : str, optional
        Decimal separator, by default '.'.

    Returns
    -------
    pd.Series
        The transformed Series.

    Raises
    ------
    ValueError
        `ser` must be of type pd.Series.
    ValueError
        `thousands_sep` cannot be equal to `decimals_sep`.
    ValueError
        `thousands_sep` and `decimals_sep` cannot be bool.
    ValueError
        `thousands_sep` and `decimals_sep` cannot be numbers.
    ValueError
        `thousands_sep` and `decimals_sep` cannot include any digits (0-9), '-', 'E' or 'e' to avoid confusions.
    """
    # Types and value validation, exceptions
    if not isinstance(ser, pd.Series):
        raise ValueError('`ser` must be of type pd.Series.')
    if thousands_sep == decimals_sep:
        raise ValueError('`thousands_sep` cannot be equal to `decimals_sep`.')
    if isinstance(thousands_sep, bool) or isinstance(decimals_sep, bool):
        raise ValueError("`thousands_sep` and `decimals_sep` cannot be bool.")
    if (
        isinstance(thousands_sep, int)
        or isinstance(thousands_sep, float)
        or isinstance(thousands_sep, complex)
        or isinstance(decimals_sep, int)
        or isinstance(decimals_sep, float)
        or isinstance(decimals_sep, complex)
    ):
        raise ValueError("`thousands_sep` and `decimals_sep` cannot be numbers.")
    regex = r'[-|\d|E|e]+'
    if bool(re.search(regex, str(thousands_sep))) or bool(re.search(regex, str(decimals_sep))):
        raise ValueError(
            "`thousands_sep` and `decimals_sep` cannot include the following: digits (0-9), '-', 'E' or 'e'; to avoid confusions."
        )

    ser_cp = ser.copy()

    # The actual transformation
    if pd.api.types.is_numeric_dtype(ser_cp):

        if pd.api.types.is_float_dtype(ser_cp):
            ser_cp = ser_cp.apply(lambda x: f'{x:,.{precision}f}')
        elif pd.api.types.is_integer_dtype(ser_cp):
            ser_cp = ser_cp.apply(lambda x: f'{x:,d}')

        # Don't do any additional transformation if not necessary
        if thousands_sep != ',' or decimals_sep != '.':
            thousands_sep_placeholder = '?' if decimals_sep != '?' else '^'
            ser_cp = ser_cp.apply(
                lambda x: x.replace(',', thousands_sep_placeholder)
                .replace('.', decimals_sep)
                .replace(thousands_sep_placeholder, thousands_sep)
            )
    return ser_cp


def number_separators(
    df: pd.DataFrame | pd.Series, precision: int = 6, thousands_sep=',', decimals_sep='.'
) -> pd.DataFrame | pd.Series:
    """Transform a DataFrame or Series adding a thousands separator and optionally modifying it and the decimals separator.

    **Important (1)**: This transforms a numeric series to dtype 'object' and each cell is a string.

    **Important (2)**: For floats, this uses String Formatting Operations. The formatting is like this: `f'{x:,f}'` and from the documentation: "The precision determines the number of significant digits before and after the decimal point and defaults to 6." So keep in mind that this will round to 6 digits. If you need a different precision use the precision parameter. See: https://docs.python.org/2/library/stdtypes.html#string-formatting-operations .

    Parameters
    ----------
    df : pd.DataFrame | pd.Series
        The DataFrame or Series where the numbers are to be changed.
    thousands_sep : str, optional
        Thousands separator, by default ','.
    decimals_sep : str, optional
        Decimal separator, by default '.'.

    Returns
    -------
    pd.DataFrame|pd.Series
        The transformed DataFrame or Series.

    Raises
    ------
    ValueError
        `df` must be of type DataFrame or Series.
    """
    if (not isinstance(df, pd.DataFrame)) and (not isinstance(df, pd.Series)):
        raise ValueError('`df` must be of type pd.DataFrame or pd.Series.')

    if isinstance(df, pd.DataFrame):
        return df.apply(
            _series_number_separators,
            precision=precision,
            thousands_sep=thousands_sep,
            decimals_sep=decimals_sep,
        )

    if isinstance(df, pd.Series):
        return _series_number_separators(
            df, precision=precision, thousands_sep=thousands_sep, decimals_sep=decimals_sep
        )


def approximate(
    df: pd.DataFrame,
    round_to: None | int | str = None,
) -> pd.DataFrame:
    """Approximate numbers using a `round_to` method.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be approximated.
    round_to : None | int | str, optional
        The way to approximate, by default None. Possible values and their meaning:
        - **None**: nothing is done.
        - **'int'**: rounds floating numbers to this decimal.
        - **'floor'**: does a floor operation on floats columns. Uses np.floor. From np.floor's documentation: "The floor of the scalar x is the largest integer i, such that i <= x."
        - **'ceil'**: does a ceil operation on floats columns. Uses np.ceil. From np.ceil's documentation: "The ceil of the scalar x is the smallest integer i, such that i >= x.".
        - **'trunc'**: removes decimals from floats columns. Uses np.trunc. From np.trunc's documentation: "The truncated value of the scalar x is the nearest integer i which is closer to zero than x is.".

    Returns
    -------
    pd.DataFrame
        The transformed DataFrame.

    Raises
    ------
    ValueError
        '`df` must be of type pd.DataFrame.'
    ValueError
        round_to must be one of None, a positive integer or a string ('floor', 'ceil', 'trunc').
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError('`df` must be of type pd.DataFrame.')

    # Nothing needs to be done
    if round_to is None:
        return df

    # Type and value validation
    if (
        isinstance(round_to, bool)
        or (isinstance(round_to, int) and round_to < 0)
        or (isinstance(round_to, str) and round_to not in ('floor', 'ceil', 'trunc'))
        or (not isinstance(round_to, int) and not isinstance(round_to, str))
    ):
        raise ValueError(
            "round_to must be one of None, a positive integer or a string ('floor', 'ceil', 'trunc')."
        )

    if isinstance(round_to, int):
        return df.round(round_to)

    if round_to in ('floor', 'ceil', 'trunc'):
        approximation_fn = None
        if round_to == 'floor':
            approximation_fn = np.floor
        elif round_to == 'ceil':
            approximation_fn = np.ceil
        elif round_to == 'trunc':
            approximation_fn = np.trunc

        df_cp = df.copy()
        for col in df_cp.columns:
            if pd.api.types.is_float_dtype(df_cp[col]):
                df_cp[col] = df_cp[col].apply(approximation_fn)
        return df_cp


def floor(df: pd.DataFrame | pd.Series) -> pd.DataFrame:
    """Does a floor operation on floats columns. Uses np.floor. From np.floor's documentation: "The floor of the scalar x is the largest integer i, such that i <= x."

    Parameters
    ----------
    df : pd.DataFrame | pd.Series
        The DataFrame or Series where the numbers are to be changed.

    Returns
    -------
    pd.DataFrame
        The transformed DataFrame.
    """
    return approximate(df, round_to='floor')


def ceil(df: pd.DataFrame | pd.Series) -> pd.DataFrame:
    """Does a ceil operation on floats columns. Uses np.ceil. From np.ceil's documentation: "The ceil of the scalar x is the smallest integer i, such that i >= x.".

    Parameters
    ----------
    df : pd.DataFrame | pd.Series
        The DataFrame or Series where the numbers are to be changed.

    Returns
    -------
    pd.DataFrame
        The transformed DataFrame.
    """
    return approximate(df, round_to='ceil')


def trunc(df: pd.DataFrame | pd.Series) -> pd.DataFrame:
    """Remove decimals from floats columns. Uses np.trunc. From np.trunc's documentation: "The truncated value of the scalar x is the nearest integer i which is closer to zero than x is.".

    Parameters
    ----------
    df : pd.DataFrame | pd.Series
        The DataFrame or Series where the numbers are to be changed.

    Returns
    -------
    pd.DataFrame
        The transformed DataFrame.
    """
    return approximate(df, round_to='trunc')


def simplify_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Allows to simplify dtypes, for instance, pass from float64 to int64 if no decimals are present.

    Doesn't convert to a dtype that supports pd.NA, like `DataFrame.convert_dtypes()` although it uses it. See https://github.com/pandas-dev/pandas/issues/58543#issuecomment-2101240339 . It might create a performance impact (not tested).

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to dtypes simplify.

    Returns
    -------
    pd.DataFrame
       The DataFrame, with simplified dtypes.

    Raises
    ------
    ValueError
        If df is not of type DataFrame.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError('df must be of type pd.DataFrame.')
    with pd.option_context('future.no_silent_downcasting', True):
        return (
            df
            # See https://github.com/pandas-dev/pandas/issues/58543#issuecomment-2101240339
            .astype('object')
            .convert_dtypes()
            .astype('object')
            .replace(pd.NA, float('nan'))
            .infer_objects()
        )
