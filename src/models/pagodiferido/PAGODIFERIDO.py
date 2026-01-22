from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class PAGODIFERIDO(BaseXmlModel):
    tasa: str = element(tag='TASA', default=...)
    ncuotas: str = element(tag='NCUOTAS', default=...)
    adudi: str = element(tag='ADUDI', default=...)
    numdi: str = element(tag='NUMDI', default=...)
    fecdi: str = element(tag='FECDI', default=...)
    cuotas: List['CUOTAS'] = element(tag='CUOTAS', default_factory=list)
