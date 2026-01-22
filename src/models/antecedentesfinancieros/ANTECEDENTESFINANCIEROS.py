from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class ANTECEDENTESFINANCIEROS(BaseXmlModel):
    gregimp: str = element(tag='GREGIMP', default=...)
    regimp: str = element(tag='REGIMP', default=...)
    bcocom: str = element(tag='BCOCOM', default=...)
    codordiv: str = element(tag='CODORDIV', default=...)
    formpago: str = element(tag='FORMPAGO', default=...)
    numdias: str = element(tag='NUMDIAS', default=...)
    valexfab: str = element(tag='VALEXFAB', default=...)
    moneda: str = element(tag='MONEDA', default=...)
    mongasfob: str = element(tag='MONGASFOB', default=...)
    clcompra: str = element(tag='CLCOMPRA', default=...)
    pagograv: str = element(tag='PAGOGRAV', default=...)
