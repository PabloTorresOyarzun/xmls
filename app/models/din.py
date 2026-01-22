from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any, Union


class LogModel(BaseModel):
    secuencia: str = Field(default="1", alias="SECUENCIA")
    aduana: str = Field(..., alias="ADUANA")
    sobre: str = Field(..., alias="SOBRE")
    fecha: str = Field(..., alias="FECHA")
    hora: str = Field(..., alias="HORA")
    van: str = Field(default="VANADU", alias="VAN")
    origen: Optional[str] = Field(default="", alias="ORIGEN")
    destino: Optional[str] = Field(default="ADUAN", alias="DESTINO")

    class Config:
        populate_by_name = True


class IdentificacionModel(BaseModel):
    nombre: str = Field(..., alias="NOMBRE")
    direc: str = Field(..., alias="DIREC")
    codcomun: str = Field(..., alias="CODCOMUN")
    tiprut: str = Field(..., alias="TIPRUT")
    rut: str = Field(..., alias="RUT")
    dvrut: str = Field(..., alias="DVRUT")
    nomrepleg: str = Field(default="", alias="NOMREPLEG")
    numrutrl: str = Field(default="", alias="NUMRUTRL")
    digverrl: str = Field(default="", alias="DIGVERRL")
    nomconsig: str = Field(default="", alias="NOMCONSIG")
    desdircon: str = Field(default="", alias="DESDIRCON")
    codpaiscon: str = Field(default="", alias="CODPAISCON")

    class Config:
        populate_by_name = True


class RegimenSuspensivoModel(BaseModel):
    desdiralm: str = Field(default="", alias="DESDIRALM")
    codcomrs: str = Field(default="00000", alias="CODCOMRS")
    aductrol: str = Field(default="00", alias="ADUCTROL")
    numplazo: str = Field(default="00000000", alias="NUMPLAZO")
    indparcial: str = Field(default="0", alias="INDPARCIAL")
    numhojins: str = Field(default="000", alias="NUMHOJINS")
    totinsum: str = Field(default="0000000.0000", alias="TOTINSUM")
    codalma: str = Field(default="000", alias="CODALMA")
    numrs: str = Field(default="0000000000", alias="NUMRS")
    fecrs: str = Field(default="", alias="FECRS")
    aduars: str = Field(default="00", alias="ADUARS")
    numhojane: str = Field(default="000", alias="NUMHOJANE")
    numsec: str = Field(default="00000", alias="NUMSEC")

    class Config:
        populate_by_name = True


class OrigenTranspAlmacenajeModel(BaseModel):
    paorig: str = Field(..., alias="PAORIG")
    gpaorig: str = Field(..., alias="GPAORIG")
    paadq: str = Field(..., alias="PAADQ")
    gpaadq: str = Field(..., alias="GPAADQ")
    viatran: str = Field(..., alias="VIATRAN")
    despuert: str = Field(default="", alias="DESPUERT")
    transb: str = Field(default="", alias="TRANSB")
    ptoemb: str = Field(..., alias="PTOEMB")
    gptodesem: str = Field(..., alias="GPTODESEM")
    ptodesem: str = Field(..., alias="PTODESEM")
    tpocarga: str = Field(..., alias="TPOCARGA")
    desalmac: str = Field(default="", alias="DESALMAC")
    almacen: str = Field(default="", alias="ALMACEN")
    fecalmac: str = Field(default="", alias="FECALMAC")
    fecretiro: str = Field(default="", alias="FECRETIRO")
    gnomciat: str = Field(..., alias="GNOMCIAT")
    codpaiscia: str = Field(..., alias="CODPAISCIA")
    numrutcia: str = Field(..., alias="NUMRUTCIA")
    digvercia: str = Field(..., alias="DIGVERCIA")
    nummanif: str = Field(..., alias="NUMMANIF")
    nummanif1: str = Field(default="", alias="NUMMANIF1")
    nummanif2: str = Field(default="", alias="NUMMANIF2")
    fecmanif: str = Field(default="", alias="FECMANIF")
    numconoc: str = Field(..., alias="NUMCONOC")
    fecconoc: str = Field(..., alias="FECCONOC")
    nomemisor: str = Field(..., alias="NOMEMISOR")
    numrutemi: str = Field(..., alias="NUMRUTEMI")
    digveremi: str = Field(..., alias="DIGVEREMI")

    class Config:
        populate_by_name = True


class AntecedentesFinancierosModel(BaseModel):
    gregimp: str = Field(..., alias="GREGIMP")
    regimp: str = Field(..., alias="REGIMP")
    bcocom: str = Field(default="00", alias="BCOCOM")
    codordiv: str = Field(default="0", alias="CODORDIV")
    formpago: str = Field(..., alias="FORMPAGO")
    numdias: str = Field(..., alias="NUMDIAS")
    valexfab: str = Field(..., alias="VALEXFAB")
    moneda: str = Field(..., alias="MONEDA")
    mongasfob: str = Field(..., alias="MONGASFOB")
    clcompra: str = Field(..., alias="CLCOMPRA")
    pagograv: str = Field(..., alias="PAGOGRAV")

    class Config:
        populate_by_name = True


