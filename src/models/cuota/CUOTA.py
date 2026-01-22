from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class CUOTA(BaseXmlModel):
    fechavenccuota: List['FECHAVENCCUOTA'] = element(tag='FECHAVENCCUOTA', default_factory=list)
    montocuota: List['MONTOCUOTA'] = element(tag='MONTOCUOTA', default_factory=list)
