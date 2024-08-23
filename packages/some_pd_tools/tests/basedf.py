import pandas as pd


class BaseDF:
    def __init__(self) -> None:
        df_original = pd.DataFrame(
            {
                'col_int': [1000, -2000, 3000, -4000000],
                'col_float': [-3333.3333333333, 4444.4444444444, -5555.5555555555, 6666.6666666666],
                'col_str': ['a', 'b', 'c', '4444.4444444444'],
                'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
                'col_strnan': ['d', 'e', 'f', float('nan')],
                'col_df1extra': [5, 6, 7, 'i'],
                'col_df2extra': ['j', 'k', 'l', 45],
            }
        )
        self._df = df_original
        self._df_diff_values = self._df.sort_values('col_int', ascending=False).reset_index(
            drop=True
        )

        self._df_simple = self._df.copy().drop(columns=['col_df1extra', 'col_df2extra'])
        self._df_simple_diff_values = self._df_diff_values.copy().drop(
            columns=['col_df1extra', 'col_df2extra']
        )

        self._df1 = self._df_simple.copy()
        self._df2 = self._df_simple.copy()

        self._df1_diff_values = self._df_simple_diff_values.copy()
        self._df2_diff_values = self._df_simple_diff_values.copy()

        self._df1_as_object = self._df_simple.copy().astype('object')
        self._df2_as_object = self._df_simple.copy().astype('object')

        self._df1_as_object_diff_values = self._df_simple_diff_values.copy().astype('object')
        self._df2_as_object_diff_values = self._df_simple_diff_values.copy().astype('object')

        self._df1_extra_col = self._df.copy().drop(columns=['col_df2extra'])
        self._df2_extra_col = self._df.copy().drop(columns=['col_df1extra'])

        self._df1_extra_col_diff_values = self._df_diff_values.copy().drop(columns=['col_df2extra'])
        self._df2_extra_col_diff_values = self._df_diff_values.copy().drop(columns=['col_df1extra'])

        self._df_index_plus1 = self._df_simple.copy()
        self._df_index_plus1.index = self._df_index_plus1.index + 1

        self._df1_index_plus1 = self._df_index_plus1.copy()
        self._df2_index_plus1 = self._df_index_plus1.copy()

        self._df1_diff_values_col_int_made_str = self._df1_diff_values.copy()
        self._df1_diff_values_col_int_made_str['col_int'] = (
            self._df1_diff_values_col_int_made_str['col_int'].astype(str) + 'endstr'
        )
        self._df2_diff_values_col_int_made_str = self._df2_diff_values.copy()
        self._df2_diff_values_col_int_made_str['col_int'] = (
            self._df2_diff_values_col_int_made_str['col_int'].astype(str) + 'endstr'
        )

        self._df1_as_object_diff_values_col_int_made_str = (
            self._df1_diff_values_col_int_made_str.copy().astype('object')
        )
        self._df2_as_object_diff_values_col_int_made_str = (
            self._df2_diff_values_col_int_made_str.copy().astype('object')
        )

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
    def df_diff_values(self) -> pd.DataFrame | pd.Series:
        return self._df_diff_values.copy()

    @df_diff_values.setter
    def df_diff_values(self, value):
        raise ValueError('df_diff_values not rewritable')

    @df_diff_values.deleter
    def df_diff_values(self, value):
        raise ValueError('df_diff_values not deletable')

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
    def df1_diff_values(self) -> pd.DataFrame | pd.Series:
        return self._df1_diff_values.copy()

    @df1_diff_values.setter
    def df1_diff_values(self, value):
        raise ValueError('df1_diff_values not rewritable')

    @df1_diff_values.deleter
    def df1_diff_values(self, value):
        raise ValueError('df1_diff_values not deletable')

    @property
    def df2_diff_values(self) -> pd.DataFrame | pd.Series:
        return self._df2_diff_values.copy()

    @df2_diff_values.setter
    def df2_diff_values(self, value):
        raise ValueError('df2_diff_values not rewritable')

    @df2_diff_values.deleter
    def df2_diff_values(self, value):
        raise ValueError('df2_diff_values not deletable')

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
    def df1_as_object_diff_values(self) -> pd.DataFrame | pd.Series:
        return self._df1_as_object_diff_values.copy()

    @df1_as_object_diff_values.setter
    def df1_as_object_diff_values(self, value):
        raise ValueError('df1_as_object_diff_values not rewritable')

    @df1_as_object_diff_values.deleter
    def df1_as_object_diff_values(self, value):
        raise ValueError('df1_as_object_diff_values not deletable')

    @property
    def df2_as_object_diff_values(self) -> pd.DataFrame | pd.Series:
        return self._df2_as_object_diff_values.copy()

    @df2_as_object_diff_values.setter
    def df2_as_object_diff_values(self, value):
        raise ValueError('df2_as_object_diff_values not rewritable')

    @df2_as_object_diff_values.deleter
    def df2_as_object_diff_values(self, value):
        raise ValueError('df2_as_object_diff_values not deletable')

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
    def df1_extra_col_diff_values(self) -> pd.DataFrame | pd.Series:
        return self._df1_extra_col_diff_values.copy()

    @df1_extra_col_diff_values.setter
    def df1_extra_col_diff_values(self, value):
        raise ValueError('df1_extra_col_diff_values not rewritable')

    @df1_extra_col_diff_values.deleter
    def df1_extra_col_diff_values(self, value):
        raise ValueError('df1_extra_col_diff_values not deletable')

    @property
    def df2_extra_col_diff_values(self) -> pd.DataFrame | pd.Series:
        return self._df2_extra_col_diff_values.copy()

    @df2_extra_col_diff_values.setter
    def df2_extra_col_diff_values(self, value):
        raise ValueError('df2_extra_col_diff_values not rewritable')

    @df2_extra_col_diff_values.deleter
    def df2_extra_col_diff_values(self, value):
        raise ValueError('df2_extra_col_diff_values not deletable')

    @property
    def df1_index_plus1(self) -> pd.DataFrame | pd.Series:
        return self._df1_index_plus1.copy()

    @df1_index_plus1.setter
    def df1_index_plus1(self, value):
        raise ValueError('df1_index_plus1 not rewritable')

    @df1_index_plus1.deleter
    def df1_index_plus1(self, value):
        raise ValueError('df1_index_plus1 not deletable')

    @property
    def df2_index_plus1(self) -> pd.DataFrame | pd.Series:
        return self._df2_index_plus1.copy()

    @df2_index_plus1.setter
    def df2_index_plus1(self, value):
        raise ValueError('df2_index_plus1 not rewritable')

    @df2_index_plus1.deleter
    def df2_index_plus1(self, value):
        raise ValueError('df2_index_plus1 not deletable')

    @property
    def df1_diff_values_col_int_made_str(self) -> pd.DataFrame | pd.Series:
        return self._df1_diff_values_col_int_made_str.copy()

    @df1_diff_values_col_int_made_str.setter
    def df1_diff_values_col_int_made_str(self, value):
        raise ValueError('df1_diff_values_col_int_made_str not rewritable')

    @df1_diff_values_col_int_made_str.deleter
    def df1_diff_values_col_int_made_str(self, value):
        raise ValueError('df1_diff_values_col_int_made_str not deletable')

    @property
    def df2_diff_values_col_int_made_str(self) -> pd.DataFrame | pd.Series:
        return self._df2_diff_values_col_int_made_str.copy()

    @df2_diff_values_col_int_made_str.setter
    def df2_diff_values_col_int_made_str(self, value):
        raise ValueError('df2_diff_values_col_int_made_str not rewritable')

    @df2_diff_values_col_int_made_str.deleter
    def df2_diff_values_col_int_made_str(self, value):
        raise ValueError('df2_diff_values_col_int_made_str not deletable')

    @property
    def df1_as_object_diff_values_col_int_made_str(self) -> pd.DataFrame | pd.Series:
        return self._df1_as_object_diff_values_col_int_made_str.copy()

    @df1_as_object_diff_values_col_int_made_str.setter
    def df1_as_object_diff_values_col_int_made_str(self, value):
        raise ValueError('df1_as_object_diff_values_col_int_made_str not rewritable')

    @df1_as_object_diff_values_col_int_made_str.deleter
    def df1_as_object_diff_values_col_int_made_str(self, value):
        raise ValueError('df1_as_object_diff_values_col_int_made_str not deletable')

    @property
    def df2_as_object_diff_values_col_int_made_str(self) -> pd.DataFrame | pd.Series:
        return self._df2_as_object_diff_values_col_int_made_str.copy()

    @df2_as_object_diff_values_col_int_made_str.setter
    def df2_as_object_diff_values_col_int_made_str(self, value):
        raise ValueError('df2_as_object_diff_values_col_int_made_str not rewritable')

    @df2_as_object_diff_values_col_int_made_str.deleter
    def df2_as_object_diff_values_col_int_made_str(self, value):
        raise ValueError('df2_as_object_diff_values_col_int_made_str not deletable')

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
