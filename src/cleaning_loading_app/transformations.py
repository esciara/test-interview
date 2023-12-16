from typing import Tuple

import pandas as pd


def remove_rows_with_empty_fields(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_without_na = df.dropna()
    df_with_na_only = pd.DataFrame(df[df.isna().any(axis=1)])

    return df_without_na, df_with_na_only
