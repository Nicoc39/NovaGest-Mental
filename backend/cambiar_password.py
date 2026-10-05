from database import conexion
from auth import generar_hash


email = input("Email del usuario: ")
nueva_password = input("Nueva contraseña: ")


password_hash = generar_hash(nueva_password)


cursor = conexion.cursor()

try:
    cursor.execute("""
        UPDATE usuario
        SET password_hash = %s
        WHERE email = %s
        RETURNING id_usuario;
    """, (
        password_hash,
        email
    ))

    usuario = cursor.fetchone()

    if usuario is None:
        print("No se encontró ningún usuario con ese email.")
        conexion.rollback()
    else:
        conexion.commit()
        print("Contraseña actualizada correctamente.")
        print("ID:", usuario[0])

except Exception as error:
    conexion.rollback()
    print("No se pudo cambiar la contraseña.")
    print(error)

finally:
    cursor.close()