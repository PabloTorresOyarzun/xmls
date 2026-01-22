from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class OBSERVACIONESITEM(BaseXmlModel):
    observacionitem: List['OBSERVACIONITEM'] = element(tag='OBSERVACIONITEM', default_factory=list)
