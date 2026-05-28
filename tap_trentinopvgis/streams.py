"""Stream type classes for tap-trentinopvgis."""

from __future__ import annotations

from typing import ClassVar

from tap_trentinopvgis.client import TrentinoPvGisStream


class AreeIdoneeStream(TrentinoPvGisStream):
    """Suitable areas for photovoltaic installations (L.P. 4/2022 Allegato B)."""

    name = "aree_idonee"
    type_name: ClassVar[str] = "pub_irraggiamento:aree_idonee"
    workspace: ClassVar[str] = "pub_irraggiamento"


class AreeNonIdoneeStream(TrentinoPvGisStream):
    """Unsuitable areas for photovoltaic installations (PUP invariants)."""

    name = "aree_non_idonee"
    type_name: ClassVar[str] = "pub_irraggiamento:aree_non_idonee"
    workspace: ClassVar[str] = "pub_irraggiamento"


class EdificatoFbkStream(TrentinoPvGisStream):
    """FBK rooftop footprints for roof-level PV analysis."""

    name = "edificato_fbk"
    type_name: ClassVar[str] = "pub_irraggiamento:edificato_fbk"
    workspace: ClassVar[str] = "pub_irraggiamento"


class VincoliIndirettiStream(TrentinoPvGisStream):
    """Indirect constraints on architectural heritage properties."""

    name = "vincoli_indiretti"
    type_name: ClassVar[str] = "pub_sbc:vinc_ind_zr_a"
    workspace: ClassVar[str] = "pub_sbc"


class VincoliDirettiStream(TrentinoPvGisStream):
    """Direct constraints on architectural heritage properties."""

    name = "vincoli_diretti"
    type_name: ClassVar[str] = "pub_sbc:vinc_dir_bea"
    workspace: ClassVar[str] = "pub_sbc"
