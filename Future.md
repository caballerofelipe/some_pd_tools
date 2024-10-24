This file has some ideas and reviews meant for future changes.

# Ideas
- Add sorting options for what is returned (DataFrames and Excel [and maybe something else?])
	- 'df1': sort as df1.
	- 'df2': sort as df2.
	- 'asc': sort columns in ascending order.
	- 'desc': sort columns in descending order.
- For what is returned, configure whether to show everything or only the parts that are different. For these structures:
	- df1_common
	- df2_common
	- equality_df
	- cols_equal_list_sorted
	- rows_equal_list_sorted
	- cols_diff_list_sorted
	- rows_diff_list_sorted
	- joined_df
	- The Excel file for the comparison.
- For files the xls file, (xls_path), if xls_overwrite maybe delete the file first? Or change the param to xls_delete_first? Or create a new parameter?

# Structure review
To check for a good structure:
- [X] Add functions where large code is done to keep code cleaner.
- [x] Check that all shown list are sorted lists and not sets or other data types.
- [X] Comparing functions should return equality (True/False) and metadata dict, including the report.
- [X] Docstrings full.
- [X] All functions documented in README.md.
- In `pd_compare.compare()` 
    - [X] Remove "--disabled=(...)" from "pylint.args" in settings.json to view possible problems and show no docstring where needed.
	- [X] Populate metadata while advancing, if a return is done, test metadata with pytest.
	- [X] Should return two equalities and a metadata dict.
	    - equalities:
	        - "full equality" True if df1.equals(df2)
	        - "partial equality" True if after doing some operation df1.equals(df2)
		- "metadata dict"
	- [X] IMPORTANT: After (MARK:EQLTY 4COMMON) all processings must be done using df1_common and df2_common or their equivalent name (these are DataFrames including only common columns and common indexes).