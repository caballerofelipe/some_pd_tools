This is an independent file with more information on what is returned in the function **`pd_compare.compare()`** and the logical flow of what is done while producing the report. This function returns three elements:
- **[0]**: (`equality_full`): checks for full equality for the two DataFrames **after** sorting columns and indexes.
  - **True** if the two compared DataFrames are completely equal.
  - **False** otherwise.
- **[1]**: (`equality_partial`): checks for full equality for the two DataFrames **after** some operation done to them, see below for explanation of which operations are done.
  - **True** if the two compared DataFrames are equal after some operation.
  - **False** otherwise.
- **[2]**: (`equality_metadata`): metadata useful to keep track of what was done during the comparison:
  - **['params']**: The list of parameters used in the function call.
  - **['variables']**: Some inner variables useful to keep track of what happened in the comparison and have information on what is different.
  - **['report']**: The same report, useful if the report wasn't printed (`report_print` == False) or to do something with it.

# The elements of the Report
These are the elements shown in the report:
- **Titles**: Starting with "#", following line.
- **Subtitles**: Below a title, in parenthesis. Only appears if it provides useful additional information.
- **Events**: Starting with a ">", depending of indentation can be a sub-event.
- **Data**: Some data is shown, after an event without specific formatting.

# Report explanation
The next section (**The Report**) explains what happens in each part of the report grouped by its Title.

For each Title the following is explained:
- **What is done.**
- **Metadata ['variables']**: the variables added while doing the comparison.
- **Logic considerations**: if the function will return, if it will go to a specific Title or if the flow will continue.

About **Metadata ['variables']**:
- If the function hits a `return` the following variables are not created (each title is shown as a header).
- These variables are the ones returned in the metadata so inner variables are not taken into consideration.
- These variables are stored inside the returned metadata (third item in the returned tuple) under the 'variables' key.

**Important considerations**. Before reporting and processing begins:
- Error checking for parameters is done.
- A copy of df1 and df2 are made with columns and indexes sorted. This allows the comparison to work even if they have differently sorted columns and indexes.
- From this point on, when referring to df1 and df2, this means the sorted copy and not the original DataFrames.

**Note about the logic**: The logic stated in this document doesn't adhere 100% to the logic in the code, specifically when calling `_dtypes_simp_and_eqlty_check()` (after Titles **CCD / Since dtypes are different, will try to simplify** and **Rounding [round_to=<round_to>] — Alias ROUNDING**). But this document explains it in a more natural way to be able to make a parallel between the report and what is returned.

# The Report

## Equality Check (full)
- **What is done**: Checks wether the two DataFrames are equal or not, **note** that columns and indexes are ordered before doing the comparison.
- **Metadata ['variables']**: No variables created.
- **Logic considerations**: Depending on the equality result:
  - `True`: shows **Returning (\<bool>[equality_full], \<bool>[equality_partial], dict[equality_metadata])** and then returns:
	  ```python
		True,
		False, 
		{
			'params': {...},
			'variables': {<empty>},
			'report': <str>
		}
		```
  - `False`: no return, continues.

## Comparing columns from [{df1_name}] and [{df2_name}]
(replace df1_name and df2_name with the given names)
- **What is done**: Compares the columns from the two DataFrames. This part of the function uses `pd_compare.compare_lists()` internally.
- **Metadata ['variables']**:
  - **cols_compare_equality**: *bool*. Whether columns in the two DataFrames are all equal or not.
  - **cols_common_set**: *set*. A set containing columns that appear in both DataFrames.
  - **cols_common_list_sorted**: *list*. The same values as in **cols_common_set** but sorted into a list.
  - **cols_df1_excl_set**: *set*. A set containing the columns that are exclusive to df1.
  - **cols_df2_excl_set**: *set*. A set containing the columns that are exclusive to df2.
  - **cols_df1_dups_dict**: dict(column:count). Columns duplicated in df1 with their respective count.
  - **cols_df2_dups_dict**: dict(column:count). Columns duplicated in df2 with their respective count.
  - **cols_df1_dups_common_dict**: dict(column:count). Columns duplicated in df1 **that also exist in df2** with their respective count.
  - **cols_df2_dups_common_dict**: dict(column:count). Columns duplicated in df2 **that also exist in df1** with their respective count.
  - **error**: str. If there are column duplicates, read on **Logic considerations**.
