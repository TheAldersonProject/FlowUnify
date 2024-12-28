"""Pandas helpers and functionalities."""

from typing import Any

import pandas as pd  # pyright:ignore[reportMissingTypeStubs]

from opsdataflow.telemetry.logger_handler import LoggerHandler

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

    log.log("DATASET", "Dataframe shape", metadata=dataframe_shape)
    log.log("DATASET", "Dataframe columns", metadata=dataframe_columns)
    log.log("DATASET", "Dataframe describe", metadata=dataframe_describe)
    log.log("DATASET", "Dataframe data types", metadata=dataframe_dtypes)
