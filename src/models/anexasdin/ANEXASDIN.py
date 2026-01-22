from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class ANEXASDIN(BaseXmlModel):
    anexa: List['ANEXA'] = element(tag='ANEXA', default_factory=list)