- **Logic considerations**:
  - If there are duplicate columns in either DataFrame that appear in the other DataFrame, the function will return and an error will be added to the report and as a key to the 'variables' section of the metadata returned. Shows the title **Returning (\<bool>[equality_full], \<bool>[equality_partial], dict[equality_metadata])** and then returns:
	  ```python
	  False,
	  False,
	  {
		  'params': {...},
		  'variables': {<all variables created up to this point>},
		  'report': <str>
	  }
	  ```
  - **cols_df1_dups_common_dict** and **cols_df2_dups_common_dict** are used to check if the error needs to be reported. If either has len() of more than 0.

## Comparing indexes from [{df1_name}] and [{df2_name}]
(replace df1_name and df2_name with the given names)
- **What is done**: Compares the indexes from the two DataFrames. This part of the function uses `pd_compare.compare_lists()` internally.
- **Metadata ['variables']**:
  - **cols_compare_equality**: *bool*. Whether indexes in the two DataFrames are all equal or not.
  - **cols_common_set**: *set*. A set containing indexes that appear in both DataFrames.
  - **cols_common_list_sorted**: *list*. The same values as in **cols_common_set** but sorted into a list.
  - **cols_df1_excl_set**: *set*. A set containing the indexes that are exclusive to df1.
  - **cols_df2_excl_set**: *set*. A set containing the indexes that are exclusive to df2.
  - **cols_df1_dups_dict**: dict(index:count). Indexes duplicated in df1 with their respective count.
  - **cols_df2_dups_dict**: dict(index:count). Indexes duplicated in df2 with their respective count.
  - **cols_df1_dups_common_dict**: dict(index:count). Indexes duplicated in df1 **that also exist in df2** with their respective count.
  - **cols_df2_dups_common_dict**: dict(index:count). Indexes duplicated in df2 **that also exist in df1** with their respective count.
  - **error**: str. If there are index duplicates, read on **Logic considerations**.
- **Logic considerations**:
  - If there are duplicate indexes in either DataFrame that appear in the other DataFrame, the function will return and an error will be added to the report and as a key to the 'variables' section of the metadata returned. Shows the title **Returning (\<bool>[equality_full], \<bool>[equality_partial], dict[equality_metadata])** and then returns:
	  ```python
	  False,
	  False,
	  {
		  'params': {...},
		  'variables': {<all variables created up to this point>},
		  'report': <str>
	  }
	  ```
  - **cols_df1_dups_common_dict** and **cols_df2_dups_common_dict** are used to check if the error needs to be reported. If either has len() of more than 0.

## Checking common columns and indexes
- **What is done**: Reports whether columns and indexes in both DataFrames are equal or not.
- **Metadata ['variables']**:
  - **df1_common**: DataFrame. A copy of df1 selecting only common columns and indexes to both compared DataFrames.
  - **df2_common**: DataFrame. A copy of df2 selecting only common columns and indexes to both compared DataFrames.
- **Notes about the variables**:
  - The variables created in this part are used from this point on and replace df1 and df2. These variables include only the common columns and indexes that exist in both DataFrames.
  - **But** if all columns and indexes exist in both DataFrames (A.K.A. their columns and indexes are equal) these variables seem redundant and *yes they are*. However, this is on purpose to avoid having to select common columns and indexes in the rest of the code (if not all columns and indexes are equal in both DataFrames), so this is to keep following code cleaner.
  - **df1_common** and **df2_common** might be changed in next steps to try to compare them according to specific conditions. Read on.
- **Logic considerations**:
  - If all columns and indexes are **not** equal, the flow continues to **Equality check for common columns and indexes** since we want to check if the two DataFrames are equal if we only take into consideration the same columns and indexes in both.
  - If all columns and indexes are equal in the two DataFrames, the flow continues to title **Comparing column dtypes** since we know all columns and indexes are equal and we don't need to redo the same comparison made in the beginning (in **Equality Check (full)**).

## Equality check (for common columns and indexes)
- **What is done**: Checks wether the two DataFrames are equal or not, selecting only the columns and indexes that are equal in the two DataFrames, **note** that columns and indexes are ordered before doing the comparison.
- **Metadata ['variables']**: No variables added.
- **Logic considerations**: Depending on the equality result:
  - `True`: shows **Returning (\<bool>[equality_full], \<bool>[equality_partial], dict[equality_metadata])** and then returns:
	  ```python
	  False,
	  True,
	  {
		  'params': {...},
		  'variables': {<all variables created up to this point>},
		  'report': <str>
	  }
	  ```
  - `False`: no return, continues.

