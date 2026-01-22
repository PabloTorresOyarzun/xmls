import traceback
import sys
from src.models.models import EnvioDin
from src.validations import DinValidator

def generate_din_xml(data: EnvioDin) -> str:
    """
    Generates the signed XML for the DIN.
    """
    try:
        # Apply validations and normalizations
        validator = DinValidator()
        data = validator.process(data)
        
        # Serialize to XML
        # we enforce UTF-8 and declaration
        xml_bytes = data.to_xml(encoding='UTF-8')
        
        return xml_bytes.decode('utf-8')
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        raise e
