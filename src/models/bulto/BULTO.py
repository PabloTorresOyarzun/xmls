from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class BULTO(BaseXmlModel):
    destipbul: str = element(tag='DESTIPBUL', default=...)
    tpobul: str = element(tag='TPOBUL', default=...)
    cantbul: str = element(tag='CANTBUL', default=...)
