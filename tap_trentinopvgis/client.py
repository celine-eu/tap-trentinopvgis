"""REST client handling, including TrentinoPvGisStream base class."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, ClassVar

from singer_sdk import typing as th
from singer_sdk.pagination import OffsetPaginator
from singer_sdk.streams import RESTStream

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

if TYPE_CHECKING:
    from collections.abc import Iterable

    import requests
    from singer_sdk.helpers.types import Context
    from singer_sdk.streams.rest import HTTPRequest, PageContext

PROXY_BASE = "https://webgis.provincia.tn.it"
PROXY_PATH = "/wgt/services/ogcproxy/wms"
INNER_GEOSERVER = "https://geoservices.cloud-intra.tn.it/geoserver"


class WFSOffsetPaginator(OffsetPaginator):
    """WFS 2.0.0 offset-based paginator using count/startIndex."""

    @override
    def has_more(self, response: requests.Response) -> bool:
        data = response.json()
        returned = data.get("numberReturned", len(data.get("features", [])))
        return returned >= self._page_size


class TrentinoPvGisStream(RESTStream):
    """Base stream for WFS layers served through the PAT OGC proxy."""

    type_name: ClassVar[str]
    workspace: ClassVar[str]

    primary_keys: ClassVar[tuple[str, ...]] = ("id",)
    replication_key = None

    schema = th.PropertiesList(
        th.Property("type", th.StringType),
        th.Property("id", th.StringType),
        th.Property("geometry", th.ObjectType()),
        th.Property("geometry_name", th.StringType),
        th.Property("properties", th.ObjectType()),
    ).to_dict()

    @property
    @override
    def url_base(self) -> str:
        return PROXY_BASE

    @property
    @override
    def path(self) -> str:
        return PROXY_PATH

    @property
    def inner_wfs_url(self) -> str:
        return f"{INNER_GEOSERVER}/{self.workspace}/wfs?"

    @property
    def page_size(self) -> int:
        return self.config.get("page_size", 2000)

    @property
    def srs_name(self) -> str:
        return self.config.get("srs_name", "EPSG:4326")

    @override
    def get_new_paginator(self) -> WFSOffsetPaginator:
        return WFSOffsetPaginator(start_value=0, page_size=self.page_size)

    @override
    def get_http_request(self, *, page: PageContext[Any]) -> HTTPRequest:
        request = super().get_http_request(page=page)
        request.params = {
            "url": self.inner_wfs_url,
            "SERVICE": "WFS",
            "VERSION": "2.0.0",
            "REQUEST": "GetFeature",
            "typeNames": self.type_name,
            "outputFormat": "application/json",
            "srsName": self.srs_name,
            "count": self.page_size,
            "startIndex": page.next_page_token if page.next_page_token is not None else 0,
        }
        return request

    @override
    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        data = response.json()
        yield from data.get("features", [])

    @override
    def post_process(
        self,
        row: dict,
        context: Context | None = None,
    ) -> dict | None:
        return row
