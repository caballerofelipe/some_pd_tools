# some_pd_tools
Some Pandas tools like compare and number formatting.

# Install
```shell
pip install some-pd-tools
```

# pd_compare
## Usage (showing default values)
```python
from some_pd_tools import pd_compare
(
  equality_full,     # True if everything is equal
  equality_partial,  # True if common elements are equal
                     # even if using "special settings"
                     # (int64_to_float, round_to_decimals
                     # and astype_str)
  equality_metadata, # Comparison metadata
  )  = pd_compare.compare(
    df1,                     # First DataFrame
    df2,                     # Second DataFrame
    df1_name='df1',          # First DataFrame name to be displayed
    df2_name='df2',          # Second DataFrame name to be displayed
    show_common_cols=False,  # List common columns
    show_common_idxs=False,  # List common indexes
    int64_to_float64=False,  # Transform float64 to int64
    round_to_decimals=False, # Decimals to round
    astype_str=False,        # Transform dtypes to str
    path=None,               # Excel file path
    fixed_cols=[],           # Columns to always display
                             # (must be part of the first DataFrame)
    report=True,             # Whether to print the report
)
```

## Example
```python
# Create the DataFrames with json string
df1_json_str = '{"schema":{"fields":[{"name":"index","type":"integer"},{"name":"col_int","type":"integer"},{"name":"col_float","type":"number"},{"name":"col_str","type":"string"},{"name":"col_nan","type":"number"},{"name":"col_strnan","type":"string"},{"name":"col_df1extra","type":"integer"}],"pandas_version":"1.4.0"},"data":[{"index":0,"col_int":1,"col_float":1.1,"col_str":"a","col_nan":null,"col_strnan":"e","col_df1extra":5},{"index":1,"col_int":2,"col_float":2.2,"col_str":"b","col_nan":null,"col_strnan":"f","col_df1extra":6},{"index":2,"col_int":3,"col_float":3.3,"col_str":"c","col_nan":null,"col_strnan":"g","col_df1extra":7},{"index":3,"col_int":4,"col_float":4.4,"col_str":"d","col_nan":null,"col_strnan":null,"col_df1extra":8},{"index":0,"col_int":1,"col_float":1.1,"col_str":"a","col_nan":null,"col_strnan":"e","col_df1extra":5},{"index":1,"col_int":2,"col_float":2.2,"col_str":"b","col_nan":null,"col_strnan":"f","col_df1extra":6},{"index":2,"col_int":3,"col_float":3.3,"col_str":"c","col_nan":null,"col_strnan":"g","col_df1extra":7},{"index":3,"col_int":4,"col_float":4.4,"col_str":"d","col_nan":null,"col_strnan":null,"col_df1extra":8}]}'
df2_json_str = '{"schema":{"fields":[{"name":"index","type":"integer"},{"name":"col_int","type":"integer"},{"name":"col_float","type":"number"},{"name":"col_str","type":"string"},{"name":"col_nan","type":"number"},{"name":"col_strnan","type":"string"}],"pandas_version":"1.4.0"},"data":[{"index":1,"col_int":1,"col_float":1.1,"col_str":"a","col_nan":null,"col_strnan":"e"},{"index":2,"col_int":2,"col_float":2.2,"col_str":"b","col_nan":null,"col_strnan":"f"},{"index":3,"col_int":3,"col_float":3.3,"col_str":"c","col_nan":null,"col_strnan":"g"},{"index":4,"col_int":4,"col_float":4.4,"col_str":"d","col_nan":null,"col_strnan":null},{"index":1,"col_int":1,"col_float":1.1,"col_str":"a","col_nan":null,"col_strnan":"e"},{"index":2,"col_int":2,"col_float":2.2,"col_str":"b","col_nan":null,"col_strnan":"f"},{"index":3,"col_int":3,"col_float":3.3,"col_str":"c","col_nan":null,"col_strnan":"g"},{"index":4,"col_int":4,"col_float":4.4,"col_str":"d","col_nan":null,"col_strnan":null}]}'
df1_from_json_str = (pd
               .read_json(df1_json_str, orient='table')
               .set_index('index')
               .rename_axis(None)
)
df2_from_json_str = (pd
               .read_json(df2_json_str, orient='table')
               .set_index('index')
               .rename_axis(None)
)

# The actual comparison
returned = pd_compare.compare(
    df1=df1_from_json_str,
    df2=df2_from_json_str,
    df1_name='first_df',
    df2_name='second_df',
    show_common_cols=True,
    show_common_idxs=True,
    int64_to_float64=True,
    round_to_decimals=1,
    astype_str=True,
)
```
This produces a report like the following:
```shell
<<< 😓 Not fully equal >>>
————————————————————
# Comparing columns
-> 😓 Columns not equal
-> 😓 Columns lengths don't match
  ->  first_df: 6
  -> second_df: 5
-> first_df
  -> 😓 Exclusive columns:
  {'col_df1extra'}
  -> ✅ No duplicate columns
  -> ✅ No duplicate columns also common
-> second_df
  -> ✅ No exclusive columns
  -> ✅ No duplicate columns
  -> ✅ No duplicate columns also common
————————————————————
# Columns present in both DataFrames (intersection)
['col_float', 'col_int', 'col_nan', 'col_str', 'col_strnan']
————————————————————
# Comparing indexes
-> 😓 Indexes not equal
-> ✅ Indexes lengths match
-> first_df
  -> 😓 Exclusive indexes:
  {0}
  -> 😓 Duplicate indexes (value:count):
  {0: 2, 1: 2, 2: 2, 3: 2}
  -> 😓 Duplicate indexes also common (value:count):
  {1: 2, 2: 2, 3: 2}
-> second_df
  -> 😓 Exclusive indexes:
  {4}
  -> 😓 Duplicate indexes (value:count):
  {1: 2, 2: 2, 3: 2, 4: 2}
  -> 😓 Duplicate indexes also common (value:count):
  {1: 2, 2: 2, 3: 2}
————————————————————
# Indexes present in both DataFrames (intersection)
[1, 2, 3]
————————————————————
# Comparing dtypes for common columns
-> ✅ No different dtypes
————————————————————
# Special settings used
-> 🧪 int64_to_float64[True]
-> 🧪 round_to_decimals[1]
-> 🧪 astype_str[True]
————————————————————
# Equality with special settings
<<< 😡 Not fully Equal (with special setting) >>>
————————————————————
# Comparing values
  (Only equal columns and equal indexes, see above non value
differences)
-> 😓 Not equal columns (count[4]):
['col_float', 'col_int', 'col_str', 'col_strnan']
-> 😓 Not equal rows (count[6]):
[1, 1, 2, 2, 3, 3]
```

# pd_format
Usage:
```python
from some_pd_tools import pd_format
pd_format.format_nums(
    df, # DataFrame to format
    thousands, # Whether to add a thousands separator
    decimals, # Decimals to round
    )
```
This returns a DataFrame with the formatting.