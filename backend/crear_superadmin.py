from database import conexion
from auth import generar_hash


nombre = input("Nombre: ")
apellido = input("Apellido: ")
email = input("Email: ")
password = input("Contraseña: ")


password_hash = generar_hash(password)


cursor = conexion.cursor()

try:
    cursor.execute("""
        INSERT INTO usuario
        (nombre, apellido, email, password_hash, rol)
        VALUES (%s, %s, %s, %s, 'SUPERADMIN')
        RETURNING id_usuario;
    """, (
        nombre,
        apellido,
        email,
        password_hash
    ))

    id_usuario = cursor.fetchone()[0]

    conexion.commit()

    print("SUPERADMIN creado correctamente.")
    print("ID:", id_usuario)

except Exception as error:
    conexion.rollback()
    print("No se pudo crear el SUPERADMIN.")
    print(error)

finally:
    cursor.close()