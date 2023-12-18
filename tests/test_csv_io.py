from io import StringIO
from pathlib import Path

import pandas as pd
from hamcrest import assert_that, equal_to
from pandas import testing

from cleaning_loading_app.csv_io import (
    load_cvs_with_date_parsing,
    load_json_without_date_parsing,
    save_cvs_in_proper_format,
)


def test_load_cvs_with_date_parsing_parses_dates_in_mixed_format() -> None:
    # Given
    csv_content_stream = StringIO(
        "id,date1,date2\n"
        "1,01/01/2020,1 july 2021\n"
        "2,2020-01-02,02/07/2022\n"
        "3,03/01/2020,13 december 2022\n"
    )

    # When
    result = load_cvs_with_date_parsing(csv_content_stream, ["date1", "date2"])

    # Then
    expected = pd.DataFrame(
        [
            [1, "2020-01-01", "2021-07-01"],
            [2, "2020-01-02", "2022-07-02"],
            [3, "2020-01-03", "2022-12-13"],
        ],
        columns=["id", "date1", "date2"],
    )

    expected["date1"] = pd.to_datetime(expected["date1"])
    expected["date2"] = pd.to_datetime(expected["date2"])

    testing.assert_frame_equal(result, expected)


def test_load_json_without_date_parsing() -> None:
    # Given
    json_content = """[
  {
    "id": 9,
    "date": "01/01/2020"
  },
  {
    "id": 10,
    "date": "01/12/2020"
  }
]"""
    json_content_stream = StringIO(json_content)

    # When
    result = load_json_without_date_parsing(json_content_stream)

    # Then
    expected = pd.DataFrame(
        [
            [9, "01/01/2020"],
            [10, "01/12/2020"],
        ],
        columns=["id", "date"],
    )

    testing.assert_frame_equal(result, expected)


def test_save_cvs_in_proper_format_passes(tmp_path: Path) -> None:
    # Given
    df = pd.DataFrame(
        [
            [1, "title1", "2021-07-01"],
            [2, "title2", "2022-07-02"],
            [3, "title3", "2022-12-13"],
        ],
        columns=["id", "title", "date"],
    )

    df["date"] = pd.to_datetime(df["date"])

    # When
    result = save_cvs_in_proper_format(None, df)

    # Then
    expected = (
        '"id","title","date"\n'
        '1,"title1","2021-07-01"\n'
        '2,"title2","2022-07-02"\n'
        '3,"title3","2022-12-13"\n'
    )
    assert_that(result, equal_to(expected))
