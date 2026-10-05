# NovaGest Mental

## Sistema Integral de Gestión para Consultorios Psicológicos

NovaGest Mental
Documento 04
Requisitos Funcionales
Versión: 0.1.0
Estado: En desarrollo
Autor: Nicolás Carranza
Proyecto: NovaGest Mental
Fecha de creación: 03/10/2026
Última actualización: 03/10/2026

## 1. Introducción

Este documento define los requisitos funcionales y no funcionales del sistema NovaGest Mental.

Los requisitos se establecen a partir del análisis del negocio, el modelo conceptual y el diseño técnico previamente definidos. Su objetivo es determinar las funcionalidades que debe ofrecer el sistema y delimitar el alcance de la versión actual.

La definición de estos requisitos sirve como referencia para la implementación, las pruebas y la posterior validación del sistema.

## 2. Objetivo

El objetivo es establecer de forma clara las funcionalidades que NovaGest Mental debe proporcionar para permitir la gestión de pacientes, profesionales, turnos, sesiones, pagos y obras sociales dentro de un consultorio o centro de atención psicológica.

Los requisitos también permiten diferenciar las funcionalidades implementadas actualmente de aquellas previstas para futuras etapas.

## 3. Usuarios del sistema

Los principales usuarios considerados para el sistema son:

- **Profesionales:** utilizan el sistema para consultar información relacionada con sus pacientes, turnos y sesiones.

- **Personal administrativo:** gestiona pacientes, turnos, pagos y otra información administrativa.

- **Administrador del consultorio:** gestiona la información general del consultorio y los profesionales asociados.

En la versión actual, la autenticación y autorización de usuarios se encuentran fuera de la implementación principal y serán incorporadas en una etapa posterior.

## 4. Requisitos funcionales

### 4.1 Gestión de pacientes

**RF-01. Registrar pacientes**

El sistema debe permitir registrar un paciente ingresando como mínimo:

- Nombre
- Apellido
- DNI
- Fecha de nacimiento
- Teléfono
- Email

El paciente debe quedar asociado a un consultorio.

**RF-02. Consultar pacientes**

El sistema debe permitir consultar los pacientes registrados y visualizar su información principal.

**RF-03. Modificar pacientes**

El sistema debe permitir modificar los datos registrados de un paciente.

**RF-04. Eliminar pacientes**

El sistema debe permitir eliminar un paciente registrado.

**RF-05. Gestionar obra social del paciente**

El sistema debe permitir asociar una obra social a un paciente y registrar su número de afiliado.

La estructura de la base de datos contempla la posibilidad de asociar más de una obra social a un mismo paciente.

### 4.2 Gestión de profesionales

**RF-06. Registrar profesionales**

El sistema debe permitir registrar un profesional mediante sus datos personales, correo electrónico, matrícula y especialidad.

El profesional debe estar asociado a un usuario del sistema.

**RF-07. Consultar profesionales**

El sistema debe permitir consultar los profesionales registrados y visualizar su información principal.

**RF-08. Asociación de profesionales a consultorios**

El sistema debe contemplar la asociación de profesionales con uno o varios consultorios.

Esta funcionalidad se encuentra definida en el modelo de datos y será incorporada a la gestión de usuarios en una etapa posterior.

### 4.3 Gestión de turnos

**RF-09. Registrar turnos**

El sistema debe permitir registrar un turno indicando:

- Paciente
- Profesional
- Fecha
- Hora de inicio
- Hora de fin
- Estado
- Observaciones

**RF-10. Consultar turnos**

El sistema debe permitir consultar los turnos registrados mostrando el paciente, profesional, fecha, horario, estado y observaciones.

**RF-11. Validar horarios de los turnos**

El sistema debe impedir registrar un turno cuando la hora de finalización sea igual o anterior a la hora de inicio.

**RF-12. Evitar superposición de turnos**

El sistema debe impedir que un profesional tenga dos turnos superpuestos en la misma fecha.

También debe impedir que un paciente tenga dos turnos superpuestos en la misma fecha.

Los turnos cancelados no deben bloquear el horario correspondiente.

### 4.4 Gestión de sesiones

**RF-13. Registrar sesiones**

El sistema debe permitir registrar una sesión asociada a un turno previamente registrado.

La sesión debe permitir registrar:

- Turno
- Fecha
- Observaciones
- Obra social, cuando corresponda

**RF-14. Consultar sesiones**

El sistema debe permitir consultar las sesiones registradas mostrando el paciente, profesional, fecha, observaciones y modalidad de cobertura.

**RF-15. Validar la existencia del turno**

El sistema no debe permitir registrar una sesión asociada a un turno inexistente.

**RF-16. Evitar sesiones duplicadas**

Un turno no puede tener más de una sesión registrada.

### 4.5 Gestión de pagos

**RF-17. Registrar pagos**

El sistema debe permitir registrar un pago asociado a una sesión indicando:

- Sesión
- Fecha
- Importe
- Medio de pago

**RF-18. Consultar pagos**

El sistema debe permitir consultar los pagos registrados mostrando el paciente, fecha, importe y medio de pago.

**RF-19. Permitir múltiples pagos por sesión**

Una sesión debe poder tener uno o varios pagos para permitir registrar pagos parciales.

**RF-20. Validar importe**

El sistema no debe permitir registrar pagos con un importe igual o menor a cero.

**RF-21. Calcular total pagado**

