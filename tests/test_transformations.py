from io import StringIO

import pandas as pd
from hamcrest import assert_that, equal_to
from numpy import nan
from pandas._testing import assert_frame_equal

from cleaning_loading_app.transformations import (
    convert_string_to_date,
    ensure_column_is_int,
    remove_rows_with_empty_or_spaces_only_string_fields,
    remove_rows_with_nan_fields,
)


def test_remove_rows_with_nan_fields() -> None:
    # Given
    csv_content_stream = StringIO('id,title\n1,"title1"\n"",title2\n3,title3\n"4",""\n')
    df = pd.read_csv(csv_content_stream, header=0)

    # When
    result, rejected = remove_rows_with_nan_fields(df, pd.DataFrame())

    # Then
    columns = ["id", "title"]
    expected = pd.DataFrame(
        [
            [1, "title1"],
            [3, "title3"],
        ],
        index=[0, 2],
        columns=columns,
    )
    expected["id"] = expected["id"].astype("float64")

    expected_rejected = pd.DataFrame(
        [
            [nan, "title2"],
            [4, nan],
        ],
        index=[1, 3],
        columns=columns,
    )
    expected_rejected["id"] = expected_rejected["id"].astype("float64")

    assert_frame_equal(result, expected)
    assert_frame_equal(rejected, expected_rejected)


def test_remove_rows_with_spaces_only_string_fields() -> None:
    # Given
    columns = ["id", "title", "journal"]
    df = pd.DataFrame(
        [
            [1, "title1", "   "],
            [nan, "title2", "journal2"],
            [3, "title3", "journal3"],
            [4, "", "journal4"],
        ],
        columns=columns,
    )
    df["id"] = df["id"].astype("float64")

    # When
    result, rejected = remove_rows_with_empty_or_spaces_only_string_fields(
        df, pd.DataFrame()
    )

    # Then
    expected = pd.DataFrame(
        [
            [nan, "title2", "journal2"],
            [3, "title3", "journal3"],
        ],
        index=[1, 2],
        columns=columns,
    )
    expected["id"] = expected["id"].astype("float64")

    expected_rejected = pd.DataFrame(
        [
            [1, "title1", "   "],
            [4, "", "journal4"],
        ],
        index=[0, 3],
        columns=columns,
    )
    expected_rejected["id"] = expected_rejected["id"].astype("float64")

    assert_frame_equal(result, expected)
    assert_frame_equal(rejected, expected_rejected)


def test_convert_string_to_date() -> None:
    # Given
    df = pd.DataFrame(
        [
            [1, "01/01/2020"],
            [2, "01/12/2020"],
        ],
        columns=["id", "date"],
    )

    # When
    result, rejected = convert_string_to_date(df, "date", pd.DataFrame())

    # Then
    expected = pd.DataFrame(
        [
            [1, "2020-01-01"],
            [2, "2020-12-01"],
        ],
        columns=["id", "date"],
    )

    expected["date"] = pd.to_datetime(expected["date"])

    assert_frame_equal(result, expected)
    assert_that(rejected.empty, equal_to(True))


def test_ensure_column_is_int() -> None:
    # Given
    df = pd.DataFrame(
        [
            [1],
            ["2"],
        ],
        columns=["id"],
    )

    # When
    result, rejected = ensure_column_is_int(df, "id", pd.DataFrame())

    # Then
    expected = pd.DataFrame(
        [
            [1],
            [2],
        ],
        columns=["id"],
    )

    assert_frame_equal(result, expected)
    assert_that(rejected.empty, equal_to(True))
