from typing import List, Optional
from pydantic_xml import BaseXmlModel, element

# --- CONSTANTES DE NAMESPACES ---
NS_ENVIO = "http://www.aduana.cl/xml/esquemas/EnvioDin"
NS_LOG = "http://www.aduana.cl/xml/esquemas/LOG"
NS_CABEZA = "http://www.aduana.cl/xml/esquemas/CABEZA"
NS_ITEMS = "http://www.aduana.cl/xml/esquemas/ITEMS"
NS_VISTOSBUENOS = "http://www.aduana.cl/xml/esquemas/VISTOSBUENOS"
NS_BULTOS = "http://www.aduana.cl/xml/esquemas/BULTOS"
NS_CUENTASYVALORES = "http://www.aduana.cl/xml/esquemas/CUENTASYVALORES"
NS_PAGODIFERIDO = "http://www.aduana.cl/xml/esquemas/PAGODIFERIDO"
NS_ERRORES = "http://www.aduana.cl/xml/esquemas/ERRORES"
NS_ANEXASDIN = "http://www.aduana.cl/xml/esquemas/ANEXASDIN"
NS_INSUMO = "http://www.aduana.cl/xml/esquemas/INSUMO"
NS_DSIG = "http://www.w3.org/2000/09/xmldsig#"

# --- CLASES ---

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

class ANEXAS(BaseXmlModel, ns=NS_ITEMS):
    anexa: List['ANEXA'] = element(tag='ANEXA', default_factory=list)

class ANEXASDIN(BaseXmlModel, ns=NS_ANEXASDIN):
    anexa: List['ANEXA'] = element(tag='ANEXA', default_factory=list)

class ANTECEDENTESFINANCIEROS(BaseXmlModel, ns=NS_CABEZA):
    gregimp: str = element(tag='GREGIMP', default=...)
    regimp: str = element(tag='REGIMP', default=...)
    bcocom: str = element(tag='BCOCOM', default=...)
    codordiv: str = element(tag='CODORDIV', default=...)
    formpago: str = element(tag='FORMPAGO', default=...)
    numdias: str = element(tag='NUMDIAS', default=...)
    valexfab: str = element(tag='VALEXFAB', default=...)
    moneda: str = element(tag='MONEDA', default=...)
    mongasfob: str = element(tag='MONGASFOB', default=...)
    clcompra: str = element(tag='CLCOMPRA', default=...)
    pagograv: str = element(tag='PAGOGRAV', default=...)

class BULTO(BaseXmlModel, ns=NS_BULTOS):
    destipbul: str = element(tag='DESTIPBUL', default=...)
    tpobul: str = element(tag='TPOBUL', default=...)
    cantbul: str = element(tag='CANTBUL', default=...)

class BULTOS(BaseXmlModel, ns=NS_BULTOS):
    idbultos: str = element(tag='IDBULTOS', default=...)
    bulto: List['BULTO'] = element(tag='BULTO', default_factory=list)

class IDENTIFICACION(BaseXmlModel, ns=NS_CABEZA):
    nombre: str = element(tag='NOMBRE', default=...)
    direc: str = element(tag='DIREC', default=...)
    codcomun: str = element(tag='CODCOMUN', default=...)
    tiprut: str = element(tag='TIPRUT', default=...)
    rut: str = element(tag='RUT', default=...)
    dvrut: str = element(tag='DVRUT', default=...)
    nomrepleg: str = element(tag='NOMREPLEG', default=...)
    numrutrl: str = element(tag='NUMRUTRL', default=...)
    digverrl: str = element(tag='DIGVERRL', default=...)
    nomconsig: str = element(tag='NOMCONSIG', default=...)
    desdircon: str = element(tag='DESDIRCON', default=...)
    codpaiscon: str = element(tag='CODPAISCON', default=...)

