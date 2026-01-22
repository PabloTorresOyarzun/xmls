from typing import List, Optional
from pydantic_xml import BaseXmlModel, element

NSMAP_VISTOBUENO = {"": "http://www.aduana.cl/xml/esquemas/VISTOBUENO"}
NSMAP_VISTOSBUENOS = {"": "http://www.aduana.cl/xml/esquemas/VISTOSBUENOS"}


class VistoBueno(BaseXmlModel, nsmap=NSMAP_VISTOBUENO):
    nuregr: str = element(tag="NUREGR")
    anoreg: str = element(tag="ANOREG")
    codvisbuen: str = element(tag="CODVISBUEN")
    numregla: str = element(tag="NUMREGLA")
    numanores: str = element(tag="NUMANORES")
    codultvb: str = element(tag="CODULTVB")


class VISTOSBUENOS(BaseXmlModel, nsmap=NSMAP_VISTOSBUENOS):
    vistosbuenos: List[VistoBueno] = element(tag="VISTOBUENO", default=[])
