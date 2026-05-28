"""TrentinoPvGis tap class."""

from __future__ import annotations

import sys

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_trentinopvgis import streams

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class TapTrentinoPvGis(Tap):
    """Singer tap for Trentino photovoltaic-potential WFS layers."""

    name = "tap-trentinopvgis"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "page_size",
            th.IntegerType,
            default=2000,
            description="Number of features per WFS GetFeature page",
        ),
        th.Property(
            "srs_name",
            th.StringType,
            default="EPSG:4326",
            description="Coordinate reference system for output geometries",
        ),
    ).to_dict()

    @override
    def discover_streams(self) -> list[streams.TrentinoPvGisStream]:
        return [
            streams.AreeIdoneeStream(self),
            streams.AreeNonIdoneeStream(self),
            streams.EdificatoFbkStream(self),
            streams.VincoliIndirettiStream(self),
            streams.VincoliDirettiStream(self),
        ]


if __name__ == "__main__":
    TapTrentinoPvGis.cli()
