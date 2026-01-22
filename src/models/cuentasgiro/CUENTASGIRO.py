from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class CUENTASGIRO(BaseXmlModel):
    cuentagiro: List['CUENTAGIRO'] = element(tag='CUENTAGIRO', default_factory=list)
