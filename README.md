# some_pd_tools
Some Pandas tools for DataFrame comparing and formatting.

This includes the following functions:
```
some_pd_tools.pd_compare.compare
some_pd_tools.pd_compare.compare_dtypes
some_pd_tools.pd_compare.compare_lists
some_pd_tools.pd_compare.compute_equality_df

some_pd_tools.pd_format.approximate
some_pd_tools.pd_format.ceil
some_pd_tools.pd_format.floor
some_pd_tools.pd_format.number_separators
some_pd_tools.pd_format.obj_as_sorted_list
some_pd_tools.pd_format.simplify_dtypes
some_pd_tools.pd_format.trunc
```

**Note**: This package was developed and tested using Python 3.11.9. Might not work in previous versions.

# Install
```shell
pip install some-pd-tools
```

# Functions in `some_pd_tools.pd_compare`



## `some_pd_tools.pd_compare.compare()`

> Compares two DataFrames, creates a report and returns useful information.

For a more in-depth explanation check: [Report and logic explanation for pd_compare.compare.md](Report&#32;and&#32;logic&#32;explanation&#32;for&#32;pd_compare.compare.md).

### Docstring
<details>

```python
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
```
</details>

### Usage
```python
from some_pd_tools import pd_compare
pd_compare.compare(
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
)
```

### Example
<details open>
<summary>Code</summary>

```python
import pandas as pd
from some_pd_tools import pd_compare

df1 = pd.DataFrame(
    {
        'col_int': [1000, -2000, 3000, -4000000],
        'col_float': [-3333.3333333333, 4444.4444444444, -5555.5555555555, 6666.6666666666],
        'col_str': ['a', 'b', 'c', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['d', 'e', 'f', float('nan')],
        'col_df1extra': [5, 6, 7, 'i'],
    }
)
df2 = pd.DataFrame( # Important: dtype forced to 'object'
    {
        'col_int': ['3000endstr', '1000endstr', '-2000endstr', '-4000000endstr'],
        'col_float': [-5555.5555555555, -3333.3333333333, 4444.4444444444, 6666.6666666666],
        'col_str': ['c', 'a', 'b', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['f', 'd', 'e', float('nan')],
        'col_df2extra': ['j', 'k', 'l', 45],
    },
    dtype='object',
)

# returned is a len=3 tuple
returned = pd_compare.compare(
    df1,
    df2,
    df1_name='first_df',
    df2_name='second_df',
    round_to=None,
    report_print=True,
    report_file_path=None,
    report_file_overwrite=False,
    show_common_cols=True,  # default=False
    show_common_idxs=True,  # default=False
    show_all_dtypes=True,  # default=False
    xls_path=None,
    xls_overwrite=False,
    xls_compare_str_equal='',
    xls_compare_str_diff='*_diff_*',
    xls_fixed_cols=None,
    xls_datetime_rpl='%Y-%m-%d %H:%M:%S',
)
```
</details>

<details>
<summary>The above code produces the following report:</summary>

```shell
————————————————————
# Equality check
  (full)
<<< 😡 Not equal >>>
————————————————————
# Comparing columns from [first_df] and [second_df]
> 😓 Columns not equal
> ✅ Columns lengths match (6)
> ✅ Columns in common:
  ['col_float', 'col_int', 'col_nan', 'col_str', 'col_strnan']
> first_df
  > 😓 Exclusive columns:
    ['col_df1extra']
  > ✅ No duplicates columns
> second_df
  > 😓 Exclusive columns:
    ['col_df2extra']
  > ✅ No duplicates columns
————————————————————
# Comparing indexes from [first_df] and [second_df]
> ✅ Indexes equal
> ✅ Indexes in common:
  [0, 1, 2, 3]
> ✅ No duplicates indexes
————————————————————
# Checking common columns and indexes
> 😓 Columns and indexes are not equal in the two DataFrames
> 😈 From this point on, comparing only common columns and indexes
————————————————————
# Equality check
  (for common columns and indexes)
<<< 😡 Not equal >>>
————————————————————
# Comparing column dtypes
> 😓 Columns have different dtypes
  |----------|---------|--------|---------|
  |column    |different|first_df|second_df|
  |----------|---------|--------|---------|
  |col_float |    *    |float64 |object   |
  |col_int   |    *    |int64   |object   |
  |col_nan   |    *    |float64 |object   |
  |col_str   |         |object  |object   |
  |col_strnan|         |object  |object   |
  |----------|---------|--------|---------|
————————————————————
# Since dtypes are different, will try to simplify
————————————————————
# Trying to simplify dtypes
> ✅ first_df... already simplified
> 😓 second_df... simplified
> 😓 dtypes changed
————————————————————
# Comparing column dtypes
> 😓 Columns have different dtypes
  |----------|---------|--------|---------|
  |column    |different|first_df|second_df|
  |----------|---------|--------|---------|
  |col_float |         |float64 |float64  |
  |col_int   |    *    |int64   |object   |
  |col_nan   |         |float64 |float64  |
  |col_str   |         |object  |object   |
  |col_strnan|         |object  |object   |
  |----------|---------|--------|---------|
————————————————————
# Skipping equality check
  (since dtypes are not equal)
————————————————————
# Comparing values
  (from this point on, the DataFrames must have at least one different cell)
> 😓 Not equal columns (count=4):
  ['col_float', 'col_int', 'col_str', 'col_strnan']
> 😓 Not equal rows (count=4):
  [0, 1, 2, 3]
————————————————————
# Returning
  (False[equality_full], False[equality_partial], dict[equality_metadata])
```
</details>


## `some_pd_tools.pd_compare.compare_dtypes()`

> Compare dtypes for columns in two DataFrames.

### Docstring
<details>

```python
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
```
</details>

### Usage
```python
from some_pd_tools import pd_compare
pd_compare.compare_dtypes(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    df1_name: str = 'df1',
    df2_name: str = 'df2',
    report_print: bool = False,
    show_all_dtypes=False,
)
```

### Example
<details open>
<summary>Code</summary>

```python
import pandas as pd
from some_pd_tools import pd_compare

df1 = pd.DataFrame(
    {
        'col_int': [1000, -2000, 3000, -4000000],
        'col_float': [-3333.3333333333, 4444.4444444444, -5555.5555555555, 6666.6666666666],
        'col_str': ['a', 'b', 'c', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['d', 'e', 'f', float('nan')],
    }
)
df2 = pd.DataFrame(  # Important: dtype forced to 'object'
    {
        'col_int': ['3000endstr', '1000endstr', '-2000endstr', '-4000000endstr'],
        'col_float': [-5555.5555555555, -3333.3333333333, 4444.4444444444, 6666.6666666666],
        'col_str': ['c', 'a', 'b', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['f', 'd', 'e', float('nan')],
    },
    dtype='object',
)

# returned is a len=2 tuple
returned = pd_compare.compare_dtypes(
    df1=df1,
    df2=df2,
    df1_name='first_df',
    df2_name='second_df',
    report_print=True,
    show_all_dtypes=True,
)
```
</details>

<details>
<summary>The above code produces the following report:</summary>

```shell
————————————————————
# Comparing column dtypes
> 😓 Columns have different dtypes
  |----------|---------|--------|---------|
  |column    |different|first_df|second_df|
  |----------|---------|--------|---------|
  |col_float |    *    |float64 |object   |
  |col_int   |    *    |int64   |object   |
  |col_nan   |    *    |float64 |object   |
  |col_str   |         |object  |object   |
  |col_strnan|         |object  |object   |
  |----------|---------|--------|---------|
```
</details>



## `some_pd_tools.pd_compare.compare_lists`

> Compares two lists, can show a report.

### Docstring
<details>

```python
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
    report_print : bool, optional
        Whether to show the report, by default False.

    Returns
    -------
    tuple[bool, dict]
        Explanation:
        - <b>tuple[0]</b>: True or False if lists are equal.
        - <b>tuple[1]</b>: Metadata dict. This contains:
            <ul>
                <li><b>'list_common_set'</b>: set. Items in both lists.</li>
                <li><b>'list_1_excl_set'</b>: set. Items only present in list_1.</li>
                <li><b>'list_2_excl_set'</b>: set. Items only present in list_2.</li>
                <li><b>'list_1_dups_dict'</b>: dict(item:count). Items duplicated in list_1 with their respective count.</li>
                <li><b>'list_2_dups_dict'</b>: dict(item:count). Items duplicated in list_2 with their respective count.</li>
                <li><b>'report'</b>: str. The generated report, this stores the report even if it wasn't shown when executing this function.</li>
            </ul>

    Raises
    ------
    ValueError
        Raised if either list_1 or list_2 are not of type list.
    ValueError
        Raised if either list_1_name, list_2_name, type_name or type_name_plural are not of type str.
    """
```
</details>

### Usage
```python
from some_pd_tools import pd_compare
pd_compare.compare_lists(
    list_1: list,
    list_2: list,
    show_common_items: bool = False,
    list_1_name: str = 'list_1',
    list_2_name: str = 'list_2',
    type_name: str = 'item',
    type_name_plural: str = 'items',
    report_print: bool = False,
)
```

### Example
<details open>
<summary>Code</summary>

```python
from some_pd_tools import pd_compare

list_1 = [1000, -2000, 3000, -4000000, 999, 'a str', 1000, 123, 123]
list_2 = ['3000endstr', '1000endstr', '-2000endstr', '-4000000endstr', 123, 123]

# returned is a len=2 tuple
returned = pd_compare.compare_lists(
    list_1=list_1,
    list_2=list_2,
    show_common_items=True,
    list_1_name='list_1',
    list_2_name='list_2',
    type_name='item',
    type_name_plural='items',
    report_print=True,
)
```
</details>

<details>
<summary>The above code produces the following report:</summary>

```shell
————————————————————
# Comparing items from [list_1] and [list_2]
> 😓 Items not equal
> 😓 Items lengths don't match
  > list_1: 9
  > list_2: 6
> ✅ Items in common:
  [123]
> list_1
  > 😓 Exclusive items:
    [-2000, -4000000, 1000, 3000, 999, 'a str']
  > 😓 Duplicates items (value,count):
    [(1000, 2), (123, 2)]
  > 😓 Duplicates items exclusive:
    [1000]
  > 😓 Duplicates items in common:
    [123]
> list_2
  > 😓 Exclusive items:
    ['-2000endstr', '-4000000endstr', '1000endstr', '3000endstr']
  > 😓 Duplicates items (value,count):
    [(123, 2)]
  > ✅ No duplicates items exclusive
  > 😓 Duplicates items in common:
    [123]
```
</details>



## `some_pd_tools.pd_compare.compute_equality_df()`

> Compares the cell values of two DataFrames.

### Docstring
<details>

```python
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
```
</details>

### Usage
```python
from some_pd_tools import pd_compare
pd_compare.compute_equality_df(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
)
```

### Example
<details open>
<summary>Code</summary>

```python
import pandas as pd
from some_pd_tools import pd_compare

df1 = pd.DataFrame(
    {
        'col_int': [1000, -2000, 3000, -4000000],
        'col_float': [-3333.3333333333, 4444.4444444444, -5555.5555555555, 6666.6666666666],
        'col_str': ['a', 'b', 'c', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['d', 'e', 'f', float('nan')],
    }
)
df2 = pd.DataFrame(  # Important: dtype forced to 'object'
    {
        'col_int': ['3000endstr', '1000endstr', '-2000endstr', '-4000000endstr'],
        'col_float': [-5555.5555555555, -3333.3333333333, 4444.4444444444, 6666.6666666666],
        'col_str': ['c', 'a', 'b', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['f', 'd', 'e', float('nan')],
    },
    dtype='object',
)

df = pd_compare.compute_equality_df(df1, df2)
print(df)
```
</details>

<details>
<summary>The above code prints the following:</summary>

```shell
   col_int  col_float  col_str  col_nan  col_strnan
0    False      False    False     True       False
1    False      False    False     True       False
2    False      False    False     True       False
3    False       True     True     True        True
```
</details>




# Functions in `some_pd_tools.pd_format`



## `some_pd_tools.pd_format.approximate`
> Approximate numbers using a `round_to` method.

### Docstring
<details>

```python
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
```
</details>

### Usage
```python
from some_pd_tools import pd_format
pd_format.approximate(
    df: pd.DataFrame,
    round_to: None | int | str = None,
)
```

### Example
<details open>
<summary>Code</summary>

```python
import pandas as pd
from some_pd_tools import pd_format

df = pd.DataFrame(
    {
        'col_int': [1000, -2000, 3000, -4000000],
        'col_float': [-3333.3333333333, 4444.4444444444, -5555.5555555555, 6666.6666666666],
        'col_str': ['a', 'b', 'c', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['d', 'e', 'f', float('nan')],
    }
)

returned_df = pd_format.approximate(df, round_to=1)
print(returned_df)
```
</details>

<details >
<summary>The code above prints this.</summary>

```
col_int  col_float          col_str  col_nan col_strnan
0     1000    -3333.3                a      NaN          d
1    -2000     4444.4                b      NaN          e
2     3000    -5555.6                c      NaN          f
3 -4000000     6666.7  4444.4444444444   8888.9        NaN
```
</details>



## `some_pd_tools.pd_format.ceil`
> Does a ceil operation on floats columns. Uses np.ceil. From np.ceil's documentation: "The ceil of the scalar x is the smallest integer i, such that i >= x.".

### Docstring
<details>

```python
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
```
</details>

### Usage
```python
from some_pd_tools import pd_format
pd_format.ceil(df: pd.DataFrame | pd.Series)
```

### Example
<details open>
<summary>Code</summary>

```python
import pandas as pd
from some_pd_tools import pd_format

df = pd.DataFrame(
    {
        'col_int': [1000, -2000, 3000, -4000000],
        'col_float': [-3333.3333333333, 4444.4444444444, -5555.5555555555, 6666.6666666666],
        'col_str': ['a', 'b', 'c', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['d', 'e', 'f', float('nan')],
    }
)

returned_df = pd_format.ceil(df)
print(returned_df)
```
</details>

<details >
<summary>The code above prints this.</summary>

```
   col_int  col_float          col_str  col_nan col_strnan
0     1000    -3333.0                a      NaN          d
1    -2000     4445.0                b      NaN          e
2     3000    -5555.0                c      NaN          f
3 -4000000     6667.0  4444.4444444444   8889.0        NaN
```
</details>



## `some_pd_tools.pd_format.floor`
> Does a floor operation on floats columns. Uses np.floor. From np.floor's documentation: "The floor of the scalar x is the largest integer i, such that i <= x."

### Docstring
<details>

```python
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
```
</details>

### Usage
```python
from some_pd_tools import pd_format
pd_format.floor(df: pd.DataFrame | pd.Series)
```

### Example
<details open>
<summary>Code</summary>

```python
import pandas as pd
from some_pd_tools import pd_format

df = pd.DataFrame(
    {
        'col_int': [1000, -2000, 3000, -4000000],
        'col_float': [-3333.3333333333, 4444.4444444444, -5555.5555555555, 6666.6666666666],
        'col_str': ['a', 'b', 'c', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['d', 'e', 'f', float('nan')],
    }
)

returned_df = pd_format.floor(df)
print(returned_df)
```
</details>

<details >
<summary>The code above prints this.</summary>

```
   col_int  col_float          col_str  col_nan col_strnan
0     1000    -3334.0                a      NaN          d
1    -2000     4444.0                b      NaN          e
2     3000    -5556.0                c      NaN          f
3 -4000000     6666.0  4444.4444444444   8888.0        NaN
```
</details>



## `some_pd_tools.pd_format.number_separators`
> Transform a DataFrame or Series adding a thousands separator and optionally modifying it and the decimals separator.

### Docstring
<details>

```python
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
```
</details>

### Usage
```python
from some_pd_tools import pd_format
pd_format.number_separators(
    df: pd.DataFrame | pd.Series, precision: int = 6, thousands_sep=',', decimals_sep='.'
)
```

### Example
<details open>
<summary>Code</summary>

```python
import pandas as pd
from some_pd_tools import pd_format

df = pd.DataFrame(
    {
        'col_int': [1000, -2000, 3000, -4000000],
        'col_float': [-3333.3333333333, 4444.4444444444, -5555.5555555555, 6666.6666666666],
        'col_str': ['a', 'b', 'c', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['d', 'e', 'f', float('nan')],
    }
)

returned_df = pd_format.number_separators(df, precision=4, thousands_sep='.', decimals_sep=',')
print(returned_df)
```
</details>

<details >
<summary>The code above prints this.</summary>

```
      col_int    col_float          col_str     col_nan col_strnan
0       1.000  -3.333,3333                a         nan          d
1      -2.000   4.444,4444                b         nan          e
2       3.000  -5.555,5556                c         nan          f
3  -4.000.000   6.666,6667  4444.4444444444  8.888,8888        NaN
```
</details>



## `some_pd_tools.pd_format.obj_as_sorted_list`
> Return an object as a sorted list. Uses `str()` to transform keys to string, so for instance sorting (1,2,12) will sort to: (1,12,2).

### Docstring
<details>

```python
    """Return an object as a sorted list. Uses `str()` to transform keys to string, so for instance sorting (1,2,12) will sort to: (1,12,2).

    Note: Not implemented for "every" object, only the ones needed in this project: dict, set, tuple and list. Raises exception if none of these types of objects are tried to be transformed.

    Parameters
    ----------
    obj : object
        The object.

    Returns
    -------
    list
        The sorted object as a list.

    Raises
    ------
    ValueError
        Function not implemented for type:{type(obj)}.
    """
```
</details>

### Usage
```python
from some_pd_tools import pd_format
pd_format.obj_as_sorted_list(obj: object)
```

### Example
<details open>
<summary>Code</summary>

```python
from some_pd_tools import pd_format
pd_format.obj_as_sorted_list([1,12,4,1,11,9,10])
```
</details>

<details >
<summary>The code above prints this.</summary>

```
[1, 1, 10, 11, 12, 4, 9]
```
</details>



## `some_pd_tools.pd_format.simplify_dtypes`
> Allows to simplify dtypes, for instance, pass from float64 to int64 if no decimals are present.

### Docstring
<details>

```python
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
```
</details>

### Usage
```python
from some_pd_tools import pd_format
pd_format.simplify_dtypes(df: pd.DataFrame)
```

### Example
<details open>
<summary>Code</summary>

```python
import pandas as pd
from some_pd_tools import pd_format

df = pd.DataFrame(
    {
        'col_int': [1000, -2000, 3000, -4000000],
        'col_float': [-3333.3333333333, 4444.4444444444, -5555.5555555555, 6666.6666666666],
        'col_str': ['a', 'b', 'c', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['d', 'e', 'f', float('nan')],
    },
    dtype='object'
)
print(df.dtypes)
print('*********')
returned_df = pd_format.simplify_dtypes(df)
print(returned_df.dtypes)
```
</details>

<details >
<summary>The code above prints this.</summary>

```
col_int       object
col_float     object
col_str       object
col_nan       object
col_strnan    object
dtype: object
*********
col_int         int64
col_float     float64
col_str        object
col_nan       float64
col_strnan     object
dtype: object
```
</details>



## `some_pd_tools.pd_format.trunc`
> Remove decimals from floats columns. Uses np.trunc. From np.trunc's documentation: "The truncated value of the scalar x is the nearest integer i which is closer to zero than x is.".

### Docstring
<details>

```python
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
```
</details>

### Usage
```python
from some_pd_tools import pd_format
pd_format.trunc(df: pd.DataFrame | pd.Series)
```

### Example
<details open>
<summary>Code</summary>

```python
import pandas as pd
from some_pd_tools import pd_format

df = pd.DataFrame(
    {
        'col_int': [1000, -2000, 3000, -4000000],
        'col_float': [-3333.3333333333, 4444.4444444444, -5555.5555555555, 6666.6666666666],
        'col_str': ['a', 'b', 'c', '4444.4444444444'],
        'col_nan': [float('nan'), float('nan'), float('nan'), 8888.8888],
        'col_strnan': ['d', 'e', 'f', float('nan')],
    }
)

returned_df = pd_format.trunc(df)
print(returned_df)
```
</details>

<details >
<summary>The code above prints this.</summary>

```
   col_int  col_float          col_str  col_nan col_strnan
0     1000    -3333.0                a      NaN          d
1    -2000     4444.0                b      NaN          e
2     3000    -5555.0                c      NaN          f
3 -4000000     6666.0  4444.4444444444   8888.0        NaN
```
</details>