from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class CUENTAITEM(BaseXmlModel):
    otro: str = element(tag='OTRO', default=...)
    cta: str = element(tag='CTA', default=...)
    sigval: str = element(tag='SIGVAL', default=...)
    valor: str = element(tag='VALOR', default=...)
