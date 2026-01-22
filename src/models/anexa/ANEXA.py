from pydantic import BaseModel, Field
from typing import List, Optional
from pydantic_xml import BaseXmlModel, element, attr

class ANEXA(BaseXmlModel):
    numsec: str = element(tag='NUMSEC', default=...)
    numdapex: str = element(tag='NUMDAPEX', default=...)
    fecdapex: str = element(tag='FECDAPEX', default=...)
    codaduana: str = element(tag='CODADUANA', default=...)
    numitem: str = element(tag='NUMITEM', default=...)
    numinsumo: str = element(tag='NUMINSUMO', default=...)
    nominsumo: str = element(tag='NOMINSUMO', default=...)
    codunmedi: str = element(tag='CODUNMEDI', default=...)
    numitemdec: str = element(tag='NUMITEMDEC', default=...)
    nomproducto: str = element(tag='NOMPRODUCTO', default=...)
    canproducto: str = element(tag='CANPRODUCTO', default=...)
    codunmedp: str = element(tag='CODUNMEDP', default=...)
    facconsumo: str = element(tag='FACCONSUMO', default=...)
    numinsuti: str = element(tag='NUMINSUTI', default=...)