class REGIMENSUSPENSIVO(BaseXmlModel, ns=NS_CABEZA):
    desdiralm: str = element(tag='DESDIRALM', default=...)
    codcomrs: str = element(tag='CODCOMRS', default=...)
    aductrol: str = element(tag='ADUCTROL', default=...)
    numplazo: str = element(tag='NUMPLAZO', default=...)
    indparcial: str = element(tag='INDPARCIAL', default=...)
    numhojins: str = element(tag='NUMHOJINS', default=...)
    totinsum: str = element(tag='TOTINSUM', default=...)
    codalma: str = element(tag='CODALMA', default=...)
    numrs: str = element(tag='NUMRS', default=...)
    fecrs: str = element(tag='FECRS', default=...)
    aduars: str = element(tag='ADUARS', default=...)
    numhojane: str = element(tag='NUMHOJANE', default=...)
    numsec: str = element(tag='NUMSEC', default=...)

class ORIGENTRANSPALMACENAJE(BaseXmlModel, ns=NS_CABEZA):
    paorig: str = element(tag='PAORIG', default=...)
    gpaorig: str = element(tag='GPAORIG', default=...)
    paadq: str = element(tag='PAADQ', default=...)
    gpaadq: str = element(tag='GPAADQ', default=...)
    viatran: str = element(tag='VIATRAN', default=...)
    despuert: str = element(tag='DESPUERT', default=...)
    transb: str = element(tag='TRANSB', default=...)
    ptoemb: str = element(tag='PTOEMB', default=...)
    gptodesem: str = element(tag='GPTODESEM', default=...)
    ptodesem: str = element(tag='PTODESEM', default=...)
    tpocarga: str = element(tag='TPOCARGA', default=...)
    desalmac: str = element(tag='DESALMAC', default=...)
    almacen: str = element(tag='ALMACEN', default=...)
    fecalmac: str = element(tag='FECALMAC', default=...)
    fecretiro: str = element(tag='FECRETIRO', default=...)
    gnomciat: str = element(tag='GNOMCIAT', default=...)
    codpaiscia: str = element(tag='CODPAISCIA', default=...)
    numrutcia: str = element(tag='NUMRUTCIA', default=...)
    digvercia: str = element(tag='DIGVERCIA', default=...)
    nummanif: str = element(tag='NUMMANIF', default=...)
    nummanif1: str = element(tag='NUMMANIF1', default=...)
    nummanif2: str = element(tag='NUMMANIF2', default=...)
    fecmanif: str = element(tag='FECMANIF', default=...)
    numconoc: str = element(tag='NUMCONOC', default=...)
    fecconoc: str = element(tag='FECCONOC', default=...)
    nomemisor: str = element(tag='NOMEMISOR', default=...)
    numrutemi: str = element(tag='NUMRUTEMI', default=...)
    digveremi: str = element(tag='DIGVEREMI', default=...)

class TOTALES(BaseXmlModel, ns=NS_CABEZA):
    totitems: str = element(tag='TOTITEMS', default=...)
    fob: str = element(tag='FOB', default=...)
    tothojas: str = element(tag='TOTHOJAS', default=...)
    codfle: str = element(tag='CODFLE', default=...)
    flete: str = element(tag='FLETE', default=...)
    totbultos: str = element(tag='TOTBULTOS', default=...)
    codseg: str = element(tag='CODSEG', default=...)
    seguro: str = element(tag='SEGURO', default=...)
    totpeso: str = element(tag='TOTPESO', default=...)
    cif: str = element(tag='CIF', default=...)

