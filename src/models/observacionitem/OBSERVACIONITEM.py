from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class OBSERVACIONITEM(BaseXmlModel):
    codobs: str = element(tag='CODOBS', default=...)
    desobs: str = element(tag='DESOBS', default=...)
