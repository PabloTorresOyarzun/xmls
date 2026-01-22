from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class INSUMOS(BaseXmlModel):
    insumo: List['INSUMO'] = element(tag='INSUMO', default_factory=list)
