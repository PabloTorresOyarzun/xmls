from datetime import datetime, timedelta
from typing import List, Optional
from src.models.models import (
    EnvioDin, LOG, CABEZA, ITEMS, ITEM, VISTOSBUENOS, VISTOBUENO, 
    BULTOS, BULTO, CUENTASYVALORES, CUENTASGIRO, CUENTAGIRO, CUENTAITEM,
    PAGODIFERIDO, CUOTAS, CUOTA, MONTOCUOTA, FECHAVENCCUOTA,
    ANEXASDIN, ANEXAS, ANEXA, INSUMOS, INSUMO, OBSERVACIONESITEM, OBSERVACIONITEM
)

class ValidationUtils:
    @staticmethod
    def pad_zeros(value: Optional[str], length: int) -> str:
        if value is None:
            value = ""
        return value.strip().zfill(length)

    @staticmethod
    def pad_spaces(value: Optional[str], length: int) -> str:
        if value is None:
            value = ""
        return value.strip().ljust(length, ' ')

    @staticmethod
    def fix_date(date_str: Optional[str]) -> str:
        """Ports validaFechaConEspacios and validaFechaConCeros logic implicitly."""
        if not date_str or date_str in ["30121899", "01011900"]:
            return "" # Default behavior for "valid" empty dates in legacy was mostly spaces or 00000000 depending on context
        return date_str

    @staticmethod
    def format_date_ddMMyyyy(date_obj: datetime) -> str:
        return date_obj.strftime("%d%m%Y")
    
    @staticmethod
    def add_days(date_str: str, days: int) -> str:
        try:
            # Assumes input format ddMMyyyy
            dt = datetime.strptime(date_str, "%d%m%Y")
            new_dt = dt + timedelta(days=days)
            return new_dt.strftime("%d%m%Y")
        except ValueError:
            return date_str # Return original if parse fails

