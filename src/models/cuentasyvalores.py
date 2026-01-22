from typing import List, Optional
from pydantic_xml import BaseXmlModel, element

NSMAP_CUENTAGIRO = {"": "http://www.aduana.cl/xml/esquemas/CUENTAGIRO"}
NSMAP_CUENTASGIRO = {"": "http://www.aduana.cl/xml/esquemas/CUENTASGIRO"}
NSMAP_CUENTASYVALORES = {"": "http://www.aduana.cl/xml/esquemas/CUENTASYVALORES"}


class CuentaGiro(BaseXmlModel, nsmap=NSMAP_CUENTAGIRO):
    ctaotro: str = element(tag="CTAOTRO")
    monotro: str = element(tag="MONOTRO")


class CuentasGiro(BaseXmlModel, nsmap=NSMAP_CUENTASGIRO):
    cuentas: List[CuentaGiro] = element(tag="CUENTAGIRO", default=[])


class CUENTASYVALORES(BaseXmlModel, nsmap=NSMAP_CUENTASYVALORES):
    mon178: str = element(tag="MON178")
    mon191: str = element(tag="MON191")
    mon699: str = element(tag="MON699")
    mon199: str = element(tag="MON199")
    cuentasgiro: CuentasGiro = element(tag="CUENTASGIRO")
