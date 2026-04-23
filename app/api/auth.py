"""
Endpoints de autenticación:
  POST /auth/register  - Registra un nuevo usuario
  POST /auth/login     - Inicia sesión y devuelve un JWT
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import User
from app.schemas.auth import Token, UserOut, UserRegister
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.
    - Verifica que el username y el email no estén ya registrados.
    - Almacena la contraseña como hash bcrypt (nunca en texto plano).
    """
    # Verificar unicidad de username
    if db.query(User).filter(User.username == payload.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El username '{payload.username}' ya está registrado.",
        )
    # Verificar unicidad de email
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El email '{payload.email}' ya está registrado.",
        )

    new_user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hash_password(payload.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión (obtener JWT)",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Autentica al usuario con username + password (formulario OAuth2).
    Devuelve un Bearer Token JWT para usar en endpoints protegidos.
    """
    user = db.query(User).filter(User.username == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": user.username})
    return Token(access_token=token)
