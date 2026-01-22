from typing import Optional
from pydantic_xml import BaseXmlModel, element

from .log import LOG
from .cabeza import CABEZA
from .items import ITEMS
from .vistosbuenos import VISTOSBUENOS
from .bultos import BULTOS
from .cuentasyvalores import CUENTASYVALORES
from .pagodiferido import PAGODIFERIDO
from .anexasdin import ANEXASDIN
from .errores import ERRORES

NSMAP = {
    "": "http://www.aduana.cl/xml/esquemas/EnvioDin",
    "pref": "http://www.aduana.cl/xml/esquemas/LOG",
    "pref1": "http://www.aduana.cl/xml/esquemas/CABEZA",
    "pref2": "http://www.aduana.cl/xml/esquemas/ITEMS",
    "pref3": "http://www.aduana.cl/xml/esquemas/VISTOSBUENOS",
    "pref4": "http://www.aduana.cl/xml/esquemas/BULTOS",
    "pref5": "http://www.aduana.cl/xml/esquemas/CUENTASYVALORES",
    "pref6": "http://www.aduana.cl/xml/esquemas/PAGODIFERIDO",
    "pref7": "http://www.aduana.cl/xml/esquemas/ERRORES",
    "pref10": "http://www.aduana.cl/xml/esquemas/ANEXASDIN",
}


class DIN(BaseXmlModel, tag="DIN", nsmap=NSMAP):
    tipoenvio: str = element(tag="TIPOENVIO")
    log: LOG = element(tag="LOG")
    cabeza: CABEZA = element(tag="CABEZA")
    items: ITEMS = element(tag="ITEMS")
    vistosbuenos: VISTOSBUENOS = element(tag="VISTOSBUENOS")
    bultos: BULTOS = element(tag="BULTOS")
    cuentasyvalores: CUENTASYVALORES = element(tag="CUENTASYVALORES")
    pagodiferido: Optional[PAGODIFERIDO] = element(tag="PAGODIFERIDO", default=None)
    anexasdin: Optional[ANEXASDIN] = element(tag="ANEXASDIN", default=None)
    errores: ERRORES = element(tag="ERRORES")
