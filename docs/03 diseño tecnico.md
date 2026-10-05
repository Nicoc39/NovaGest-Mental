# NovaGest Mental

## Sistema Integral de Gestión para Consultorios Psicológicos

NovaGest Mental
Documento 03
Diseño Técnico

Versión: 0.1.0
Estado: En desarrollo
Autor: Nicolás Carranza
Proyecto: NovaGest Mental
Fecha de creación: 03/10/2026
Última actualización: 03/10/2026

---

## 1. Introducción

Este documento define la estructura técnica de NovaGest Mental a partir del modelo conceptual desarrollado previamente.

Se establece el modelo relacional de la base de datos, las principales tablas y relaciones, junto con una descripción general de la arquitectura que utilizará el sistema.

El diseño busca mantener una estructura organizada, escalable y coherente con los procesos definidos en el análisis del negocio.

---

## 2. Objetivo

Definir la estructura técnica necesaria para implementar NovaGest Mental, estableciendo:

- las tablas principales de la base de datos;

- las claves primarias y foráneas;

- las relaciones entre las tablas;

- las principales restricciones de integridad;

- la arquitectura general del sistema;

- la separación entre frontend, backend y base de datos.

---

## 3. Modelo relacional

A partir del modelo conceptual se identifican las siguientes tablas principales:

| Tabla | Descripción |
| :--- | :--- |
| ****consultorio**** | Información de los consultorios u organizaciones que utilizan el sistema. |
| ****usuario**** | Personas autorizadas a acceder al sistema. |
| ****profesional**** | Información específica de los profesionales que brindan atención. |
| ****consultorio_usuario**** | Relación entre usuarios y consultorios a los que tienen acceso. |
| ****consultorio_profesional**** | Relación entre profesionales y consultorios donde trabajan. |
| ****paciente**** | Información de las personas que reciben atención. |
| ****historia_clinica**** | Historia clínica asociada a cada paciente. |
| ****turno**** | Reservas de fechas y horarios para la atención. |
| ****sesion**** | Registro de una atención efectivamente realizada. |
| ****pago**** | Registros de pagos asociados a las sesiones. |
| ****obra_social**** | Obras sociales disponibles para la cobertura de prestaciones. |
| ****paciente_obra_social**** | Relación entre pacientes y obras sociales. |

---

## 4. Estructura de las tablas

### 4.1. Consultorio

Representa una organización o centro que utiliza NovaGest Mental.

Campos principales:

- `id_consultorio` — clave primaria.

- `nombre` — nombre del consultorio.

- `direccion` — dirección.

- `telefono` — teléfono de contacto.

- `email` — correo electrónico.

- `activo` — indica si el consultorio se encuentra activo.

---

### 4.2. Usuario

Representa a las personas autorizadas a acceder al sistema.

Campos principales:

- `id_usuario` — clave primaria.

- `nombre` — nombre del usuario.

- `apellido` — apellido del usuario.

- `email` — correo electrónico utilizado para el acceso.

- `password_hash` — contraseña almacenada de forma segura.

- `rol` — rol dentro del sistema.

- `activo` — indica si el usuario puede acceder.

---

### 4.3. Profesional

Contiene la información específica de los profesionales.

Campos principales:

- `id_profesional` — clave primaria.

- `id_usuario` — clave foránea hacia `usuario`.

- `matricula` — matrícula profesional.

- `especialidad` — especialidad profesional.

- `activo` — indica si el profesional se encuentra activo.

---

### 4.4. Consultorio_Usuario

Permite representar los consultorios a los que puede acceder cada usuario.

Campos principales:

- `id_consultorio` — clave foránea hacia `consultorio`.

- `id_usuario` — clave foránea hacia `usuario`.

La combinación de ambos campos funciona como clave primaria compuesta.

---

### 4.5. Consultorio_Profesional

Representa la relación entre profesionales y consultorios.

Campos principales:

- `id_consultorio` — clave foránea hacia `consultorio`.

- `id_profesional` — clave foránea hacia `profesional`.

La combinación de ambos campos funciona como clave primaria compuesta.

---

### 4.6. Paciente

Contiene la información básica de los pacientes.

Campos principales:

- `id_paciente` — clave primaria.

- `id_consultorio` — clave foránea hacia `consultorio`.

- `nombre` — nombre del paciente.

- `apellido` — apellido del paciente.

- `dni` — documento de identidad.

- `fecha_nacimiento` — fecha de nacimiento.

- `telefono` — teléfono de contacto.

- `email` — correo electrónico.

- `activo` — indica si el paciente se encuentra activo.

El DNI debe ser único dentro del consultorio correspondiente.

---

### 4.7. Historia_Clinica

Representa la historia clínica de cada paciente.

Campos principales:

- `id_historia` — clave primaria.

- `id_paciente` — clave foránea hacia `paciente`.

- `fecha_apertura` — fecha de creación de la historia clínica.

- `observaciones` — información clínica general.

Cada paciente posee una única historia clínica.

---

### 4.8. Turno

Representa una reserva de atención.

Campos principales:

- `id_turno` — clave primaria.

- `id_paciente` — clave foránea hacia `paciente`.

- `id_profesional` — clave foránea hacia `profesional`.

- `fecha` — fecha del turno.

- `hora_inicio` — hora de inicio.

- `hora_fin` — hora de finalización.

- `estado` — estado del turno.

