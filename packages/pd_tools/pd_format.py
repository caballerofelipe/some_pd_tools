import pandas as pd

__all__ = ['format_nums']


def format_nums(df: pd.DataFrame, thousands: bool = False, decimals: int = 4):
    '''
    See https://stackoverflow.com/a/69190425/1071459
    '''
    if thousands:
        # Thousands sep
        return df.map(lambda x: f'{x:,.{decimals}f}' if isinstance(x, float) else x).map(
            lambda x: f'{x:,d}' if isinstance(x, int) else x
        )
    else:
        # No Thousands sep
        return df.map(lambda x: f'{x:.{decimals}f}' if isinstance(x, float) else x).map(
            lambda x: f'{x:d}' if isinstance(x, int) else x
        )