class TotalesModel(BaseModel):
    totitems: str = Field(..., alias="TOTITEMS")
    fob: str = Field(..., alias="FOB")
    tothojas: str = Field(..., alias="TOTHOJAS")
    codfle: str = Field(default="0", alias="CODFLE")
    flete: str = Field(..., alias="FLETE")
    totbultos: str = Field(..., alias="TOTBULTOS")
    codseg: str = Field(default="0", alias="CODSEG")
    seguro: str = Field(..., alias="SEGURO")
    totpeso: str = Field(..., alias="TOTPESO")
    cif: str = Field(..., alias="CIF")

    class Config:
        populate_by_name = True


class RespuestaModel(BaseModel):
    fechaceptacion: str = Field(default="", alias="FECHACEPTACION")
    numeroencriptado: str = Field(default="", alias="NUMEROENCRIPTADO")
    estado: str = Field(default="", alias="ESTADO")
    tiposeleccion: Optional[str] = Field(default="", alias="TIPOSELECCION")

    class Config:
        populate_by_name = True


class CabezaModel(BaseModel):
    form: str = Field(..., alias="FORM")
    numidentif: str = Field(..., alias="NUMIDENTIF")
    fecvenci: str = Field(..., alias="FECVENCI")
    adu: str = Field(..., alias="ADU")
    agente: str = Field(..., alias="AGENTE")
    tpodocto: str = Field(..., alias="TPODOCTO")
    tipoingr: str = Field(..., alias="TIPOINGR")
    numaut: str = Field(default="999", alias="NUMAUT")
    fecaut: str = Field(default="", alias="FECAUT")
    gbcocen: str = Field(default="", alias="GBCOCEN")
    fectra: str = Field(..., alias="FECTRA")
    fecacep: str = Field(default="", alias="FECACEP")
    aforo: str = Field(default="00", alias="AFORO")
    fecconfdi: str = Field(..., alias="FECCONFDI")
    numencrip: str = Field(default="", alias="NUMENCRIP")
    fecconfec: str = Field(..., alias="FECCONFEC")
    numidenacl: str = Field(default="", alias="NUMIDENACL")
    numres: str = Field(default="00000000", alias="NUMRES")
    fecres: str = Field(default="00000000", alias="FECRES")
    identificacion: IdentificacionModel = Field(..., alias="IDENTIFICACION")
    regimensuspensivo: Optional[RegimenSuspensivoModel] = Field(
        default=None, alias="REGIMENSUSPENSIVO"
    )
    origentranspalmacenaje: OrigenTranspAlmacenajeModel = Field(
        ..., alias="ORIGENTRANSPALMACENAJE"
    )
    antecedentesfinancieros: AntecedentesFinancierosModel = Field(
        ..., alias="ANTECEDENTESFINANCIEROS"
    )
    totales: TotalesModel = Field(..., alias="TOTALES")
    respuesta: Optional[RespuestaModel] = Field(default=None, alias="RESPUESTA")

    class Config:
        populate_by_name = True

    @field_validator("regimensuspensivo", mode="before")
    @classmethod
    def parse_regimensuspensivo(cls, v):
        if v is None or v == "":
            return RegimenSuspensivoModel()
        return v

    @field_validator("respuesta", mode="before")
    @classmethod
    def parse_respuesta(cls, v):
        if v is None or v == "":
            return RespuestaModel()
        return v


class ObservacionItemModel(BaseModel):
    codobs: str = Field(..., alias="CODOBS")
    desobs: str = Field(..., alias="DESOBS")

    class Config:
        populate_by_name = True


class CuentaItemModel(BaseModel):
    otro: str = Field(..., alias="OTRO")
    cta: str = Field(..., alias="CTA")
    sigval: str = Field(..., alias="SIGVAL")
    valor: str = Field(..., alias="VALOR")

    class Config:
        populate_by_name = True


class InsumoModel(BaseModel):
    numitem: str = Field(..., alias="NUMITEM")
    numinsumo: str = Field(..., alias="NUMINSUMO")
    desinsumo: str = Field(..., alias="DESINSUMO")
    caninsumo: str = Field(..., alias="CANINSUMO")
    codmedida: str = Field(..., alias="CODMEDIDA")
    cifinsumo: str = Field(..., alias="CIFINSUMO")

    class Config:
        populate_by_name = True