class CABEZA(BaseXmlModel, ns=NS_CABEZA):
    form: str = element(tag='FORM', default=...)
    numidentif: str = element(tag='NUMIDENTIF', default=...)
    fecvenci: str = element(tag='FECVENCI', default=...)
    adu: str = element(tag='ADU', default=...)
    agente: str = element(tag='AGENTE', default=...)
    tpodocto: str = element(tag='TPODOCTO', default=...)
    tipoingr: str = element(tag='TIPOINGR', default=...)
    numaut: str = element(tag='NUMAUT', default=...)
    fecaut: str = element(tag='FECAUT', default=...)
    gbcocen: str = element(tag='GBCOCEN', default=...)
    fectra: str = element(tag='FECTRA', default=...)
    fecacep: str = element(tag='FECACEP', default=...)
    aforo: str = element(tag='AFORO', default=...)
    fecconfdi: str = element(tag='FECCONFDI', default=...)
    numencrip: str = element(tag='NUMENCRIP', default=...)
    fecconfec: str = element(tag='FECCONFEC', default=...)
    numidenacl: str = element(tag='NUMIDENACL', default=...)
    numres: str = element(tag='NUMRES', default=...)
    fecres: str = element(tag='FECRES', default=...)
    identificacion: List['IDENTIFICACION'] = element(tag='IDENTIFICACION', default_factory=list)
    regimensuspensivo: List['REGIMENSUSPENSIVO'] = element(tag='REGIMENSUSPENSIVO', default_factory=list)
    origentranspalmacenaje: List['ORIGENTRANSPALMACENAJE'] = element(tag='ORIGENTRANSPALMACENAJE', default_factory=list)
    antecedentesfinancieros: List['ANTECEDENTESFINANCIEROS'] = element(tag='ANTECEDENTESFINANCIEROS', default_factory=list)
    totales: List['TOTALES'] = element(tag='TOTALES', default_factory=list)

class CUENTAGIRO(BaseXmlModel, ns=NS_CUENTASYVALORES):
    ctaotro: str = element(tag='CTAOTRO', default=...)
    monotro: str = element(tag='MONOTRO', default=...)

class CUENTAITEM(BaseXmlModel, ns=NS_ITEMS):
    otro: Optional[str] = element(tag='OTRO', default=None)
    cta: Optional[str] = element(tag='CTA', default=None)
    sigval: Optional[str] = element(tag='SIGVAL', default=None)
    valor: Optional[str] = element(tag='VALOR', default=None)

class CUENTASGIRO(BaseXmlModel, ns=NS_CUENTASYVALORES):
    cuentagiro: List['CUENTAGIRO'] = element(tag='CUENTAGIRO', default_factory=list)

class CUENTASITEM(BaseXmlModel, ns=NS_ITEMS):
    cuentaitem: List['CUENTAITEM'] = element(tag='CUENTAITEM', default_factory=list)

class CUENTASYVALORES(BaseXmlModel, ns=NS_CUENTASYVALORES):
    mon178: str = element(tag='MON178', default=...)
    mon191: str = element(tag='MON191', default=...)
    mon699: str = element(tag='MON699', default=...)
    mon199: str = element(tag='MON199', default=...)
    cuentasgiro: List['CUENTASGIRO'] = element(tag='CUENTASGIRO', default_factory=list)

class FECHAVENCCUOTA(BaseXmlModel, ns=NS_PAGODIFERIDO):
    fecha: str = element(tag='FECHA', default=...)
    codfecha: str = element(tag='CODFECHA', default=...)

class MONTOCUOTA(BaseXmlModel, ns=NS_PAGODIFERIDO):
    valor: str = element(tag='VALOR', default=...)
    codvalor: str = element(tag='CODVALOR', default=...)

class CUOTA(BaseXmlModel, ns=NS_PAGODIFERIDO):
    fechavenccuota: List['FECHAVENCCUOTA'] = element(tag='FECHAVENCCUOTA', default_factory=list)
    montocuota: List['MONTOCUOTA'] = element(tag='MONTOCUOTA', default_factory=list)

class CUOTAS(BaseXmlModel, ns=NS_PAGODIFERIDO):
    cuota: List['CUOTA'] = element(tag='CUOTA', default_factory=list)

class PAGODIFERIDO(BaseXmlModel, ns=NS_PAGODIFERIDO):
    tasa: str = element(tag='TASA', default=...)
    ncuotas: str = element(tag='NCUOTAS', default=...)
    adudi: str = element(tag='ADUDI', default=...)
    numdi: str = element(tag='NUMDI', default=...)
    fecdi: str = element(tag='FECDI', default=...)
    cuotas: List['CUOTAS'] = element(tag='CUOTAS', default_factory=list)

class ERROR(BaseXmlModel, ns=NS_ERRORES):
    pass

