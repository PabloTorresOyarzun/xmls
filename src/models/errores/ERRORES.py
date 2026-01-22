from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class ERRORES(BaseXmlModel):
    fechaproceso: str = element(tag='FECHAPROCESO', default=...)
    error: List['ERROR'] = element(tag='ERROR', default_factory=list)