## Comparing column dtypes — Alias CCD
- **What is done**: Reports dtypes differences between the two DataFrames' common columns.
- **Metadata ['variables']**:
  - **common_cols_dtypes_equality**: bool. True if all dtypes are equal, False otherwise.
  - **common_cols_dtypes_df**: DataFrame. Contains the dtypes of the original DataFrames (only common columns), where the index is the analyzed column and the following 3 columns:
		1. 'different' representing wether the column is different or not in both input DataFrames (True means different, False means equal).
		2. {df1_name} (stated name for first DataFrame): the dtype for the given column in df1.
		3. {df2_name} (stated name for second DataFrame): the dtype for the given column in df2.
- **Logic considerations**:
  - If all dtypes are equal (**common_cols_dtypes_equality** is True), we know that the two DataFrame must have different values since the dtypes are equal. All bellow sections starting with "CCD / " are omitted.
  - If there are different dtypes, the function will try simplifying them in **CCD / Since dtypes are different, will try to simplify**.

### CCD / Since dtypes are different, will try to simplify
- **What is done**: Does nothing, this is only a message stating that the function will try to simplify the dtypes.
- **Metadata ['variables']**: No variables added.
- **Logic considerations**: Flow continues to next **CCD / Trying to simplify dtypes**.

### CCD / Trying to simplify dtypes
- **What is done**: Tries to simplify the dtypes of both DataFrames using `pd_format.simplify_dtypes()`. The goal is to make dtypes as simple as possible and then check if the two DataFrames are equal (in another title), meaning the values are equal but not considered equal because of different dtypes.
- **Metadata ['variables']**:
  - **common_cols_dtypes_simplified**: bool. True if dtypes was simplified, False otherwise.
  - If the dtypes of their columns was simplified (**common_cols_dtypes_simplified** is True), modifies **df1_common** and **df2_common**.
- **Logic considerations**:
  - If dtypes could not be simplified (message "✅ No dtypes changed") all remaining "CCD / " titles are skipped.
  - If dtypes could be simplified the function shows **CCD / Comparing column dtypes**.

### CCD / Comparing column dtypes
- **What is done**: Reports dtypes differences between the two DataFrames' common columns after simplifying attempt in **CCD / Trying to simplify dtypes**.
- **Metadata ['variables']**:
  - **common_cols_dtypes_simplified_equality**: bool. True if simplified dtypes for columns in the two DataFrames are equal (meaning each column in one DataFrame has the same dtype as the same column in the other DataFrame), False otherwise.
  - **common_cols_dtypes_simplified_df**: DataFrame. Contains the dtypes of the modified (simplified dtypes) DataFrames (only common columns), where the index is the analyzed column and the following 3 columns:
		1. 'different' representing wether the column is different or not in both input DataFrames (True means different, False means equal).
		2. {df1_name} (stated name for first DataFrame): the dtype for the given column in df1.
		3. {df2_name} (stated name for second DataFrame): the dtype for the given column in df2.
- **Logic considerations**:
  - If all simplified dtypes are **not** equal, continues to **CCD / Skipping equality check (since dtypes are not equal)**.
  - If all simplified dtypes are equal, continues to **CCD / Equality check (since dtypes are now equal)**.

### CCD / Skipping equality check (since dtypes are not equal)
- **What is done**: Does nothing, this is only a message to explain that an equality check is not useful at this point since the dtypes are different and an equality would return False.
- **Metadata ['variables']**: No variables added.
- **Logic considerations**: Skip remaining "CCD / " titles.

### CCD / Equality check (since dtypes are now equal)
- **What is done**: Checks wether the two modified DataFrames are equal or not.
- **Metadata ['variables']**: No variables created.
- **Logic considerations**: Depending on the equality result:
  - `True`: shows **Returning (\<bool>[equality_full], \<bool>[equality_partial], dict[equality_metadata])** and then returns:
	  ```python
		False,
		True, 
		{
			'params': {...},
			'variables': {<all variables created up to this point>},
			'report': <str>
		}
		```
  - `False`: no return, continues.

## Rounding [round_to=<round_to>] — Alias ROUNDING
- **What is done**: This is an optional operation done when setting the `round_to` parameter, it uses `pd_format.approximate()`. Since we want to check how similar the two DataFrames are we will modify slightly the numbers and check if that modification makes them equal. `round_to` can be one of these parameters:
  - **Positive integer**: When setting `round_to` to a positive integer, it will round the float columns to the decimal designated by this positive integer. (e.g. 1.1111111 rounded to 1 decimal means 1.1).
  - **floor**: floors floats (e.g. 1.8 is transformed to 1).
  - **cleil**: ceils floats (e.g. 1.8 is transformed to 2).
  - **trunc**: removes the decimal part from numbers (e.g. 1.8 is transformed to 1).
