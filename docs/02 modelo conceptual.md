# NovaGest Mental

Documento 02
Modelo Conceptual de Datos

Versión: 0.2.0
Estado: En desarrollo

Autor:
Nicolás Carranza

Proyecto:
NovaGest Mental

Fecha de creación:
02/07/2026

Última actualización:
02/07/2026

###

1. Introducción

El presente documento desarrolla el modelo conceptual de datos de NovaGest Mental. A partir del análisis del negocio realizado previamente, se identifican las principales entidades del dominio y las relaciones existentes entre ellas, estableciendo la base para el posterior diseño del modelo relacional e implementación de la base de datos.

2. Objetivo

El objetivo de este documento es identificar y modelar conceptualmente los elementos fundamentales del negocio y sus relaciones, representando la estructura de información necesaria para el funcionamiento del sistema, sin considerar aún aspectos propios de la implementación física o técnica de la base de datos.

3. Metodología

El modelo conceptual se construye a partir del análisis del negocio realizado en el Documento 01. En esta etapa se identifican las entidades del dominio, sus relaciones y las restricciones conceptuales del negocio, evitando considerar decisiones propias del modelo relacional o de la implementación física.

4. Entidades identificadas

Para estructurar la información del negocio, se definen los siguientes componentes principales que interactúan dentro del ecosistema de NovaGest Mental:

| Entidad | Descripción |
| :--- | :--- |
| **Consultorio** | Representa el consultorio donde se presta el servicio de atención psicológica y se administra la información del sistema. |
| **Usuario** | Representa a las personas autorizadas a acceder al sistema, diferenciadas y validadas según su rol (Administrador, Personal Administrativo o Profesional). |
| **Profesional** | Representa a los psicólogos que brindan atención clínica a los pacientes dentro del consultorio. |
| **Paciente** |Representa a las personas que reciben atención psicológica dentro del consultorio. |
| **Historia Clínica** | Expediente clínico asociado de forma única a un paciente, donde se registra la información relevante y evolutiva de su tratamiento. |
| **Turno** | Reserva formal de una fecha y horario específicos para coordinar el encuentro entre un paciente y un profesional. |
| **Sesión** | Representa la atención clínica efectivamente realizada entre un profesional y un paciente. |
| **Pago** | Registro económico asociado a la prestación de una sesión, que controla los montos y los estados de las cuentas. |
| **Obra Social** | Cobertura médica vinculada a los pacientes y utilizada para financiar determinadas prestaciones. |

5. Relaciones entre entidades

A partir de las entidades identificadas, se establecen las siguientes relaciones que representan las interacciones principales entre los elementos del negocio:

| Entidades | Relación |
| :--- | :--- |
| **Consultorio – Usuario** | Un consultorio puede contar con múltiples usuarios y un usuario puede tener acceso a uno o varios consultorios. |
| **Consultorio – Profesional** | Un consultorio puede contar con múltiples profesionales y un profesional puede trabajar en uno o varios consultorios. |
| **Usuario – Profesional** | Un profesional corresponde a un usuario del sistema y utiliza sus credenciales para acceder a la plataforma. |
| **Paciente – Historia Clínica** | Cada paciente posee una única historia clínica y cada historia clínica corresponde a un único paciente. |
| **Paciente – Turno** | Un paciente puede tener múltiples turnos. Cada turno corresponde a un único paciente. |
| **Profesional – Turno** | Un profesional puede tener múltiples turnos. Cada turno corresponde a un único profesional. |
| **Turno – Sesión** | Un turno puede dar lugar a una sesión y toda sesión debe estar asociada a un turno previo. |
| **Paciente – Sesión** | Un paciente puede tener múltiples sesiones. Cada sesión corresponde a un único paciente. |
| **Profesional – Sesión** | Un profesional puede realizar múltiples sesiones. Cada sesión corresponde a un único profesional. |
| **Sesión – Pago** | Una sesión puede tener uno o varios pagos asociados, permitiendo registrar pagos parciales hasta completar el importe correspondiente. |
| **Paciente – Obra Social** | Un paciente puede estar asociado a una o varias obras sociales, y una obra social puede estar asociada a múltiples pacientes. |
| **Sesión – Obra Social** | Una sesión puede estar asociada a una obra social o corresponder a una atención particular. |

6. Convenciones de cardinalidad

- 1: representa una única instancia obligatoria.

- N: representa múltiples instancias.

- 0..1: representa una relación opcional, donde puede existir una única instancia relacionada o ninguna.

- 0..N: representa una relación opcional, donde pueden existir múltiples instancias relacionadas o ninguna.

- 1..N: representa una relación obligatoria con múltiples instancias.

7. Cardinalidades de las relaciones

