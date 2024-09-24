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
- **Flow considerations**: if the function will return, if it will go to a specific Title or if the flow will continue.

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
- **Flow considerations**: Depending on the equality result:
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
	- **error**: str. If there are column duplicates, read on **Flow considerations**.
- **Flow considerations**:
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
	- **error**: str. If there are index duplicates, read on **Flow considerations**.
- **Flow considerations**:
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
- **Flow considerations**:
	- If all columns and indexes are **not** equal, the flow continues to **Equality check for common columns and indexes** since we want to check if the two DataFrames are equal if we only take into consideration the same columns and indexes in both.
	- If all columns and indexes are equal in the two DataFrames, the flow continues to title **Comparing column dtypes** since we know all columns and indexes are equal and we don't need to redo the same comparison made in the beginning (in **Equality Check (full)**).

## Equality check (for common columns and indexes)
- **What is done**: Checks wether the two DataFrames are equal or not, selecting only the columns and indexes that are equal in the two DataFrames, **note** that columns and indexes are ordered before doing the comparison.
- **Metadata ['variables']**: No variables added.
- **Flow considerations**: Depending on the equality result:
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
- **Flow considerations**:
	- If all dtypes are equal (**common_cols_dtypes_equality** is True), we know that the two DataFrame must have different values since the dtypes are equal. All bellow sections starting with "CCD / " are omitted.
	- If there are different dtypes, the function will try simplifying them in **CCD / Since dtypes are different, will try to simplify**.

### CCD / Since dtypes are different, will try to simplify
- **What is done**: Does nothing, this is only a message stating that the function will try to simplify the dtypes.
- **Metadata ['variables']**: No variables added.
- **Flow considerations**: Flow continues to next **CCD / Trying to simplify dtypes**.

### CCD / Trying to simplify dtypes
- **What is done**: Tries to simplify the dtypes of both DataFrames using `pd_format.simplify_dtypes()`. The goal is to make dtypes as simple as possible and then check if the two DataFrames are equal (in another title), meaning the values are equal but not considered equal because of different dtypes.
- **Metadata ['variables']**:
	- **common_cols_dtypes_simplified**: bool. True if dtypes was simplified, False otherwise.
	- If the dtypes of their columns was simplified (**common_cols_dtypes_simplified** is True), modifies **df1_common** and **df2_common**.
- **Flow considerations**:
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
- **Flow considerations**:
	- If all simplified dtypes are **not** equal, continues to **CCD / Skipping equality check (since dtypes are not equal)**.
	- If all simplified dtypes are equal, continues to **CCD / Equality check (since dtypes are now equal)**.

### CCD / Skipping equality check (since dtypes are not equal)
- **What is done**: Does nothing, this is only a message to explain that an equality check is not useful at this point since the dtypes are different and an equality would return False.
- **Metadata ['variables']**: No variables added.
- **Flow considerations**: Skip remaining "CCD / " titles.

### CCD / Equality check (since dtypes are now equal)
- **What is done**: Checks wether the two modified DataFrames are equal or not.
- **Metadata ['variables']**: No variables created.
- **Flow considerations**: Depending on the equality result:
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
- **Flow considerations**:
	- After the rounding, the function will try to simplify the dtypes in **ROUNDING / Trying to simplify dtypes**.
	- If the rounding had no effect the simplification will have no effect.

### ROUNDING / Trying to simplify dtypes
- **What is done**: Tries to simplify the dtypes of both DataFrames using `pd_format.simplify_dtypes()`. The goal is to make dtypes as simple as possible and then check if the two DataFrames are equal (in another title), meaning the values are equal but not considered equal because of different dtypes.
- **Metadata ['variables']**:
	- **common_cols_post_round_dtypes_simplified**: bool. True if dtypes was simplified, False otherwise.
	- If the dtypes of their columns was simplified (**common_cols_post_round_dtypes_simplified** is True), modifies **df1_common** and **df2_common**.
- **Flow considerations**:
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
- **Flow considerations**:
	- If all simplified dtypes are **not** equal, continues to **ROUNDING / Skipping equality check (since dtypes are not equal)**.
	- If all simplified dtypes are equal, continues to **ROUNDING / Equality check (since dtypes are now equal)**.

### ROUNDING / Skipping equality check (since dtypes are not equal)
- **What is done**: Does nothing, this is only a message to explain that an equality check is not useful at this point since the dtypes are different and an equality would return False.
- **Metadata ['variables']**: No variables added.
- **Flow considerations**: Skip remaining "ROUNDING / " titles.

### ROUNDING / Equality check (since dtypes are now equal)
- **What is done**: Checks wether the two modified DataFrames are equal or not.
- **Metadata ['variables']**: No variables created.
- **Flow considerations**: Depending on the equality result:
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
	- **joined_df**: DataFrame. A DataFrame containing the values from **df1_common**, **df2_common** and columns containing a boolean stating if a cell in the two DataFrames is different. This DataFrame has a column MultiIndex, the first index is the column to be compared, for every compared column the second index has three columns: the values from the column in **df1_common** (using df1_name as column name), the values from the column in **df2_common** (using df2_name as column name) and a column called **different** where True means the given cells are different and False otherwise.
- **Flow considerations**: Flow continues to next title.

## Creating Excel (\<file location>)
- **What is done**: This is an optional operation done when setting the `xls_path` parameter, it creates an Excel file. These are the parameters that can be changed on the function call:
	- **xls_path**: str. The path to the Excel file.
	- **xls_overwrite**: bool. Defines if an existing file should be overwritten. True overwrites, False raises an exception if the file exists.
	- **xls_compare_str_equal**: str. A string to be placed inside a cell in the Excel file when both DataFrames contain the same value. Useful to know what cells are equal in the two DataFrames, by default empty. Can be used with the *find* function in Excel.
	- **xls_compare_str_diff**: str. A string to be placed inside a cell in the Excel file when the cell's value in the tow DataFrames is different. Useful to know what cells are different in the two DataFrames, by default "`*_diff_*`". Can be used with the *find* function in Excel.
	- **xls_fixed_cols**: list. A list of str containing columns that will be fixed in the generated Excel file.
	- **xls_datetime_rpl**: str. A string containing the format to be used for a column with a datetime64 dtype, useful to have a specific format for dates in Excel.
- **Metadata ['variables']**:
	- **xls_path**: str. The full path to the created Excel file.
- **Flow considerations**: Flow continues to next title.

## Saving report file (\<file location>)
- **What is done**: This is an optional operation done when setting the `report_file_path` parameter, it creates an file containing the report created by the function. These are the parameters that can be changed on the function call:
	- **report_file_path**: str. The path to the report file.
	- **report_file_overwrite**: bool. Defines if an existing file should be overwritten. True overwrites, False raises an exception if the file exists.
- **Metadata ['variables']**:
	- **report_file_path**: str. The full path to the created report file.
- **Flow considerations**: Flow continues to next title.

## Returning (\<bool>[equality_full], \<bool>[equality_partial], dict[equality_metadata])
- **What is done**: This states that the function is returning.
- **Metadata ['variables']**: No variables created.
- **Flow considerations**: This ends the function.