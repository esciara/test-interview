from pathlib import Path

import pandas as pd

from cleaning_loading_app.csv_io import (
    load_cvs_with_date_parsing,
    save_cvs_in_proper_format,
    load_json_without_date_parsing,
)
from cleaning_loading_app.transformations import (
    remove_rows_with_empty_fields,
    remove_rows_with_empty_or_spaces_only_string_fields,
    convert_string_to_dates,
)

DATA_PATH = Path("data")
PROCESSED_PATH = DATA_PATH / "processed"
REJECTED_PATH = DATA_PATH / "rejected"


def clean_and_load(incoming_file_path: Path) -> None:
    _check_expected_path_exists(PROCESSED_PATH)
    _check_expected_path_exists(REJECTED_PATH)

    _cleanup_target_files(incoming_file_path)

    _clean_and_load_publications(incoming_file_path.with_suffix(".csv"))
    _clean_and_load_publications(incoming_file_path.with_suffix(".json"))


def _check_expected_path_exists(path_to_check: Path) -> None:
    if not path_to_check.exists():
        print(
            f"Path for processed files '{path_to_check.absolute()}' does not exist. "
            "Please create before proceeding."
        )
        exit(1)


def _cleanup_target_files(incoming_file_path: Path) -> None:
    target_data_file_name = _build_target_data_file_name(incoming_file_path)
    processed_data_file_path = PROCESSED_PATH / target_data_file_name
    rejected_data_file_path = REJECTED_PATH / target_data_file_name

    processed_data_file_path.unlink(missing_ok=True)
    rejected_data_file_path.unlink(missing_ok=True)


def _clean_and_load_publications(incoming_file_path: Path) -> None:
    if incoming_file_path.suffix == ".csv":
        df = load_cvs_with_date_parsing(incoming_file_path, ["date"])
    elif incoming_file_path.suffix == ".json":
        df = load_json_without_date_parsing(incoming_file_path)
    else:
        print(f"unsupported file suffix {incoming_file_path.suffix!r}. Exiting...")
        exit(1)

    all_dirty_elements = pd.DataFrame()

    if incoming_file_path.suffix == ".json":
        df, all_dirty_elements = convert_string_to_dates(df, "date", all_dirty_elements)

    df, all_dirty_elements = remove_rows_with_empty_or_spaces_only_string_fields(
        df, all_dirty_elements
    )

    df, all_dirty_elements = remove_rows_with_empty_fields(df, all_dirty_elements)

    target_data_file_name = _build_target_data_file_name(incoming_file_path)
    processed_data_file_path = PROCESSED_PATH / target_data_file_name
    rejected_data_file_path = REJECTED_PATH / target_data_file_name

    save_cvs_in_proper_format(processed_data_file_path, df)
    save_cvs_in_proper_format(rejected_data_file_path, all_dirty_elements)


def _build_target_data_file_name(incoming_file_path: Path) -> str:
    return incoming_file_path.with_suffix(".csv").name
