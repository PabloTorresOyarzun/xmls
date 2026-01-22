from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class SignatureType(BaseXmlModel):
    signedInfo: 'SignedInfoType' = element(tag='SignedInfo', default=...)
    signatureValue: 'SignatureValueType' = element(tag='SignatureValue', default=...)
    keyInfo: Optional['KeyInfoType'] = element(tag='KeyInfo', default=None)
    object: List['ObjectType'] = element(tag='Object', default_factory=list)
