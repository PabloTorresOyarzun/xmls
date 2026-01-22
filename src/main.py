from typing import Any
from litestar import Litestar, get, post, MediaType
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Contact
from pydantic import BaseModel, Field

from .models import DIN
from .services import DINService


class XMLRequest(BaseModel):
    """Request body for XML validation and parsing endpoints."""
    xml_content: str = Field(
        description="Contenido XML a procesar. Pega aqui tu documento XML completo.",
        examples=['<?xml version="1.0"?><test>Hello World</test>']
    )


class ValidationResponse(BaseModel):
    """Response from validation endpoints."""
    is_valid: bool
    errors: list[str]


class ParseResponse(BaseModel):
    """Response from parse endpoint."""
    success: bool
    data: dict[str, Any] | None = None
    error: str | None = None


class DINRequest(BaseModel):
    """Request body for generating DIN XML."""
    tipoenvio: str = Field(default="01", description="Tipo de envio")
    # LOG
    secuencia: str = Field(default="000001", description="Numero de secuencia")
    aduana: str = Field(default="901", description="Codigo de aduana")
    sobre: str = Field(default="001", description="Numero de sobre")
    # CABEZA
    form: str = Field(default="15", description="Codigo de formulario")
    numidentif: str = Field(default="", description="Numero de identificacion")
    adu: str = Field(default="901", description="Codigo de aduana destino")
    agente: str = Field(default="0001", description="Codigo de agente")
    tpodocto: str = Field(default="15", description="Tipo de documento")
    tipoingr: str = Field(default="1", description="Tipo de ingreso")
    # IDENTIFICACION
    nombre: str = Field(default="", description="Nombre del importador")
    direc: str = Field(default="", description="Direccion del importador")
    codcomun: str = Field(default="13101", description="Codigo de comuna")
    rut: str = Field(default="", description="RUT sin digito verificador")
    dvrut: str = Field(default="", description="Digito verificador del RUT")
    # TOTALES
    totitems: str = Field(default="1", description="Total de items")
    fob: str = Field(default="0.00", description="Valor FOB")
    flete: str = Field(default="0.00", description="Valor del flete")
    seguro: str = Field(default="0.00", description="Valor del seguro")
    cif: str = Field(default="0.00", description="Valor CIF")


class HealthResponse(BaseModel):
    status: str
    service: str


# Initialize service
din_service = DINService()


@get("/", media_type=MediaType.JSON)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy", service="DIN XML API")


@get("/sample", media_type=MediaType.TEXT)
async def get_sample_din() -> str:
    """
    Obtener un documento DIN XML de ejemplo.

    Retorna un XML DIN completo que puede usarse como plantilla.
    """
    sample_din = din_service.create_sample_din()
    return din_service.to_xml(sample_din)


@get("/sample/json", media_type=MediaType.JSON)
async def get_sample_din_json() -> dict[str, Any]:
    """
    Obtener el DIN de ejemplo como JSON.

    Retorna la estructura del DIN en formato JSON para facilitar su inspeccion.
    """
    sample_din = din_service.create_sample_din()
    return sample_din.model_dump()


# ============================================================================
# VALIDATE ENDPOINTS
# ============================================================================

@post("/validate", media_type=MediaType.JSON)
async def validate_din_xml(data: XMLRequest) -> ValidationResponse:
    """
    Validar un documento DIN XML contra el esquema XSD.

    Pega el contenido XML en el campo `xml_content` y ejecuta para validar.
    """
    if not data.xml_content or not data.xml_content.strip():
        return ValidationResponse(is_valid=False, errors=["El contenido XML esta vacio."])

    is_valid, errors = din_service.validate_din(data.xml_content)
    return ValidationResponse(is_valid=is_valid, errors=errors)


