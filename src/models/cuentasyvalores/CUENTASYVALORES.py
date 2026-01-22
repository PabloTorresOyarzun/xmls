from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class CUENTASYVALORES(BaseXmlModel):
    mon178: str = element(tag='MON178', default=...)
    mon191: str = element(tag='MON191', default=...)
    mon699: str = element(tag='MON699', default=...)
    mon199: str = element(tag='MON199', default=...)
    cuentasgiro: List['CUENTASGIRO'] = element(tag='CUENTASGIRO', default_factory=list)
