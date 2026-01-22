from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class VISTOBUENO(BaseXmlModel):
    nuregr: str = element(tag='NUREGR', default=...)
    anoreg: str = element(tag='ANOREG', default=...)
    codvisbuen: str = element(tag='CODVISBUEN', default=...)
    numregla: str = element(tag='NUMREGLA', default=...)
    numanores: str = element(tag='NUMANORES', default=...)
    codultvb: str = element(tag='CODULTVB', default=...)