class AnexaModel(BaseModel):
    numsec: str = Field(..., alias="NUMSEC")
    numdapex: str = Field(..., alias="NUMDAPEX")
    fecdapex: str = Field(..., alias="FECDAPEX")
    codaduana: str = Field(..., alias="CODADUANA")
    numitem: str = Field(..., alias="NUMITEM")
    numinsumo: str = Field(..., alias="NUMINSUMO")
    nominsumo: str = Field(..., alias="NOMINSUMO")
    codunmedi: str = Field(..., alias="CODUNMEDI")
    numitemdec: str = Field(..., alias="NUMITEMDEC")
    nomproducto: str = Field(..., alias="NOMPRODUCTO")
    canproducto: str = Field(..., alias="CANPRODUCTO")
    codunmedp: str = Field(..., alias="CODUNMEDP")
    facconsumo: str = Field(..., alias="FACCONSUMO")
    numinsuti: str = Field(..., alias="NUMINSUTI")

    class Config:
        populate_by_name = True


def extract_list(v: Any, key: str) -> list:
    """Extrae lista de un dict con clave anidada o retorna lista directa."""
    if v is None:
        return []
    if isinstance(v, list):
        return v
    if isinstance(v, dict):
        if key in v:
            inner = v[key]
            if isinstance(inner, list):
                return inner
            elif isinstance(inner, dict):
                return [inner]
        return []
    return []


class ItemModel(BaseModel):
    numitem: str = Field(..., alias="NUMITEM")
    dnombre: str = Field(..., alias="DNOMBRE")
    dmarca: str = Field(default="", alias="DMARCA")
    dvariedad: str = Field(default="", alias="DVARIEDAD")
    dotro1: str = Field(default="", alias="DOTRO1")
    dotro2: str = Field(default="", alias="DOTRO2")
    atr5: str = Field(default="", alias="ATR5")
    atr6: str = Field(default="", alias="ATR6")
    sajuitem: str = Field(default="", alias="SAJUITEM")
    ajuitem: str = Field(default="0000000000.00", alias="AJUITEM")
    cantmerc: str = Field(..., alias="CANTMERC")
    medida: str = Field(..., alias="MEDIDA")
    codestum: str = Field(default="", alias="CODESTUM")
    preunit: str = Field(..., alias="PREUNIT")
    arancala: str = Field(..., alias="ARANCALA")
    numcor: str = Field(default="0", alias="NUMCOR")
    numacu: str = Field(default="", alias="NUMACU")
    concupo: str = Field(default="0", alias="CONCUPO")
    arancnac: str = Field(..., alias="ARANCNAC")
    cifitem: str = Field(..., alias="CIFITEM")
    advalala: str = Field(default="0000.00", alias="ADVALALA")
    adval: str = Field(..., alias="ADVAL")
    valad: str = Field(default="0000000000.00", alias="VALAD")
    observacionesitem: list[ObservacionItemModel] = Field(
        default_factory=list, alias="OBSERVACIONESITEM"
    )
    cuentasitem: list[CuentaItemModel] = Field(
        default_factory=list, alias="CUENTASITEM"
    )
    insumos: list[InsumoModel] = Field(default_factory=list, alias="INSUMOS")
    anexas: list[AnexaModel] = Field(default_factory=list, alias="ANEXAS")

    class Config:
        populate_by_name = True

    @field_validator("observacionesitem", mode="before")
    @classmethod
    def parse_observacionesitem(cls, v):
        return extract_list(v, "OBSERVACIONITEM")

    @field_validator("cuentasitem", mode="before")
    @classmethod
    def parse_cuentasitem(cls, v):
        return extract_list(v, "CUENTAITEM")

    @field_validator("insumos", mode="before")
    @classmethod
    def parse_insumos(cls, v):
        return extract_list(v, "INSUMO")

    @field_validator("anexas", mode="before")
    @classmethod
    def parse_anexas(cls, v):
        return extract_list(v, "ANEXA")


class VistoBuenoModel(BaseModel):
    nuregr: str = Field(default="000000", alias="NUREGR")
    anoreg: str = Field(default="0000", alias="ANOREG")
    codvisbuen: str = Field(default="0", alias="CODVISBUEN")
    numregla: str = Field(default="0000000000000", alias="NUMREGLA")
    numanores: str = Field(default="0000", alias="NUMANORES")
    codultvb: str = Field(default="000", alias="CODULTVB")

    class Config:
        populate_by_name = True


class BultoModel(BaseModel):
    destipbul: str = Field(..., alias="DESTIPBUL")
    tpobul: str = Field(..., alias="TPOBUL")
    cantbul: str = Field(..., alias="CANTBUL")

    class Config:
        populate_by_name = True


class BultosModel(BaseModel):
    idbultos: str = Field(..., alias="IDBULTOS")
    bultos: list[BultoModel] = Field(default_factory=list, alias="BULTO")

    class Config:
        populate_by_name = True

    @field_validator("bultos", mode="before")
    @classmethod
    def parse_bultos(cls, v):
        return extract_list(v, "BULTO") if isinstance(v, dict) else (v if isinstance(v, list) else [])


