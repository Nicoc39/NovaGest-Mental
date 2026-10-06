from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from database import conexion
from auth import (
    generar_hash,
    verificar_password,
    crear_token_acceso,
    decodificar_token
)

seguridad = HTTPBearer()


def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(seguridad)
):
    token = credenciales.credentials

    datos = decodificar_token(token)

    if datos is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado"
        )

    return datos

def verificar_roles(*roles_permitidos):
    def verificar(usuario=Depends(obtener_usuario_actual)):
        if usuario["rol"] not in roles_permitidos:
            raise HTTPException(
                status_code=403,
                detail="No tenés permisos para realizar esta acción"
            )

        return usuario

    return verificar

def obtener_consultorios_usuario(usuario):
    cursor = conexion.cursor()

    try:
        if usuario["rol"] == "SUPERADMIN":
            cursor.execute("""
                SELECT id_consultorio
                FROM consultorio;
            """)

        elif usuario["rol"] == "PROFESIONAL":
            cursor.execute("""
                SELECT id_consultorio
                FROM consultorio_profesional cp
                JOIN profesional p
                    ON p.id_profesional = cp.id_profesional
                WHERE p.id_usuario = %s;
            """, (int(usuario["sub"]),))

        else:
            cursor.execute("""
                SELECT id_consultorio
                FROM consultorio_usuario
                WHERE id_usuario = %s;
            """, (int(usuario["sub"]),))

        consultorios = cursor.fetchall()

        return [fila[0] for fila in consultorios]

    finally:
        cursor.close()


