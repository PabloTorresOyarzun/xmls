from typing import List, Optional
from pydantic_xml import BaseXmlModel, element

NSMAP_FECHAVENCCUOTA = {"": "http://www.aduana.cl/xml/esquemas/FECHAVENCCUOTA"}
NSMAP_MONTOCUOTA = {"": "http://www.aduana.cl/xml/esquemas/MONTOCUOTA"}
NSMAP_CUOTA = {"": "http://www.aduana.cl/xml/esquemas/CUOTA"}
NSMAP_CUOTAS = {"": "http://www.aduana.cl/xml/esquemas/CUOTAS"}
NSMAP_PAGODIFERIDO = {"": "http://www.aduana.cl/xml/esquemas/PAGODIFERIDO"}


class FechaVencCuota(BaseXmlModel, nsmap=NSMAP_FECHAVENCCUOTA):
    fecha: str = element(tag="FECHA")
    codfecha: str = element(tag="CODFECHA")


class MontoCuota(BaseXmlModel, nsmap=NSMAP_MONTOCUOTA):
    valor: str = element(tag="VALOR")
    codvalor: str = element(tag="CODVALOR")


class Cuota(BaseXmlModel, nsmap=NSMAP_CUOTA):
    fechavenccuota: List[FechaVencCuota] = element(tag="FECHAVENCCUOTA")
    montocuota: List[MontoCuota] = element(tag="MONTOCUOTA")


class Cuotas(BaseXmlModel, nsmap=NSMAP_CUOTAS):
    cuotas: List[Cuota] = element(tag="CUOTA")


class PAGODIFERIDO(BaseXmlModel, nsmap=NSMAP_PAGODIFERIDO):
    tasa: str = element(tag="TASA")
    ncuotas: str = element(tag="NCUOTAS")
    adudi: str = element(tag="ADUDI")
    numdi: str = element(tag="NUMDI")
    fecdi: str = element(tag="FECDI")
    cuotas: Optional[Cuotas] = element(tag="CUOTAS", default=None)
