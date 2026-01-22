from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class VISTOSBUENOS(BaseXmlModel):
    vistobueno: List['VISTOBUENO'] = element(tag='VISTOBUENO', default_factory=list)
