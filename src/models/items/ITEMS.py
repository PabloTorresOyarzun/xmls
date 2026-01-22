from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class ITEMS(BaseXmlModel):
    item: List['ITEM'] = element(tag='ITEM', default_factory=list)
