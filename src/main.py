from litestar import Litestar, post
from litestar.openapi.config import OpenAPIConfig
from litestar.status_codes import HTTP_201_CREATED
from litestar.response import Response
from src.models.models import EnvioDin
from src.service import generate_din_xml

@post("/din/generate", status_code=HTTP_201_CREATED, media_type="application/xml")
async def create_din(data: EnvioDin) -> Response[str]:
    # Litestar automatically parses the body into EnvioDin if the Content-Type is application/json or compatible
    # However, for XML input, we might need a custom extractor or just accept the object.
    # The user said "haga la confeccion de la din", implies input might be JSON (data) -> Output XML (DIN).
    # Since we use EnvioDin as input, Litestar expects JSON by default matching the model.
    # We return the generated XML.
    
    xml_content = generate_din_xml(data)
    
    return Response(content=xml_content, media_type="application/xml")

app = Litestar(
    route_handlers=[create_din],
    openapi_config=OpenAPIConfig(title="DIN Service", version="1.0.0")
)