class ERRORES(BaseXmlModel, ns=NS_ERRORES):
    fechaproceso: str = element(tag='FECHAPROCESO', default=...)
    error: List['ERROR'] = element(tag='ERROR', default_factory=list)

class INSUMO(BaseXmlModel, ns=NS_INSUMO):
    numitem: str = element(tag='NUMITEM', default=...)
    numinsumo: str = element(tag='NUMINSUMO', default=...)
    desinsumo: str = element(tag='DESINSUMO', default=...)
    caninsumo: str = element(tag='CANINSUMO', default=...)
    codmedida: str = element(tag='CODMEDIDA', default=...)
    cifinsumo: str = element(tag='CIFINSUMO', default=...)

class INSUMOS(BaseXmlModel, ns=NS_ITEMS):
    insumo: List['INSUMO'] = element(tag='INSUMO', default_factory=list)

class OBSERVACIONITEM(BaseXmlModel, ns=NS_ITEMS):
    codobs: Optional[str] = element(tag='CODOBS', default=None)
    desobs: Optional[str] = element(tag='DESOBS', default=None)

class OBSERVACIONESITEM(BaseXmlModel, ns=NS_ITEMS):
    observacionitem: List['OBSERVACIONITEM'] = element(tag='OBSERVACIONITEM', default_factory=list)

class ITEM(BaseXmlModel, ns=NS_ITEMS):
    numitem: str = element(tag='NUMITEM', default=...)
    dnombre: str = element(tag='DNOMBRE', default=...)
    dmarca: str = element(tag='DMARCA', default=...)
    dvariedad: str = element(tag='DVARIEDAD', default=...)
    dotro1: str = element(tag='DOTRO1', default=...)
    dotro2: str = element(tag='DOTRO2', default=...)
    atr5: str = element(tag='ATR5', default=...)
    atr6: str = element(tag='ATR6', default=...)
    sajuitem: str = element(tag='SAJUITEM', default=...)
    ajuitem: str = element(tag='AJUITEM', default=...)
    cantmerc: str = element(tag='CANTMERC', default=...)
    medida: str = element(tag='MEDIDA', default=...)
    codestum: str = element(tag='CODESTUM', default=...)
    preunit: str = element(tag='PREUNIT', default=...)
    arancala: str = element(tag='ARANCALA', default=...)
    numcor: str = element(tag='NUMCOR', default=...)
    numacu: str = element(tag='NUMACU', default=...)
    concupo: str = element(tag='CONCUPO', default=...)
    arancnac: str = element(tag='ARANCNAC', default=...)
    cifitem: str = element(tag='CIFITEM', default=...)
    advalala: str = element(tag='ADVALALA', default=...)
    adval: str = element(tag='ADVAL', default=...)
    valad: str = element(tag='VALAD', default=...)
    observacionesitem: List['OBSERVACIONESITEM'] = element(tag='OBSERVACIONESITEM', default_factory=list)
    cuentasitem: List['CUENTASITEM'] = element(tag='CUENTASITEM', default_factory=list)
    insumos: List['INSUMOS'] = element(tag='INSUMOS', default_factory=list)
    anexas: List['ANEXAS'] = element(tag='ANEXAS', default_factory=list)

class ITEMS(BaseXmlModel, ns=NS_ITEMS):
    item: List['ITEM'] = element(tag='ITEM', default_factory=list)

class LOG(BaseXmlModel, ns=NS_LOG):
    secuencia: str = element(tag='SECUENCIA', default=...)
    aduana: str = element(tag='ADUANA', default=...)
    sobre: str = element(tag='SOBRE', default=...)
    fecha: str = element(tag='FECHA', default=...)
    hora: str = element(tag='HORA', default=...)
    van: str = element(tag='VAN', default=...)
    origen: Optional[str] = element(tag='ORIGEN', default=None)
    destino: Optional[str] = element(tag='DESTINO', default=None)

class ObjectType(BaseXmlModel, ns=NS_LOG):
    pass