El sistema debe calcular el total acumulado de los pagos correspondientes a una sesión.

### 4.6 Gestión de obras sociales

**RF-22. Registrar obras sociales**

El sistema debe permitir registrar una obra social indicando su nombre y número de contacto.

**RF-23. Consultar obras sociales**

El sistema debe permitir consultar las obras sociales registradas y conocer su estado.

**RF-24. Asociar obras sociales a sesiones**

El sistema debe permitir indicar una obra social al registrar una sesión.

Cuando no corresponda utilizar una obra social, la sesión podrá registrarse como atención particular.

## 5. Requisitos no funcionales

### RNF-01. Usabilidad

La interfaz debe ser clara y sencilla de utilizar, permitiendo acceder a las principales funcionalidades sin conocimientos técnicos.

### RNF-02. Diseño responsive

La interfaz debe adaptarse a diferentes tamaños de pantalla, especialmente computadoras y dispositivos móviles.

### RNF-03. Integridad de datos

El sistema debe utilizar restricciones de la base de datos y validaciones del backend para evitar información inconsistente.

### RNF-04. Separación de responsabilidades

La aplicación debe mantener separadas las responsabilidades entre:

- Frontend
- Backend
- Base de datos

El frontend se encargará de la interacción con el usuario, el backend de la lógica y las validaciones, y PostgreSQL del almacenamiento de la información.

### RNF-05. Persistencia

La información registrada debe almacenarse de forma persistente en PostgreSQL.

### RNF-06. Seguridad

Las operaciones sobre la información deben estar controladas por el backend.

Las credenciales de usuarios deberán almacenarse mediante mecanismos de hash seguro antes de una puesta en producción.

### RNF-07. Mantenibilidad

El código debe mantenerse organizado y separado en archivos según su responsabilidad, facilitando futuras modificaciones y ampliaciones del sistema.

## 6. Reglas de negocio relacionadas

Los requisitos funcionales deben respetar las siguientes reglas de negocio:

- Un profesional debe estar asociado al menos a un consultorio y puede trabajar en múltiples consultorios.

- Un profesional puede atender a múltiples pacientes.

- No existe una asignación permanente entre profesionales y pacientes. La relación se determina mediante turnos y sesiones.

- Un profesional no puede tener dos turnos superpuestos en el mismo horario.

- Un paciente no puede tener dos turnos superpuestos en el mismo horario.

- Una sesión requiere un turno previo.

- Un turno puede existir sin generar una sesión, por ejemplo, cuando es cancelado.

- Un turno no puede generar más de una sesión.

- Una sesión puede tener múltiples pagos.

- Un paciente puede tener una o varias obras sociales.

- Una sesión puede realizarse de forma particular o mediante una obra social.

- La información perteneciente a cada consultorio debe mantenerse separada según los permisos de acceso correspondientes.

## 7. Alcance de la versión actual

La versión actual de NovaGest Mental prioriza las funcionalidades necesarias para gestionar la información administrativa básica de un consultorio psicológico.

Las funcionalidades implementadas actualmente son:

- Gestión de pacientes.

- Consulta, alta, modificación y eliminación de pacientes.

- Asociación de una obra social y número de afiliado al registrar un paciente.

- Gestión y consulta de profesionales.

- Gestión y consulta de turnos.

- Validación de horarios de los turnos.

- Prevención de superposición de turnos para profesionales y pacientes.

- Gestión y consulta de sesiones.

- Validación de turnos existentes y prevención de sesiones duplicadas.

- Gestión y consulta de pagos.

- Validación de importes.

- Cálculo del total pagado por sesión.

- Gestión y consulta de obras sociales.

- Asociación de obras sociales a sesiones.

- Persistencia de información mediante PostgreSQL.

- Comunicación entre frontend y backend mediante una API REST.

La asociación de profesionales con múltiples consultorios, la autenticación y la autorización avanzada se encuentran contempladas en el diseño del sistema, pero serán desarrolladas en una etapa posterior.

## 8. Funcionalidades fuera de alcance

Las siguientes funcionalidades no forman parte de la versión actual:

- Facturación electrónica.

- Aplicación móvil.

- Videollamadas.

- Integración con WhatsApp.

- Firma digital.

- Portal para pacientes.

- Integraciones con sistemas externos.

- Integración directa con organismos o empresas de obras sociales.

Estas funcionalidades podrán evaluarse en futuras versiones de NovaGest Mental.

## 9. Estado de implementación

La implementación se encuentra en desarrollo.

Las principales funcionalidades de gestión cuentan con una primera implementación funcional mediante:

- Frontend desarrollado con HTML, CSS y JavaScript.

- Backend desarrollado con FastAPI y Python.

- Base de datos PostgreSQL.

- API REST para la comunicación entre frontend y backend.

Las funcionalidades contempladas pero todavía no implementadas serán incorporadas progresivamente de acuerdo con las necesidades del proyecto y las futuras versiones del sistema.

## 10. Conclusión

Los requisitos definidos establecen el alcance funcional de NovaGest Mental y sirven como referencia para el desarrollo y las pruebas del sistema.

La versión actual prioriza la gestión de pacientes, profesionales, turnos, sesiones, pagos y obras sociales, incorporando validaciones básicas para mantener la integridad de la información.

La estructura definida permite continuar ampliando el sistema en futuras versiones sin modificar el objetivo general del proyecto.
