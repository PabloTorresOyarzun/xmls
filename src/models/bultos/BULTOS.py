from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class BULTOS(BaseXmlModel):
    idbultos: str = element(tag='IDBULTOS', default=...)
    bulto: List['BULTO'] = element(tag='BULTO', default_factory=list)
