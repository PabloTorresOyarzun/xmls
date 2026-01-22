from typing import List
from pydantic_xml import BaseXmlModel, element

NSMAP_ERROR = {"": "http://www.aduana.cl/xml/esquemas/ERROR"}
NSMAP_ERRORES = {"": "http://www.aduana.cl/xml/esquemas/ERRORES"}


class Error(BaseXmlModel, nsmap=NSMAP_ERROR):
    codigo: str = element(tag="CODIGO")
    glosa: str = element(tag="GLOSA")


class ERRORES(BaseXmlModel, nsmap=NSMAP_ERRORES):
    fechaproceso: str = element(tag="FECHAPROCESO")
    errores: List[Error] = element(tag="ERROR")
