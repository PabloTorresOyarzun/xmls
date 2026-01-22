from typing import Any
from litestar import Litestar, get, post, MediaType, Request
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Contact
from pydantic import BaseModel

from .models import DIN
from .services import DINService


class ValidationRequest(BaseModel):
    """Request body for validation endpoints (JSON format)."""
    xml_content: str


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


# ============================================================================
# VALIDATE ENDPOINTS - Accept XML directly in request body
# ============================================================================

@post("/validate", media_type=MediaType.JSON)
async def validate_din_xml(request: Request) -> ValidationResponse:
    """
    Validate a DIN XML document against the XSD schema.

    Send XML directly in the request body.

    Example with curl:
    ```bash
    curl -X POST http://localhost:8000/validate \\
         -H "Content-Type: application/xml" \\
         -d '<?xml version="1.0"?><DIN>...</DIN>'
    ```

    Or from a file:
    ```bash
    curl -X POST http://localhost:8000/validate \\
         -H "Content-Type: application/xml" \\
         --data-binary @mi_documento.xml
    ```
    """
    body = await request.body()
    xml_content = body.decode("utf-8") if body else ""

    if not xml_content.strip():
        return ValidationResponse(is_valid=False, errors=["Empty request body. Send XML content directly."])

    is_valid, errors = din_service.validate_din(xml_content)
    return ValidationResponse(is_valid=is_valid, errors=errors)


@post("/validate/structure", media_type=MediaType.JSON)
async def validate_structure_xml(request: Request) -> ValidationResponse:
    """
    Validate XML structure only (well-formed check, no schema validation).

    Send XML directly in the request body.

    Example with curl:
    ```bash
    curl -X POST http://localhost:8000/validate/structure \\
         -H "Content-Type: application/xml" \\
         -d '<?xml version="1.0"?><test>Hello</test>'
    ```
    """
    body = await request.body()
    xml_content = body.decode("utf-8") if body else ""

    if not xml_content.strip():
        return ValidationResponse(is_valid=False, errors=["Empty request body. Send XML content directly."])

    is_valid, errors = din_service.validator.validate_structure(xml_content)
    return ValidationResponse(is_valid=is_valid, errors=errors)


@post("/parse", media_type=MediaType.JSON)
async def parse_din_xml(request: Request) -> ParseResponse:
    """
    Parse a DIN XML document to JSON.

    Send XML directly in the request body.

    Example with curl:
    ```bash
    curl -X POST http://localhost:8000/parse \\
         -H "Content-Type: application/xml" \\
         --data-binary @mi_documento.xml
    ```
    """
    body = await request.body()
    xml_content = body.decode("utf-8") if body else ""

    if not xml_content.strip():
        return ParseResponse(success=False, error="Empty request body. Send XML content directly.")

    try:
        din = din_service.from_xml(xml_content)
        return ParseResponse(success=True, data=din.model_dump())
    except Exception as e:
        return ParseResponse(success=False, error=str(e))


# ============================================================================
# GENERATE ENDPOINT
# ============================================================================

@post("/generate", media_type=MediaType.TEXT)
async def generate_din_xml(data: DINRequest) -> str:
    """
    Generate a DIN XML document from provided data.

    Send a JSON body with the fields you want to set.
    Missing fields will use default values.

    Example with curl:
    ```bash
    curl -X POST http://localhost:8000/generate \\
         -H "Content-Type: application/json" \\
         -d '{"nombre": "MI EMPRESA S.A.", "rut": "76123456", "dvrut": "7"}'
    ```
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


@get("/usage", media_type=MediaType.JSON)
async def get_usage_examples() -> dict[str, Any]:
    """
    Get usage examples for all endpoints.
    """
    return {
        "endpoints": {
            "GET /sample": {
                "description": "Get a sample DIN XML",
                "curl": "curl http://localhost:8000/sample"
            },
            "GET /sample/json": {
                "description": "Get sample DIN as JSON",
                "curl": "curl http://localhost:8000/sample/json"
            },
            "POST /validate": {
                "description": "Validate XML against XSD schema",
                "curl": "curl -X POST http://localhost:8000/validate -H 'Content-Type: application/xml' --data-binary @documento.xml"
            },
            "POST /validate/structure": {
                "description": "Check if XML is well-formed",
                "curl": "curl -X POST http://localhost:8000/validate/structure -H 'Content-Type: application/xml' -d '<test>hello</test>'"
            },
            "POST /parse": {
                "description": "Convert DIN XML to JSON",
                "curl": "curl -X POST http://localhost:8000/parse -H 'Content-Type: application/xml' --data-binary @documento.xml"
            },
            "POST /generate": {
                "description": "Generate DIN XML from JSON data",
                "curl": "curl -X POST http://localhost:8000/generate -H 'Content-Type: application/json' -d '{\"nombre\": \"MI EMPRESA\", \"rut\": \"12345678\"}'"
            },
        },
        "quick_test": {
            "validate_structure": "curl -X POST http://localhost:8000/validate/structure -d '<test>hello</test>'",
            "get_sample_and_validate": "curl -s http://localhost:8000/sample | curl -X POST http://localhost:8000/validate/structure -d @-"
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

## Uso Rapido

### Validar estructura XML
```bash
curl -X POST http://localhost:8000/validate/structure -d '<test>hello</test>'
```

### Obtener XML de ejemplo
```bash
curl http://localhost:8000/sample
```

### Validar un archivo XML
```bash
curl -X POST http://localhost:8000/validate --data-binary @mi_documento.xml
```

### Parsear XML a JSON
```bash
curl -X POST http://localhost:8000/parse --data-binary @mi_documento.xml
```

## Endpoints disponibles

- `GET /sample` - Obtener DIN XML de ejemplo
- `GET /sample/json` - Obtener DIN como JSON
- `POST /validate` - Validar XML contra esquema XSD
- `POST /validate/structure` - Verificar que XML este bien formado
- `POST /parse` - Convertir XML a JSON
- `POST /generate` - Generar XML desde JSON
- `GET /usage` - Ver ejemplos de uso
        """,
        contact=Contact(name="DIN API Support"),
    ),
    debug=True,
)
