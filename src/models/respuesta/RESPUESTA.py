from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class RESPUESTA(BaseXmlModel):
    fechaceptacion: str = element(tag='FECHACEPTACION', default=...)
    numeroencriptado: str = element(tag='NUMEROENCRIPTADO', default=...)
    estado: str = element(tag='ESTADO', default=...)
    tiposeleccion: Optional[str] = element(tag='TIPOSELECCION', default=None)
