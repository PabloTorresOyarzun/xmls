from typing import List, Optional
from pydantic_xml import BaseXmlModel, element

NSMAP_OBSERVACIONITEM = {"": "http://www.aduana.cl/xml/esquemas/OBSERVACIONITEM"}
NSMAP_OBSERVACIONESITEM = {"": "http://www.aduana.cl/xml/esquemas/OBSERVACIONESITEM"}
NSMAP_CUENTAITEM = {"": "http://www.aduana.cl/xml/esquemas/CUENTAITEM"}
NSMAP_CUENTASITEM = {"": "http://www.aduana.cl/xml/esquemas/CUENTASITEM"}
NSMAP_INSUMO = {"": "http://www.aduana.cl/xml/esquemas/INSUMO"}
NSMAP_INSUMOS = {"": "www.aduana.cl/xml/esquemas/INSUMOS"}
NSMAP_ANEXA = {"": "http://www.aduana.cl/xml/esquemas/ANEXA"}
NSMAP_ANEXAS = {"": "http://www.aduana.cl/xml/esquemas/ANEXAS"}
NSMAP_ITEM = {"": "http://www.aduana.cl/xml/esquemas/ITEM"}
NSMAP_ITEMS = {"": "http://www.aduana.cl/xml/esquemas/ITEMS"}


class ObservacionItem(BaseXmlModel, nsmap=NSMAP_OBSERVACIONITEM):
    codobs: str = element(tag="CODOBS")
    desobs: str = element(tag="DESOBS")


class ObservacionesItem(BaseXmlModel, nsmap=NSMAP_OBSERVACIONESITEM):
    observaciones: List[ObservacionItem] = element(tag="OBSERVACIONITEM")


class CuentaItem(BaseXmlModel, nsmap=NSMAP_CUENTAITEM):
    otro: str = element(tag="OTRO")
    cta: str = element(tag="CTA")
    sigval: str = element(tag="SIGVAL")
    valor: str = element(tag="VALOR")


class CuentasItem(BaseXmlModel, nsmap=NSMAP_CUENTASITEM):
    cuentas: List[CuentaItem] = element(tag="CUENTAITEM")


class Insumo(BaseXmlModel, nsmap=NSMAP_INSUMO):
    numitem: str = element(tag="NUMITEM")
    numinsumo: str = element(tag="NUMINSUMO")
    desinsumo: str = element(tag="DESINSUMO")
    caninsumo: str = element(tag="CANINSUMO")
    codmedida: str = element(tag="CODMEDIDA")
    cifinsumo: str = element(tag="CIFINSUMO")


class Insumos(BaseXmlModel, nsmap=NSMAP_INSUMOS):
    insumos: List[Insumo] = element(tag="INSUMO", default=[])


class Anexa(BaseXmlModel, nsmap=NSMAP_ANEXA):
    numsec: str = element(tag="NUMSEC")
    numdapex: str = element(tag="NUMDAPEX")
    fecdapex: str = element(tag="FECDAPEX")
    codaduana: str = element(tag="CODADUANA")
    numitem: str = element(tag="NUMITEM")
    numinsumo: str = element(tag="NUMINSUMO")
    nominsumo: str = element(tag="NOMINSUMO")
    codunmedi: str = element(tag="CODUNMEDI")
    numitemdec: str = element(tag="NUMITEMDEC")
    nomproducto: str = element(tag="NOMPRODUCTO")
    canproducto: str = element(tag="CANPRODUCTO")
    codunmedp: str = element(tag="CODUNMEDP")
    facconsumo: str = element(tag="FACCONSUMO")
    numinsuti: str = element(tag="NUMINSUTI")


class Anexas(BaseXmlModel, nsmap=NSMAP_ANEXAS):
    anexas: List[Anexa] = element(tag="ANEXA", default=[])


class ITEM(BaseXmlModel, nsmap=NSMAP_ITEM):
    numitem: str = element(tag="NUMITEM")
    dnombre: str = element(tag="DNOMBRE")
    dmarca: str = element(tag="DMARCA")
    dvariedad: str = element(tag="DVARIEDAD")
    dotro1: str = element(tag="DOTRO1")
    dotro2: str = element(tag="DOTRO2")
    atr5: str = element(tag="ATR5")
    atr6: str = element(tag="ATR6")
    sajuitem: str = element(tag="SAJUITEM")
    ajuitem: str = element(tag="AJUITEM")
    cantmerc: str = element(tag="CANTMERC")
    medida: str = element(tag="MEDIDA")
    codestum: str = element(tag="CODESTUM")
    preunit: str = element(tag="PREUNIT")
    arancala: str = element(tag="ARANCALA")
    numcor: str = element(tag="NUMCOR")
    numacu: str = element(tag="NUMACU")
    concupo: str = element(tag="CONCUPO")
    arancnac: str = element(tag="ARANCNAC")
    cifitem: str = element(tag="CIFITEM")
    advalala: str = element(tag="ADVALALA")
    adval: str = element(tag="ADVAL")
    valad: str = element(tag="VALAD")
    observacionesitem: ObservacionesItem = element(tag="OBSERVACIONESITEM")
    cuentasitem: CuentasItem = element(tag="CUENTASITEM")
    insumos: Insumos = element(tag="INSUMOS")
    anexas: Anexas = element(tag="ANEXAS")


class ITEMS(BaseXmlModel, nsmap=NSMAP_ITEMS):
    items: List[ITEM] = element(tag="ITEM")