- **Metadata ['variables']**: **df1_common** and **df2_common** might be changed if they contain floats.
- **Logic considerations**:
  - After the rounding, an equality check will be performed in **ROUNDING / Equality check**.

### ROUNDING / Equality check
- **What is done**: Checks wether the two modified DataFrames, after the rounding, are equal or not.
- **Metadata ['variables']**:  No variables added.
- **Logic considerations**:
  - `True`: shows **Returning (\<bool>[equality_full], \<bool>[equality_partial], dict[equality_metadata])** and then returns:
	  ```python
		False,
		True, 
		{
			'params': {...},
			'variables': {<all variables created up to this point>},
			'report': <str>
		}
		```
  - `False`: If the equality fails, the function will try to simplify the dtypes in **ROUNDING / Trying to simplify dtypes**. If the rounding had no effect on the DataFrames the simplification will also have no effect.

### ROUNDING / Trying to simplify dtypes
- **What is done**: Tries to simplify the dtypes of both DataFrames using `pd_format.simplify_dtypes()`. The goal is to make dtypes as simple as possible and then check if the two DataFrames are equal (in another title), meaning the values are equal but not considered equal because of different dtypes.
- **Metadata ['variables']**:
  - **common_cols_post_round_dtypes_simplified**: bool. True if dtypes was simplified, False otherwise.
  - If the dtypes of their columns was simplified (**common_cols_post_round_dtypes_simplified** is True), modifies **df1_common** and **df2_common**.
- **Logic considerations**:
  - If dtypes could not be simplified (message "✅ No dtypes changed") all remaining "ROUNDING / " titles are skipped.
  - If dtypes could be simplified the function shows **ROUNDING / Comparing column dtypes**.

### ROUNDING / Comparing column dtypes
- **What is done**: Reports dtypes differences between the two DataFrames' common columns after simplifying attempt in **ROUNDING / Trying to simplify dtypes**.
- **Metadata ['variables']**:
  - **common_cols_post_round_dtypes_simplified_equality**: bool. True if simplified dtypes for columns in the two DataFrames are equal (meaning each column in one DataFrame has the same dtype as the same column in the other DataFrame), False otherwise.
  - **common_cols_post_round_dtypes_simplified_df**: DataFrame. Contains the dtypes of the modified (simplified dtypes) DataFrames (only common columns), where the index is the analyzed column and the following 3 columns:
		1. 'different' representing wether the column is different or not in both input DataFrames (True means different, False means equal).
		2. {df1_name} (stated name for first DataFrame): the dtype for the given column in df1.
		3. {df2_name} (stated name for second DataFrame): the dtype for the given column in df2.
- **Logic considerations**:
  - If all simplified dtypes are **not** equal, continues to **ROUNDING / Skipping equality check (since dtypes are not equal)**.
  - If all simplified dtypes are equal, continues to **ROUNDING / Equality check (since dtypes are now equal)**.

### ROUNDING / Skipping equality check (since dtypes are not equal)
- **What is done**: Does nothing, this is only a message to explain that an equality check is not useful at this point since the dtypes are different and an equality would return False.
- **Metadata ['variables']**: No variables added.
- **Logic considerations**: Skip remaining "ROUNDING / " titles.

### ROUNDING / Equality check (since dtypes are now equal)
- **What is done**: Checks wether the two modified DataFrames are equal or not.
- **Metadata ['variables']**: No variables created.
- **Logic considerations**: Depending on the equality result:
  - `True`: shows **Returning (\<bool>[equality_full], \<bool>[equality_partial], dict[equality_metadata])** and then returns:
	  ```python
		False,
		True, 
		{
			'params': {...},
			'variables': {<all variables created up to this point>},
			'report': <str>
		}
		```
  - `False`: no return, continues.