class CuentaGiroModel(BaseModel):
    ctaotro: str = Field(..., alias="CTAOTRO")
    monotro: str = Field(..., alias="MONOTRO")

    class Config:
        populate_by_name = True


class CuentasYValoresModel(BaseModel):
    mon178: str = Field(default="0000000000.00", alias="MON178")
    mon191: str = Field(default="0000000000.00", alias="MON191")
    mon699: str = Field(default="0000000000.00", alias="MON699")
    mon199: str = Field(default="0000000000.00", alias="MON199")
    cuentasgiro: list[CuentaGiroModel] = Field(
        default_factory=list, alias="CUENTASGIRO"
    )

    class Config:
        populate_by_name = True

    @field_validator("cuentasgiro", mode="before")
    @classmethod
    def parse_cuentasgiro(cls, v):
        return extract_list(v, "CUENTAGIRO")


class FechaVencCuotaModel(BaseModel):
    fecha: str = Field(..., alias="FECHA")
    codfecha: str = Field(..., alias="CODFECHA")

    class Config:
        populate_by_name = True


class MontoCuotaModel(BaseModel):
    valor: str = Field(..., alias="VALOR")
    codvalor: str = Field(..., alias="CODVALOR")

    class Config:
        populate_by_name = True


class CuotaModel(BaseModel):
    fechavenccuota: list[FechaVencCuotaModel] = Field(..., alias="FECHAVENCCUOTA")
    montocuota: list[MontoCuotaModel] = Field(..., alias="MONTOCUOTA")

    class Config:
        populate_by_name = True


class PagoDiferidoModel(BaseModel):
    tasa: str = Field(..., alias="TASA")
    ncuotas: str = Field(..., alias="NCUOTAS")
    adudi: str = Field(..., alias="ADUDI")
    numdi: str = Field(..., alias="NUMDI")
    fecdi: str = Field(..., alias="FECDI")
    cuotas: list[CuotaModel] = Field(default_factory=list, alias="CUOTAS")

    class Config:
        populate_by_name = True


class ErrorModel(BaseModel):
    codigo: str = Field(..., alias="CODIGO")
    glosa: str = Field(..., alias="GLOSA")

    class Config:
        populate_by_name = True


class ErroresModel(BaseModel):
    fechaproceso: str = Field(default="", alias="FECHAPROCESO")
    errores: list[ErrorModel] = Field(default_factory=list, alias="ERROR")

    class Config:
        populate_by_name = True

    @field_validator("errores", mode="before")
    @classmethod
    def parse_errores(cls, v):
        return extract_list(v, "ERROR") if isinstance(v, dict) else (v if isinstance(v, list) else [])


class DINModel(BaseModel):
    tipoenvio: str = Field(default="DIN", alias="TIPOENVIO")
    log: LogModel = Field(..., alias="LOG")
    cabeza: CabezaModel = Field(..., alias="CABEZA")
    items: list[ItemModel] = Field(..., alias="ITEMS")
    vistosbuenos: list[VistoBuenoModel] = Field(
        default_factory=list, alias="VISTOSBUENOS"
    )
    bultos: BultosModel = Field(..., alias="BULTOS")
    cuentasyvalores: CuentasYValoresModel = Field(..., alias="CUENTASYVALORES")
    pagodiferido: Optional[PagoDiferidoModel] = Field(default=None, alias="PAGODIFERIDO")
    anexasdin: list[AnexaModel] = Field(default_factory=list, alias="ANEXASDIN")
    errores: Optional[ErroresModel] = Field(default=None, alias="ERRORES")

    class Config:
        populate_by_name = True

    @field_validator("items", mode="before")
    @classmethod
    def parse_items(cls, v):
        return extract_list(v, "ITEM")

    @field_validator("vistosbuenos", mode="before")
    @classmethod
    def parse_vistosbuenos(cls, v):
        return extract_list(v, "VISTOBUENO")

    @field_validator("anexasdin", mode="before")
    @classmethod
    def parse_anexasdin(cls, v):
        return extract_list(v, "ANEXA")

    @field_validator("errores", mode="before")
    @classmethod
    def parse_errores(cls, v):
        if v is None or v == "":
            return ErroresModel()
        return v


class DINRequest(BaseModel):
    din: DINModel = Field(..., alias="DIN")

    class Config:
        populate_by_name = True


class DINResponse(BaseModel):
    success: bool
    ticket: Optional[str] = None
    message: str
    xml: Optional[str] = None
    raw_response: Optional[str] = None


class StatusResponse(BaseModel):
    success: bool
    status: Optional[str] = None
    message: str
    details: Optional[dict] = None
