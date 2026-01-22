from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class REGIMENSUSPENSIVO(BaseXmlModel):
    desdiralm: str = element(tag='DESDIRALM', default=...)
    codcomrs: str = element(tag='CODCOMRS', default=...)
    aductrol: str = element(tag='ADUCTROL', default=...)
    numplazo: str = element(tag='NUMPLAZO', default=...)
    indparcial: str = element(tag='INDPARCIAL', default=...)
    numhojins: str = element(tag='NUMHOJINS', default=...)
    totinsum: str = element(tag='TOTINSUM', default=...)
    codalma: str = element(tag='CODALMA', default=...)
    numrs: str = element(tag='NUMRS', default=...)
    fecrs: str = element(tag='FECRS', default=...)
    aduars: str = element(tag='ADUARS', default=...)
    numhojane: str = element(tag='NUMHOJANE', default=...)
    numsec: str = element(tag='NUMSEC', default=...)
