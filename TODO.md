# TODO
- Add parameter to save report to file.
- `compare()` should return three equalities and a metadata dict.
    - equalities:
        - fully_equal True if df1.equals(df2)
        - equal_w_special_settings True if after applying special settings df1.equals(df2)
        - common_cols_idx_equal True if all is equal in common columns and indexes
- IMPORTANT: After (MARK:EQUAL COMMON) all processings must be done using df1_common and df2_common or their equivalent name (these are DataFrames including only common columns and common indexes).
- For testing, add all parameters for functions calls to avoid problems if default parameters change.
- Add docstrings.
- Remove "--disabled=****" from "pylint.args" in settings.json to view possible problems and show no docstring where needed.

# Evaluate
- (Evaluate) Think if maybe a parameter should exist to do an ordered copy or not (columns and indexes) in `compare()`.
- (Evaluate) Initially the complete equality check should check if both DataFrames are equal (before sorting), then sort them (and inform about the sorting) and then do an equality check again.
    - Or specify in the documentation that this function should be ran when df1.equals(df2) is not enough.
- (Evaluate) Instead of metadata being a dict, maybe it should be a list and in each position of the list is what has been done and the metadata generated, so maybe dicts inside the list position.
- (Evaluate) When using the original DataFrames, not the ones copied, be aware that the columns on the copies where sorted. Check if this is a problem somehow.

# Structure review
To check for a good structure:
- Add functions for where large code is done to keep code cleaner.
- Populate metadata while advancing, if a return is done, test metadata with pytest.
- Check that all shown list are sorted lists and not sets or other data types.
- Add documentation for all functions in README.md.
- Comparing functions should return equality (True/False) and metadata dict, including the report.