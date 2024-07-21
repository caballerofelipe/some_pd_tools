import pandas as pd


class BaseDF:
    def __init__(self) -> None:
        df = pd.DataFrame(
            {
                'col_int': [1, 2, 3, 4],
                'col_float': [1.1, 2.2, 3.3, 4.4],
                'col_str': ['a', 'b', 'c', 'd'],
                'col_nan': [float('nan'), float('nan'), float('nan'), float('nan')],
                'col_strnan': ['e', 'f', 'g', float('nan')],
                'col_df1extra': [5, 6, 7, 8],
                'col_df2extra': ['i', 'j', 'k', 45],
            }
        )
        self._df = df

        self._df_simple = df.copy().drop(columns=['col_df1extra', 'col_df2extra'])

        self._df1 = self._df_simple.copy()
        self._df2 = self._df_simple.copy()

        self._df1_as_object = self._df_simple.copy().astype('object')
        self._df2_as_object = self._df_simple.copy().astype('object')

        self._df1_extra_col = df.copy().drop(columns=['col_df2extra'])
        self._df2_extra_col = df.copy().drop(columns=['col_df1extra'])

        self._df_index_plus1 = self._df_simple.copy()
        self._df_index_plus1.index = self._df_index_plus1.index + 1

        self._df1_index_plus1 = self._df_index_plus1.copy()
        self._df2_index_plus1 = self._df_index_plus1.copy()

        self._df1_name = 'first_df'
        self._df2_name = 'second_df'

    @property
    def df(self) -> pd.DataFrame | pd.Series:
        return self._df.copy()

    @df.setter
    def df(self, value):
        raise ValueError('df not rewritable')

    @df.deleter
    def df(self, value):
        raise ValueError('df not deletable')

    @property
    def df1(self) -> pd.DataFrame | pd.Series:
        return self._df1.copy()

    @df1.setter
    def df1(self, value):
        raise ValueError('df1 not rewritable')

    @df1.deleter
    def df1(self, value):
        raise ValueError('df1 not deletable')

    @property
    def df2(self) -> pd.DataFrame | pd.Series:
        return self._df2.copy()

    @df2.setter
    def df2(self, value):
        raise ValueError('df2 not rewritable')

    @df2.deleter
    def df2(self, value):
        raise ValueError('df2 not deletable')

    @property
    def df1_as_object(self) -> pd.DataFrame | pd.Series:
        return self._df1_as_object.copy()

    @df1_as_object.setter
    def df1_as_object(self, value):
        raise ValueError('df1_as_object not rewritable')

    @df1_as_object.deleter
    def df1_as_object(self, value):
        raise ValueError('df1_as_object not deletable')

    @property
    def df2_as_object(self) -> pd.DataFrame | pd.Series:
        return self._df2_as_object.copy()

    @df2_as_object.setter
    def df2_as_object(self, value):
        raise ValueError('df2_as_object not rewritable')

    @df2_as_object.deleter
    def df2_as_object(self, value):
        raise ValueError('df2_as_object not deletable')

    @property
    def df1_extra_col(self) -> pd.DataFrame | pd.Series:
        return self._df1_extra_col.copy()

    @df1_extra_col.setter
    def df1_extra_col(self, value):
        raise ValueError('df1_extra_col not rewritable')

    @df1_extra_col.deleter
    def df1_extra_col(self, value):
        raise ValueError('df1_extra_col not deletable')

    @property
    def df2_extra_col(self) -> pd.DataFrame | pd.Series:
        return self._df2_extra_col.copy()

    @df2_extra_col.setter
    def df2_extra_col(self, value):
        raise ValueError('df2_extra_col not rewritable')

    @df2_extra_col.deleter
    def df2_extra_col(self, value):
        raise ValueError('df2_extra_col not deletable')

    @property
    def df1_index_plus1(self) -> pd.DataFrame | pd.Series:
        return self._df1_index_plus1

    @df1_index_plus1.setter
    def df1_index_plus1(self, value):
        raise ValueError('df1_index_plus1 not rewritable')

    @df1_index_plus1.deleter
    def df1_index_plus1(self, value):
        raise ValueError('df1_index_plus1 not deletable')

    @property
    def df2_index_plus1(self) -> pd.DataFrame | pd.Series:
        return self._df2_index_plus1

    @df2_index_plus1.setter
    def df2_index_plus1(self, value):
        raise ValueError('df2_index_plus1 not rewritable')

    @df2_index_plus1.deleter
    def df2_index_plus1(self, value):
        raise ValueError('df2_index_plus1 not deletable')

    @property
    def df1_name(self):
        return self._df1_name

    @df1_name.setter
    def df1_name(self, value):
        raise ValueError('df1_name not rewritable')

    @df1_name.deleter
    def df1_name(self, value):
        raise ValueError('df1_name not deletable')

    @property
    def df2_name(self):
        return self._df2_name

    @df2_name.setter
    def df2_name(self, value):
        raise ValueError('df2_name not rewritable')

    @df2_name.deleter
    def df2_name(self, value):
        raise ValueError('df2_name not deletable')
