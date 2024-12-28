"""Pandas helpers and functionalities."""

from typing import Any

import pandas as pd  # pyright:ignore[reportMissingTypeStubs]

from telemetry import LoggerHandler

log = LoggerHandler().logger


def analyze_pandas_dataframe_and_emit_signals(analysis_df: pd.DataFrame) -> None:
    """Analyses the dataframe to emit signals."""
    dataframe_columns: Any = analysis_df.columns.tolist()
    dataframe_shape: Any = analysis_df.shape
    dataframe_describe: Any = analysis_df.describe().to_dict()  # pyright:ignore[reportUnknownMemberType]
    dataframe_dtypes: dict[str, str] = {
        str(col): str(dtype).replace("dtype('", "").replace("')", "")  # pyright:ignore[reportUnknownMemberType, reportUnknownVariableType, reportUnknownArgumentType]
        for col, dtype in analysis_df.dtypes.items()  # pyright:ignore[reportUnknownMemberType, reportUnknownVariableType, reportUnknownArgumentType]
    }

    log.dataset("Dataframe shape", metadata=dataframe_shape)
    log.dataset("Dataframe columns", metadata=dataframe_columns)
    log.dataset("Dataframe describe", metadata=dataframe_describe)
    log.dataset("Dataframe data types", metadata=dataframe_dtypes)
