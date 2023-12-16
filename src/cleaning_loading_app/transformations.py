from typing import Tuple

import pandas as pd


def remove_rows_with_empty_fields(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_without_na = df.dropna()
    df_with_na_only = pd.DataFrame(df[df.isna().any(axis=1)])

    return df_without_na, df_with_na_only


def remove_rows_with_spaces_only_string_fields(
    df: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    condition = df.apply(lambda x: x.astype(str).str.contains(r"^\s+$").any(), axis=1)

    df_without_spaces = df[~condition]
    df_with_spaces = df[condition]

    return df_without_spaces, df_with_spaces