@post("/validate/structure", media_type=MediaType.JSON)
async def validate_structure_xml(data: XMLRequest) -> ValidationResponse:
    """
    Validar solo la estructura del XML (que este bien formado).

    NO valida contra el esquema XSD, solo verifica que el XML sea valido sintacticamente.
    Pega el contenido XML en el campo `xml_content` y ejecuta para validar.
    """
    if not data.xml_content or not data.xml_content.strip():
        return ValidationResponse(is_valid=False, errors=["El contenido XML esta vacio."])

    is_valid, errors = din_service.validator.validate_structure(data.xml_content)
    return ValidationResponse(is_valid=is_valid, errors=errors)


@post("/parse", media_type=MediaType.JSON)
async def parse_din_xml(data: XMLRequest) -> ParseResponse:
    """
    Parsear un documento DIN XML a formato JSON.

    Convierte el XML a una estructura JSON para facilitar su inspeccion.
    Pega el contenido XML en el campo `xml_content` y ejecuta.
    """
    if not data.xml_content or not data.xml_content.strip():
        return ParseResponse(success=False, error="El contenido XML esta vacio.")

    try:
        din = din_service.from_xml(data.xml_content)
        return ParseResponse(success=True, data=din.model_dump())
    except Exception as e:
        return ParseResponse(success=False, error=str(e))


# ============================================================================
# GENERATE ENDPOINT
# ============================================================================