- `observaciones` — información administrativa relacionada con el turno.

Los estados posibles contemplados inicialmente son pendiente, confirmado, cancelado y reprogramado.

---

### 4.9. Sesion

Representa una atención efectivamente realizada.

Campos principales:

- `id_sesion` — clave primaria.

- `id_turno` — clave foránea hacia `turno`.

- `fecha` — fecha de realización.

- `observaciones` — información correspondiente a la sesión.

Una sesión debe estar asociada a un turno previo.

---

### 4.10. Pago

Representa un pago asociado a una sesión.

Campos principales:

- `id_pago` — clave primaria.

- `id_sesion` — clave foránea hacia `sesion`.

- `fecha` — fecha del pago.

- `importe` — importe abonado.

- `medio_pago` — medio utilizado para realizar el pago.

Una sesión puede tener múltiples pagos para permitir registrar pagos parciales.

---

### 4.11. Obra_Social

Representa las obras sociales utilizadas para cubrir prestaciones.

Campos principales:

- `id_obra_social` — clave primaria.

- `nombre` — nombre de la obra social.

- `numero_contacto` — teléfono o medio de contacto.

- `activo` — indica si se encuentra disponible.

---

### 4.12. Paciente_Obra_Social

Representa la relación entre pacientes y obras sociales.

Campos principales:

- `id_paciente` — clave foránea hacia `paciente`.

- `id_obra_social` — clave foránea hacia `obra_social`.

- `numero_afiliado` — número de afiliado del paciente.

- `activo` — indica si la cobertura se encuentra vigente.

La combinación de `id_paciente` e `id_obra_social` funciona como clave primaria compuesta.

---

## 5. Relaciones entre tablas

Las principales relaciones del modelo relacional son:

| Relación | Tipo |
| :--- | :--- |
| ****Consultorio – Usuario**** | N:N mediante `consultorio_usuario`. |
| ****Consultorio – Profesional**** | N:N mediante `consultorio_profesional`. |
| ****Usuario – Profesional**** | 1:0..1. |
| ****Consultorio – Paciente**** | 1:N. |
| ****Paciente – Historia Clínica**** | 1:1. |
| ****Paciente – Turno**** | 1:N. |
| ****Profesional – Turno**** | 1:N. |
| ****Turno – Sesión**** | 1:0..1. |
| ****Sesión – Pago**** | 1:N. |
| ****Paciente – Obra Social**** | N:N mediante `paciente_obra_social`. |

La relación entre sesión y obra social se podrá implementar posteriormente mediante una clave foránea opcional desde `sesion` hacia `obra_social`, permitiendo diferenciar prestaciones particulares de prestaciones con cobertura.

---

## 6. Integridad de los datos

El modelo relacional deberá contemplar las siguientes reglas:

- Las claves primarias deben identificar de forma única cada registro.

- Las claves foráneas deben mantener la integridad entre las tablas relacionadas.

- El DNI de un paciente no debe repetirse dentro del mismo consultorio.

- La matrícula profesional debe ser única.

- Un profesional no puede tener dos turnos superpuestos.

- Un paciente no puede tener dos turnos superpuestos.

- Una sesión solamente puede registrarse para un turno existente.

- Un turno cancelado no debe generar una sesión.

- Los importes de los pagos deben ser mayores que cero.

- Los datos de cada consultorio deben mantenerse separados mediante las relaciones correspondientes.

---

## 7. Arquitectura general

NovaGest Mental utilizará una arquitectura dividida en tres componentes principales:

**Frontend**

Interfaz utilizada por los usuarios para interactuar con el sistema.

Tecnologías previstas:

- HTML

- CSS

- JavaScript

**Backend**

Responsable de procesar las solicitudes del frontend, aplicar reglas de negocio, validar información y comunicarse con la base de datos.

Tecnología prevista:

- FastAPI

**Base de datos**

Responsable del almacenamiento persistente de la información.

Tecnología prevista:

- PostgreSQL

La comunicación general será:

`Frontend → API REST → PostgreSQL`

El frontend no accederá directamente a la base de datos.

---

## 8. Flujo general de información

El funcionamiento básico de una operación será:

1. El usuario realiza una acción desde la interfaz.

2. JavaScript prepara la solicitud.

3. El frontend envía una petición HTTP a la API.

4. El backend recibe y valida los datos.

5. El backend ejecuta la operación correspondiente sobre PostgreSQL.

6. PostgreSQL devuelve el resultado.

7. El backend responde a la API.

8. El frontend actualiza la información mostrada al usuario.

---

## 9. Consideraciones de seguridad

La aplicación deberá contemplar inicialmente:

- almacenamiento seguro de contraseñas mediante hash;

- validación de los datos recibidos por la API;

- control de acceso según el rol del usuario;

- separación de información entre consultorios;

- utilización de variables de entorno para información sensible;

- evitar almacenar contraseñas directamente en la base de datos.

Las medidas de seguridad podrán ampliarse en futuras versiones según las necesidades del sistema.

---

## 10. Conclusión

El diseño técnico establece la estructura necesaria para transformar el modelo conceptual de NovaGest Mental en una aplicación funcional.

La separación entre frontend, backend y base de datos permite organizar las responsabilidades del sistema y facilita futuras modificaciones o ampliaciones.

El modelo relacional definido servirá como base para la implementación de PostgreSQL, el desarrollo de la API y la construcción de la interfaz de usuario.