A partir de las relaciones identificadas y las convenciones de cardinalidad definidas, se establecen las siguientes cardinalidades:

| Relación | Cardinalidad |
| :--- | :--- |
| **Consultorio – Usuario** | Un consultorio puede tener 0..N usuarios y un usuario puede tener acceso a 1..N consultorios. |
| **Consultorio – Profesional** | Un consultorio puede contar con 0..N profesionales y un profesional debe trabajar en 1..N consultorios. |
| **Usuario – Profesional** | Un usuario puede corresponder a 0..1 profesional y cada profesional corresponde a 1 usuario. |
| **Paciente – Historia Clínica** | Cada paciente tiene 1 historia clínica y cada historia clínica corresponde a 1 paciente. |
| **Paciente – Turno** | Un paciente puede tener 0..N turnos y cada turno corresponde a 1 paciente. |
| **Profesional – Turno** | Un profesional puede tener 0..N turnos y cada turno corresponde a 1 profesional. |
| **Turno – Sesión** | Un turno puede dar lugar a 0..1 sesión y cada sesión corresponde a 1 turno. |
| **Paciente – Sesión** | Un paciente puede tener 0..N sesiones y cada sesión corresponde a 1 paciente. |
| **Profesional – Sesión** | Un profesional puede realizar 0..N sesiones y cada sesión corresponde a 1 profesional. |
| **Sesión – Pago** | Una sesión puede tener 0..N pagos y cada pago corresponde a 1 sesión. |
| **Paciente – Obra Social** | Un paciente puede estar asociado a 0..N obras sociales y una obra social puede estar asociada a 0..N pacientes. |
| **Sesión – Obra Social** | Una sesión puede estar asociada a 0..1 obra social y una obra social puede estar asociada a 0..N sesiones. |

8. Restricciones conceptuales

A partir de las entidades, relaciones y cardinalidades definidas, se establecen las siguientes restricciones conceptuales:

- Un usuario puede tener acceso a uno o varios consultorios según los permisos asignados.

- Un profesional debe estar asociado al menos a un consultorio y puede trabajar en múltiples consultorios.

- Un profesional debe contar con un usuario del sistema para acceder a la plataforma.

- Cada paciente debe contar con una única historia clínica.

- Todo turno debe estar asociado a un único paciente y a un único profesional.

- Un profesional no puede tener más de un turno asignado en el mismo horario.

- Un paciente no puede tener más de un turno asignado en el mismo horario.

- Toda sesión debe corresponder a un turno previo.

- Un turno puede no generar una sesión, por ejemplo, cuando es cancelado.

- Una sesión puede tener uno o varios pagos asociados, permitiendo registrar pagos parciales.

- Una sesión puede ser particular o estar asociada a una obra social.

- Un paciente puede estar asociado a una o varias obras sociales.

- La información de cada consultorio debe mantenerse aislada de la información de otros consultorios.

9. Decisiones de diseño

Durante la construcción del modelo conceptual se establecen las siguientes decisiones de diseño:

- Profesionales y usuarios: los profesionales tendrán una cuenta de usuario para acceder al sistema. La relación permite diferenciar la información profesional de las credenciales de acceso.

- Profesionales y consultorios: un profesional puede trabajar en uno o varios consultorios. Esto permite que NovaGest Mental pueda administrar organizaciones con profesionales compartidos entre diferentes centros.

- Relación entre profesionales y pacientes: no se establece una asignación permanente entre profesionales y pacientes. La relación se determina mediante los turnos y las sesiones registradas.

- Turnos y sesiones: una sesión debe estar asociada a un turno previo. Un turno puede existir sin generar una sesión, por ejemplo, cuando es cancelado.

- Pagos: una sesión puede registrar múltiples pagos para permitir el seguimiento de pagos parciales hasta completar el importe correspondiente.

- Obras sociales: un paciente puede tener una o varias obras sociales y una sesión puede realizarse de forma particular o mediante una obra social.

- Aislamiento de información: la información perteneciente a cada consultorio debe mantenerse separada, respetando los permisos de acceso de los usuarios.

Estas decisiones forman parte del modelo conceptual y serán consideradas posteriormente durante la definición del modelo relacional y la implementación del sistema.

10. Próximas etapas

El modelo conceptual de NovaGest Mental permite representar los principales elementos del negocio y las relaciones existentes entre ellos. Se definieron las entidades involucradas, sus relaciones, cardinalidades y restricciones, tomando como base el análisis del negocio realizado previamente.

El modelo establece una estructura que permite representar la gestión de consultorios, usuarios, profesionales, pacientes, turnos, sesiones, pagos y obras sociales, manteniendo la separación de la información correspondiente a cada consultorio.

Este modelo servirá como base para la elaboración del modelo relacional y para las siguientes etapas de diseño e implementación de la base de datos.