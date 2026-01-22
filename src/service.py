import traceback
import sys
from src.models.models import EnvioDin
from src.validations import DinValidator

def generate_din_xml(data: EnvioDin) -> str:
    """
    Generates the signed XML for the DIN wrapped in a SOAP Envelope.
    """
    try:
        # 1. Aplicar validaciones y formateo de datos
        validator = DinValidator()
        data = validator.process(data)
        
        # 2. Generar el XML interno (DIN) con los namespaces correctos
        # encoding='UTF-8' devuelve bytes, lo decodificamos a string
        din_xml_bytes = data.to_xml(encoding='UTF-8', standalone=None)
        din_xml_str = din_xml_bytes.decode('utf-8')
        
        # 3. Envolver en el Envelope SOAP
        # El servicio de Aduana espera que el DIN viaje dentro del Body SOAP.
        soap_envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soapenv:Header/>
   <soapenv:Body>
{din_xml_str}
   </soapenv:Body>
</soapenv:Envelope>"""

        return soap_envelope

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        raise e