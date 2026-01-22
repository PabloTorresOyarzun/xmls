from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class MONTOCUOTA(BaseXmlModel):
    valor: str = element(tag='VALOR', default=...)
    codvalor: str = element(tag='CODVALOR', default=...)
