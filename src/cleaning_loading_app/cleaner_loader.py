from pathlib import Path

from icecream import ic

from cleaning_loading_app.csv_io import (
    load_cvs_with_date_parsing,
    save_cvs_in_proper_format,
)
from cleaning_loading_app.transformations import remove_rows_with_empty_fields

DATA_PATH = Path("data")
PROCESSED_PATH = DATA_PATH / "processed"
REJECTED_PATH = DATA_PATH / "rejected"


def clean_and_load(incoming_file_path: Path) -> None:
    _check_expected_path_exists(PROCESSED_PATH)
    _check_expected_path_exists(REJECTED_PATH)

    df = load_cvs_with_date_parsing(incoming_file_path, ["date"])

    df, dirty_elements = remove_rows_with_empty_fields(df)

    ic(df)
    ic(dirty_elements)

    data_file_name = incoming_file_path.name
    save_cvs_in_proper_format(PROCESSED_PATH / data_file_name, df)

    save_cvs_in_proper_format(REJECTED_PATH / data_file_name, dirty_elements)


def _check_expected_path_exists(path_to_check: Path) -> None:
    if not path_to_check.exists():
        print(
            f"Path for processed files '{path_to_check.absolute()}' does not exist. "
            "Please create before proceeding."
        )
        exit(1)