@post("/generate", media_type=MediaType.TEXT)
async def generate_din_xml(data: DINRequest) -> str:
    """
    Generar un documento DIN XML a partir de datos JSON.

    Completa los campos que desees y ejecuta para generar el XML.
    Los campos no especificados usaran valores por defecto.
    """
    from datetime import datetime
    from .models.cabeza import (
        Identificacion,
        RegimenSuspensivo,
        OrigenTranspAlmacenaje,
        AntecedentesFinancieros,
        Totales,
        Respuesta,
    )
    from .models.items import ObservacionesItem, ObservacionItem, CuentasItem, CuentaItem, Insumos, Anexas
    from .models.cuentasyvalores import CuentasGiro
    from .models import LOG, CABEZA, ITEMS, ITEM, VISTOSBUENOS, BULTOS, CUENTASYVALORES, ERRORES, Error

    now = datetime.now()

    log = LOG(
        secuencia=data.secuencia,
        aduana=data.aduana,
        sobre=data.sobre,
        fecha=now.strftime("%Y%m%d"),
        hora=now.strftime("%H%M%S"),
        van="1",
        origen="AGENTE",
        destino="ADUANA",
    )

    identificacion = Identificacion(
        nombre=data.nombre or "IMPORTADORA EJEMPLO S.A.",
        direc=data.direc or "AV. EJEMPLO 1234",
        codcomun=data.codcomun,
        tiprut="1",
        rut=data.rut or "76123456",
        dvrut=data.dvrut or "7",
        nomrepleg="",
        numrutrl="",
        digverrl="",
        nomconsig="",
        desdircon="",
        codpaiscon="",
    )

    regimensuspensivo = RegimenSuspensivo(
        desdiralm="", codcomrs="", aductrol="", numplazo="", indparcial="",
        numhojins="", totinsum="", codalma="", numrs="", fecrs="",
        aduars="", numhojane="", numsec="",
    )

    origentranspalmacenaje = OrigenTranspAlmacenaje(
        paorig="", gpaorig="", paadq="", gpaadq="", viatran="",
        despuert="", transb="", ptoemb="", gptodesem="", ptodesem="",
        tpocarga="", desalmac="", almacen="", fecalmac="", fecretiro="",
        gnomciat="", codpaiscia="", numrutcia="", digvercia="",
        nummanif="", nummanif1="", nummanif2="", fecmanif="",
        numconoc="", fecconoc="", nomemisor="", numrutemi="", digveremi="",
    )

    antecedentesfinancieros = AntecedentesFinancieros(
        gregimp="", regimp="", bcocom="", codordiv="", formpago="",
        numdias="", valexfab="", moneda="", mongasfob="", clcompra="", pagograv="",
    )

    totales = Totales(
        totitems=data.totitems,
        fob=data.fob,
        tothojas="1",
        codfle="",
        flete=data.flete,
        totbultos="0",
        codseg="",
        seguro=data.seguro,
        totpeso="0",
        cif=data.cif,
    )

    respuesta = Respuesta(
        fechaceptacion="", numeroencriptado="", estado="", tiposeleccion=None,
    )

    cabeza = CABEZA(
        form=data.form,
        numidentif=data.numidentif or now.strftime("%Y%m%d%H%M%S"),
        fecvenci="",
        adu=data.adu,
        agente=data.agente,
        tpodocto=data.tpodocto,
        tipoingr=data.tipoingr,
        numaut="", fecaut="", gbcocen="",
        fectra=now.strftime("%Y%m%d"),
        fecacep="", aforo="", fecconfdi="", numencrip="",
        fecconfec=now.strftime("%Y%m%d"),
        numidenacl="", numres="", fecres="",
        identificacion=identificacion,
        regimensuspensivo=regimensuspensivo,
        origentranspalmacenaje=origentranspalmacenaje,
        antecedentesfinancieros=antecedentesfinancieros,
        totales=totales,
        respuesta=respuesta,
    )

    observacionesitem = ObservacionesItem(
        observaciones=[ObservacionItem(codobs="", desobs="")]
    )
    cuentasitem = CuentasItem(cuentas=[CuentaItem(otro="", cta="", sigval="", valor="")])
    insumos = Insumos(insumos=[])
    anexas = Anexas(anexas=[])

    item = ITEM(
        numitem="001", dnombre="", dmarca="", dvariedad="",
        dotro1="", dotro2="", atr5="", atr6="", sajuitem="", ajuitem="",
        cantmerc="0", medida="", codestum="", preunit="0",
        arancala="", numcor="", numacu="", concupo="", arancnac="",
        cifitem="0", advalala="", adval="", valad="",
        observacionesitem=observacionesitem,
        cuentasitem=cuentasitem,
        insumos=insumos,
        anexas=anexas,
    )

    items = ITEMS(items=[item])
    vistosbuenos = VISTOSBUENOS(vistosbuenos=[])
    bultos = BULTOS(idbultos="", bultos=[])
    cuentasgiro = CuentasGiro(cuentas=[])
    cuentasyvalores = CUENTASYVALORES(
        mon178="0", mon191="0", mon699="0", mon199="0", cuentasgiro=cuentasgiro,
    )
    error = Error(codigo="0", glosa="")
    errores = ERRORES(fechaproceso=now.strftime("%Y%m%d%H%M%S"), errores=[error])

    din = DIN(
        tipoenvio=data.tipoenvio,
        log=log,
        cabeza=cabeza,
        items=items,
        vistosbuenos=vistosbuenos,
        bultos=bultos,
        cuentasyvalores=cuentasyvalores,
        pagodiferido=None,
        anexasdin=None,
        errores=errores,
    )

    return din_service.to_xml(din)


