"""Schemas Pydantic para autenticación."""
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    """Payload para registrar un nuevo usuario."""
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    """Respuesta pública de un usuario (sin contraseña)."""
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    """Respuesta del endpoint /login."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Datos extraídos del JWT."""
    username: str | None = None
