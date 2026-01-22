from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class FECHAVENCCUOTA(BaseXmlModel):
    fecha: str = element(tag='FECHA', default=...)
    codfecha: str = element(tag='CODFECHA', default=...)