## Comparing values (from this point on, the DataFrames must have at least one different cell)
- **What is done**: At this point we know that the values in the two DataFames must be different, *at least for one cell*. All processes done prior to this point didn't make the DataFrames equal so we're left with comparing the values on a per cell basis, this is what is done at this point.
- **Metadata ['variables']**:
  - **equality_df**: DataFrame. A DataFrame having the same structure, common indexes and columns for the two DataFrames. The whole DataFrame is filled with booleans. True in a cell means that specific cell's value is equal in the two DataFrames, False means otherwise.
  - **cols_equal_list_sorted**: list. Contains a sorted list of all columns that are equal in the two DataFrames.
  - **rows_equal_list_sorted**:  list. Contains a sorted list of all rows that are equal in the two DataFrames.
  - **cols_diff_list_sorted**: list. Contains a sorted list of all columns that are **not** equal in the two DataFrames (at least one cell is different).
  - **rows_diff_list_sorted**: list. Contains a sorted list of all rows that are **not** equal in the two DataFrames (at least one cell is different).
  - **joined_df**: DataFrame. Allows to see the differences of the two DataFrames in one single DataFrame. This new DataFrame only takes into account the rows and columns (indexes and columns) that are common to the two DataFrames to be compared. It has the following properties:
    - It contains the values from **df1_common**, **df2_common** and also booleans stating if those values are different or not.
    - It has a MultiIndex for columns.
      - The first level is the name of a given compared column, which appears in df1 and df2. The first level is sorted according to the compared columns' names.
      - For every first level column, there are three second level columns:
        - The first sub-column's name is the given name to the first DataFrame (configured using `df1_name` parameter). This column contains the values from df1.
        - The second sub-column's name is the given name to the second DataFrame (configured using `df2_name` parameter). This column contains the values from df2.
        - The third sub-column is called 'different'. It contains a boolean, True if the values from df1 and df2 are equal, False otherwise.
     - See an example of what **joined_df** in the Example section below.
- **Logic considerations**: Flow continues to next title.

