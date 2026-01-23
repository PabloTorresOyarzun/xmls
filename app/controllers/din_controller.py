import logging
from litestar import Controller, get, post
from litestar.response import Response
from litestar.status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from pydantic import BaseModel
from typing import Optional

from app.models.din import DINRequest, DINResponse, StatusResponse
from app.services.xml_builder import XMLBuilderService
from app.services.signer import SignerService
from app.services.soap_client import SoapClientService
from app.config import get_settings

logger = logging.getLogger(__name__)


class CertTestRequest(BaseModel):
    cert_path: str
    password: str


class CertTestResponse(BaseModel):
    success: bool
    message: str
    subject: Optional[str] = None
    issuer: Optional[str] = None
    valid_from: Optional[str] = None
    valid_until: Optional[str] = None


class DINController(Controller):
    path = "/api/v1/din"
    tags = ["DIN"]

    @post("/test-cert")
    async def test_certificate(self, data: CertTestRequest) -> Response[CertTestResponse]:
        """Endpoint para probar contraseñas de certificados."""
        from pathlib import Path
        from cryptography.hazmat.primitives.serialization import pkcs12

        cert_path = Path(data.cert_path)
        if not cert_path.exists():
            return Response(
                content=CertTestResponse(
                    success=False,
                    message=f"Archivo no encontrado: {cert_path}",
                ),
                status_code=HTTP_400_BAD_REQUEST,
            )

        try:
            with open(cert_path, "rb") as f:
                pfx_data = f.read()

            password = data.password.encode("utf-8") if data.password else None

            key, cert, chain = pkcs12.load_key_and_certificates(
                pfx_data, password
            )

            return Response(
                content=CertTestResponse(
                    success=True,
                    message="Certificado cargado correctamente",
                    subject=cert.subject.rfc4514_string(),
                    issuer=cert.issuer.rfc4514_string(),
                    valid_from=cert.not_valid_before_utc.isoformat(),
                    valid_until=cert.not_valid_after_utc.isoformat(),
                ),
                status_code=HTTP_200_OK,
            )

        except ValueError as e:
            return Response(
                content=CertTestResponse(
                    success=False,
                    message=f"Contraseña incorrecta o archivo inválido: {str(e)}",
                ),
                status_code=HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                content=CertTestResponse(
                    success=False,
                    message=f"Error: {str(e)}",
                ),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @get("/list-certs")
    async def list_certificates(self) -> dict:
        """Lista los certificados disponibles en /app/certs."""
        from pathlib import Path
        certs_dir = Path("/app/certs")
        if not certs_dir.exists():
            return {"certs": [], "message": "Directorio /app/certs no existe"}

        certs = list(certs_dir.glob("*.pfx")) + list(certs_dir.glob("*.p12"))
        return {"certs": [str(c) for c in certs]}

    @post("/generate-xml-unsigned")
    async def generate_xml_unsigned(self, data: DINRequest) -> Response[DINResponse]:
        """Genera XML sin firma digital (para testing/validación)."""
        try:
            logger.info("Generando XML sin firma")

            xml_builder = XMLBuilderService()
            xml_unsigned = xml_builder.build_xml(data.din)

            valid, msg = xml_builder.validate_xml_structure(xml_unsigned)
            if not valid:
                return Response(
                    content=DINResponse(
                        success=False,
                        message=f"Error en estructura XML: {msg}",
                    ),
                    status_code=HTTP_400_BAD_REQUEST,
                )

            return Response(
                content=DINResponse(
                    success=True,
                    message="XML generado correctamente (sin firma)",
                    xml=xml_unsigned,
                ),
                status_code=HTTP_200_OK,
            )

        except Exception as e:
            logger.error(f"Error generando XML: {e}", exc_info=True)
            return Response(
                content=DINResponse(
                    success=False,
                    message=f"Error interno: {str(e)}",
                ),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @post("/generate-signed-xml")
    async def generate_signed_xml(self, data: DINRequest) -> Response[DINResponse]:
        try:
            logger.info("Iniciando generación de XML firmado")

            xml_builder = XMLBuilderService()
            xml_unsigned = xml_builder.build_xml(data.din)

            valid, msg = xml_builder.validate_xml_structure(xml_unsigned)
            if not valid:
                logger.error(f"XML generado inválido: {msg}")
                return Response(
                    content=DINResponse(
                        success=False,
                        message=f"Error en estructura XML: {msg}",
                    ),
                    status_code=HTTP_400_BAD_REQUEST,
                )

            signer = SignerService()
            signed_xml = signer.sign_xml_string(xml_unsigned)

            logger.info("XML firmado generado exitosamente")

            return Response(
                content=DINResponse(
                    success=True,
                    message="XML firmado generado correctamente",
                    xml=signed_xml,
                ),
                status_code=HTTP_200_OK,
            )

        except FileNotFoundError as e:
            logger.error(f"Certificado no encontrado: {e}")
            return Response(
                content=DINResponse(
                    success=False,
                    message=f"Error de certificado: {str(e)}",
                ),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Error generando XML: {e}", exc_info=True)
            return Response(
                content=DINResponse(
                    success=False,
                    message=f"Error interno: {str(e)}",
                ),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @post("/send")
    async def send_din(self, data: DINRequest) -> Response[DINResponse]:
        try:
            logger.info("Iniciando envío de DIN a Aduana")

            xml_builder = XMLBuilderService()
            xml_unsigned = xml_builder.build_xml(data.din)

            valid, msg = xml_builder.validate_xml_structure(xml_unsigned)
            if not valid:
                logger.error(f"XML generado inválido: {msg}")
                return Response(
                    content=DINResponse(
                        success=False,
                        message=f"Error en estructura XML: {msg}",
                    ),
                    status_code=HTTP_400_BAD_REQUEST,
                )

            signer = SignerService()
            signed_xml = signer.sign_xml_string(xml_unsigned)

            soap_client = SoapClientService()
            result = await soap_client.send_din(signed_xml)

            if result["success"]:
                logger.info(f"DIN enviado exitosamente. Ticket: {result.get('ticket')}")
                return Response(
                    content=DINResponse(
                        success=True,
                        ticket=result.get("ticket"),
                        message=result.get("message", "Envío exitoso"),
                        raw_response=result.get("raw_response"),
                    ),
                    status_code=HTTP_200_OK,
                )
            else:
                logger.warning(f"Error en envío DIN: {result.get('message')}")
                return Response(
                    content=DINResponse(
                        success=False,
                        message=result.get("message", "Error en envío"),
                        raw_response=result.get("raw_response"),
                    ),
                    status_code=HTTP_400_BAD_REQUEST,
                )

        except FileNotFoundError as e:
            logger.error(f"Certificado no encontrado: {e}")
            return Response(
                content=DINResponse(
                    success=False,
                    message=f"Error de certificado: {str(e)}",
                ),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Error enviando DIN: {e}", exc_info=True)
            return Response(
                content=DINResponse(
                    success=False,
                    message=f"Error interno: {str(e)}",
                ),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @get("/status/{ticket_id:str}")
    async def get_status(self, ticket_id: str) -> Response[StatusResponse]:
        try:
            logger.info(f"Consultando estado de ticket: {ticket_id}")

            soap_client = SoapClientService()
            result = await soap_client.consulta_din(ticket_id)

            if result["success"]:
                return Response(
                    content=StatusResponse(
                        success=True,
                        status=result.get("estado"),
                        message="Consulta exitosa",
                        details=result.get("detalles"),
                    ),
                    status_code=HTTP_200_OK,
                )
            else:
                return Response(
                    content=StatusResponse(
                        success=False,
                        message=result.get("message", "Error en consulta"),
                    ),
                    status_code=HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            logger.error(f"Error consultando estado: {e}", exc_info=True)
            return Response(
                content=StatusResponse(
                    success=False,
                    message=f"Error interno: {str(e)}",
                ),
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            )
