"""Singer Tap for CSV files in a folder."""

from __future__ import annotations

import singer_sdk.typing as th
from singer_sdk.contrib.filesystem import FolderTap

from tap_csv_folder.client import CSVStream


class TapCSVFolder(FolderTap):
    """Singer tap for CSV files in a folder."""

    name = "tap-csv-folder"
    valid_extensions: tuple[str, ...] = (".csv",)
    default_stream_class = CSVStream

    config_jsonschema = th.PropertiesList(
        th.Property(
            "delimiter",
            th.StringType,
            default=",",
            description="Field delimiter character.",
        ),
        th.Property(
            "quotechar",
            th.StringType,
            default='"',
            description="Quote character.",
        ),
        th.Property(
            "escapechar",
            th.StringType,
            default=None,
            description="Escape character.",
        ),
        th.Property(
            "doublequote",
            th.BooleanType,
            default=True,
            description="Whether quotechar inside a field should be doubled.",
        ),
        th.Property(
            "lineterminator",
            th.StringType,
            default="\r\n",
            description="Line terminator character.",
        ),
    ).to_dict()
