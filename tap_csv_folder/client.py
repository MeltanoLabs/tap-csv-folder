"""Stream class for CSV files."""

from __future__ import annotations

import csv
from typing import TYPE_CHECKING, Any

from singer_sdk.contrib.filesystem import FileStream
from singer_sdk.contrib.filesystem.stream import SDC_META_FILEPATH

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    from singer_sdk.helpers.types import Record


SDC_META_LINE_NUMBER = "_sdc_line_number"


class CSVStream(FileStream):
    """CSV stream class."""

    @property
    def primary_keys(self) -> Sequence[str]:
        """Return the primary key fields for records in this stream."""
        if self._primary_keys is None:
            self._primary_keys = (SDC_META_FILEPATH, SDC_META_LINE_NUMBER)

        return self._primary_keys

    @primary_keys.setter
    def primary_keys(self, value: Sequence[str]) -> None:
        """Set the primary key fields for records in this stream."""
        self._primary_keys = value

    def get_schema(self, path: str) -> dict[str, Any]:
        """Return a schema for the given file."""
        with self.filesystem.open(path, mode="r") as file:
            reader = csv.DictReader(
                file,
                delimiter=self.config["delimiter"],
                quotechar=self.config["quotechar"],
                escapechar=self.config.get("escapechar"),
                doublequote=self.config["doublequote"],
                lineterminator=self.config["lineterminator"],
            )
            schema: dict[str, Any] = {
                "type": "object",
                "properties": {
                    key: {"type": "string"}  # By default all fields are strings
                    for key in reader.fieldnames or []
                },
            }
            schema["properties"][SDC_META_LINE_NUMBER] = {"type": "integer"}  # ty: ignore[possibly-missing-implicit-call]
            return schema

    def read_file(self, path: str) -> Iterable[Record]:
        """Read the given file and emit records."""
        with self.filesystem.open(path, mode="r") as file:
            reader = csv.DictReader(
                file,
                delimiter=self.config["delimiter"],
                quotechar=self.config["quotechar"],
                escapechar=self.config.get("escapechar"),
                doublequote=self.config["doublequote"],
                lineterminator=self.config["lineterminator"],
            )
            for record in reader:
                record[SDC_META_LINE_NUMBER] = reader.line_num
                yield record
