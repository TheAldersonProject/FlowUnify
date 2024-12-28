"""Pandas helpers and functionalities."""

from typing import Any

import pandas as pd  # pyright:ignore[reportMissingTypeStubs]

from opsdataflow import Signals


class PandasOps:
    """Pandas object analysis and accelerators."""

    def __init__(self, signals: Signals) -> None:
        """Initialize class attributes."""
        self.__signals: Signals = signals

    def analyze_pandas_dataframe_and_emit_signals(self, analysis_df: pd.DataFrame) -> None:
        """Analyses the dataframe to emit signals."""
        dataframe_columns: Any = analysis_df.columns.tolist()
        dataframe_shape: Any = analysis_df.shape
        dataframe_describe: Any = analysis_df.describe().to_dict()  # pyright:ignore[reportUnknownMemberType]
        dataframe_dtypes: dict[str, str] = {
            str(col): str(dtype).replace("dtype('", "").replace("')", "")  # pyright:ignore[reportUnknownMemberType, reportUnknownVariableType, reportUnknownArgumentType]
            for col, dtype in analysis_df.dtypes.items()  # pyright:ignore[reportUnknownMemberType, reportUnknownVariableType, reportUnknownArgumentType]
        }

        self.__signals.dataset("Dataframe shape", metadata=dataframe_shape)
        self.__signals.dataset("Dataframe columns", metadata=dataframe_columns)
        self.__signals.dataset("Dataframe describe", metadata=dataframe_describe)
        self.__signals.dataset("Dataframe data types", metadata=dataframe_dtypes)
