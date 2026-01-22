from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class INSUMO(BaseXmlModel):
    numitem: str = element(tag='NUMITEM', default=...)
    numinsumo: str = element(tag='NUMINSUMO', default=...)
    desinsumo: str = element(tag='DESINSUMO', default=...)
    caninsumo: str = element(tag='CANINSUMO', default=...)
    codmedida: str = element(tag='CODMEDIDA', default=...)
    cifinsumo: str = element(tag='CIFINSUMO', default=...)
