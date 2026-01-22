from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class TOTALES(BaseXmlModel):
    totitems: str = element(tag='TOTITEMS', default=...)
    fob: str = element(tag='FOB', default=...)
    tothojas: str = element(tag='TOTHOJAS', default=...)
    codfle: str = element(tag='CODFLE', default=...)
    flete: str = element(tag='FLETE', default=...)
    totbultos: str = element(tag='TOTBULTOS', default=...)
    codseg: str = element(tag='CODSEG', default=...)
    seguro: str = element(tag='SEGURO', default=...)
    totpeso: str = element(tag='TOTPESO', default=...)
    cif: str = element(tag='CIF', default=...)