@get("/schema/info", media_type=MediaType.JSON)
async def get_schema_info() -> dict[str, Any]:
    """
    Obtener informacion sobre el esquema DIN XML.

    Retorna la estructura y namespaces usados en el esquema DIN.
    """
    return {
        "target_namespace": "http://www.aduana.cl/xml/esquemas/EnvioDin",
        "root_element": "DIN",
        "required_elements": [
            "TIPOENVIO",
            "LOG",
            "CABEZA",
            "ITEMS",
            "VISTOSBUENOS",
            "BULTOS",
            "CUENTASYVALORES",
            "ERRORES",
        ],
        "optional_elements": [
            "PAGODIFERIDO",
            "ANEXASDIN",
        ],
        "namespaces": {
            "EnvioDin": "http://www.aduana.cl/xml/esquemas/EnvioDin",
            "LOG": "http://www.aduana.cl/xml/esquemas/LOG",
            "CABEZA": "http://www.aduana.cl/xml/esquemas/CABEZA",
            "ITEMS": "http://www.aduana.cl/xml/esquemas/ITEMS",
            "VISTOSBUENOS": "http://www.aduana.cl/xml/esquemas/VISTOSBUENOS",
            "BULTOS": "http://www.aduana.cl/xml/esquemas/BULTOS",
            "CUENTASYVALORES": "http://www.aduana.cl/xml/esquemas/CUENTASYVALORES",
            "PAGODIFERIDO": "http://www.aduana.cl/xml/esquemas/PAGODIFERIDO",
            "ERRORES": "http://www.aduana.cl/xml/esquemas/ERRORES",
            "ANEXASDIN": "http://www.aduana.cl/xml/esquemas/ANEXASDIN",
        },
        "web_services": {
            "recepcion": "http://testsoa.aduana.cl/MensajeriaServicios/http/RecibeDin?wsdl",
            "consulta": "http://testsoa.aduana.cl/ConsultaServiciosESB/http/servicioConsultaDIN?wsdl",
        },
    }


@get("/usage", media_type=MediaType.JSON)
async def get_usage_examples() -> dict[str, Any]:
    """
    Obtener ejemplos de uso de todos los endpoints.
    """
    return {
        "endpoints": {
            "GET /sample": {
                "description": "Obtener un XML DIN de ejemplo",
                "curl": "curl http://localhost:8000/sample"
            },
            "GET /sample/json": {
                "description": "Obtener el DIN de ejemplo como JSON",
                "curl": "curl http://localhost:8000/sample/json"
            },
            "POST /validate": {
                "description": "Validar XML contra esquema XSD",
                "curl": 'curl -X POST http://localhost:8000/validate -H "Content-Type: application/json" -d \'{"xml_content": "<test>hello</test>"}\''
            },
            "POST /validate/structure": {
                "description": "Verificar que el XML este bien formado",
                "curl": 'curl -X POST http://localhost:8000/validate/structure -H "Content-Type: application/json" -d \'{"xml_content": "<test>hello</test>"}\''
            },
            "POST /parse": {
                "description": "Convertir DIN XML a JSON",
                "curl": 'curl -X POST http://localhost:8000/parse -H "Content-Type: application/json" -d \'{"xml_content": "<DIN>...</DIN>"}\''
            },
            "POST /generate": {
                "description": "Generar DIN XML desde datos JSON",
                "curl": 'curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d \'{"nombre": "MI EMPRESA", "rut": "12345678"}\''
            },
        }
    }


# Create Litestar application
app = Litestar(
    route_handlers=[
        health_check,
        get_sample_din,
        get_sample_din_json,
        validate_din_xml,
        validate_structure_xml,
        parse_din_xml,
        generate_din_xml,
        get_schema_info,
        get_usage_examples,
    ],
    openapi_config=OpenAPIConfig(
        title="DIN XML API",
        version="1.0.0",
        description="""
API para confeccionar, probar y presentar XMLs de DIN (Declaracion de Ingreso)
para el Servicio Nacional de Aduanas de Chile.

## Como usar

### Validar XML
1. Ve al endpoint `POST /validate` o `POST /validate/structure`
2. En el campo `xml_content`, pega tu documento XML
3. Ejecuta para ver el resultado

### Parsear XML a JSON
1. Ve al endpoint `POST /parse`
2. En el campo `xml_content`, pega tu documento DIN XML
3. Ejecuta para obtener la estructura JSON

### Generar XML
1. Ve al endpoint `POST /generate`
2. Completa los campos que necesites
3. Ejecuta para obtener el XML generado

### Obtener ejemplo
Usa `GET /sample` para obtener un XML DIN de ejemplo completo.
        """,
        contact=Contact(name="DIN API Support"),
    ),
    debug=True,
)
