from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class LOG(BaseXmlModel):
    secuencia: str = element(tag='SECUENCIA', default=...)
    aduana: str = element(tag='ADUANA', default=...)
    sobre: str = element(tag='SOBRE', default=...)
    fecha: str = element(tag='FECHA', default=...)
    hora: str = element(tag='HORA', default=...)
    van: str = element(tag='VAN', default=...)
    origen: Optional[str] = element(tag='ORIGEN', default=None)
    destino: Optional[str] = element(tag='DESTINO', default=None)
