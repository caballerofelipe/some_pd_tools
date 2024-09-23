# TODO
- [ ] Add Docstrings.
- [ ] Review README, add documentation for all functions.

# Structure review
To check for a good structure:
- [ ] Add functions where large code is done to keep code cleaner.
- [ ] Check that all shown list are sorted lists and not sets or other data types.
- [ ] Comparing functions should return equality (True/False) and metadata dict, including the report.
- [ ] Docstrings full.
- [ ] All functions documented in README.md.
- In `pd_compare.compare()` 
    - [ ] Remove "--disabled=(...)" from "pylint.args" in settings.json to view possible problems and show no docstring where needed.
	- [ ] Populate metadata while advancing, if a return is done, test metadata with pytest.
	- [ ] Should return two equalities and a metadata dict.
	    - equalities:
	        - "full equality" True if df1.equals(df2)
	        - "partial equality" True if after doing some operation df1.equals(df2)
		- "metadata dict"
	- [X] IMPORTANT: After (MARK:EQLTY 4COMMON) all processings must be done using df1_common and df2_common or their equivalent name (these are DataFrames including only common columns and common indexes).