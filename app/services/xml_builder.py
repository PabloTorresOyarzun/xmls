import os
import logging
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from lxml import etree

from app.models.din import DINModel

logger = logging.getLogger(__name__)

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"


class XMLBuilderService:
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.template = self.env.get_template("din_soap.xml.j2")

    def build_xml(self, din: DINModel) -> str:
        din_dict = din.model_dump(by_alias=False)
        # Renombrar 'items' para evitar conflicto con método builtin de dict
        if 'items' in din_dict:
            din_dict['items_list'] = din_dict.pop('items')
        xml_content = self.template.render(din=din_dict)
        return xml_content

    def build_xml_for_signing(self, din: DINModel) -> etree._Element:
        xml_str = self.build_xml(din)
        parser = etree.XMLParser(remove_blank_text=True)
        return etree.fromstring(xml_str.encode("utf-8"), parser=parser)

    def validate_xml_structure(self, xml_str: str) -> tuple[bool, str]:
        try:
            parser = etree.XMLParser(remove_blank_text=True)
            etree.fromstring(xml_str.encode("utf-8"), parser=parser)
            return True, "XML válido"
        except etree.XMLSyntaxError as e:
            logger.error(f"Error de sintaxis XML: {e}")
            return False, str(e)

    def prettify_xml(self, xml_str: str) -> str:
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.fromstring(xml_str.encode("utf-8"), parser=parser)
        return etree.tostring(tree, pretty_print=True, encoding="unicode")
