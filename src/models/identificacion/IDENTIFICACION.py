from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class IDENTIFICACION(BaseXmlModel):
    nombre: str = element(tag='NOMBRE', default=...)
    direc: str = element(tag='DIREC', default=...)
    codcomun: str = element(tag='CODCOMUN', default=...)
    tiprut: str = element(tag='TIPRUT', default=...)
    rut: str = element(tag='RUT', default=...)
    dvrut: str = element(tag='DVRUT', default=...)
    nomrepleg: str = element(tag='NOMREPLEG', default=...)
    numrutrl: str = element(tag='NUMRUTRL', default=...)
    digverrl: str = element(tag='DIGVERRL', default=...)
    nomconsig: str = element(tag='NOMCONSIG', default=...)
    desdircon: str = element(tag='DESDIRCON', default=...)
    codpaiscon: str = element(tag='CODPAISCON', default=...)
