from typing import Optional
from pydantic_xml import BaseXmlModel, element

NSMAP = {
    "": "http://www.aduana.cl/xml/esquemas/LOG",
}


class LOG(BaseXmlModel, nsmap=NSMAP):
    secuencia: str = element(tag="SECUENCIA")
    aduana: str = element(tag="ADUANA")
    sobre: str = element(tag="SOBRE")
    fecha: str = element(tag="FECHA")
    hora: str = element(tag="HORA")
    van: str = element(tag="VAN")
    origen: Optional[str] = element(tag="ORIGEN", default=None)
    destino: Optional[str] = element(tag="DESTINO", default=None)
