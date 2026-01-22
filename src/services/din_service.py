from datetime import datetime
from typing import Optional

from ..models import (
    DIN,
    LOG,
    CABEZA,
    ITEMS,
    ITEM,
    VISTOSBUENOS,
    BULTOS,
    CUENTASYVALORES,
    ERRORES,
    Error,
)
from ..models.cabeza import (
    Identificacion,
    RegimenSuspensivo,
    OrigenTranspAlmacenaje,
    AntecedentesFinancieros,
    Totales,
    Respuesta,
)
from ..models.items import ObservacionesItem, ObservacionItem, CuentasItem, CuentaItem, Insumos, Anexas
from ..models.cuentasyvalores import CuentasGiro
from .xml_validator import XMLValidator


class DINService:
    def __init__(self):
        self.validator = XMLValidator()

    def create_sample_din(self) -> DIN:
        """Create a sample DIN document for testing."""
        now = datetime.now()

        log = LOG(
            secuencia="000001",
            aduana="901",
            sobre="001",
            fecha=now.strftime("%Y%m%d"),
            hora=now.strftime("%H%M%S"),
            van="1",
            origen="AGENTE",
            destino="ADUANA",
        )

        identificacion = Identificacion(
            nombre="IMPORTADORA EJEMPLO S.A.",
            direc="AV. EJEMPLO 1234",
            codcomun="13101",
            tiprut="1",
            rut="76123456",
            dvrut="7",
            nomrepleg="JUAN PEREZ",
            numrutrl="12345678",
            digverrl="9",
            nomconsig="CONSIGNATARIO EJEMPLO",
            desdircon="123 MAIN STREET",
            codpaiscon="US",
        )

        regimensuspensivo = RegimenSuspensivo(
            desdiralm="",
            codcomrs="",
            aductrol="",
            numplazo="",
            indparcial="",
            numhojins="",
            totinsum="",
            codalma="",
            numrs="",
            fecrs="",
            aduars="",
            numhojane="",
            numsec="",
        )

        origentranspalmacenaje = OrigenTranspAlmacenaje(
            paorig="US",
            gpaorig="ESTADOS UNIDOS",
            paadq="US",
            gpaadq="ESTADOS UNIDOS",
            viatran="1",
            despuert="PUERTO EJEMPLO",
            transb="0",
            ptoemb="USLAX",
            gptodesem="VALPARAISO",
            ptodesem="CLVAP",
            tpocarga="1",
            desalmac="ALMACEN EJEMPLO",
            almacen="001",
            fecalmac=now.strftime("%Y%m%d"),
            fecretiro="",
            gnomciat="NAVIERA EJEMPLO",
            codpaiscia="CL",
            numrutcia="76654321",
            digvercia="K",
            nummanif="123456",
            nummanif1="",
            nummanif2="",
            fecmanif=now.strftime("%Y%m%d"),
            numconoc="BL123456",
            fecconoc=now.strftime("%Y%m%d"),
            nomemisor="EMISOR EJEMPLO",
            numrutemi="76111222",
            digveremi="3",
        )

        antecedentesfinancieros = AntecedentesFinancieros(
            gregimp="IMPORTACION NORMAL",
            regimp="4",
            bcocom="001",
            codordiv="0",
            formpago="1",
            numdias="0",
            valexfab="10000.00",
            moneda="USD",
            mongasfob="500.00",
            clcompra="1",
            pagograv="0",
        )

        totales = Totales(
            totitems="1",
            fob="10500.00",
            tothojas="1",
            codfle="1",
            flete="800.00",
            totbultos="10",
            codseg="1",
            seguro="100.00",
            totpeso="500.00",
            cif="11400.00",
        )

        respuesta = Respuesta(
            fechaceptacion="",
            numeroencriptado="",
            estado="",
            tiposeleccion=None,
        )

        cabeza = CABEZA(
            form="15",
            numidentif="2024000001",
            fecvenci=now.strftime("%Y%m%d"),
            adu="901",
            agente="0001",
            tpodocto="15",
            tipoingr="1",
            numaut="",
            fecaut="",
            gbcocen="BANCO CENTRAL",
            fectra=now.strftime("%Y%m%d"),
            fecacep="",
            aforo="",
            fecconfdi="",
            numencrip="",
            fecconfec=now.strftime("%Y%m%d"),
            numidenacl="",
            numres="",
            fecres="",
            identificacion=identificacion,
            regimensuspensivo=regimensuspensivo,
            origentranspalmacenaje=origentranspalmacenaje,
            antecedentesfinancieros=antecedentesfinancieros,
            totales=totales,
            respuesta=respuesta,
        )

        observacion = ObservacionItem(codobs="001", desobs="SIN OBSERVACIONES")
        observacionesitem = ObservacionesItem(observaciones=[observacion])

        cuentaitem = CuentaItem(otro="", cta="178", sigval="+", valor="1140.00")
        cuentasitem = CuentasItem(cuentas=[cuentaitem])

        insumos = Insumos(insumos=[])
        anexas = Anexas(anexas=[])

        item = ITEM(
            numitem="001",
            dnombre="PRODUCTO EJEMPLO",
            dmarca="MARCA EJEMPLO",
            dvariedad="VARIEDAD A",
            dotro1="",
            dotro2="",
            atr5="",
            atr6="",
            sajuitem="",
            ajuitem="",
            cantmerc="100",
            medida="UN",
            codestum="1",
            preunit="105.00",
            arancala="8471.30.00",
            numcor="",
            numacu="",
            concupo="",
            arancnac="8471.30.00",
            cifitem="11400.00",
            advalala="6",
            adval="6",
            valad="684.00",
            observacionesitem=observacionesitem,
            cuentasitem=cuentasitem,
            insumos=insumos,
            anexas=anexas,
        )

        items = ITEMS(items=[item])

        vistosbuenos = VISTOSBUENOS(vistosbuenos=[])

        bultos = BULTOS(idbultos="1", bultos=[])

        cuentasgiro = CuentasGiro(cuentas=[])
        cuentasyvalores = CUENTASYVALORES(
            mon178="684.00",
            mon191="2166.00",
            mon199="2850.00",
            mon699="0.00",
            cuentasgiro=cuentasgiro,
        )

        error = Error(codigo="0", glosa="SIN ERRORES")
        errores = ERRORES(fechaproceso=now.strftime("%Y%m%d%H%M%S"), errores=[error])

        din = DIN(
            tipoenvio="01",
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

        return din

    def to_xml(self, din: DIN, pretty: bool = True) -> str:
        """Convert DIN model to XML string."""
        xml_bytes = din.to_xml(
            encoding="UTF-8",
            xml_declaration=True,
            pretty_print=pretty,
        )
        return xml_bytes.decode("utf-8")

    def from_xml(self, xml_content: str | bytes) -> DIN:
        """Parse XML content to DIN model."""
        if isinstance(xml_content, str):
            xml_content = xml_content.encode("utf-8")
        return DIN.from_xml(xml_content)

    def validate_din(self, xml_content: str | bytes) -> tuple[bool, list[str]]:
        """Validate DIN XML against XSD schema."""
        return self.validator.validate(xml_content)
