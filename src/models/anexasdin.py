from typing import List
from pydantic_xml import BaseXmlModel, element
from .items import Anexa

NSMAP_ANEXASDIN = {"": "http://www.aduana.cl/xml/esquemas/ANEXASDIN"}


class ANEXASDIN(BaseXmlModel, nsmap=NSMAP_ANEXASDIN):
    anexas: List[Anexa] = element(tag="ANEXA", default=[])
