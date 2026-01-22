from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class IngresoConsultaDIN(BaseXmlModel):
    numeroDIN: str = element(tag='numeroDIN', default=...)
    numeroAclaracion: str = element(tag='numeroAclaracion', default=...)
    tipoEnvio: str = element(tag='tipoEnvio', default=...)
    ultimaRespuesta: str = element(tag='ultimaRespuesta', default=...)
