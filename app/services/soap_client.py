import logging
import httpx
from lxml import etree

from app.config import get_settings

logger = logging.getLogger(__name__)

SOAP_NS = "http://schemas.xmlsoap.org/soap/envelope/"


class SoapClientService:
    def __init__(self):
        self.settings = get_settings()
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def send_din(self, signed_xml: str) -> dict:
        url = self.settings.aduana_recibe_din_url
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": '""',
        }

        logger.info(f"Enviando DIN a: {url}")
        logger.debug(f"XML a enviar (primeros 500 chars): {signed_xml[:500]}")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    content=signed_xml.encode("utf-8"),
                    headers=headers,
                )

            logger.info(f"Respuesta HTTP Status: {response.status_code}")
            logger.debug(f"Respuesta completa: {response.text}")

            return self._parse_response(response)

        except httpx.TimeoutException as e:
            logger.error(f"Timeout en envío a Aduana: {e}")
            return {
                "success": False,
                "error": "TIMEOUT",
                "message": f"Timeout de conexión: {str(e)}",
                "raw_response": None,
            }
        except httpx.RequestError as e:
            logger.error(f"Error de conexión con Aduana: {e}")
            return {
                "success": False,
                "error": "CONNECTION_ERROR",
                "message": f"Error de conexión: {str(e)}",
                "raw_response": None,
            }
        except Exception as e:
            logger.error(f"Error inesperado en envío: {e}", exc_info=True)
            return {
                "success": False,
                "error": "UNEXPECTED_ERROR",
                "message": str(e),
                "raw_response": None,
            }

    async def consulta_din(self, ticket_id: str) -> dict:
        url = self.settings.aduana_consulta_din_url
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": '""',
        }

        consulta_xml = self._build_consulta_xml(ticket_id)

        logger.info(f"Consultando DIN ticket: {ticket_id}")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    content=consulta_xml.encode("utf-8"),
                    headers=headers,
                )

            logger.info(f"Respuesta consulta HTTP Status: {response.status_code}")

            return self._parse_consulta_response(response)

        except httpx.TimeoutException as e:
            logger.error(f"Timeout en consulta: {e}")
            return {
                "success": False,
                "error": "TIMEOUT",
                "message": f"Timeout de conexión: {str(e)}",
            }
        except Exception as e:
            logger.error(f"Error en consulta: {e}", exc_info=True)
            return {
                "success": False,
                "error": "UNEXPECTED_ERROR",
                "message": str(e),
            }

    def _parse_response(self, response: httpx.Response) -> dict:
        raw_text = response.text

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP_{response.status_code}",
                "message": f"Error HTTP {response.status_code}",
                "raw_response": raw_text,
            }

        try:
            tree = etree.fromstring(raw_text.encode("utf-8"))

            fault = tree.find(f".//{{{SOAP_NS}}}Fault")
            if fault is not None:
                fault_string = fault.findtext("faultstring", "Error desconocido")
                fault_code = fault.findtext("faultcode", "UNKNOWN")
                return {
                    "success": False,
                    "error": fault_code,
                    "message": fault_string,
                    "raw_response": raw_text,
                }

            ticket = self._extract_ticket(tree)
            estado = self._extract_estado(tree)

            return {
                "success": True,
                "ticket": ticket,
                "estado": estado,
                "message": "DIN enviado correctamente",
                "raw_response": raw_text,
            }

        except etree.XMLSyntaxError as e:
            logger.error(f"Error parseando respuesta XML: {e}")
            return {
                "success": False,
                "error": "XML_PARSE_ERROR",
                "message": f"Error parseando respuesta: {str(e)}",
                "raw_response": raw_text,
            }

    def _parse_consulta_response(self, response: httpx.Response) -> dict:
        raw_text = response.text

        if response.status_code != 200:
            return {
                "success": False,
                "error": f"HTTP_{response.status_code}",
                "message": f"Error HTTP {response.status_code}",
                "raw_response": raw_text,
            }

        try:
            tree = etree.fromstring(raw_text.encode("utf-8"))
            estado = self._extract_estado(tree)
            detalles = self._extract_detalles_consulta(tree)

            return {
                "success": True,
                "estado": estado,
                "detalles": detalles,
                "raw_response": raw_text,
            }

        except Exception as e:
            logger.error(f"Error parseando consulta: {e}")
            return {
                "success": False,
                "error": "PARSE_ERROR",
                "message": str(e),
                "raw_response": raw_text,
            }

    def _extract_ticket(self, tree: etree._Element) -> str:
        paths = [
            ".//TICKET",
            ".//ticket",
            ".//{*}TICKET",
            ".//{*}ticket",
            ".//NUMEROENCRIPTADO",
            ".//{*}NUMEROENCRIPTADO",
        ]

        for path in paths:
            elem = tree.find(path)
            if elem is not None and elem.text:
                return elem.text.strip()

        return None

    def _extract_estado(self, tree: etree._Element) -> str:
        paths = [
            ".//ESTADO",
            ".//estado",
            ".//{*}ESTADO",
            ".//{*}estado",
        ]

        for path in paths:
            elem = tree.find(path)
            if elem is not None and elem.text:
                return elem.text.strip()

        return None

    def _extract_detalles_consulta(self, tree: etree._Element) -> dict:
        detalles = {}

        campos = [
            "ESTADO",
            "TIPOSELECCION",
            "FECHACEPTACION",
            "NUMEROENCRIPTADO",
            "NUMEROACEPTACION",
        ]

        for campo in campos:
            elem = tree.find(f".//{{{SOAP_NS}}}{campo}") or tree.find(f".//{campo}")
            if elem is not None and elem.text:
                detalles[campo.lower()] = elem.text.strip()

        return detalles

    def _build_consulta_xml(self, ticket_id: str) -> str:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header/>
    <soapenv:Body>
        <ConsultaDIN>
            <TICKET>{ticket_id}</TICKET>
        </ConsultaDIN>
    </soapenv:Body>
</soapenv:Envelope>"""
