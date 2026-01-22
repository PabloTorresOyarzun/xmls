from typing import Any
from litestar import Litestar, get, post, MediaType, Response
from litestar.datastructures import State
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Contact
from pydantic import BaseModel

from .models import DIN
from .services import DINService


class ValidationRequest(BaseModel):
    xml_content: str


class ValidationResponse(BaseModel):
    is_valid: bool
    errors: list[str]


class DINRequest(BaseModel):
    tipoenvio: str = "01"
    # LOG
    secuencia: str = "000001"
    aduana: str = "901"
    sobre: str = "001"
    # CABEZA
    form: str = "15"
    numidentif: str = ""
    adu: str = "901"
    agente: str = "0001"
    tpodocto: str = "15"
    tipoingr: str = "1"
    # IDENTIFICACION
    nombre: str = ""
    direc: str = ""
    codcomun: str = "13101"
    rut: str = ""
    dvrut: str = ""
    # TOTALES
    totitems: str = "1"
    fob: str = "0.00"
    flete: str = "0.00"
    seguro: str = "0.00"
    cif: str = "0.00"


class XMLResponse(BaseModel):
    xml: str
    pretty: bool = True


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
    Get a sample DIN XML document.

    Returns a complete sample DIN XML that can be used as a template.
    """
    sample_din = din_service.create_sample_din()
    return din_service.to_xml(sample_din)


@get("/sample/json", media_type=MediaType.JSON)
async def get_sample_din_json() -> dict[str, Any]:
    """
    Get a sample DIN as JSON.

    Returns the sample DIN structure as JSON for easier inspection.
    """
    sample_din = din_service.create_sample_din()
    return sample_din.model_dump()


@post("/validate", media_type=MediaType.JSON)
async def validate_din(data: ValidationRequest) -> ValidationResponse:
    """
    Validate a DIN XML document.

    Validates the XML content against the official DIN XSD schema.
    Returns validation result and any error messages.
    """
    is_valid, errors = din_service.validate_din(data.xml_content)
    return ValidationResponse(is_valid=is_valid, errors=errors)


@post("/validate/structure", media_type=MediaType.JSON)
async def validate_structure(data: ValidationRequest) -> ValidationResponse:
    """
    Validate XML structure only (well-formed check).

    Only checks if the XML is well-formed, without schema validation.
    """
    is_valid, errors = din_service.validator.validate_structure(data.xml_content)
    return ValidationResponse(is_valid=is_valid, errors=errors)


@post("/parse", media_type=MediaType.JSON)
async def parse_din(data: ValidationRequest) -> dict[str, Any]:
    """
    Parse a DIN XML document to JSON.

    Converts the XML content to a structured JSON representation.
    """
    try:
        din = din_service.from_xml(data.xml_content)
        return {"success": True, "data": din.model_dump()}
    except Exception as e:
        return {"success": False, "error": str(e)}


@post("/generate", media_type=MediaType.TEXT)
async def generate_din_xml(data: DINRequest) -> str:
    """
    Generate a DIN XML document from provided data.

    Creates a DIN XML document using the provided parameters.
    Missing fields will use default values from the sample template.
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
    Get information about the DIN XML schema.

    Returns the structure and namespaces used in the DIN schema.
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


# Create Litestar application
app = Litestar(
    route_handlers=[
        health_check,
        get_sample_din,
        get_sample_din_json,
        validate_din,
        validate_structure,
        parse_din,
        generate_din_xml,
        get_schema_info,
    ],
    openapi_config=OpenAPIConfig(
        title="DIN XML API",
        version="1.0.0",
        description="""
API para confeccionar, probar y presentar XMLs de DIN (Declaración de Ingreso)
para el Servicio Nacional de Aduanas de Chile.

## Funcionalidades

- **Generar XML**: Crear documentos DIN XML a partir de datos estructurados
- **Validar XML**: Validar documentos contra el esquema XSD oficial
- **Parsear XML**: Convertir XML a formato JSON
- **Plantilla de ejemplo**: Obtener un documento DIN de ejemplo

## Documentación

Los esquemas XSD están basados en la documentación oficial de Aduana Chile.
        """,
        contact=Contact(name="DIN API Support"),
    ),
    debug=True,
)
