from pathlib import Path
from lxml import etree
from typing import Tuple, List, Optional


class XMLValidator:
    def __init__(self, schema_dir: Optional[Path] = None):
        if schema_dir is None:
            schema_dir = Path(__file__).parent.parent.parent / "docs" / "mensajeriaDin"
        self.schema_dir = schema_dir
        self._schema: Optional[etree.XMLSchema] = None

    @property
    def schema(self) -> etree.XMLSchema:
        if self._schema is None:
            self._schema = self._load_schema()
        return self._schema

    def _load_schema(self) -> etree.XMLSchema:
        schema_path = self.schema_dir / "EnvioDin.xsd"
        with open(schema_path, "rb") as f:
            schema_doc = etree.parse(f)
        return etree.XMLSchema(schema_doc)

    def validate(self, xml_content: str | bytes) -> Tuple[bool, List[str]]:
        """
        Validate XML content against the DIN schema.

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors: List[str] = []

        try:
            if isinstance(xml_content, str):
                xml_content = xml_content.encode("utf-8")

            doc = etree.fromstring(xml_content)
            is_valid = self.schema.validate(doc)

            if not is_valid:
                for error in self.schema.error_log:
                    errors.append(f"Line {error.line}: {error.message}")

            return is_valid, errors

        except etree.XMLSyntaxError as e:
            return False, [f"XML Syntax Error: {str(e)}"]
        except Exception as e:
            return False, [f"Validation Error: {str(e)}"]

    def validate_structure(self, xml_content: str | bytes) -> Tuple[bool, List[str]]:
        """
        Validate only the XML structure (well-formed check).
        """
        try:
            if isinstance(xml_content, str):
                xml_content = xml_content.encode("utf-8")

            etree.fromstring(xml_content)
            return True, []

        except etree.XMLSyntaxError as e:
            return False, [f"XML Syntax Error: {str(e)}"]
