"""Test suite for tap-csv-folder."""

from __future__ import annotations

import datetime

import pytest
from singer_sdk.testing import SuiteConfig, get_tap_test_class

from tap_csv_folder.tap import TapCSVFolder

_TestCSVMerge = get_tap_test_class(
    tap_class=TapCSVFolder,
    config={
        "path": "fixtures",
        "read_mode": "merge",
        "stream_name": "people",
        "delimiter": "\t",
    },
)


class TestCSVMerge(_TestCSVMerge):
    """Test tap in file merge mode."""


_TestCSVOneStreamPerFile = get_tap_test_class(
    tap_class=TapCSVFolder,
    config={
        "path": "fixtures",
        "read_mode": "one_stream_per_file",
        "delimiter": "\t",
    },
)


class TestCSVOneStreamPerFile(_TestCSVOneStreamPerFile):
    """Test tap in one 'stream per file' mode."""


# Three days into the future.
FUTURE = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=3)

STATE = {
    "bookmarks": {
        "customers": {
            "partitions": [
                {
                    "context": {"_sdc_path": "fixtures/customers.csv"},
                    "replication_key": "_sdc_modified_at",
                    "replication_key_value": FUTURE.isoformat(),
                }
            ]
        },
        "employees": {
            "partitions": [
                {
                    "context": {"_sdc_path": "fixtures/employees.csv"},
                    "replication_key": "_sdc_modified_at",
                    "replication_key_value": FUTURE.isoformat(),
                }
            ]
        },
    }
}


_TestCSVOneStreamPerFileIncremental = get_tap_test_class(
    tap_class=TapCSVFolder,
    config={
        "path": "fixtures",
        "read_mode": "one_stream_per_file",
        "delimiter": "\t",
    },
    state=STATE,
    suite_config=SuiteConfig(ignore_no_records=True),
)


class TestCSVOneStreamPerFileIncremental(_TestCSVOneStreamPerFileIncremental):
    """Test tap in one 'stream per file' mode with incremental replication."""

    @pytest.mark.xfail(reason="No records are extracted", strict=True)
    def test_tap_stream_transformed_catalog_schema_matches_record(self, stream: str) -> None:
        """This test shoould fail because no records are extracted for the bookmark."""
        super().test_tap_stream_transformed_catalog_schema_matches_record(stream)

    @pytest.mark.xfail(reason="No records are extracted", strict=True)
    def test_tap_stream_returns_record(self, stream: str) -> None:
        """This test shoould fail because no records are extracted for the bookmark."""
        super().test_tap_stream_returns_record(stream)
