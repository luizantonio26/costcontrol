

from pydantic import BaseModel


class SecuritySettingsSchema(BaseModel):
    otp_configured: bool
    secret: str