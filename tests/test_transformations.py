from io import StringIO

import pandas as pd
from numpy import NaN
from pandas._testing import assert_frame_equal

from cleaning_loading_app.transformations import remove_rows_with_empty_fields


def test_remove_rows_with_empty_fields() -> None:
    # Given
    csv_content_stream = StringIO('id,title\n1,"title1"\n"",title2\n3,title3\n"4",""\n')
    df = pd.read_csv(csv_content_stream, header=0)

    # When
    result, rejected = remove_rows_with_empty_fields(df)

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
            [NaN, "title2"],
            [4, NaN],
        ],
        index=[1, 3],
        columns=columns,
    )
    expected_rejected["id"] = expected_rejected["id"].astype("float64")

    assert_frame_equal(result, expected)
    assert_frame_equal(rejected, expected_rejected)
