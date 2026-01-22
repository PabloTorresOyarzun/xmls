from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class EnvioDin(BaseXmlModel):
    tipoenvio: str = element(tag='TIPOENVIO', default=...)
    log: List['LOG'] = element(tag='LOG', default_factory=list)
    cabeza: List['CABEZA'] = element(tag='CABEZA', default_factory=list)
    items: 'ITEMS' = element(tag='ITEMS', default=...)
    vistosbuenos: 'VISTOSBUENOS' = element(tag='VISTOSBUENOS', default=...)
    bultos: List['BULTOS'] = element(tag='BULTOS', default_factory=list)
    cuentasyvalores: List['CUENTASYVALORES'] = element(tag='CUENTASYVALORES', default_factory=list)
    pagodiferido: List['PAGODIFERIDO'] = element(tag='PAGODIFERIDO', default_factory=list)
    anexasdin: Optional['ANEXASDIN'] = element(tag='ANEXASDIN', default=None)
    respuesta: Optional['RESPUESTA'] = element(tag='RESPUESTA', default=None)
    errores: List['ERRORES'] = element(tag='ERRORES', default_factory=list)
    signature: 'SignatureType' = element(tag='Signature', default=...)
