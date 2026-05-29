"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_tap_test_class

from tap_trentinopvgis.tap import TapTrentinoPvGis

SAMPLE_CONFIG: dict[str, str] = {}

TestTapTrentinoPvGis = get_tap_test_class(
    tap_class=TapTrentinoPvGis,
    config=SAMPLE_CONFIG,
)