## Creating Excel (\<file location>)
- **What is done**: This is an optional operation done when setting the `xls_path` parameter, it creates an Excel file. The Excel created by path is similar to **joined_df**. The file is useful to have a look at the data and play with it inside Excel without having to program to do so. It differs in the following:
  - If used, `xls_fixed_cols`, creates a set of fixed columns in the beginning of the Excel file. These columns are fixed like when using 'Freeze panes' on Excel directly. This is useful to browse data having columns that don't move and seeing data related to those columns.
  - Because of the MultiIndex, there are 3 rows at the top, 2 of those are the first and second index. The third row is empty but could be used to the index name (rows' name).
  - The second row has a filter (or AutoFilter).
  - This function's parameters `xls_compare_str_equal` and `xls_compare_str_diff` can configure how differences are shown. The default for `xls_compare_str_equal` is an empty string and the default for `xls_compare_str_diff` is '`*_diff_*`', which makes it easy to use Find in Excel to locate differences. These parameters can be any string according to the user's needs.
  - These are the parameters that can be changed on the function call:
    - **xls_path**: str. The path to the Excel file.
    - **xls_overwrite**: bool. Defines if an existing file should be overwritten. True overwrites, False raises an exception if the file exists.
    - **xls_compare_str_equal**: str. A string to be placed inside a cell in the Excel file when both DataFrames contain the same value. Useful to know what cells are equal in the two DataFrames, by default empty. Can be used with the *find* function in Excel.
    - **xls_compare_str_diff**: str. A string to be placed inside a cell in the Excel file when the cell's value in the tow DataFrames is different. Useful to know what cells are different in the two DataFrames, by default "`*_diff_*`". Can be used with the *find* function in Excel.
    - **xls_fixed_cols**: list. A list of str containing columns that will be fixed in the generated Excel file. The columns in the list must exist in both DataFrames.
    - **xls_datetime_rpl**: str. A string containing the format to be used for a column with a datetime64 dtype, useful to have a specific format for dates in Excel.
- **Metadata ['variables']**:
  - **xls_path**: str. The full path to the created Excel file.
- **Logic considerations**: Flow continues to next title.

### Generated Excel example
This is what is seen in Excel when opening the file. Consider that 'col_float' is fixed.

<table class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="2" halign="left">col_float (fixed cols)</th>
      <th colspan="3" halign="left">col_float</th>
      <th colspan="3" halign="left">col_int</th>
      <th colspan="3" halign="left">col_nan</th>
      <th colspan="3" halign="left">col_str</th>
      <th colspan="3" halign="left">col_strnan</th>
    </tr>
    <tr>
      <th></th>
      <th>first_df</th>
      <th>second_df</th>
      <th>first_df</th>
      <th>second_df</th>
      <th>different</th>
      <th>first_df</th>
      <th>second_df</th>
      <th>different</th>
      <th>first_df</th>
      <th>second_df</th>
      <th>different</th>
      <th>first_df</th>
      <th>second_df</th>
      <th>different</th>
      <th>first_df</th>
      <th>second_df</th>
      <th>different</th>
    </tr>
    <tr>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
      <th>&nbsp;</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th><td>-3333.333333</td><td>-5555.555556</td><td>-3333.333333</td><td>-5555.555556</td><td style="color:red;">True</td><td>1000</td><td>3000endstr</td><td style="color:red;">True</td><td>NaN</td><td>NaN</td><td style="color:blue">False</td><td>a</td><td>c</td><td style="color:red;">True</td><td>d</td><td>f</td><td style="color:red;">True</td>
    </tr>
    <tr>
      <th>1</th><td>4444.444444</td><td>-3333.333333</td><td>4444.444444</td><td>-3333.333333</td><td style="color:red;">True</td><td>-2000</td><td>1000endstr</td><td style="color:red;">True</td><td>NaN</td><td>NaN</td><td style="color:blue">False</td><td>b</td><td>a</td><td style="color:red;">True</td><td>e</td><td>d</td><td style="color:red;">True</td>
    </tr>
    <tr>
      <th>2</th><td>-5555.555556</td><td>4444.444444</td><td>-5555.555556</td><td>4444.444444</td><td style="color:red;">True</td><td>3000</td><td>-2000endstr</td><td style="color:red;">True</td><td>NaN</td><td>NaN</td><td style="color:blue">False</td><td>c</td><td>b</td><td style="color:red;">True</td><td>f</td><td>e</td><td style="color:red;">True</td>
    </tr>
    <tr>
      <th>3</th><td>6666.666667</td><td>6666.666667</td><td>6666.666667</td><td>6666.666667</td><td style="color:blue">False</td><td>-4000000</td><td>-4000000endstr</td><td style="color:red;">True</td><td>8888.8888</td><td>8888.8888</td><td style="color:blue">False</td><td>4444.4444444444</td><td>4444.4444444444</td><td style="color:blue">False</td><td>NaN</td><td>NaN</td><td style="color:blue">False</td>
    </tr>
  </tbody>
</table>

## Saving report file (\<file location>)
- **What is done**: This is an optional operation done when setting the `report_file_path` parameter, it creates an file containing the report created by the function. These are the parameters that can be changed on the function call:
  - **report_file_path**: str. The path to the report file.
  - **report_file_overwrite**: bool. Defines if an existing file should be overwritten. True overwrites, False raises an exception if the file exists.
- **Metadata ['variables']**:
  - **report_file_path**: str. The full path to the created report file.
- **Logic considerations**: Flow continues to next title.

## Returning (\<bool>[equality_full], \<bool>[equality_partial], dict[equality_metadata])
- **What is done**: This states that the function is returning.
- **Metadata ['variables']**: No variables created.
- **Logic considerations**: This ends the function.

# Example

## DataFrames
To create the DataFrames for this example, do:
```python
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
```

### df1
<table class="dataframe"> <thead> <tr> <th></th> <th>col_int</th> <th>col_float</th> <th>col_str</th> <th>col_nan</th> <th>col_strnan</th> <th>col_df1extra</th> </tr> </thead> <tbody> <tr> <th>0</th> <td>1000</td> <td>-3333.333333</td> <td>a</td> <td>NaN</td> <td>d</td> <td>5</td> </tr> <tr> <th>1</th> <td>-2000</td> <td>4444.444444</td> <td>b</td> <td>NaN</td> <td>e</td> <td>6</td> </tr> <tr> <th>2</th> <td>3000</td> <td>-5555.555556</td> <td>c</td> <td>NaN</td> <td>f</td> <td>7</td> </tr> <tr> <th>3</th> <td>-4000000</td> <td>6666.666667</td> <td>4444.4444444444</td> <td>8888.8888</td> <td>NaN</td> <td>i</td> </tr> </tbody> </table>

### df2
<table class="dataframe"> <thead> <tr> <th></th> <th>col_int</th> <th>col_float</th> <th>col_str</th> <th>col_nan</th> <th>col_strnan</th> <th>col_df2extra</th> </tr> </thead> <tbody> <tr> <th>0</th> <td>3000endstr</td> <td>-5555.555556</td> <td>c</td> <td>NaN</td> <td>f</td> <td>j</td> </tr> <tr> <th>1</th> <td>1000endstr</td> <td>-3333.333333</td> <td>a</td> <td>NaN</td> <td>d</td> <td>k</td> </tr> <tr> <th>2</th> <td>-2000endstr</td> <td>4444.444444</td> <td>b</td> <td>NaN</td> <td>e</td> <td>l</td> </tr> <tr> <th>3</th> <td>-4000000endstr</td> <td>6666.666667</td> <td>4444.4444444444</td> <td>8888.8888</td> <td>NaN</td> <td>45</td> </tr> </tbody> </table>

## Executing `pd_compare.compare()`
```python
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
Prints:
```
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

## returned\[2]\['variables']

### returned[2]['variables']['cols_compare_equality']
False

### returned[2]['variables']['cols_common_set']
{'col_int', 'col_nan', 'col_float', 'col_str', 'col_strnan'}

### returned[2]['variables']['cols_common_list_sorted']
['col_float', 'col_int', 'col_nan', 'col_str', 'col_strnan']

### returned[2]['variables']['cols_df1_excl_set']
{'col_df1extra'}

### returned[2]['variables']['cols_df2_excl_set']
{'col_df2extra'}

### returned[2]['variables']['cols_df1_dups_dict']
{}

### returned[2]['variables']['cols_df2_dups_dict']
{}

### returned[2]['variables']['cols_df1_dups_common_dict']
{}

### returned[2]['variables']['cols_df2_dups_common_dict']
{}

### returned[2]['variables']['idxs_compare_equality']
True

### returned[2]['variables']['idxs_common_set']
{0, 1, 2, 3}

### returned[2]['variables']['idxs_common_list_sorted']
[0, 1, 2, 3]

### returned[2]['variables']['idxs_df1_excl_set']
set()

### returned[2]['variables']['idxs_df2_excl_set']
set()

### returned[2]['variables']['idxs_df1_dups_dict']
{}

### returned[2]['variables']['idxs_df2_dups_dict']
{}

### returned[2]['variables']['idxs_df1_dups_common_dict']
{}

### returned[2]['variables']['idxs_df2_dups_common_dict']
{}

### returned[2]['variables']['df1_common']
<table class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>col_float</th>
      <th>col_int</th>
      <th>col_nan</th>
      <th>col_str</th>
      <th>col_strnan</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th><td>-3333.333333</td><td>1000</td><td>NaN</td><td>a</td><td>d</td>
    </tr>
    <tr>
      <th>1</th><td>4444.444444</td><td>-2000</td><td>NaN</td><td>b</td><td>e</td>
    </tr>
    <tr>
      <th>2</th><td>-5555.555556</td><td>3000</td><td>NaN</td><td>c</td><td>f</td>
    </tr>
    <tr>
      <th>3</th><td>6666.666667</td><td>-4000000</td><td>8888.8888</td><td>4444.4444444444</td><td>NaN</td>
    </tr>
  </tbody>
</table>

### returned[2]['variables']['df2_common']
<table class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>col_float</th>
      <th>col_int</th>
      <th>col_nan</th>
      <th>col_str</th>
      <th>col_strnan</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th><td>-5555.555556</td><td>3000endstr</td><td>NaN</td><td>c</td><td>f</td>
    </tr>
    <tr>
      <th>1</th><td>-3333.333333</td><td>1000endstr</td><td>NaN</td><td>a</td><td>d</td>
    </tr>
    <tr>
      <th>2</th><td>4444.444444</td><td>-2000endstr</td><td>NaN</td><td>b</td><td>e</td>
    </tr>
    <tr>
      <th>3</th><td>6666.666667</td><td>-4000000endstr</td><td>8888.8888</td><td>4444.4444444444</td><td>NaN</td>
    </tr>
  </tbody>
</table>

### returned[2]['variables']['common_cols_dtypes_equality']
False

### returned[2]['variables']['common_cols_dtypes_df']
<table class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>different</th>
      <th>first_df</th>
      <th>second_df</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>col_float</th><td style="color:red;">True</td><td>float64</td><td>object</td>
    </tr>
    <tr>
      <th>col_int</th><td style="color:red;">True</td><td>int64</td><td>object</td>
    </tr>
    <tr>
      <th>col_nan</th><td style="color:red;">True</td><td>float64</td><td>object</td>
    </tr>
    <tr>
      <th>col_str</th><td style="color:blue;">False</td><td>object</td><td>object</td>
    </tr>
    <tr>
      <th>col_strnan</th><td style="color:blue;">False</td><td>object</td><td>object</td>
    </tr>
  </tbody>
</table>

### returned[2]['variables']['common_cols_dtypes_simplified']
True

### returned[2]['variables']['common_cols_dtypes_simplified_equality']
False

### returned[2]['variables']['common_cols_dtypes_simplified_df']
<table class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>different</th>
      <th>first_df</th>
      <th>second_df</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>col_float</th><td style="color:blue;">False</td><td>float64</td><td>float64</td>
    </tr>
    <tr>
      <th>col_int</th><td style="color:red;">True</td><td>int64</td><td>object</td>
    </tr>
    <tr>
      <th>col_nan</th><td style="color:blue;">False</td><td>float64</td><td>float64</td>
    </tr>
    <tr>
      <th>col_str</th><td style="color:blue;">False</td><td>object</td><td>object</td>
    </tr>
    <tr>
      <th>col_strnan</th><td style="color:blue;">False</td><td>object</td><td>object</td>
    </tr>
  </tbody>
</table>

### returned[2]['variables']['equality_df']
<table class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>col_float</th>
      <th>col_int</th>
      <th>col_nan</th>
      <th>col_str</th>
      <th>col_strnan</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th><td style="color:red;">False</td><td style="color:red;">False</td><td style="color:blue;">True</td><td style="color:red;">False</td><td style="color:red;">False</td>
    </tr>
    <tr>
      <th>1</th><td style="color:red;">False</td><td style="color:red;">False</td><td style="color:blue;">True</td><td style="color:red;">False</td><td style="color:red;">False</td>
    </tr>
    <tr>
      <th>2</th><td style="color:red;">False</td><td style="color:red;">False</td><td style="color:blue;">True</td><td style="color:red;">False</td><td style="color:red;">False</td>
    </tr>
    <tr>
      <th>3</th><td style="color:blue;">True</td><td style="color:red;">False</td><td style="color:blue;">True</td><td style="color:blue;">True</td><td style="color:blue;">True</td>
    </tr>
  </tbody>
</table>

### returned[2]['variables']['cols_equal_list_sorted']
['col_nan']

### returned[2]['variables']['rows_equal_list_sorted']
[]

### returned[2]['variables']['cols_diff_list_sorted']
['col_float', 'col_int', 'col_str', 'col_strnan']

### returned[2]['variables']['rows_diff_list_sorted']
[0, 1, 2, 3]

### returned[2]['variables']['joined_df']
<table class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th colspan="3" halign="left">col_float</th>
      <th colspan="3" halign="left">col_int</th>
      <th colspan="3" halign="left">col_nan</th>
      <th colspan="3" halign="left">col_str</th>
      <th colspan="3" halign="left">col_strnan</th>
    </tr>
    <tr>
      <th></th>
      <th>first_df</th>
      <th>second_df</th>
      <th>different</th>
      <th>first_df</th>
      <th>second_df</th>
      <th>different</th>
      <th>first_df</th>
      <th>second_df</th>
      <th>different</th>
      <th>first_df</th>
      <th>second_df</th>
      <th>different</th>
      <th>first_df</th>
      <th>second_df</th>
      <th>different</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th><td>-3333.333333</td><td>-5555.555556</td><td style="color:red;">True</td><td>1000</td><td>3000endstr</td><td style="color:red;">True</td><td>NaN</td><td>NaN</td><td style="color:blue">False</td><td>a</td><td>c</td><td style="color:red;">True</td><td>d</td><td>f</td><td style="color:red;">True</td>
    </tr>
    <tr>
      <th>1</th><td>4444.444444</td><td>-3333.333333</td><td style="color:red;">True</td><td>-2000</td><td>1000endstr</td><td style="color:red;">True</td><td>NaN</td><td>NaN</td><td style="color:blue">False</td><td>b</td><td>a</td><td style="color:red;">True</td><td>e</td><td>d</td><td style="color:red;">True</td>
    </tr>
    <tr>
      <th>2</th><td>-5555.555556</td><td>4444.444444</td><td style="color:red;">True</td><td>3000</td><td>-2000endstr</td><td style="color:red;">True</td><td>NaN</td><td>NaN</td><td style="color:blue">False</td><td>c</td><td>b</td><td style="color:red;">True</td><td>f</td><td>e</td><td style="color:red;">True</td>
    </tr>
    <tr>
      <th>3</th><td>6666.666667</td><td>6666.666667</td><td style="color:blue">False</td><td>-4000000</td><td>-4000000endstr</td><td style="color:red;">True</td><td>8888.8888</td><td>8888.8888</td><td style="color:blue">False</td><td>4444.4444444444</td><td>4444.4444444444</td><td style="color:blue">False</td><td>NaN</td><td>NaN</td><td style="color:blue">False</td>
    </tr>
  </tbody>
</table>

