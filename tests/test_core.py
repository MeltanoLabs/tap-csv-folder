"""Test suite for tap-csv-folder."""

from __future__ import annotations

import datetime
import typing as t

import pytest
from singer_sdk.testing import SuiteConfig, TapTestRunner, get_tap_test_class

from tap_csv_folder.tap import TapCSVFolder

if t.TYPE_CHECKING:
    from tap_csv_folder.client import CSVStream


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
                    "context": {"_sdc_path": "./customers.csv"},
                    "replication_key": "_sdc_modified_at",
                    "replication_key_value": FUTURE.isoformat(),
                }
            ]
        },
        "employees": {
            "partitions": [
                {
                    "context": {"_sdc_path": "./employees.csv"},
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
)


class TestCSVOneStreamPerFileIncremental(_TestCSVOneStreamPerFileIncremental):
    """Test tap in one 'stream per file' incremental mode."""

    @pytest.mark.xfail(
        reason="There are no records because the state is set to the future.",
        strict=True,
    )
    def test_tap_stream_returns_record(
        self,
        config: SuiteConfig,
        resource: t.Any,  # noqa: ANN401
        runner: TapTestRunner,
        stream: CSVStream,
    ) -> None:
        """Test that the tap stream returns records."""
        super().test_tap_stream_returns_record(config, resource, runner, stream)


TestCSVOneStreamPerFileIncrementalIgnoreNoRecords = get_tap_test_class(
    tap_class=TapCSVFolder,
    config={
        "path": "fixtures",
        "read_mode": "one_stream_per_file",
        "delimiter": "\t",
    },
    state=STATE,
    suite_config=SuiteConfig(ignore_no_records=True),
)
