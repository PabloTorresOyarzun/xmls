import logging
from litestar import Litestar, get
from litestar.openapi import OpenAPIConfig
from litestar.logging import LoggingConfig

from app.controllers import DINController
from app.config import get_settings

settings = get_settings()

logging_config = LoggingConfig(
    root={"level": settings.log_level, "handlers": ["console"]},
    formatters={
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        }
    },
    loggers={
        "app": {"level": settings.log_level, "handlers": ["console"]},
        "httpx": {"level": "INFO", "handlers": ["console"]},
    },
)


@get("/health")
async def health_check() -> dict:
    return {"status": "healthy", "environment": settings.app_env}


@get("/")
async def root() -> dict:
    return {
        "service": "DIN API - Aduana Chile",
        "version": "1.0.0",
        "environment": settings.app_env,
        "active_agent": settings.active_agent,
    }


app = Litestar(
    route_handlers=[root, health_check, DINController],
    openapi_config=OpenAPIConfig(
        title="DIN API - Aduana Chile",
        version="1.0.0",
        description="API para tramitación de Declaraciones de Ingreso (DIN) ante Aduana Chile",
    ),
    logging_config=logging_config,
    debug=settings.app_env != "production",
)
