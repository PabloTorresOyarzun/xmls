from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class CUENTASITEM(BaseXmlModel):
    cuentaitem: List['CUENTAITEM'] = element(tag='CUENTAITEM', default_factory=list)
