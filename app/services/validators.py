"""
Módulo de validaciones y transformaciones de datos DIN.
Implementa las reglas del sistema antiguo de Aduana Chile.
"""
import logging
from datetime import datetime, timedelta
from typing import Optional
from app.models.din import DINModel

logger = logging.getLogger(__name__)

# Fechas consideradas inválidas
INVALID_DATES = {"30121899", "01011900", "", None}

# Operaciones que requieren validación de manifiesto
OPS_MANIFIESTO = {
    "151", "152", "156", "157", "158", "159", "160", "161", "162",
    "163", "164", "165", "167", "175", "176", "180", "125", "126"
}

# Operaciones para limpieza de forma de pago
OPS_FORMPAGO_CLEAN = {"106", "126", "156", "160", "175", "176"}

# Operaciones para limpieza masiva de antecedentes financieros
OPS_ANTEC_FIN_CLEAN = {"156", "176", "125", "126", "106"}

# Operaciones para limpieza de observaciones
OPS_OBS_CLEAN = {"130", "180"}

# Cuentas que siempre se formatean
CUENTAS_SIEMPRE = {"223", "197", "270", "209", "179", "174", "116", "115"}


class DINValidator:
    """Validador y transformador de datos DIN."""

    def __init__(self, din: DINModel):
        self.din = din
        self.tpodocto = din.cabeza.tpodocto
        self.form = din.cabeza.form
        self.tipoingr = din.cabeza.tipoingr

    def validate_and_transform(self) -> DINModel:
        """Ejecuta todas las validaciones y transformaciones."""
        logger.info("Iniciando validaciones y transformaciones DIN")

        self._transform_fechas()
        self._calculate_fecvenci()
        self._validate_manifiesto()
        self._validate_financieros()
        self._validate_identificacion()
        self._validate_items()
        self._validate_cuentas_giro()
        self._validate_bultos()
        self._apply_padding()

        logger.info("Validaciones completadas")
        return self.din

    # =========================================================================
    # 1. VALIDACIONES Y TRANSFORMACIONES DE FECHAS
    # =========================================================================

    def _transform_fechas(self):
        """Limpia fechas inválidas transformándolas a '00000000' o ''."""
        cabeza = self.din.cabeza

        # Campos de fecha en CABEZA
        fecha_fields = [
            "fecvenci", "fecaut", "fectra", "fecacep", "fecconfdi",
            "fecconfec", "fecres"
        ]

        for field in fecha_fields:
            value = getattr(cabeza, field, None)
            if value in INVALID_DATES:
                setattr(cabeza, field, "00000000")

        # Fechas en REGIMENSUSPENSIVO
        if cabeza.regimensuspensivo:
            if cabeza.regimensuspensivo.fecrs in INVALID_DATES:
                cabeza.regimensuspensivo.fecrs = ""

        # Fechas en ORIGENTRANSPALMACENAJE
        origen = cabeza.origentranspalmacenaje
        if origen:
            if origen.fecalmac in INVALID_DATES:
                origen.fecalmac = ""
            if origen.fecretiro in INVALID_DATES:
                origen.fecretiro = ""
            if origen.fecmanif in INVALID_DATES:
                origen.fecmanif = ""
            if origen.fecconoc in INVALID_DATES:
                origen.fecconoc = ""

        # Fecha en LOG
        if self.din.log.fecha in INVALID_DATES:
            self.din.log.fecha = datetime.now().strftime("%d%m%Y")

    def _calculate_fecvenci(self):
        """Calcula automáticamente la fecha de vencimiento según FORM y TPODOCTO."""
        cabeza = self.din.cabeza
        today = datetime.now()

        # Si ya tiene fecha válida, no recalcular
        if cabeza.fecvenci and cabeza.fecvenci != "00000000":
            return

        if self.form in ("15", "14"):
            if self.tpodocto in ("113", "163", "114", "164"):
                # +90 días
                new_date = today + timedelta(days=90)
            elif self.tpodocto in ("107", "108", "157", "158"):
                if self.form == "15":
                    # +15 días solo para Form 15
                    new_date = today + timedelta(days=15)
                else:
                    # Form 14: limpiar
                    cabeza.fecvenci = "00000000"
                    return
            else:
                # Por defecto +15 días
                new_date = today + timedelta(days=15)

            cabeza.fecvenci = new_date.strftime("%d%m%Y")

        elif not self.form:
            # Formulario vacío
            if self.tpodocto in ("180", "106", "176", "156"):
                cabeza.fecvenci = "00000000"

    # =========================================================================
    # 2. VALIDACIÓN DE MANIFIESTO
    # =========================================================================

    def _validate_manifiesto(self):
        """Valida y transforma datos de manifiesto según operación."""
        if self.tpodocto not in OPS_MANIFIESTO:
            return

        origen = self.din.cabeza.origentranspalmacenaje
        if not origen:
            return

        # Prioridad: nummanif1 > nombreVehiculo (gnomciat)
        if origen.nummanif1:
            # Recortar a 15 caracteres y rellenar con espacios
            origen.nummanif1 = origen.nummanif1[:15].ljust(15)
        else:
            # Usar nombre del vehículo
            origen.nummanif1 = (origen.gnomciat or "")[:15].ljust(15)

    # =========================================================================
    # 3. VALIDACIONES FINANCIERAS
    # =========================================================================

    def _validate_financieros(self):
        """Valida y transforma antecedentes financieros."""
        antec = self.din.cabeza.antecedentesfinancieros
        if not antec:
            return

        # Limpieza forzada de forma de pago
        if self.tipoingr == "N" and self.tpodocto in OPS_FORMPAGO_CLEAN:
            antec.formpago = "00"
        elif self.tipoingr != "N" and self.tpodocto in {"156", "176", "126", "106"}:
            antec.formpago = "00"

        # Limpieza masiva para operaciones específicas
        if self.tpodocto in OPS_ANTEC_FIN_CLEAN:
            antec.regimp = ""
            antec.bcocom = "00"
            antec.codordiv = "0"
            antec.formpago = "00"
            antec.numdias = "0000"
            antec.valexfab = "0000000000.00"
            antec.moneda = "000"
            antec.mongasfob = "0000000000.00"
            antec.clcompra = "0"
            antec.pagograv = "00"

            # Excepción Op. 125
            if self.tpodocto == "125":
                antec.pagograv = "00"

        # Validación cláusula de compra
        try:
            if antec.clcompra and int(antec.clcompra) > 9:
                antec.clcompra = "8"
        except ValueError:
            pass

        # Validación flete y seguro
        totales = self.din.cabeza.totales
        if totales:
            if totales.codfle in ("X", ""):
                totales.codfle = "0"
            if totales.codseg in ("X", ""):
                totales.codseg = "0"

    # =========================================================================
    # 4. VALIDACIÓN DE IDENTIFICACIÓN
    # =========================================================================

    def _validate_identificacion(self):
        """Valida tipo de RUT según dígito verificador."""
        ident = self.din.cabeza.identificacion
        if not ident:
            return

        # Si DV es "P" (Pasaporte), TIPRUT = "04", sino "03"
        if ident.dvrut == "P":
            ident.tiprut = "04"
        elif ident.tiprut not in ("03", "04"):
            ident.tiprut = "03"

    # =========================================================================
    # 5. VALIDACIONES DE ÍTEMS
    # =========================================================================

    def _validate_items(self):
        """Valida y transforma datos de ítems."""
        for item in self.din.items:
            self._validate_item_descripcion(item)
            self._validate_item_medida(item)
            self._validate_item_observaciones(item)
            self._validate_item_cuentas(item)

    def _validate_item_descripcion(self, item):
        """Trunca campos de descripción a sus largos máximos."""
        # NOMBRE: 50 chars
        item.dnombre = (item.dnombre or "")[:50]
        # MARCA: 30 chars
        item.dmarca = (item.dmarca or "")[:30]
        # VARIEDAD: 30 chars
        item.dvariedad = (item.dvariedad or "")[:30]
        # DOTRO1: 30 chars
        item.dotro1 = (item.dotro1 or "")[:30]
        # DOTRO2: 30 chars
        item.dotro2 = (item.dotro2 or "")[:30]
        # ATR5: 30 chars
        item.atr5 = (item.atr5 or "")[:30]
        # ATR6: 30 chars
        item.atr6 = (item.atr6 or "")[:30]

    def _validate_item_medida(self, item):
        """Valida unidad de medida según código arancel."""
        if item.arancala and item.arancala != "0":
            item.medida = (item.medida or "").zfill(2)
            if not item.codestum:
                item.codestum = " "
        else:
            item.medida = "00"
            item.codestum = ""

    def _validate_item_observaciones(self, item):
        """Limpia observaciones según operación."""
        if self.tpodocto in OPS_OBS_CLEAN:
            item.observacionesitem = []
        else:
            # Filtrar observaciones vacías
            item.observacionesitem = [
                obs for obs in item.observacionesitem
                if obs.codobs and obs.desobs
            ]

    def _validate_item_cuentas(self, item):
        """Valida cuentas del ítem (impuestos/gravámenes)."""
        cuentas_validas = []

        for cuenta in item.cuentasitem:
            # Limpiar cuentas vacías
            if (cuenta.otro == "0.000000" and 
                not cuenta.cta and 
                cuenta.valor == "0.00"):
                continue

            # Calcular signo
            cuenta.sigval = self._calculate_sigval(cuenta, item)

            # Manejar valores negativos
            if cuenta.valor and cuenta.valor.startswith("-"):
                cuenta.sigval = "-"
                cuenta.valor = cuenta.valor[1:]  # Remover guion

            # Formatear valor con padding
            cuenta.valor = self._format_monto(cuenta.valor, 13)
            cuenta.otro = self._format_monto(cuenta.otro, 12, decimals=6)

            cuentas_validas.append(cuenta)

        item.cuentasitem = cuentas_validas

    def _calculate_sigval(self, cuenta, item) -> str:
        """Calcula el signo de una cuenta."""
        cta = cuenta.cta
        valor = self._parse_decimal(cuenta.valor)
        otro = self._parse_decimal(cuenta.otro)
        valad = self._parse_decimal(item.valad)

        if cta == "222":
            suma = valor + valad
            return "+" if suma > 0 else "-"
        elif cta in ("174", "116", "115"):
            return "+"
        elif cta in ("211", "179"):
            if valor == 0 and otro == 0:
                return "+"
        
        # Regla general
        return "+" if valor > 0 else "-"

    # =========================================================================
    # 6. VALIDACIONES DE CUENTAS DE GIRO
    # =========================================================================

    def _validate_cuentas_giro(self):
        """Valida cuentas de giro globales."""
        cuentas = self.din.cuentasyvalores
        if not cuentas:
            return

        cuentas_validas = []
        for cg in cuentas.cuentasgiro:
            # Si es guion, enviar tal cual
            if cg.ctaotro == "-":
                cuentas_validas.append(cg)
                continue

            # Cuentas que siempre se formatean
            if cg.ctaotro in CUENTAS_SIEMPRE:
                cg.monotro = self._format_monto(cg.monotro, 13)
                cuentas_validas.append(cg)
                continue

            # Regla del 0.00: si monto es 0, limpiar cuenta
            monto = self._parse_decimal(cg.monotro)
            if monto == 0:
                cg.ctaotro = "000"
                cg.monotro = "0000000000.00"
            else:
                cg.monotro = self._format_monto(cg.monotro, 13)

            cuentas_validas.append(cg)

        cuentas.cuentasgiro = cuentas_validas

    # =========================================================================
    # 7. VALIDACIÓN DE BULTOS
    # =========================================================================

    def _validate_bultos(self):
        """Valida y concatena identificadores de bultos."""
        bultos = self.din.bultos
        if not bultos:
            return

        # IDBULTOS ya viene como string concatenado
        # Asegurar que no exceda el largo máximo (250 chars típico)
        bultos.idbultos = (bultos.idbultos or "")[:250]

    # =========================================================================
    # 8. FORMATEO GENERAL (PADDING)
    # =========================================================================

    def _apply_padding(self):
        """Aplica formateo de padding a todos los campos."""
        cabeza = self.din.cabeza
        log = self.din.log
        totales = cabeza.totales
        ident = cabeza.identificacion

        # LOG
        log.secuencia = (log.secuencia or "1").zfill(1)
        log.aduana = (log.aduana or "").zfill(2)

        # CABEZA - códigos numéricos
        cabeza.form = (cabeza.form or "").zfill(2)
        cabeza.adu = (cabeza.adu or "").zfill(2)
        cabeza.tpodocto = (cabeza.tpodocto or "").zfill(3)
        cabeza.aforo = (cabeza.aforo or "00").zfill(2)
        cabeza.numres = (cabeza.numres or "00000000").zfill(8)

        # IDENTIFICACION
        if ident:
            ident.codcomun = (ident.codcomun or "").zfill(5)
            ident.tiprut = (ident.tiprut or "03").zfill(2)
            ident.codpaiscon = (ident.codpaiscon or "").zfill(3)

        # TOTALES - montos
        if totales:
            totales.totitems = (totales.totitems or "001").zfill(3)
            totales.fob = self._format_monto(totales.fob, 14)
            totales.tothojas = (totales.tothojas or "001").zfill(3)
            totales.flete = self._format_monto(totales.flete, 14)
            totales.totbultos = (totales.totbultos or "000001").zfill(6)
            totales.seguro = self._format_monto(totales.seguro, 14)
            totales.totpeso = self._format_monto(totales.totpeso, 13, decimals=2)
            totales.cif = self._format_monto(totales.cif, 14)

        # ANTECEDENTES FINANCIEROS
        antec = cabeza.antecedentesfinancieros
        if antec:
            antec.regimp = (antec.regimp or "").zfill(2) if antec.regimp else ""
            antec.bcocom = (antec.bcocom or "00").zfill(2)
            antec.codordiv = (antec.codordiv or "0").zfill(1)
            antec.formpago = (antec.formpago or "00").zfill(2)
            antec.numdias = (antec.numdias or "0000").zfill(4)
            antec.valexfab = self._format_monto(antec.valexfab, 13)
            antec.moneda = (antec.moneda or "000").zfill(3)
            antec.mongasfob = self._format_monto(antec.mongasfob, 13)
            antec.clcompra = (antec.clcompra or "0").zfill(1)
            antec.pagograv = (antec.pagograv or "00").zfill(2)

        # REGIMEN SUSPENSIVO
        rs = cabeza.regimensuspensivo
        if rs:
            rs.codcomrs = (rs.codcomrs or "00000").zfill(5)
            rs.aductrol = (rs.aductrol or "00").zfill(2)
            rs.numplazo = (rs.numplazo or "00000000").zfill(8)
            rs.indparcial = (rs.indparcial or "0").zfill(1)
            rs.numhojins = (rs.numhojins or "000").zfill(3)
            rs.totinsum = self._format_monto(rs.totinsum, 11, decimals=4)
            rs.codalma = (rs.codalma or "000").zfill(3)
            rs.numrs = (rs.numrs or "0000000000").zfill(10)
            rs.aduars = (rs.aduars or "00").zfill(2)
            rs.numhojane = (rs.numhojane or "000").zfill(3)
            rs.numsec = (rs.numsec or "00000").zfill(5)

        # ORIGEN TRANSPORTE
        origen = cabeza.origentranspalmacenaje
        if origen:
            origen.paorig = (origen.paorig or "").zfill(3)
            origen.paadq = (origen.paadq or "").zfill(3)
            origen.viatran = (origen.viatran or "").zfill(2)
            origen.ptoemb = (origen.ptoemb or "").zfill(3)
            origen.ptodesem = (origen.ptodesem or "").zfill(3)
            origen.codpaiscia = (origen.codpaiscia or "").zfill(3)

        # ITEMS
        for item in self.din.items:
            item.numitem = (item.numitem or "001").zfill(3)
            item.ajuitem = self._format_monto(item.ajuitem, 13)
            item.cantmerc = self._format_cantidad(item.cantmerc, 12, decimals=4)
            item.medida = (item.medida or "00").zfill(2)
            item.preunit = self._format_monto(item.preunit, 14, decimals=6)
            item.arancala = (item.arancala or "00000000").zfill(8)
            item.numcor = (item.numcor or "0").zfill(1)
            item.numacu = (item.numacu or "").zfill(3) if item.numacu else ""
            item.concupo = (item.concupo or "0").zfill(1)
            item.arancnac = (item.arancnac or "00000000").zfill(8)
            item.cifitem = self._format_monto(item.cifitem, 13)
            item.advalala = self._format_monto(item.advalala, 7, decimals=2)
            item.adval = (item.adval or "000").zfill(3)
            item.valad = self._format_monto(item.valad, 13)

        # CUENTAS Y VALORES
        cv = self.din.cuentasyvalores
        if cv:
            cv.mon178 = self._format_monto(cv.mon178, 13)
            cv.mon191 = self._format_monto(cv.mon191, 13)
            cv.mon699 = self._format_monto(cv.mon699, 13)
            cv.mon199 = self._format_monto(cv.mon199, 13)

        # VISTOS BUENOS
        for vb in self.din.vistosbuenos:
            vb.nuregr = (vb.nuregr or "000000").zfill(6)
            vb.anoreg = (vb.anoreg or "0000").zfill(4)
            vb.codvisbuen = (vb.codvisbuen or "0").zfill(1)
            vb.numregla = (vb.numregla or "0000000000000").zfill(13)
            vb.numanores = (vb.numanores or "0000").zfill(4)
            vb.codultvb = (vb.codultvb or "000").zfill(3)

        # BULTOS
        for bulto in self.din.bultos.bultos:
            bulto.tpobul = (bulto.tpobul or "000").zfill(3)
            bulto.cantbul = (bulto.cantbul or "000001").zfill(6)

    # =========================================================================
    # UTILIDADES
    # =========================================================================

    def _parse_decimal(self, value: Optional[str]) -> float:
        """Parsea un string a decimal de forma segura."""
        if not value:
            return 0.0
        try:
            # Remover caracteres no numéricos excepto punto y guion
            clean = value.replace(",", ".").strip()
            return float(clean)
        except (ValueError, TypeError):
            return 0.0

    def _format_monto(self, value: Optional[str], total_len: int, decimals: int = 2) -> str:
        """Formatea un monto con padding de ceros."""
        num = self._parse_decimal(value)
        # Formato con decimales fijos
        formatted = f"{abs(num):.{decimals}f}"
        # Padding izquierdo con ceros
        return formatted.zfill(total_len)

    def _format_cantidad(self, value: Optional[str], total_len: int, decimals: int = 4) -> str:
        """Formatea una cantidad con padding de ceros."""
        return self._format_monto(value, total_len, decimals)


def validate_din(din: DINModel) -> DINModel:
    """Función helper para validar un DIN."""
    validator = DINValidator(din)
    return validator.validate_and_transform()
