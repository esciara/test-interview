import logging
import shutil
from pathlib import Path

from cleaning_loading_app.const import (
    INCOMING_FILES_PATH,
    INGESTED_DATA_PATH,
    PROCESSED_FILES_PATH,
    REJECTED_DATA_PATH,
)


def preliminary_checks_and_cleaning() -> None:
    _check_expected_path_exists(INCOMING_FILES_PATH)

    _recreate_directory(PROCESSED_FILES_PATH)
    _recreate_directory(INGESTED_DATA_PATH)
    _recreate_directory(REJECTED_DATA_PATH)


def _check_expected_path_exists(path: Path) -> None:
    if path.exists():
        logging.info(f"Checking directory exists: '{path.absolute()}' exists.")
    else:
        logging.warning(
            f"Directory '{path.absolute()}' does not exist. "
            "Please create before proceeding."
        )
        exit(1)


def _recreate_directory(path: Path) -> None:
    logging.info(f"Destroying and recreating directory '{path.absolute()}'.")
    shutil.rmtree(path, ignore_errors=True)
    path.mkdir()


def move_processed_file(filepath: Path) -> None:
    logging.info(
        f"Moving processed file from '{filepath.parent}' to '{PROCESSED_FILES_PATH}'."
    )
    filepath.rename(PROCESSED_FILES_PATH / filepath.name)
