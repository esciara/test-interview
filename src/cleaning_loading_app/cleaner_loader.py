from pathlib import Path

from cleaning_loading_app.csv_io import (
    load_cvs_with_date_parsing,
    save_cvs_in_proper_format,
)

DATA_PATH = Path("data")
PROCESSED_PATH = DATA_PATH / "processed"
REJECTED_PATH = DATA_PATH / "rejected"

def clean_and_load(incoming_file_path: Path) -> None:
    _check_expected_path_exists(PROCESSED_PATH)
    _check_expected_path_exists(REJECTED_PATH)

    df = load_cvs_with_date_parsing(incoming_file_path, ["date"])

    data_file_name = incoming_file_path.name
    save_cvs_in_proper_format(PROCESSED_PATH / data_file_name, df)


def _check_expected_path_exists(path_to_check: Path) -> None:
    if not path_to_check.exists():
        print(
            f"Path for processed files {path_to_check} does not exist. "
            "Please create before proceeding."
        )
