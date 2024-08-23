import re

import pytest

from some_pd_tools import pd_format

from ..basedf import BaseDF


def test_wrong_types():
    """Test if wrong parameters type raises Exception."""
    with pytest.raises(
        ValueError,
        match=re.escape('df must be of type pd.DataFrame.'),
    ):
        pd_format.simplify_dtypes([1, 2, 3])
    with pytest.raises(
        ValueError,
        match=re.escape('df must be of type pd.DataFrame.'),
    ):
        pd_format.simplify_dtypes(1)
    with pytest.raises(
        ValueError,
        match=re.escape('df must be of type pd.DataFrame.'),
    ):
        pd_format.simplify_dtypes('hola')


def test_already_simplified():
    bdf = BaseDF()
    df1_simplified = pd_format.simplify_dtypes(bdf.df1)
    df1_dtypes = bdf.df1.dtypes
    df1_simplified_dtypes = df1_simplified.dtypes
    assert df1_dtypes.equals(df1_simplified_dtypes)


def test_simplified():
    bdf = BaseDF()
    df1_as_object_simplified = pd_format.simplify_dtypes(bdf.df1_as_object)
    df1_as_object_dtypes = bdf.df1_as_object.dtypes
    df1_as_object_simplified_dtypes = df1_as_object_simplified.dtypes
    assert not df1_as_object_dtypes.equals(df1_as_object_simplified_dtypes)
    print(df1_as_object_simplified_dtypes['col_str'])
    print(df1_as_object_simplified_dtypes)
    assert df1_as_object_simplified_dtypes['col_int'] == 'int64'
    assert df1_as_object_simplified_dtypes['col_float'] == 'float64'
    assert df1_as_object_simplified_dtypes['col_str'] == 'object'
    assert df1_as_object_simplified_dtypes['col_nan'] == 'float64'
    assert df1_as_object_simplified_dtypes['col_strnan'] == 'object'
