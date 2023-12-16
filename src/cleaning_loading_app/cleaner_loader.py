from pathlib import Path

import pandas as pd

from cleaning_loading_app.csv_io import (
    load_cvs_with_date_parsing,
    save_cvs_in_proper_format,
)
from cleaning_loading_app.transformations import (
    remove_rows_with_empty_fields,
    remove_rows_with_spaces_only_string_fields,
)

DATA_PATH = Path("data")
PROCESSED_PATH = DATA_PATH / "processed"
REJECTED_PATH = DATA_PATH / "rejected"


def clean_and_load(incoming_file_path: Path) -> None:
    _check_expected_path_exists(PROCESSED_PATH)
    _check_expected_path_exists(REJECTED_PATH)

    df = load_cvs_with_date_parsing(incoming_file_path, ["date"])
    all_dirty_elements = pd.DataFrame()

    df, all_dirty_elements = remove_rows_with_spaces_only_string_fields(
        df, all_dirty_elements
    )

    df, all_dirty_elements = remove_rows_with_empty_fields(df, all_dirty_elements)

    data_file_name = incoming_file_path.name
    processed_data_file_path = PROCESSED_PATH / data_file_name
    rejected_data_file_path = REJECTED_PATH / data_file_name

    processed_data_file_path.unlink()
    save_cvs_in_proper_format(processed_data_file_path, df)
    rejected_data_file_path.unlink()
    save_cvs_in_proper_format(rejected_data_file_path, all_dirty_elements)


def _check_expected_path_exists(path_to_check: Path) -> None:
    if not path_to_check.exists():
        print(
            f"Path for processed files '{path_to_check.absolute()}' does not exist. "
            "Please create before proceeding."
        )
        exit(1)
