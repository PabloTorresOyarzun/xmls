from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from functools import lru_cache


class AgentConfig(BaseSettings):
    cod_agente: str
    cert_path: str
    cert_password: str
    ws_user: str
    ws_password_qa: str
    ws_password_prod: Optional[str] = ""


class Settings(BaseSettings):
    app_env: str = Field(default="testing", alias="APP_ENV")
    log_level: str = Field(default="DEBUG", alias="LOG_LEVEL")
    active_agent: str = Field(default="G02", alias="ACTIVE_AGENT")

    c25_cod_agente: str = Field(default="C25", alias="C25_COD_AGENTE")
    c25_cert_path: str = Field(default="/app/certs/C25.pfx", alias="C25_CERT_PATH")
    c25_cert_password: str = Field(default="", alias="C25_CERT_PASSWORD")
    c25_ws_user: str = Field(default="", alias="C25_WS_USER")
    c25_ws_password_qa: str = Field(default="", alias="C25_WS_PASSWORD_QA")
    c25_ws_password_prod: str = Field(default="", alias="C25_WS_PASSWORD_PROD")

    g02_cod_agente: str = Field(default="G02", alias="G02_COD_AGENTE")
    g02_cert_path: str = Field(default="/app/certs/G02.pfx", alias="G02_CERT_PATH")
    g02_cert_password: str = Field(default="", alias="G02_CERT_PASSWORD")
    g02_ws_user: str = Field(default="", alias="G02_WS_USER")
    g02_ws_password_qa: str = Field(default="", alias="G02_WS_PASSWORD_QA")
    g02_ws_password_prod: str = Field(default="", alias="G02_WS_PASSWORD_PROD")

    c74_cod_agente: str = Field(default="C74", alias="C74_COD_AGENTE")
    c74_cert_path: str = Field(default="/app/certs/C74.pfx", alias="C74_CERT_PATH")
    c74_cert_password: str = Field(default="", alias="C74_CERT_PASSWORD")
    c74_ws_user: str = Field(default="", alias="C74_WS_USER")
    c74_ws_password_qa: str = Field(default="", alias="C74_WS_PASSWORD_QA")
    c74_ws_password_prod: str = Field(default="", alias="C74_WS_PASSWORD_PROD")

    aduana_recibe_din_url: str = Field(
        default="http://testsoa.aduana.cl/MensajeriaServicios/http/RecibeDin",
        alias="ADUANA_RECIBE_DIN_URL",
    )
    aduana_consulta_din_url: str = Field(
        default="http://testsoa.aduana.cl/ConsultaServiciosESB/http/servicioConsultaDIN",
        alias="ADUANA_CONSULTA_DIN_URL",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

    def get_active_agent_config(self) -> AgentConfig:
        agent = self.active_agent.upper()
        if agent == "C25":
            return AgentConfig(
                cod_agente=self.c25_cod_agente,
                cert_path=self.c25_cert_path,
                cert_password=self.c25_cert_password,
                ws_user=self.c25_ws_user,
                ws_password_qa=self.c25_ws_password_qa,
                ws_password_prod=self.c25_ws_password_prod,
            )
        elif agent == "G02":
            return AgentConfig(
                cod_agente=self.g02_cod_agente,
                cert_path=self.g02_cert_path,
                cert_password=self.g02_cert_password,
                ws_user=self.g02_ws_user,
                ws_password_qa=self.g02_ws_password_qa,
                ws_password_prod=self.g02_ws_password_prod,
            )
        elif agent == "C74":
            return AgentConfig(
                cod_agente=self.c74_cod_agente,
                cert_path=self.c74_cert_path,
                cert_password=self.c74_cert_password,
                ws_user=self.c74_ws_user,
                ws_password_qa=self.c74_ws_password_qa,
                ws_password_prod=self.c74_ws_password_prod,
            )
        else:
            raise ValueError(f"Agente no válido: {agent}")

    def get_ws_password(self) -> str:
        agent_config = self.get_active_agent_config()
        if self.app_env == "production":
            return agent_config.ws_password_prod
        return agent_config.ws_password_qa


@lru_cache
def get_settings() -> Settings:
    return Settings()