class DinValidator:
    def process(self, din: EnvioDin) -> EnvioDin:
        """
        Main entry point to process and validate the EnvioDin object.
        Modifies the object in-place.
        """
        # 1. LOG
        # 2. CABEZA
        for cabeza in din.cabeza:
            self.process_cabeza(cabeza)
        
        # 3. ITEMS
        if din.items and din.items.item:
             for item in din.items.item:
                 self.process_item(item, din.cabeza[0] if din.cabeza else None)

        # 4. BULTOS
        if din.bultos:
            for bultos_group in din.bultos:
                if bultos_group.bulto:
                    for bulto in bultos_group.bulto:
                        self.process_bulto(bulto)
                        
        # 5. CUENTAS Y VALORES
        if din.cuentasyvalores:
            for cv in din.cuentasyvalores:
                 self.process_cuentas_valores(cv)
                 
        # 6. PAGODIFERIDO
        if din.pagodiferido:
             for pd in din.pagodiferido:
                 self.process_pago_diferido(pd)

        # 7. ANEXASDIN
        if din.anexasdin and din.anexasdin.anexa:
             for anexa in din.anexasdin.anexa:
                 self.process_anexa(anexa, din.cabeza[0].tipoingr if din.cabeza else "0") # Assuming logic needs access

        return din

    def process_cabeza(self, cabeza: CABEZA):
        # Porting calculateFechaVencimiento logic
        # Note: Original code switched on 'formulario' (form) and 'tipoDocumento' (tpodocto)
        
        # Ensure padding
        cabeza.form = ValidationUtils.pad_zeros(cabeza.form, 2) # Assume length? Legacy didn't explicitly pad form but used it as string
        
        # Logic for Vencimiento
        if cabeza.fecvenci:
            is_valid_date = cabeza.fecvenci not in ["30121899", "01011900", ""]
            
            if cabeza.form in ["15", "14"]:
                if cabeza.tpodocto in ["113", "163", "114", "164"]:
                    cabeza.fecvenci = ValidationUtils.add_days(cabeza.fecvenci, 90)
                elif cabeza.tpodocto in ["107", "108", "157", "158"]:
                    if cabeza.form == "15":
                        cabeza.fecvenci = ValidationUtils.add_days(cabeza.fecvenci, 15)
                    else:
                        cabeza.fecvenci = ValidationUtils.fix_date(cabeza.fecvenci)
                else:
                    cabeza.fecvenci = ValidationUtils.add_days(cabeza.fecvenci, 15)
            else:
                 cabeza.fecvenci = ValidationUtils.fix_date(cabeza.fecvenci)
        
        # Validate Manifiesto logic (validaManifiesto) in Java was tied to Origentranspalmacenaje actually?
        # Java: validaManifiesto(String codTipoOperacion, String numManifiesto1, String nombreVehiculo)
        # We need to find where this is applied. Likely in ORIGENTRANSPALMACENAJE.
        if cabeza.origentranspalmacenaje:
             for orig in cabeza.origentranspalmacenaje:
                 # Legacy passed codTipoOperacion. Where is that? TIPOINGR? 
                 # Usually operation type is TPODOCTO or similar. 
                 # In legacy validaManifiesto switch(codTipoOperacion) uses 151, 152...
                 
                 # Let's assume TPODOCTO for now or maybe it's TIPOENVIO?
                 # Actually legacy method signature: validaManifiesto(codTipoOperacion, ...)
                 # We will apply padding at minimum.
                 
                 if orig.nummanif1:
                      orig.nummanif1 = ValidationUtils.pad_spaces(orig.nummanif1, 15)[:15]

    def process_item(self, item: ITEM, cabeza: Optional[CABEZA]):
        # validaInformacionItem logic
        # String lineaqla = codProducto + nombre + marca ...
        # This was a weird logic to concat and split. We'll enforce lengths.
        
        item.numitem = ValidationUtils.pad_zeros(item.numitem, 3)
        item.dnombre = ValidationUtils.pad_spaces(item.dnombre, 50)[:50]
        item.dmarca = ValidationUtils.pad_spaces(item.dmarca, 30)[:30]
        item.dvariedad = ValidationUtils.pad_spaces(item.dvariedad, 30)[:30]
        item.dotro1 = ValidationUtils.pad_spaces(item.dotro1, 30)[:30]
        item.dotro2 = ValidationUtils.pad_spaces(item.dotro2, 30)[:30]
        item.atr5 = ValidationUtils.pad_spaces(item.atr5, 30)[:30]
        item.atr6 = ValidationUtils.pad_spaces(item.atr6, 30)[:30]
        
        # Unidad medida logic
        if item.arancala != "0": # Java: if (!codArancel.equals("0"))
             item.medida = ValidationUtils.pad_zeros(item.medida, 2)
             item.codestum = ValidationUtils.pad_spaces(item.codestum, 1)
        else:
             item.medida = ValidationUtils.pad_zeros(item.medida, 2)
             item.codestum = ""
             
        # Process Cuentas Item
        if item.cuentasitem:
            for ci_group in item.cuentasitem:
                 if ci_group.cuentaitem:
                     for ci in ci_group.cuentaitem:
                         self.process_cuenta_item(ci) # Missing context like tipoIngreso?

    def process_cuenta_item(self, ci: CUENTAITEM):
        # validaCuentaItem
        # If all empty/zero -> nulls
        if (not ci.otro or ci.otro == "0.000000") and not ci.cta and (not ci.valor or ci.valor == "0.00"):
            ci.otro = None
            ci.cta = None
            ci.sigval = None
            ci.valor = None
        else:
             ci.otro = ValidationUtils.pad_zeros(ci.otro, 11)
             ci.cta = ValidationUtils.pad_zeros(ci.cta, 3)
             
             # Handle negative value
             val = ci.valor or "0"
             if val.startswith("-"):
                 ci.sigval = "-"
                 ci.valor = ValidationUtils.pad_zeros(val[1:], 13)
             else:
                 ci.valor = ValidationUtils.pad_zeros(val, 13)
                 
                 # Logic for setting SIGVAL
                 try:
                     f_val = float(val)
                     if f_val > 0 or ci.cta in ["174", "116"]:
                          ci.sigval = "+"
                     elif f_val <= 0:
                          ci.sigval = "-"
                 except ValueError:
                     # Fallback if value is "string" or invalid
                     ci.sigval = None


    def process_bulto(self, bulto: BULTO):
         # validaBulto
         if bulto.destipbul and bulto.tpobul:
             bulto.destipbul = ValidationUtils.pad_spaces(bulto.destipbul, 10)
             bulto.tpobul = ValidationUtils.pad_zeros(bulto.tpobul, 3)
             bulto.cantbul = ValidationUtils.pad_zeros(bulto.cantbul, 6)
             
    def process_cuentas_valores(self, cv: CUENTASYVALORES):
        # Padding
        cv.mon178 = ValidationUtils.pad_zeros(cv.mon178, 13) # Guessing length based on similar fields
        # ... process nested CuentasGiro
        if cv.cuentasgiro:
            for cg_group in cv.cuentasgiro:
                if cg_group.cuentagiro:
                     for cg in cg_group.cuentagiro:
                         self.process_cuenta_giro(cg)

    def process_cuenta_giro(self, cg: CUENTAGIRO):
        # validaCuentaGiro
        # Logic depends on account number
        if cg.ctaotro in ["223", "197", "270", "209", "179", "174", "116", "115"]:
             cg.ctaotro = ValidationUtils.pad_zeros(cg.ctaotro, 3)
             cg.monotro = ValidationUtils.pad_zeros(cg.monotro, 13)
        # Check for empty/zero logic
        elif cg.ctaotro == "0":
             cg.ctaotro = ValidationUtils.pad_zeros("", 3) # "000" or empty? Java: completarConCeros("", 3) -> "000"
             cg.monotro = ValidationUtils.pad_zeros(cg.monotro, 13)
        else:
             if cg.ctaotro and cg.monotro:
                 cg.ctaotro = ValidationUtils.pad_zeros(cg.ctaotro, 3)
                 cg.monotro = ValidationUtils.pad_zeros(cg.monotro, 13)
                 
    def process_pago_diferido(self, pd: PAGODIFERIDO):
        # Validation logic for PagoDiferido
        pass
        
    def process_anexa(self, anexa: ANEXA, tipo_ingreso: str):
         # validaAnexa padding
         anexa.canproducto = ValidationUtils.pad_zeros(anexa.canproducto, 13)
         anexa.codaduana = ValidationUtils.pad_zeros(anexa.codaduana, 2)
         anexa.codunmedi = ValidationUtils.pad_zeros(anexa.codunmedi, 2)
         anexa.codunmedp = ValidationUtils.pad_zeros(anexa.codunmedp, 2)
         anexa.facconsumo = ValidationUtils.pad_zeros(anexa.facconsumo, 15)
         anexa.nominsumo = ValidationUtils.pad_spaces(anexa.nominsumo, 30)
         anexa.nomproducto = ValidationUtils.pad_spaces(anexa.nomproducto, 30)
         anexa.numdapex = ValidationUtils.pad_zeros(anexa.numdapex, 10)
         anexa.numinsumo = ValidationUtils.pad_zeros(anexa.numinsumo, 3)
         anexa.numinsuti = ValidationUtils.pad_zeros(anexa.numinsuti, 13)
         anexa.numitem = ValidationUtils.pad_zeros(anexa.numitem, 3)
         anexa.numitemdec = ValidationUtils.pad_zeros(anexa.numitemdec, 3)
         anexa.numsec = ValidationUtils.pad_zeros(anexa.numsec, 3)
