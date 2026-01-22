from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class CUOTAS(BaseXmlModel):
    cuota: List['CUOTA'] = element(tag='CUOTA', default_factory=list)
