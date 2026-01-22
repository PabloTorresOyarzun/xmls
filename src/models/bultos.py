from typing import List, Optional
from pydantic_xml import BaseXmlModel, element

NSMAP_BULTO = {"": "http://www.aduana.cl/xml/esquemas/BULTO"}
NSMAP_BULTOS = {"": "http://www.aduana.cl/xml/esquemas/BULTOS"}


class Bulto(BaseXmlModel, nsmap=NSMAP_BULTO):
    destipbul: str = element(tag="DESTIPBUL")
    tpobul: str = element(tag="TPOBUL")
    cantbul: str = element(tag="CANTBUL")


class BULTOS(BaseXmlModel, nsmap=NSMAP_BULTOS):
    idbultos: str = element(tag="IDBULTOS")
    bultos: List[Bulto] = element(tag="BULTO", default=[])
