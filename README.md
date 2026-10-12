# MP1 Data Pipeline

This pipeline loads a CSV file, validates it, cleans it, and saves the result. Data moves through four stages: `load_data` reads the input and the config, `validate_dataframe` checks required columns and removes rows with invalid numeric values, `process_data` removes duplicates, missing values, and outliers, and `save_data` writes the cleaned CSV. `pipeline.py` coordinates these steps, handles errors, and prints a cleaning report at the end. The `src/` package holds the modules: `data_loaders.py` reads CSV, JSON, and YAML files, `data_validator.py` checks the data's structure and types, `data_processor.py` cleans the data and builds the report, `data_output.py` saves the result, and `utils.py` provides logging setup and input-path validation. Column names and cleaning options live in `config/config.yaml`, so the same code can process other compatible CSV files. Test data is in `fixtures/`, and generated results go to `output/`, which Git does not track.

# Example

python3 pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose

Output:
 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv, config=config/config.yaml
 INFO     src.utils — Input file validated: fixtures/sample_data.csv
 INFO     src.utils — Input file validated: config/config.yaml
 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
 WARNING  src.data_validator — Removed 2 rows with invalid numeric values in rating
 DEBUG    src.data_validator — Validation: 100 -> 98 rows
 INFO     __main__ — Validation complete: 100 -> 98 rows
 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
 DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.6, upper=106.6, removed=2
 INFO     __main__ — Processing complete: 98 -> 92 rows
 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
 INFO     __main__ — Saved cleaned data to output/clean.csv
