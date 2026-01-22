from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class CUENTAGIRO(BaseXmlModel):
    ctaotro: str = element(tag='CTAOTRO', default=...)
    monotro: str = element(tag='MONOTRO', default=...)
