import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise ValueError(
        "La variable de entorno JWT_SECRET_KEY no está configurada. "
        "Configurá esta variable antes de iniciar el backend."
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def verificar_password(password_plana, password_hash):
    return pwd_context.verify(password_plana, password_hash)


def generar_hash(password):
    return pwd_context.hash(password)


def crear_token_acceso(datos):
    datos_token = datos.copy()

    vencimiento = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    datos_token.update({
        "exp": vencimiento
    })

    return jwt.encode(
        datos_token,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decodificar_token(token):
    try:
        datos = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return datos

    except JWTError:
        return None