class VISTOBUENO(BaseXmlModel, ns=NS_VISTOSBUENOS):
    nuregr: str = element(tag='NUREGR', default=...)
    anoreg: str = element(tag='ANOREG', default=...)
    codvisbuen: str = element(tag='CODVISBUEN', default=...)
    numregla: str = element(tag='NUMREGLA', default=...)
    numanores: str = element(tag='NUMANORES', default=...)
    codultvb: str = element(tag='CODULTVB', default=...)

class VISTOSBUENOS(BaseXmlModel, ns=NS_VISTOSBUENOS):
    vistobueno: List['VISTOBUENO'] = element(tag='VISTOBUENO', default_factory=list)

class SignedInfoType(BaseXmlModel, ns=NS_DSIG):
    pass

class SignatureValueType(BaseXmlModel, ns=NS_DSIG):
    pass

class KeyInfoType(BaseXmlModel, ns=NS_DSIG):
    pass

class SignatureType(BaseXmlModel, ns=NS_DSIG):
    signedInfo: 'SignedInfoType' = element(tag='SignedInfo', default=...)
    signatureValue: 'SignatureValueType' = element(tag='SignatureValue', default=...)
    keyInfo: Optional['KeyInfoType'] = element(tag='KeyInfo', default=None)
    object: List['ObjectType'] = element(tag='Object', default_factory=list)

class EnvioDin(BaseXmlModel, 
               tag='DIN', 
               ns=NS_ENVIO,
               nsmap={
                   'tns': NS_ENVIO,
                   'pref': NS_LOG,
                   'pref1': NS_CABEZA,
                   'pref2': NS_ITEMS,
                   'pref3': NS_VISTOSBUENOS,
                   'pref4': NS_BULTOS,
                   'pref5': NS_CUENTASYVALORES,
                   'pref6': NS_PAGODIFERIDO,
                   'pref7': NS_ERRORES,
                   'pref8': NS_INSUMO,
                   'pref10': NS_ANEXASDIN,
                   'pref11': NS_DSIG
               }):
    tipoenvio: str = element(tag='TIPOENVIO', default=...)
    log: List['LOG'] = element(tag='LOG', default_factory=list)
    cabeza: List['CABEZA'] = element(tag='CABEZA', default_factory=list)
    items: 'ITEMS' = element(tag='ITEMS', default=...)
    vistosbuenos: 'VISTOSBUENOS' = element(tag='VISTOSBUENOS', default=...)
    bultos: List['BULTOS'] = element(tag='BULTOS', default_factory=list)
    cuentasyvalores: List['CUENTASYVALORES'] = element(tag='CUENTASYVALORES', default_factory=list)
    pagodiferido: List['PAGODIFERIDO'] = element(tag='PAGODIFERIDO', default_factory=list)
    anexasdin: Optional['ANEXASDIN'] = element(tag='ANEXASDIN', default=None)
    errores: List['ERRORES'] = element(tag='ERRORES', default_factory=list)
    signature: 'SignatureType' = element(tag='Signature', default=...)


# Rebuild de modelos para referencias
EnvioDin.model_rebuild()
ITEMS.model_rebuild()
SignatureType.model_rebuild()
ANEXAS.model_rebuild()
ANEXASDIN.model_rebuild()
ANTECEDENTESFINANCIEROS.model_rebuild()
BULTO.model_rebuild()
BULTOS.model_rebuild()
CABEZA.model_rebuild()
CUENTAGIRO.model_rebuild()
CUENTAITEM.model_rebuild()
CUENTASGIRO.model_rebuild()
CUENTASITEM.model_rebuild()
CUENTASYVALORES.model_rebuild()
CUOTA.model_rebuild()
CUOTAS.model_rebuild()
ERRORES.model_rebuild()
FECHAVENCCUOTA.model_rebuild()
IDENTIFICACION.model_rebuild()
INSUMOS.model_rebuild()
ITEM.model_rebuild()
MONTOCUOTA.model_rebuild()
OBSERVACIONESITEM.model_rebuild()
ORIGENTRANSPALMACENAJE.model_rebuild()
PAGODIFERIDO.model_rebuild()
REGIMENSUSPENSIVO.model_rebuild()
TOTALES.model_rebuild()
VISTOSBUENOS.model_rebuild()