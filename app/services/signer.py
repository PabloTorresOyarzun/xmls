import logging
from pathlib import Path
from lxml import etree
from signxml import XMLSigner, methods
from cryptography.hazmat.primitives.serialization import pkcs12
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import Certificate
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from app.config import get_settings, AgentConfig

logger = logging.getLogger(__name__)

XMLDSIG_NS = "http://www.w3.org/2000/09/xmldsig#"
SOAP_NS = "http://schemas.xmlsoap.org/soap/envelope/"


class SignerService:
    def __init__(self, agent_config: AgentConfig = None):
        self.settings = get_settings()
        self.agent_config = agent_config or self.settings.get_active_agent_config()
        self._private_key: RSAPrivateKey = None
        self._certificate: Certificate = None
        self._load_certificate()

    def _load_certificate(self):
        cert_path = Path(self.agent_config.cert_path)
        if not cert_path.exists():
            raise FileNotFoundError(f"Certificado no encontrado: {cert_path}")

        with open(cert_path, "rb") as f:
            pfx_data = f.read()

        password = self.agent_config.cert_password.encode("utf-8")

        try:
            self._private_key, self._certificate, _ = pkcs12.load_key_and_certificates(
                pfx_data, password, default_backend()
            )
            logger.info(f"Certificado cargado: {self.agent_config.cod_agente}")
        except Exception as e:
            logger.error(f"Error cargando certificado: {e}")
            raise

    def sign_xml(self, xml_tree: etree._Element) -> etree._Element:
        body = xml_tree.find(f".//{{{SOAP_NS}}}Body")
        if body is None:
            raise ValueError("No se encontró el elemento Body en el SOAP Envelope")

        din_element = body.find("DIN")
        if din_element is None:
            for child in body:
                if child.tag.endswith("DIN") or "DIN" in child.tag:
                    din_element = child
                    break

        if din_element is None:
            raise ValueError("No se encontró el elemento DIN dentro del Body")

        signer = XMLSigner(
            method=methods.enveloped,
            signature_algorithm="rsa-sha1",
            digest_algorithm="sha1",
            c14n_algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315",
        )

        signed_din = signer.sign(
            din_element,
            key=self._private_key,
            cert=self._certificate,
            reference_uri="",
        )

        body.remove(din_element)
        body.append(signed_din)

        return xml_tree

    def sign_xml_string(self, xml_str: str) -> str:
        parser = etree.XMLParser(remove_blank_text=True)
        xml_tree = etree.fromstring(xml_str.encode("utf-8"), parser=parser)
        signed_tree = self.sign_xml(xml_tree)
        return etree.tostring(signed_tree, encoding="unicode", xml_declaration=True)

    def get_certificate_info(self) -> dict:
        if self._certificate is None:
            return {}

        return {
            "subject": self._certificate.subject.rfc4514_string(),
            "issuer": self._certificate.issuer.rfc4514_string(),
            "serial_number": str(self._certificate.serial_number),
            "not_valid_before": self._certificate.not_valid_before_utc.isoformat(),
            "not_valid_after": self._certificate.not_valid_after_utc.isoformat(),
        }
