# pd_tools
Some Pandas tools like compare and number formatting.

# Install
```shell
pip install pd-tools
```

# pd_compare
Usage:
```python
from pd_tools import pd_compare
pd_compare.compare(
    df1, # First DataFrame
    df1_name, # First DataFrame name to be displayed
    df2,  # Second DataFrame
    df2_name,  # Second DataFrame name to be displayed
    show_common_cols, # List common columns
    int64_to_float64, # Transform float64 to int64
    round_to_decimals, # Decimals to round
    astype_str, # Transform dtypes to str
    path, # Excel file path
    fixed_cols, # Columns to always display (must be part of the first DataFrame)
)
```

This produces a report like the following:

```shell
** 😓 Not fully equal
————————————————————
...Comparing dtypes for common columns...
(Without special settings)
* No different dtypes.
————————————————————
🧪 Special settings:
* round_to_decimals[4]
————————————————————
** 😡 Not equal
————————————————————
...Comparing columns...
* Column count matches
* For original_spl:
  No extra columns.
* For loaded_spl:
  No extra columns.
————————————————————
...Comparing indexes...
* All indexes equal.
————————————————————
...Comparing values...
(Only equal columns and equal indexes, see above non value differences)
* 😓 Not equal columns (count[1]):
['description']
* 😓 Not equal rows (count[1]):
[0]
```
And returns:
```python
joined_df, equal_mask_df, diff_df, diff_columns, diff_rows, diff_original_vals_df = pd_compare.compare(...)
'''
joined_df: A DataFrame containing both input DataFrames, with fixed_cols from DataFrame 1, all columns from DataFrame 1 with suffix '_{df1_name}' and all columns from DataFrame 2 with suffix '_{df2_name}' and columns that differ in at least one cell with the name '{original column name}_diff' (containing the word 'diff' where the columns from DataFrame 1 and DataFrame 2 differ).

equal_mask_df: A DataFrame with True where the value is equal and False where the value is False for the common columns and indexes of both DataFrames.

diff_df: A subset of joined_df showing only rows and columns with differences.

diff_columns: Columns that have differences.

diff_rows: Rows that have differences.

diff_original_vals_df: A DataFrame where differences where found but with the original values.
'''
```


# pd_format
Usage:
```python
from pd_tools import pd_format
pd_format.format_nums(
    df, # DataFrame to format
    thousands, # Whether to add a thousands separator
    decimals, # Decimals to round
    )
```
This returns a DataFrame with the formatting.