from typing import Optional
from pydantic_xml import BaseXmlModel, element

NSMAP_IDENTIFICACION = {"": "http://www.aduana.cl/xml/esquemas/IDENTIFICACION"}
NSMAP_REGIMENSUSPENSIVO = {"": "http://www.aduana.cl/xml/esquemas/REGIMENSUSPENSIVO"}
NSMAP_ORIGENTRANSPALMACENAJE = {"": "http://www.aduana.cl/xml/esquemas/ORIGENTRANSPALMACENAJE"}
NSMAP_ANTECEDENTESFINANCIEROS = {"": "http://www.aduana.cl/xml/esquemas/ANTECEDENTESFINANCIEROS"}
NSMAP_TOTALES = {"": "http://www.aduana.cl/xml/esquemas/TOTALES"}
NSMAP_RESPUESTA = {"": "http://www.aduana.cl/xml/esquemas/RESPUESTA"}
NSMAP_CABEZA = {"": "http://www.aduana.cl/xml/esquemas/CABEZA"}


class Identificacion(BaseXmlModel, nsmap=NSMAP_IDENTIFICACION):
    nombre: str = element(tag="NOMBRE")
    direc: str = element(tag="DIREC")
    codcomun: str = element(tag="CODCOMUN")
    tiprut: str = element(tag="TIPRUT")
    rut: str = element(tag="RUT")
    dvrut: str = element(tag="DVRUT")
    nomrepleg: str = element(tag="NOMREPLEG")
    numrutrl: str = element(tag="NUMRUTRL")
    digverrl: str = element(tag="DIGVERRL")
    nomconsig: str = element(tag="NOMCONSIG")
    desdircon: str = element(tag="DESDIRCON")
    codpaiscon: str = element(tag="CODPAISCON")


class RegimenSuspensivo(BaseXmlModel, nsmap=NSMAP_REGIMENSUSPENSIVO):
    desdiralm: str = element(tag="DESDIRALM")
    codcomrs: str = element(tag="CODCOMRS")
    aductrol: str = element(tag="ADUCTROL")
    numplazo: str = element(tag="NUMPLAZO")
    indparcial: str = element(tag="INDPARCIAL")
    numhojins: str = element(tag="NUMHOJINS")
    totinsum: str = element(tag="TOTINSUM")
    codalma: str = element(tag="CODALMA")
    numrs: str = element(tag="NUMRS")
    fecrs: str = element(tag="FECRS")
    aduars: str = element(tag="ADUARS")
    numhojane: str = element(tag="NUMHOJANE")
    numsec: str = element(tag="NUMSEC")


class OrigenTranspAlmacenaje(BaseXmlModel, nsmap=NSMAP_ORIGENTRANSPALMACENAJE):
    paorig: str = element(tag="PAORIG")
    gpaorig: str = element(tag="GPAORIG")
    paadq: str = element(tag="PAADQ")
    gpaadq: str = element(tag="GPAADQ")
    viatran: str = element(tag="VIATRAN")
    despuert: str = element(tag="DESPUERT")
    transb: str = element(tag="TRANSB")
    ptoemb: str = element(tag="PTOEMB")
    gptodesem: str = element(tag="GPTODESEM")
    ptodesem: str = element(tag="PTODESEM")
    tpocarga: str = element(tag="TPOCARGA")
    desalmac: str = element(tag="DESALMAC")
    almacen: str = element(tag="ALMACEN")
    fecalmac: str = element(tag="FECALMAC")
    fecretiro: str = element(tag="FECRETIRO")
    gnomciat: str = element(tag="GNOMCIAT")
    codpaiscia: str = element(tag="CODPAISCIA")
    numrutcia: str = element(tag="NUMRUTCIA")
    digvercia: str = element(tag="DIGVERCIA")
    nummanif: str = element(tag="NUMMANIF")
    nummanif1: str = element(tag="NUMMANIF1")
    nummanif2: str = element(tag="NUMMANIF2")
    fecmanif: str = element(tag="FECMANIF")
    numconoc: str = element(tag="NUMCONOC")
    fecconoc: str = element(tag="FECCONOC")
    nomemisor: str = element(tag="NOMEMISOR")
    numrutemi: str = element(tag="NUMRUTEMI")
    digveremi: str = element(tag="DIGVEREMI")


class AntecedentesFinancieros(BaseXmlModel, nsmap=NSMAP_ANTECEDENTESFINANCIEROS):
    gregimp: str = element(tag="GREGIMP")
    regimp: str = element(tag="REGIMP")
    bcocom: str = element(tag="BCOCOM")
    codordiv: str = element(tag="CODORDIV")
    formpago: str = element(tag="FORMPAGO")
    numdias: str = element(tag="NUMDIAS")
    valexfab: str = element(tag="VALEXFAB")
    moneda: str = element(tag="MONEDA")
    mongasfob: str = element(tag="MONGASFOB")
    clcompra: str = element(tag="CLCOMPRA")
    pagograv: str = element(tag="PAGOGRAV")


class Totales(BaseXmlModel, nsmap=NSMAP_TOTALES):
    totitems: str = element(tag="TOTITEMS")
    fob: str = element(tag="FOB")
    tothojas: str = element(tag="TOTHOJAS")
    codfle: str = element(tag="CODFLE")
    flete: str = element(tag="FLETE")
    totbultos: str = element(tag="TOTBULTOS")
    codseg: str = element(tag="CODSEG")
    seguro: str = element(tag="SEGURO")
    totpeso: str = element(tag="TOTPESO")
    cif: str = element(tag="CIF")


class Respuesta(BaseXmlModel, nsmap=NSMAP_RESPUESTA):
    fechaceptacion: str = element(tag="FECHACEPTACION")
    numeroencriptado: str = element(tag="NUMEROENCRIPTADO")
    estado: str = element(tag="ESTADO")
    tiposeleccion: Optional[str] = element(tag="TIPOSELECCION", default=None)


class CABEZA(BaseXmlModel, nsmap=NSMAP_CABEZA):
    form: str = element(tag="FORM")
    numidentif: str = element(tag="NUMIDENTIF")
    fecvenci: str = element(tag="FECVENCI")
    adu: str = element(tag="ADU")
    agente: str = element(tag="AGENTE")
    tpodocto: str = element(tag="TPODOCTO")
    tipoingr: str = element(tag="TIPOINGR")
    numaut: str = element(tag="NUMAUT")
    fecaut: str = element(tag="FECAUT")
    gbcocen: str = element(tag="GBCOCEN")
    fectra: str = element(tag="FECTRA")
    fecacep: str = element(tag="FECACEP")
    aforo: str = element(tag="AFORO")
    fecconfdi: str = element(tag="FECCONFDI")
    numencrip: str = element(tag="NUMENCRIP")
    fecconfec: str = element(tag="FECCONFEC")
    numidenacl: str = element(tag="NUMIDENACL")
    numres: str = element(tag="NUMRES")
    fecres: str = element(tag="FECRES")
    identificacion: Identificacion = element(tag="IDENTIFICACION")
    regimensuspensivo: RegimenSuspensivo = element(tag="REGIMENSUSPENSIVO")
    origentranspalmacenaje: OrigenTranspAlmacenaje = element(tag="ORIGENTRANSPALMACENAJE")
    antecedentesfinancieros: AntecedentesFinancieros = element(tag="ANTECEDENTESFINANCIEROS")
    totales: Totales = element(tag="TOTALES")
    respuesta: Respuesta = element(tag="RESPUESTA")
