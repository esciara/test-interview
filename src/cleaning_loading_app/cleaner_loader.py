import logging
from pathlib import Path

import pandas as pd

from cleaning_loading_app.const import (
    INCOMING_FILES_PATH,
    INGESTED_DATA_PATH,
    REJECTED_DATA_PATH,
)
from cleaning_loading_app.csv_io import (
    load_cvs_with_date_parsing,
    load_json_without_date_parsing,
    save_cvs_in_proper_format,
)
from cleaning_loading_app.filesystem import (
    move_processed_file,
    preliminary_checks_and_cleaning,
)
from cleaning_loading_app.transformations import (
    convert_string_to_dates,
    remove_rows_with_empty_fields,
    remove_rows_with_empty_or_spaces_only_string_fields,
)


def ingest_files() -> None:
    preliminary_checks_and_cleaning()

    _clean_and_load_publications(INCOMING_FILES_PATH / "clinical_trials.csv")
    _clean_and_load_publications(INCOMING_FILES_PATH / "pubmed.csv")
    _clean_and_load_publications(INCOMING_FILES_PATH / "pubmed.json")
    _clean_and_load_publications(INCOMING_FILES_PATH / "drugs.csv")


def _clean_and_load_publications(incoming_file_path: Path) -> None:
    if not incoming_file_path.exists():
        logging.warning(
            f"No file to import: '{incoming_file_path}' not found. Doing nothing..."
        )
        return

    pipeline_type = "drugs" if incoming_file_path.stem == "drugs" else "publications"

    logging.info(f"Cleaning and loading file '{incoming_file_path}'.")
    if incoming_file_path.suffix == ".csv":
        date_columns = None if pipeline_type == "drugs" else ["date"]
        df = load_cvs_with_date_parsing(incoming_file_path, date_columns)
    elif incoming_file_path.suffix == ".json":
        df = load_json_without_date_parsing(incoming_file_path)
    else:
        logging.warning(
            f"Unsupported file suffix {incoming_file_path.suffix!r}. "
            "Aborting processing..."
        )
        exit(1)

    all_dirty_elements = pd.DataFrame()

    if pipeline_type != "drugs":
        if incoming_file_path.suffix == ".json":
            df, all_dirty_elements = convert_string_to_dates(
                df, "date", all_dirty_elements
            )

        df, all_dirty_elements = remove_rows_with_empty_or_spaces_only_string_fields(
            df, all_dirty_elements
        )

        df, all_dirty_elements = remove_rows_with_empty_fields(df, all_dirty_elements)

    target_data_file_name = _build_target_data_file_name(incoming_file_path)
    ingested_data_file_path = INGESTED_DATA_PATH / target_data_file_name
    rejected_data_file_path = REJECTED_DATA_PATH / target_data_file_name

    save_cvs_in_proper_format(ingested_data_file_path, df)
    save_cvs_in_proper_format(rejected_data_file_path, all_dirty_elements)

    move_processed_file(incoming_file_path)


def _clean_and_load_drugs(incoming_file_path: Path) -> None:
    if not incoming_file_path.exists():
        logging.warning(
            f"No file to import: '{incoming_file_path}' not found. Doing nothing..."
        )
        return

    logging.info(f"Cleaning and loading file '{incoming_file_path}'.")
    if incoming_file_path.suffix == ".csv":
        df = load_cvs_with_date_parsing(incoming_file_path)
    else:
        logging.warning(
            f"Unsupported file suffix {incoming_file_path.suffix!r}. "
            "Aborting processing..."
        )
        exit(1)

    target_data_file_name = _build_target_data_file_name(incoming_file_path)
    ingested_data_file_path = INGESTED_DATA_PATH / target_data_file_name

    save_cvs_in_proper_format(ingested_data_file_path, df)

    move_processed_file(incoming_file_path)


def _build_target_data_file_name(incoming_file_path: Path) -> str:
    return incoming_file_path.with_suffix(".csv").name