app = FastAPI(

    title="NovaGest Mental",

    swagger_ui_parameters={

        "persistAuthorization": True

    }

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://novagest-mental.netlify.app",
        "https://nicoc39.github.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




class Consultorio(BaseModel):
    nombre: str
    direccion: str | None = None
    telefono: str | None = None
    email: str | None = None

class Paciente(BaseModel):
    id_consultorio: int
    nombre: str
    apellido: str
    dni: str
    fecha_nacimiento: str | None = None
    telefono: str | None = None
    email: str | None = None


class Profesional(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str
    matricula: str
    especialidad: str | None = None
    id_consultorio: int


class Usuario(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str
    rol: str
    id_consultorio: int

class Login(BaseModel):
    email: str
    password: str

@app.post("/login")
def iniciar_sesion(login: Login):
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT id_usuario,
                   nombre,
                   apellido,
                   email,
                   password_hash,
                   rol,
                   activo
            FROM usuario
            WHERE email = %s;
        """, (login.email,))

        usuario = cursor.fetchone()

        if usuario is None:
            raise HTTPException(
                status_code=401,
                detail="Email o contraseña incorrectos"
            )

        if not usuario[6]:
            raise HTTPException(
                status_code=403,
                detail="El usuario está inactivo"
            )

        if not verificar_password(login.password, usuario[4]):
            raise HTTPException(
                status_code=401,
                detail="Email o contraseña incorrectos"
            )

        token = crear_token_acceso({
            "sub": str(usuario[0]),
            "rol": usuario[5]
        })

        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id_usuario": usuario[0],
                "nombre": usuario[1],
                "apellido": usuario[2],
                "email": usuario[3],
                "rol": usuario[5]
            }
        }

    finally:
        cursor.close()



class HistoriaClinica(BaseModel):
    id_paciente: int
    fecha_apertura: str
    observaciones: str | None = None


@app.get("/consultorios")
def listar_consultorios(
    usuario=Depends(obtener_usuario_actual)
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if not consultorios:
            return []

        cursor.execute("""
            SELECT id_consultorio,
                   nombre,
                   direccion,
                   telefono,
                   email
            FROM consultorio
            WHERE id_consultorio = ANY(%s)
            ORDER BY id_consultorio;
        """, (consultorios,))

        resultados = cursor.fetchall()

        respuesta = []

        for consultorio in resultados:
            respuesta.append({
                "id_consultorio": consultorio[0],
                "nombre": consultorio[1],
                "direccion": consultorio[2],
                "telefono": consultorio[3],
                "email": consultorio[4]
            })

        return respuesta

    finally:
        cursor.close()


@app.post("/consultorios")
def crear_consultorio(
    consultorio: Consultorio,
    usuario=Depends(verificar_roles("SUPERADMIN"))
):
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO consultorio
            (nombre, direccion, telefono, email)
            VALUES (%s, %s, %s, %s)
            RETURNING id_consultorio;
        """, (
            consultorio.nombre,
            consultorio.direccion,
            consultorio.telefono,
            consultorio.email
        ))

        id_nuevo = cursor.fetchone()[0]

        conexion.commit()

        return {
            "mensaje": "Consultorio creado correctamente",
            "id_consultorio": id_nuevo
        }

    except Exception as error:
        conexion.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()

@app.get("/")
def inicio():
    return {"mensaje": "NovaGest Mental API funcionando"}





@app.get("/pacientes")
def listar_pacientes(usuario=Depends(obtener_usuario_actual)):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if not consultorios:
            return []

        cursor.execute("""
            SELECT p.id_paciente,
                   p.id_consultorio,
                   p.nombre,
                   p.apellido,
                   p.dni,
                   p.fecha_nacimiento,
                   p.telefono,
                   p.email,
                   p.activo,
                   os.nombre,
                   pos.numero_afiliado
            FROM paciente p
            LEFT JOIN paciente_obra_social pos
                ON p.id_paciente = pos.id_paciente
                AND pos.activo = TRUE
            LEFT JOIN obra_social os
                ON pos.id_obra_social = os.id_obra_social
            WHERE p.id_consultorio = ANY(%s)
              AND p.activo = TRUE
            ORDER BY p.id_paciente;
        """, (consultorios,))

        pacientes = cursor.fetchall()

        resultado = []

        for paciente in pacientes:
            resultado.append({
                "id_paciente": paciente[0],
                "id_consultorio": paciente[1],
                "nombre": paciente[2],
                "apellido": paciente[3],
                "dni": paciente[4],
                "fecha_nacimiento": paciente[5],
                "telefono": paciente[6],
                "email": paciente[7],
                "obra_social": paciente[9],
                "numero_afiliado": paciente[10]
            })

        return resultado

    finally:
        cursor.close()

@app.get("/historias-clinicas")
def listar_historias_clinicas(
    usuario=Depends(
        verificar_roles("SUPERADMIN", "ADMINISTRADOR", "PROFESIONAL")
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if not consultorios:
            return []

        cursor.execute("""
            SELECT h.id_historia,
                   h.id_paciente,
                   p.nombre,
                   p.apellido,
                   h.fecha_apertura,
                   h.observaciones
            FROM historia_clinica h
            INNER JOIN paciente p
                ON h.id_paciente = p.id_paciente
            WHERE p.id_consultorio = ANY(%s)
            ORDER BY h.id_historia;
        """, (consultorios,))

        historias = cursor.fetchall()

        resultado = []

        for historia in historias:
            resultado.append({
                "id_historia": historia[0],
                "id_paciente": historia[1],
                "paciente": historia[2] + " " + historia[3],
                "fecha_apertura": historia[4],
                "observaciones": historia[5]
            })

        return resultado

    finally:
        cursor.close()

@app.post("/historias-clinicas")
def crear_historia_clinica(
    historia: HistoriaClinica,
    usuario=Depends(
        verificar_roles("SUPERADMIN", "ADMINISTRADOR", "PROFESIONAL")
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        cursor.execute("""
            SELECT id_consultorio
            FROM paciente
            WHERE id_paciente = %s;
        """, (historia.id_paciente,))

        paciente_existente = cursor.fetchone()

        if paciente_existente is None:
            raise HTTPException(
                status_code=404,
                detail="El paciente no existe"
            )

        if paciente_existente[0] not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a este paciente"
            )

        cursor.execute("""
            SELECT id_historia
            FROM historia_clinica
            WHERE id_paciente = %s;
        """, (historia.id_paciente,))

        historia_existente = cursor.fetchone()

        if historia_existente is not None:
            raise HTTPException(
                status_code=400,
                detail="El paciente ya tiene una historia clínica"
            )

        cursor.execute("""
            INSERT INTO historia_clinica
            (id_paciente, fecha_apertura, observaciones)
            VALUES (%s, %s, %s)
            RETURNING id_historia;
        """, (
            historia.id_paciente,
            historia.fecha_apertura,
            historia.observaciones
        ))

        id_nuevo = cursor.fetchone()[0]

        conexion.commit()

        return {
            "mensaje": "Historia clínica creada correctamente",
            "id_historia": id_nuevo
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()


@app.post("/pacientes")
def crear_paciente(
    paciente: Paciente,
    usuario=Depends(obtener_usuario_actual)
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if paciente.id_consultorio not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a este consultorio"
            )

        cursor.execute("""
            SELECT id_paciente
            FROM paciente
            WHERE id_consultorio = %s
              AND dni = %s;
        """, (
            paciente.id_consultorio,
            paciente.dni
        ))

        paciente_existente = cursor.fetchone()

        if paciente_existente is not None:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un paciente con ese DNI en este consultorio"
            )

        cursor.execute("""
            INSERT INTO paciente
            (id_consultorio, nombre, apellido, dni,
             fecha_nacimiento, telefono, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_paciente;
        """, (
            paciente.id_consultorio,
            paciente.nombre,
            paciente.apellido,
            paciente.dni,
            paciente.fecha_nacimiento,
            paciente.telefono,
            paciente.email
        ))

        id_nuevo = cursor.fetchone()[0]
        conexion.commit()

        return {
            "mensaje": "Paciente creado correctamente",
            "id_paciente": id_nuevo
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()

@app.get("/pacientes/{id_paciente}")
def obtener_paciente(
    id_paciente: int,
    usuario=Depends(obtener_usuario_actual)
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        cursor.execute("""
            SELECT id_paciente,
                   id_consultorio,
                   nombre,
                   apellido,
                   dni,
                   fecha_nacimiento,
                   telefono,
                   email
            FROM paciente
            WHERE id_paciente = %s;
        """, (id_paciente,))

        paciente = cursor.fetchone()

        if paciente is None:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        if paciente[1] not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a este paciente"
            )

        return {
            "id_paciente": paciente[0],
            "id_consultorio": paciente[1],
            "nombre": paciente[2],
            "apellido": paciente[3],
            "dni": paciente[4],
            "fecha_nacimiento": paciente[5],
            "telefono": paciente[6],
            "email": paciente[7]
        }

    finally:
        cursor.close()

@app.put("/pacientes/{id_paciente}")
def modificar_paciente(
    id_paciente: int,
    paciente: Paciente,
    usuario=Depends(obtener_usuario_actual)
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        cursor.execute("""
            SELECT id_consultorio
            FROM paciente
            WHERE id_paciente = %s;
        """, (id_paciente,))

        paciente_actual = cursor.fetchone()

        if paciente_actual is None:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        if paciente_actual[0] not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a este paciente"
            )

        if paciente.id_consultorio != paciente_actual[0]:
            raise HTTPException(
                status_code=403,
                detail="No podés cambiar el paciente de consultorio"
            )

        cursor.execute("""
            UPDATE paciente
            SET nombre = %s,
                apellido = %s,
                dni = %s,
                fecha_nacimiento = %s,
                telefono = %s,
                email = %s
            WHERE id_paciente = %s
            RETURNING id_paciente;
        """, (
            paciente.nombre,
            paciente.apellido,
            paciente.dni,
            paciente.fecha_nacimiento,
            paciente.telefono,
            paciente.email,
            id_paciente
        ))

        resultado = cursor.fetchone()

        if resultado is None:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        conexion.commit()

        return {
            "mensaje": "Paciente modificado correctamente"
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()


@app.delete("/pacientes/{id_paciente}")
def eliminar_paciente(
    id_paciente: int,
    usuario=Depends(obtener_usuario_actual)
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        cursor.execute("""
            SELECT id_consultorio
            FROM paciente
            WHERE id_paciente = %s;
        """, (id_paciente,))

        paciente = cursor.fetchone()

        if paciente is None:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        if paciente[0] not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a este paciente"
            )

        cursor.execute("""
            UPDATE paciente
            SET activo = FALSE
            WHERE id_paciente = %s
            RETURNING id_paciente;
        """, (id_paciente,))

        resultado = cursor.fetchone()

        if resultado is None:
            raise HTTPException(
                status_code=404,
                detail="Paciente no encontrado"
            )

        conexion.commit()

        return {
            "mensaje": "Paciente desactivado correctamente"
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()


@app.get("/profesionales")
def listar_profesionales(
    usuario=Depends(obtener_usuario_actual)
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if not consultorios:
            return []

        cursor.execute("""
            SELECT DISTINCT
                   p.id_profesional,
                   u.id_usuario,
                   u.nombre,
                   u.apellido,
                   u.email,
                   p.matricula,
                   p.especialidad,
                   p.activo
            FROM profesional p
            INNER JOIN usuario u
                ON p.id_usuario = u.id_usuario
            INNER JOIN consultorio_profesional cp
                ON p.id_profesional = cp.id_profesional
            WHERE cp.id_consultorio = ANY(%s)
            ORDER BY p.id_profesional;
        """, (consultorios,))

        profesionales = cursor.fetchall()

        resultado = []

        for profesional in profesionales:
            resultado.append({
                "id_profesional": profesional[0],
                "id_usuario": profesional[1],
                "nombre": profesional[2],
                "apellido": profesional[3],
                "email": profesional[4],
                "matricula": profesional[5],
                "especialidad": profesional[6],
                "activo": profesional[7]
            })

        return resultado

    finally:
        cursor.close()


@app.post("/profesionales")
def crear_profesional(
    profesional: Profesional,
    usuario=Depends(
        verificar_roles("SUPERADMIN", "ADMINISTRADOR")
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if profesional.id_consultorio not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a este consultorio"
            )

        cursor.execute("""
            SELECT id_usuario
            FROM usuario
            WHERE email = %s;
        """, (
            profesional.email,
        ))

        usuario_existente = cursor.fetchone()

        if usuario_existente is not None:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con ese email"
            )

        cursor.execute("""
            SELECT id_profesional
            FROM profesional
            WHERE matricula = %s;
        """, (
            profesional.matricula,
        ))

        profesional_existente = cursor.fetchone()

        if profesional_existente is not None:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un profesional con esa matrícula"
            )

        cursor.execute("""
            INSERT INTO usuario
            (nombre, apellido, email, password_hash, rol)
            VALUES (%s, %s, %s, %s, 'PROFESIONAL')
            RETURNING id_usuario;
        """, (
            profesional.nombre,
            profesional.apellido,
            profesional.email,
            generar_hash(profesional.password)
        ))

        id_usuario = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO profesional
            (id_usuario, matricula, especialidad)
            VALUES (%s, %s, %s)
            RETURNING id_profesional;
        """, (
            id_usuario,
            profesional.matricula,
            profesional.especialidad
        ))

        id_profesional = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO consultorio_profesional
            (id_consultorio, id_profesional)
            VALUES (%s, %s);
        """, (
            profesional.id_consultorio,
            id_profesional
        ))

        conexion.commit()

        return {
            "mensaje": "Profesional creado correctamente",
            "id_profesional": id_profesional
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=400,
            detail="No se pudo crear el profesional"
        )

    finally:
        cursor.close()

@app.get("/usuarios")
def listar_usuarios(
    usuario=Depends(
        verificar_roles("SUPERADMIN", "ADMINISTRADOR")
    )
):
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT
                u.id_usuario,
                u.nombre,
                u.apellido,
                u.email,
                u.rol,
                u.activo
            FROM usuario u
            INNER JOIN consultorio_usuario cu
                ON cu.id_usuario = u.id_usuario
            WHERE cu.id_consultorio = ANY(%s)
            ORDER BY u.apellido, u.nombre;
        """, (
            obtener_consultorios_usuario(usuario),
        ))

        usuarios = cursor.fetchall()

        return [
            {
                "id_usuario": fila[0],
                "nombre": fila[1],
                "apellido": fila[2],
                "email": fila[3],
                "rol": fila[4],
                "activo": fila[5]
            }
            for fila in usuarios
        ]

    finally:
        cursor.close()

@app.post("/usuarios")
def crear_usuario(
    usuario_nuevo: Usuario,
    usuario=Depends(
        verificar_roles("SUPERADMIN", "ADMINISTRADOR")
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if usuario_nuevo.id_consultorio not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a este consultorio"
            )

        if usuario_nuevo.rol not in [
            "ADMINISTRADOR",
            "ADMINISTRATIVO"
        ]:
            raise HTTPException(
                status_code=400,
                detail="Rol no permitido para este registro"
            )

        if (
            usuario["rol"] == "ADMINISTRADOR"
            and usuario_nuevo.rol == "ADMINISTRADOR"
        ):
            raise HTTPException(
                status_code=403,
                detail="Un administrador no puede crear otro administrador"
            )

        cursor.execute("""
            SELECT id_usuario
            FROM usuario
            WHERE email = %s;
        """, (
            usuario_nuevo.email,
        ))

        usuario_existente = cursor.fetchone()

        if usuario_existente is not None:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con ese email"
            )

        cursor.execute("""
            INSERT INTO usuario
            (nombre, apellido, email, password_hash, rol)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_usuario;
        """, (
            usuario_nuevo.nombre,
            usuario_nuevo.apellido,
            usuario_nuevo.email,
            generar_hash(usuario_nuevo.password),
            usuario_nuevo.rol
        ))

        id_usuario = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO consultorio_usuario
            (id_consultorio, id_usuario)
            VALUES (%s, %s);
        """, (
            usuario_nuevo.id_consultorio,
            id_usuario
        ))

        conexion.commit()

        return {
            "mensaje": "Usuario creado correctamente",
            "id_usuario": id_usuario
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()

@app.put("/usuarios/{id_usuario}")
def editar_usuario(
    id_usuario: int,
    datos: dict,
    usuario=Depends(
        verificar_roles("SUPERADMIN", "ADMINISTRADOR")
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        cursor.execute("""
            SELECT id_usuario
            FROM consultorio_usuario
            WHERE id_usuario = %s
              AND id_consultorio = ANY(%s);
        """, (
            id_usuario,
            consultorios
        ))

        usuario_existente = cursor.fetchone()

        if usuario_existente is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        nombre = datos.get("nombre")
        apellido = datos.get("apellido")
        email = datos.get("email")

        if not nombre or not apellido or not email:
            raise HTTPException(
                status_code=400,
                detail="Nombre, apellido y email son obligatorios"
            )

        cursor.execute("""
            SELECT id_usuario
            FROM usuario
            WHERE email = %s
              AND id_usuario <> %s;
        """, (
            email,
            id_usuario
        ))

        email_existente = cursor.fetchone()

        if email_existente is not None:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con ese email"
            )

        cursor.execute("""
            UPDATE usuario
            SET
                nombre = %s,
                apellido = %s,
                email = %s
            WHERE id_usuario = %s;
        """, (
            nombre,
            apellido,
            email,
            id_usuario
        ))

        conexion.commit()

        return {
            "mensaje": "Usuario modificado correctamente"
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()


@app.put("/usuarios/{id_usuario}/estado")
def cambiar_estado_usuario(
    id_usuario: int,
    datos: dict,
    usuario=Depends(
        verificar_roles("SUPERADMIN", "ADMINISTRADOR")
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        cursor.execute("""
            SELECT id_usuario
            FROM consultorio_usuario
            WHERE id_usuario = %s
              AND id_consultorio = ANY(%s);
        """, (
            id_usuario,
            consultorios
        ))

        usuario_existente = cursor.fetchone()

        if usuario_existente is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )

        activo = datos.get("activo")

        if not isinstance(activo, bool):
            raise HTTPException(
                status_code=400,
                detail="El estado debe ser verdadero o falso"
            )

        cursor.execute("""
            UPDATE usuario
            SET activo = %s
            WHERE id_usuario = %s;
        """, (
            activo,
            id_usuario
        ))

        conexion.commit()

        return {
            "mensaje": "Estado del usuario actualizado correctamente"
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()


class Turno(BaseModel):
    id_paciente: int
    id_profesional: int
    fecha: str
    hora_inicio: str
    hora_fin: str
    estado: str
    observaciones: str | None = None


@app.get("/turnos")
def listar_turnos(
    usuario=Depends(
        verificar_roles(
            "SUPERADMIN",
            "ADMINISTRADOR",
            "ADMINISTRATIVO",
            "PROFESIONAL"
        )
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if not consultorios:
            return []

        cursor.execute("""
            SELECT t.id_turno,
                   t.id_paciente,
                   p.nombre,
                   p.apellido,
                   t.id_profesional,
                   u.nombre,
                   u.apellido,
                   t.fecha,
                   t.hora_inicio,
                   t.hora_fin,
                   t.estado,
                   t.observaciones
            FROM turno t
            INNER JOIN paciente p
                ON t.id_paciente = p.id_paciente
            INNER JOIN profesional pr
                ON t.id_profesional = pr.id_profesional
            INNER JOIN usuario u
                ON pr.id_usuario = u.id_usuario
            WHERE p.id_consultorio = ANY(%s)
            ORDER BY t.fecha, t.hora_inicio;
        """, (consultorios,))

        turnos = cursor.fetchall()

        resultado = []

        for turno in turnos:
            resultado.append({
                "id_turno": turno[0],
                "id_paciente": turno[1],
                "paciente": turno[2] + " " + turno[3],
                "id_profesional": turno[4],
                "profesional": turno[5] + " " + turno[6],
                "fecha": turno[7],
                "hora_inicio": turno[8],
                "hora_fin": turno[9],
                "estado": turno[10],
                "observaciones": turno[11]
            })

        return resultado

    finally:
        cursor.close()


@app.post("/turnos")
def crear_turno(
    turno: Turno,
    usuario=Depends(obtener_usuario_actual)
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        # Verificar que el paciente pertenezca a un consultorio permitido
        cursor.execute("""
            SELECT id_consultorio
            FROM paciente
            WHERE id_paciente = %s;
        """, (turno.id_paciente,))

        paciente = cursor.fetchone()

        if paciente is None:
            raise HTTPException(
                status_code=404,
                detail="El paciente no existe"
            )

        if paciente[0] not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a este paciente"
            )

        # Verificar que el profesional esté asociado a ese mismo consultorio
        cursor.execute("""
            SELECT cp.id_consultorio
            FROM consultorio_profesional cp
            WHERE cp.id_profesional = %s
              AND cp.id_consultorio = %s;
        """, (
            turno.id_profesional,
            paciente[0]
        ))

        profesional = cursor.fetchone()

        if profesional is None:
            raise HTTPException(
                status_code=403,
                detail="El profesional no pertenece al consultorio del paciente"
            )

        if turno.hora_fin <= turno.hora_inicio:
            raise HTTPException(
                status_code=400,
                detail="La hora de fin debe ser posterior a la hora de inicio"
            )

        cursor.execute("""
            SELECT id_turno
            FROM turno
            WHERE id_profesional = %s
              AND fecha = %s
              AND estado <> 'CANCELADO'
              AND hora_inicio < %s
              AND hora_fin > %s;
        """, (
            turno.id_profesional,
            turno.fecha,
            turno.hora_fin,
            turno.hora_inicio
        ))

        turno_existente = cursor.fetchone()

        if turno_existente is not None:
            raise HTTPException(
                status_code=400,
                detail="El profesional ya tiene un turno en ese horario"
            )

        cursor.execute("""
            SELECT id_turno
            FROM turno
            WHERE id_paciente = %s
              AND fecha = %s
              AND estado <> 'CANCELADO'
              AND hora_inicio < %s
              AND hora_fin > %s;
        """, (
            turno.id_paciente,
            turno.fecha,
            turno.hora_fin,
            turno.hora_inicio
        ))

        turno_paciente = cursor.fetchone()

        if turno_paciente is not None:
            raise HTTPException(
                status_code=400,
                detail="El paciente ya tiene un turno en ese horario"
            )

        cursor.execute("""
            INSERT INTO turno
            (id_paciente, id_profesional, fecha,
             hora_inicio, hora_fin, estado, observaciones)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_turno;
        """, (
            turno.id_paciente,
            turno.id_profesional,
            turno.fecha,
            turno.hora_inicio,
            turno.hora_fin,
            turno.estado,
            turno.observaciones
        ))

        id_nuevo = cursor.fetchone()[0]

        conexion.commit()

        return {
            "mensaje": "Turno creado correctamente",
            "id_turno": id_nuevo
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()

class Sesion(BaseModel):
    id_turno: int
    fecha: str
    observaciones: str | None = None
    id_obra_social: int | None = None


@app.get("/sesiones")
def listar_sesiones(
    usuario=Depends(
        verificar_roles(
            "SUPERADMIN",
            "ADMINISTRADOR",
            "PROFESIONAL"
        )
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if not consultorios:
            return []

        cursor.execute("""
            SELECT s.id_sesion,
                   s.id_turno,
                   p.id_paciente,
                   s.fecha,
                   s.observaciones,
                   s.id_obra_social,
                   p.nombre,
                   p.apellido,
                   u.nombre,
                   u.apellido
            FROM sesion s
            INNER JOIN turno t
                ON s.id_turno = t.id_turno
            INNER JOIN paciente p
                ON t.id_paciente = p.id_paciente
            INNER JOIN profesional pr
                ON t.id_profesional = pr.id_profesional
            INNER JOIN usuario u
                ON pr.id_usuario = u.id_usuario
            WHERE p.id_consultorio = ANY(%s)
            ORDER BY s.fecha;
        """, (consultorios,))

        sesiones = cursor.fetchall()

        resultado = []

        for sesion in sesiones:
            resultado.append({
                "id_sesion": sesion[0],
                "id_turno": sesion[1],
                "id_paciente": sesion[2],
                "fecha": sesion[3],
                "observaciones": sesion[4],
                "id_obra_social": sesion[5],
                "paciente": sesion[6] + " " + sesion[7],
                "profesional": sesion[8] + " " + sesion[9]
            })

        return resultado

    finally:
        cursor.close()


@app.post("/sesiones")
def crear_sesion(
    sesion: Sesion,
    usuario=Depends(
        verificar_roles(
            "SUPERADMIN",
            "ADMINISTRADOR",
            "PROFESIONAL"
        )
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        cursor.execute("""
            SELECT t.id_paciente,
                   p.id_consultorio
            FROM turno t
            INNER JOIN paciente p
                ON t.id_paciente = p.id_paciente
            WHERE t.id_turno = %s;
        """, (sesion.id_turno,))

        turno_existente = cursor.fetchone()

        if turno_existente is None:
            raise HTTPException(
                status_code=404,
                detail="El turno no existe"
            )

        id_paciente = turno_existente[0]
        id_consultorio = turno_existente[1]

        if id_consultorio not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a este turno"
            )

        cursor.execute("""
            SELECT id_sesion
            FROM sesion
            WHERE id_turno = %s;
        """, (sesion.id_turno,))

        sesion_existente = cursor.fetchone()

        if sesion_existente is not None:
            raise HTTPException(
                status_code=400,
                detail="El turno ya tiene una sesión registrada"
            )

        cursor.execute("""
            INSERT INTO sesion
            (id_turno, fecha, observaciones, id_obra_social)
            VALUES (%s, %s, %s, %s)
            RETURNING id_sesion;
        """, (
            sesion.id_turno,
            sesion.fecha,
            sesion.observaciones,
            sesion.id_obra_social
        ))

        id_nuevo = cursor.fetchone()[0]

        conexion.commit()

        return {
            "mensaje": "Sesión creada correctamente",
            "id_sesion": id_nuevo
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()

@app.put("/sesiones/{id_sesion}")
def actualizar_sesion(
    id_sesion: int,
    sesion: Sesion,
    usuario=Depends(
        verificar_roles(
            "SUPERADMIN",
            "ADMINISTRADOR",
            "PROFESIONAL"
        )
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        cursor.execute("""
            SELECT p.id_consultorio
            FROM sesion s
            INNER JOIN turno t
                ON s.id_turno = t.id_turno
            INNER JOIN paciente p
                ON t.id_paciente = p.id_paciente
            WHERE s.id_sesion = %s;
        """, (id_sesion,))

        sesion_existente = cursor.fetchone()

        if sesion_existente is None:
            raise HTTPException(
                status_code=404,
                detail="La sesión no existe"
            )

        id_consultorio = sesion_existente[0]

        if id_consultorio not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a esta sesión"
            )

        cursor.execute("""
            UPDATE sesion
            SET fecha = %s,
                observaciones = %s,
                id_obra_social = %s
            WHERE id_sesion = %s;
        """, (
            sesion.fecha,
            sesion.observaciones,
            sesion.id_obra_social,
            id_sesion
        ))

        conexion.commit()

        return {
            "mensaje": "Sesión actualizada correctamente"
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()

class Pago(BaseModel):
    id_sesion: int
    fecha: str
    importe: float
    medio_pago: str


@app.get("/pagos")
def listar_pagos(
    usuario=Depends(
        verificar_roles(
            "SUPERADMIN",
            "ADMINISTRADOR",
            "ADMINISTRATIVO"
        )
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if not consultorios:
            return []

        cursor.execute("""
            SELECT pa.id_pago,
                   pa.id_sesion,
                   pa.fecha,
                   pa.importe,
                   pa.medio_pago,
                   p.nombre,
                   p.apellido,
                   (
                       SELECT SUM(pa2.importe)
                       FROM pago pa2
                       WHERE pa2.id_sesion = pa.id_sesion
                   ) AS total_pagado
            FROM pago pa
            INNER JOIN sesion s
                ON pa.id_sesion = s.id_sesion
            INNER JOIN turno t
                ON s.id_turno = t.id_turno
            INNER JOIN paciente p
                ON t.id_paciente = p.id_paciente
            WHERE p.id_consultorio = ANY(%s)
            ORDER BY pa.fecha;
        """, (consultorios,))

        pagos = cursor.fetchall()

        resultado = []

        for pago in pagos:
            resultado.append({
                "id_pago": pago[0],
                "id_sesion": pago[1],
                "fecha": pago[2],
                "importe": float(pago[3]),
                "medio_pago": pago[4],
                "paciente": pago[5] + " " + pago[6],
                "total_pagado": float(pago[7])
            })

        return resultado

    finally:
        cursor.close()


@app.post("/pagos")
def crear_pago(
    pago: Pago,
    usuario=Depends(
        verificar_roles(
            "SUPERADMIN",
            "ADMINISTRADOR",
            "ADMINISTRATIVO"
        )
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if pago.importe <= 0:
            raise HTTPException(
                status_code=400,
                detail="El importe del pago debe ser mayor a cero"
            )

        cursor.execute("""
            SELECT p.id_consultorio
            FROM sesion s
            INNER JOIN turno t
                ON s.id_turno = t.id_turno
            INNER JOIN paciente p
                ON t.id_paciente = p.id_paciente
            WHERE s.id_sesion = %s;
        """, (pago.id_sesion,))

        sesion_existente = cursor.fetchone()

        if sesion_existente is None:
            raise HTTPException(
                status_code=404,
                detail="La sesión no existe"
            )

        id_consultorio = sesion_existente[0]

        if id_consultorio not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a esta sesión"
            )

        cursor.execute("""
            INSERT INTO pago
            (id_sesion, fecha, importe, medio_pago)
            VALUES (%s, %s, %s, %s)
            RETURNING id_pago;
        """, (
            pago.id_sesion,
            pago.fecha,
            pago.importe,
            pago.medio_pago
        ))

        id_nuevo = cursor.fetchone()[0]

        conexion.commit()

        return {
            "mensaje": "Pago creado correctamente",
            "id_pago": id_nuevo
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()

class ObraSocial(BaseModel):
    nombre: str
    numero_contacto: str | None = None


@app.get("/obras-sociales")
def listar_obras_sociales(
    usuario=Depends(
        verificar_roles(
            "SUPERADMIN",
            "ADMINISTRADOR",
            "ADMINISTRATIVO"
        )
    )
):
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            SELECT id_obra_social,
                   nombre,
                   numero_contacto,
                   activo
            FROM obra_social
            ORDER BY id_obra_social;
        """)

        obras_sociales = cursor.fetchall()

        resultado = []

        for obra_social in obras_sociales:
            resultado.append({
                "id_obra_social": obra_social[0],
                "nombre": obra_social[1],
                "numero_contacto": obra_social[2],
                "activo": obra_social[3]
            })

        return resultado

    finally:
        cursor.close()

@app.post("/obras-sociales")
def crear_obra_social(
    obra_social: ObraSocial,
    usuario=Depends(
        verificar_roles(
            "SUPERADMIN",
            "ADMINISTRADOR",
            "ADMINISTRATIVO"
        )
    )
):
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO obra_social
            (nombre, numero_contacto)
            VALUES (%s, %s)
            RETURNING id_obra_social;
        """, (
            obra_social.nombre,
            obra_social.numero_contacto
        ))

        id_nuevo = cursor.fetchone()[0]

        conexion.commit()

        return {
            "mensaje": "Obra social creada correctamente",
            "id_obra_social": id_nuevo
        }

    except Exception as error:
        conexion.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()

class PacienteObraSocial(BaseModel):
    id_paciente: int
    id_obra_social: int
    numero_afiliado: str | None = None


@app.get("/pacientes-obras-sociales")
def listar_pacientes_obras_sociales(
    usuario=Depends(
        verificar_roles(
            "SUPERADMIN",
            "ADMINISTRADOR",
            "ADMINISTRATIVO"
        )
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        if not consultorios:
            return []

        cursor.execute("""
            SELECT pos.id_paciente,
                   p.nombre,
                   p.apellido,
                   pos.id_obra_social,
                   os.nombre,
                   pos.numero_afiliado,
                   pos.activo
            FROM paciente_obra_social pos
            INNER JOIN paciente p
                ON pos.id_paciente = p.id_paciente
            INNER JOIN obra_social os
                ON pos.id_obra_social = os.id_obra_social
            WHERE p.id_consultorio = ANY(%s)
            ORDER BY pos.id_paciente;
        """, (consultorios,))

        relaciones = cursor.fetchall()

        resultado = []

        for relacion in relaciones:
            resultado.append({
                "id_paciente": relacion[0],
                "paciente": relacion[1] + " " + relacion[2],
                "id_obra_social": relacion[3],
                "obra_social": relacion[4],
                "numero_afiliado": relacion[5],
                "activo": relacion[6]
            })

        return resultado

    finally:
        cursor.close()


@app.post("/pacientes-obras-sociales")
def crear_paciente_obra_social(
    relacion: PacienteObraSocial,
    usuario=Depends(
        verificar_roles(
            "SUPERADMIN",
            "ADMINISTRADOR",
            "ADMINISTRATIVO"
        )
    )
):
    cursor = conexion.cursor()

    try:
        consultorios = obtener_consultorios_usuario(usuario)

        cursor.execute("""
            SELECT id_consultorio
            FROM paciente
            WHERE id_paciente = %s;
        """, (relacion.id_paciente,))

        paciente = cursor.fetchone()

        if paciente is None:
            raise HTTPException(
                status_code=404,
                detail="El paciente no existe"
            )

        if paciente[0] not in consultorios:
            raise HTTPException(
                status_code=403,
                detail="No tenés acceso a este paciente"
            )

        cursor.execute("""
            SELECT id_obra_social
            FROM obra_social
            WHERE id_obra_social = %s
              AND activo = TRUE;
        """, (relacion.id_obra_social,))

        obra_social = cursor.fetchone()

        if obra_social is None:
            raise HTTPException(
                status_code=404,
                detail="La obra social no existe o está inactiva"
            )

        cursor.execute("""
            INSERT INTO paciente_obra_social
            (id_paciente, id_obra_social, numero_afiliado)
            VALUES (%s, %s, %s)
            RETURNING id_paciente;
        """, (
            relacion.id_paciente,
            relacion.id_obra_social,
            relacion.numero_afiliado
        ))

        id_paciente = cursor.fetchone()[0]

        conexion.commit()

        return {
            "mensaje": "Obra social asociada correctamente",
            "id_paciente": id_paciente
        }

    except HTTPException:
        conexion.rollback()
        raise

    except Exception as error:
        conexion.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    finally:
        cursor.close()

@app.post("/admin/seed-demo")
def cargar_datos_demo(
    usuario=Depends(verificar_roles("SUPERADMIN"))
):
    cursor = conexion.cursor()

    try:
        # Limpiar todos los datos excepto el SUPERADMIN
        cursor.execute("""
            DELETE FROM pago;
            DELETE FROM sesion;
            DELETE FROM paciente_obra_social;
            DELETE FROM historia_clinica;
            DELETE FROM turno;
            DELETE FROM consultorio_profesional;
            DELETE FROM consultorio_usuario;
            DELETE FROM paciente;
            DELETE FROM profesional;
            DELETE FROM obra_social;
            DELETE FROM consultorio;
            DELETE FROM usuario
            WHERE id_usuario <> %s;
        """, (int(usuario["sub"]),))

        # Obtener la contraseña actual del SUPERADMIN
        cursor.execute("""
            SELECT password_hash
            FROM usuario
            WHERE id_usuario = %s;
        """, (int(usuario["sub"]),))

        password_hash = cursor.fetchone()[0]

        # Consultorios
        cursor.execute("""
            INSERT INTO consultorio
            (nombre, direccion, telefono, email)
            VALUES
            ('NovaGest Consultorio Centro',
             'Av. Colón 1234',
             '0351-4567890',
             'centro@novagest.com.ar'),
            ('NovaGest Consultorio Norte',
             'Av. Rafael Núñez 4567',
             '0351-4789123',
             'norte@novagest.com.ar')
            RETURNING id_consultorio;
        """)

        consultorios = cursor.fetchall()
        id_consultorio_1 = consultorios[0][0]
        id_consultorio_2 = consultorios[1][0]

        # Usuarios administrativos y profesionales
        usuarios = [
            ("Laura", "Gómez", "laura@novagest.com.ar", "ADMINISTRADOR"),
            ("Martín", "Pérez", "martin@novagest.com.ar", "ADMINISTRATIVO"),
            ("Lucía", "Fernández", "lucia@novagest.com.ar", "PROFESIONAL"),
            ("Diego", "Martínez", "diego@novagest.com.ar", "PROFESIONAL"),
            ("Carolina", "Sosa", "carolina@novagest.com.ar", "PROFESIONAL")
        ]

        ids_usuarios = {}

        for nombre, apellido, email, rol in usuarios:
            cursor.execute("""
                INSERT INTO usuario
                (nombre, apellido, email, password_hash, rol, activo)
                VALUES (%s, %s, %s, %s, %s, TRUE)
                RETURNING id_usuario;
            """, (
                nombre,
                apellido,
                email,
                password_hash,
                rol
            ))

            ids_usuarios[email] = cursor.fetchone()[0]

        # Profesionales
        profesionales = [
            (
                ids_usuarios["lucia@novagest.com.ar"],
                "MP-12345",
                "Psicología Clínica"
            ),
            (
                ids_usuarios["diego@novagest.com.ar"],
                "MP-23456",
                "Psicología Cognitivo Conductual"
            ),
            (
                ids_usuarios["carolina@novagest.com.ar"],
                "MP-34567",
                "Psicología Infantil"
            )
        ]

        ids_profesionales = []

        for id_usuario, matricula, especialidad in profesionales:
            cursor.execute("""
                INSERT INTO profesional
                (id_usuario, matricula, especialidad, activo)
                VALUES (%s, %s, %s, TRUE)
                RETURNING id_profesional;
            """, (
                id_usuario,
                matricula,
                especialidad
            ))

            ids_profesionales.append(cursor.fetchone()[0])

        # Asociaciones de usuarios a consultorios
        asociaciones_usuario = [
            (id_consultorio_1, ids_usuarios["laura@novagest.com.ar"]),
            (id_consultorio_1, ids_usuarios["martin@novagest.com.ar"]),
            (id_consultorio_1, ids_usuarios["lucia@novagest.com.ar"]),
            (id_consultorio_1, ids_usuarios["diego@novagest.com.ar"]),
            (id_consultorio_2, ids_usuarios["laura@novagest.com.ar"]),
            (id_consultorio_2, ids_usuarios["martin@novagest.com.ar"]),
            (id_consultorio_2, ids_usuarios["diego@novagest.com.ar"]),
            (id_consultorio_2, ids_usuarios["carolina@novagest.com.ar"])
        ]

        for id_consultorio, id_usuario in asociaciones_usuario:
            cursor.execute("""
                INSERT INTO consultorio_usuario
                (id_consultorio, id_usuario)
                VALUES (%s, %s);
            """, (
                id_consultorio,
                id_usuario
            ))

        # Asociaciones de profesionales
        asociaciones_profesional = [
            (id_consultorio_1, ids_profesionales[0]),
            (id_consultorio_1, ids_profesionales[1]),
            (id_consultorio_2, ids_profesionales[1]),
            (id_consultorio_2, ids_profesionales[2])
        ]

        for id_consultorio, id_profesional in asociaciones_profesional:
            cursor.execute("""
                INSERT INTO consultorio_profesional
                (id_consultorio, id_profesional)
                VALUES (%s, %s);
            """, (
                id_consultorio,
                id_profesional
            ))

        # Obras sociales
        obras_sociales = [
            ("OSDE", "0800-555-6733"),
            ("Swiss Medical", "0810-333-8876"),
            ("APROSS", "0800-888-2776"),
            ("Particular", None)
        ]

        ids_obras = []

        for nombre, contacto in obras_sociales:
            cursor.execute("""
                INSERT INTO obra_social
                (nombre, numero_contacto, activo)
                VALUES (%s, %s, TRUE)
                RETURNING id_obra_social;
            """, (
                nombre,
                contacto
            ))

            ids_obras.append(cursor.fetchone()[0])

        # Pacientes
        pacientes = [
            (id_consultorio_1, "Juan", "Pérez", "30123456", "1990-05-12", "351-5551001", "juan.perez@email.com"),
            (id_consultorio_1, "María", "Gómez", "31234567", "1988-08-24", "351-5551002", "maria.gomez@email.com"),
            (id_consultorio_1, "Sofía", "Rodríguez", "32345678", "1995-03-17", "351-5551003", "sofia.rodriguez@email.com"),
            (id_consultorio_1, "Pedro", "Sánchez", "33456789", "1985-11-03", "351-5551004", "pedro.sanchez@email.com"),
            (id_consultorio_1, "Valentina", "López", "34567890", "2000-01-29", "351-5551005", "valentina.lopez@email.com"),
            (id_consultorio_1, "Carlos", "Fernández", "35678901", "1979-06-14", "351-5551006", "carlos.fernandez@email.com"),
            (id_consultorio_2, "Camila", "Torres", "36789012", "1998-09-21", "351-5551007", "camila.torres@email.com"),
            (id_consultorio_2, "Lucas", "Martínez", "37890123", "1992-12-08", "351-5551008", "lucas.martinez@email.com"),
            (id_consultorio_2, "Agustina", "Sosa", "38901234", "1997-04-15", "351-5551009", "agustina.sosa@email.com"),
            (id_consultorio_2, "Federico", "Romero", "39012345", "1987-07-30", "351-5551010", "federico.romero@email.com"),
            (id_consultorio_2, "Julieta", "Díaz", "40123456", "1994-10-11", "351-5551011", "julieta.diaz@email.com"),
            (id_consultorio_2, "Mateo", "Herrera", "41234567", "2001-02-19", "351-5551012", "mateo.herrera@email.com")
        ]

        ids_pacientes = []

        for paciente in pacientes:
            cursor.execute("""
                INSERT INTO paciente
                (id_consultorio, nombre, apellido, dni,
                 fecha_nacimiento, telefono, email, activo)
                VALUES (%s, %s, %s, %s, %s, %s, %s, TRUE)
                RETURNING id_paciente;
            """, paciente)

            ids_pacientes.append(cursor.fetchone()[0])

        # Historias clínicas
        for id_paciente in ids_pacientes:
            cursor.execute("""
                INSERT INTO historia_clinica
                (id_paciente, observaciones)
                VALUES (%s, %s);
            """, (
                id_paciente,
                "Historia clínica de seguimiento."
            ))

        # Obras sociales de pacientes
        for i, id_paciente in enumerate(ids_pacientes):
            cursor.execute("""
                INSERT INTO paciente_obra_social
                (id_paciente, id_obra_social, numero_afiliado)
                VALUES (%s, %s, %s);
            """, (
                id_paciente,
                ids_obras[i % len(ids_obras)],
                f"AF-{10000 + i}"
            ))

        conexion.commit()

        return {
            "mensaje": "Datos demo cargados correctamente",
            "consultorios": 2,
            "usuarios": 6,
            "profesionales": 3,
            "pacientes": 12,
            "obras_sociales": 4,
            "historias_clinicas": 12
        }

    except Exception as error:
        conexion.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        cursor.close()
