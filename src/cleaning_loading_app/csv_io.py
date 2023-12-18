import csv
from pathlib import Path
from typing import List, TextIO

import pandas as pd


def load_cvs_with_date_parsing(
    file_path: Path | TextIO,
    date_columns: List[str] | None = None,
) -> pd.DataFrame:
    return pd.read_csv(
        file_path,
        header=0,
        parse_dates=date_columns,  # type: ignore[arg-type]
        date_format="mixed",
        dayfirst=True,
    )


def load_json_without_date_parsing(
    file_path: Path | TextIO,
) -> pd.DataFrame:
    return pd.read_json(file_path, convert_dates=False, orient="records")


def save_cvs_in_proper_format(file_path: Path | None, df: pd.DataFrame) -> str | None:
    if not df.empty:
        write_header = True
        if file_path is not None and file_path.exists():
            write_header = False

        return df.to_csv(
            file_path,
            index=False,
            header=write_header,
            mode="a",
            quoting=csv.QUOTE_NONNUMERIC,
        )
    return None
