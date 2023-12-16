from typing import Tuple

import pandas as pd


def remove_rows_with_empty_fields(
    df: pd.DataFrame,
    all_dirty_elements: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df_without_na = df.dropna()
    df_with_na_only = pd.DataFrame(df[df.isna().any(axis=1)])

    all_dirty_elements = pd.concat([all_dirty_elements, df_with_na_only])

    return df_without_na, all_dirty_elements


def remove_rows_with_spaces_only_string_fields(
    df: pd.DataFrame,
    all_dirty_elements: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    condition = df.apply(lambda x: x.astype(str).str.contains(r"^\s+$").any(), axis=1)

    df_without_spaces = df[~condition]
    df_with_spaces = df[condition]

    all_dirty_elements = pd.concat([all_dirty_elements, df_with_spaces])

    return df_without_spaces, all_dirty_elements
