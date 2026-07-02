# NovaGest Mental

## Sistema Integral de Gestión para Consultorios Psicológicos

---

### Documento

Análisis del Negocio

### Versión

v0.1.0

### Estado

En desarrollo

### Autor

Nicolás Carranza

### Fecha

30 de junio de 2026

###
Índice

1. Introducción

2. Objetivo

3. Alcance

4. Actores involucrados

5. Procesos del negocio

6. Reglas de negocio

7. Descripción del negocio

8. Problemas identificados

9. Riesgos y supuestos

10. Próximas etapas

###
1. Introducción

NovaGest Mental es un proyecto que busca desarrollar un sistema de gestión administrativa destinado a consultorios, personal administrativo y profesionales del area de la salud mental, cuya finalidad es centralizar la información relevante de la actividad profesional y brindar herramientas para la gestión de turnos, historias clínicas, pagos y demás procesos administrativos relacionados con la atención de pacientes.
Este documento presenta el análisis del negocio y en las siguientes secciones se explicaran los objetivos, su alcance, los actores intervinientes, el proceso del negocio y las reglas que servirán como base para el diseño del sistema.

2. Objetivos

Objetivo General: Desarrollar una solución tecnologica que contribuya a optimizar la gestion administrativa de los profesionales de la salud mental y de los consultorios de atencion psicologica, mediante la centralización y automatización de procesos relacionados con la gestión de pacientes y sesiones.

Objetivos Específicos:
● Registrar y administrar la información de pacientes y sesiones 
realizadas. 
● Optimizar el seguimiento de pagos, pagos pendientes e ingresos generados por la 
actividad profesional. 
● Facilitar la gestión administrativa relacionada con las prestaciones realizadas a través de obras 
sociales. 
● Proporcionar reportes e indicadores que permitan conocer la situación administrativa de 
cada profesional o consultorio. 
● Permitir la administración de múltiples profesionales dentro de una misma organización, manteniendo 
la información organizada y centralizada. 
● Reducir el tiempo destinado a tareas administrativas mediante la automatización de procesos 
rutinarios.

3. Alcance

NovaGest Mental abarca la gestión de consultorios psicológicos, centralizando la información de pacientes, profesionales y la administración de la prestación de servicios psicologicos.

En esta versión se prevén las siguientes funcionalidades:
*Gestión de la información de pacientes
*Registro e historial de sesiones
*Gestión administrativa y económica del consultorio
*Gestión de obras sociales
*Agenda y gestión de turnos
*Reportes administrativos
*Gestión de múltiples profesionales dentro de un mismo consultorio

Las funcionalidades que no se incluyen son:
*Facturación electrónica
*Aplicación móvil
*Videoconsultas
*Integración con WhatsApp
*Firma Digital
*Portal para pacientes
*Integración con sistemas externos

4. Actores involucrados

Los actores principales que interactuan con el sistema NovaGest Mental son:

Psicólogos: Son los profesionales que brindan sus servicios a los pacientes. Utilizan el sistema para  registrar sesiones y consultar el historial de los pacientes. Pueden trabajar de forma independiente o dentro de una consultorio, de ser independientes tambien se ocupan de su propia organización administrativa gestionando turnos y su agenda y registrando los pagos, tanto efectuados como los pendientes.

Personal Administrativo: Son aquellas personas a cargo de la organización de la parte operativa.  Administran los turnos de los pacientes, la agenda de los profesionales y registran los pagos.

Administrador del consultorio: En los casos de haberlo, es el actor interviniente en la administración del personal del consultorio, en la revisión de los reportes y el control del funcionamiento general.

A modo de actor secundario tenemos a los pacientes, si bien no interactua directamente con el sistema es una parte importante dentro del funcionamiento del negocio.

5. Procesos del Negocio

    1. Proceso de gestión de turnos
* Se solicita un turno
* Se verifica disponibilidad
* Se asigna un horario/profesional
* Se confirma la solicitud del turno
* Se registra en la agenda
* El paciente acude al turno/ Cancela o reprograma el turno

    2. Proceso de atención de sesión
* El paciente acude al turno
* El profesional revisa el historial del paciente
* El profesional lleva adelante la sesión
* Se registra la informacion de la sesión
* Se actualiza el historial del paciente

    3. Proceso de registro de paciente
* Se ingresan los datos del paciente al sistema
* Se valida la información ingresada
* Se crea la ficha clínica

    4. Proceso de gestión de pagos
* Se registra el pago de la sesión
* Se verifica la situacion del estado de la cuenta
* Se actualiza el estado de la cuenta
* Se controlan los pagos pendientes

    5. Proceso de administración de profesionales
* Se verifican las credenciales del profesional
* Se da de alta al profesional en el sistema
*Se le asigna una agenda 
*Se configura su disponibilidad de dias y horarios
*Se gestionan las asignaciones de pacientes

    6. Proceso de reportes
* Se recopilan los datos de las sesiones
* Se realizan análisis de los ingresos
* Se visualiza la actividad por profesionales
* Se genera la documentacion informativa para el consultorio


6. Reglas de negocio

REGLAS DE NEGOCIO

    1. Gestión de turnos
*Un profesional no puede tener mas de un turno en el mismo horario
*Un paciente no puede tener mas de un turno simultáneo
*Un turno puede estar en estado: Pendiente, Confirmado, Cancelado, Reprogramado
*Se puede reasignar un turno en estado Cancelado

    2. Sesiones
*Toda sesión debe asociarse a un paciente y a un profesional
*Toda sesión es con turno previo
*Las sesiones son presenciales

    3. Pacientes
*La planilla de un paciente debe estar completa con los datos minimos obligatorios
*No pueden existir dos pacientes con el mismo dni

    4. Profesionales
*Todo profesional debe contar con la matricula profesional vigente
*Un profesional debe estar asociado al menos a un consultorio
*Un profesional puede tener varios pacientes asignados
*Los turnos se asignan de acuerdo a la disponibilidad del profesional

    5. Pagos
*Cada sesión puede tener un pago asociado
*Un pago puede estar en estado: Pendiente, parcial o completo
*Un paciente puede tener saldo pendiente acumulado

    6. Consultorio (Nivel gral)
*Un consultorio puede tener varios profesionales
*Toda la información esta aislada por consultorio
*Un profesional no puede acceder al registro de sesiones de un paciente que no sea suyo

    7. Obras sociales
*Un paciente puede tener una o varias obras sociales
*Una sesión puede estar asociada a una obra social o ser consulta particular

7. Descripción del negocio

Un consultorio psicológico es un espacio dedicado a la prestación de servicios de atención clínica y salud mental, orientado al diagnóstico, tratamiento y acompañamiento de los pacientes. Más allá de la actividad terapéutica central que ocurre dentro del espacio de consulta, el funcionamiento viable y sostenible de estos centros —o de la práctica de profesionales independientes— depende de una sólida estructura operativa subyacente. Esta estructura engloba todas las tareas administrativas del día a día, las cuales van desde la recepción y asignación de la demanda de atención, hasta la coordinación de los recursos disponibles, la gestión financiera y el cumplimiento de las normativas vigentes para el ejercicio profesional.

En el desarrollo de esta actividad cotidiana, se genera y manipula un volumen constante de información interconectada que constituye el activo operativo del negocio. El flujo comienza con los datos filiatorios y de cobertura médica de los pacientes, que deben cruzarse con las especialidades, matrículas y horarios disponibles de los profesionales del centro. Esta interacción se materializa en la agenda mediante la asignación de turnos, los cuales determinan el ritmo de trabajo diario y derivan formalmente en la realización de las sesiones clínicas. Finalmente, cada una de estas prestaciones desencadena un circuito económico reflejado en el registro de pagos —ya sean particulares o procesados a través del sistema de obras sociales—, lo que requiere un seguimiento estricto para mantener las cuentas al día.

La administración precisa y oportuna de toda esta información es crítica, ya que un control deficiente de las variables operativas impacta negativamente en la calidad del servicio y en la salud financiera del consultorio. La superposición de horarios, la pérdida de trazabilidad en las historias clínicas, la falta de control sobre los saldos pendientes o la desorganización en los trámites de las obras sociales no solo desgastan al personal administrativo y a los terapeutas, sino que también afectan directamente la experiencia del paciente. Por lo tanto, asegurar el orden, la confidencialidad y la fluidez de estos datos es un requisito indispensable para la sostenibilidad económica del negocio y para garantizar un entorno profesional enfocado en el bienestar clínico.

8. Problemas identificados

A partir del análisis de la dinámica operativa actual en los consultorios y en la práctica de los profesionales independientes, se han detectado los siguientes problemas en su gestión diaria:

Información distribuida en múltiples herramientas o registros manuales: Los datos esenciales del negocio (fichas de pacientes, agendas de turnos, registros de cobros) suelen encontrarse fragmentados en cuadernos físicos, planillas de cálculo independientes o aplicaciones de mensajería. Esta dispersión dificulta el acceso inmediato a la información y obliga a consultar diferentes fuentes para resolver una sola gestión administrativa.

Dificultad para controlar la disponibilidad de los profesionales: La coordinación de las agendas se vuelve compleja al gestionar múltiples profesionales con diferentes días, horarios y consultorios asignados. Sin una validación centralizada en tiempo real, aumenta significativamente el riesgo de superposición de turnos para un mismo profesional o la asignación de citas en horarios donde el psicólogo no se encuentra disponible.

Seguimiento ineficiente de pagos y saldos pendientes: Debido a que las sesiones pueden abonarse de forma particular (total o parcial) o facturarse a través de diferentes obras sociales, el control de las cuentas se vuelve propenso a errores. El negocio carece de un mecanismo ágil para identificar de forma inmediata qué pacientes registran saldos pendientes acumulados o qué prestaciones a coberturas médicas aún no han sido liquidadas.

Riesgo de pérdida o inconsistencia de información: El uso de formatos físicos o archivos locales e independientes para registrar las sesiones y los datos de los pacientes eleva el riesgo de extravío de documentación valiosa. Asimismo, al no existir validaciones estrictas (como el control de duplicidad por DNI), se genera la duplicación de registros o la existencia de fichas clínicas incompletas.

Tiempo excesivo dedicado a tareas administrativas repetitivas: El personal operativo (o el propio profesional en su práctica independiente) invierte una gran parte de su jornada laboral en procesos rutinarios y manuales, tales como la transcripción de datos para obras sociales y la actualización manual de agendas, registros de sesiones y estados de cuentade cuenta. Esto reduce el tiempo disponible para actividades de mayor valor o para la atención directa.

Dificultad para obtener información consolidada sobre la actividad del consultorio: Al finalizar un período, resulta sumamente complejo y lento evaluar el rendimiento del negocio. Calcular los ingresos totales generados, identificar el volumen de sesiones realizadas por cada profesional o conocer el índice de ausentismo de los pacientes requiere recolectar y unificar manualmente datos de diversas planillas, lo que impide una toma de decisiones basada en indicadores claros y actualizados.

9. Riesgos y supuestos

Predisposición al cambio operativo: La dirección del consultorio y su equipo están totalmente dispuestos a reemplazar o complementar sus registros manuales y planillas tradicionales por un sistema digital centralizado.

Compromiso con la actualización de datos: La información que se ingrese al sistema será responsabilidad exclusiva de los usuarios autorizados, asumiendo el compromiso de mantenerla al día con el fin de garantizar la integridad y actualización de la información registrada.

Cumplimiento del marco legal vigente: Los profesionales que utilicen la plataforma cuentan con la matrícula profesional habilitante y la documentación legal requerida para ejercer su actividad clínica.

Disponibilidad de información inicial: Se asume que el consultorio dispone de la información mínima necesaria de pacientes, profesionales y agenda para realizar la carga inicial del sistema.



Riesgos
A continuación, se detallan aquellos factores del entorno, del negocio y del ámbito técnico que podrían afectar negativamente el éxito del proyecto o la continuidad de la operación del consultorio:

Resistencia al cambio organizacional: Existe la posibilidad de que los psicólogos o el personal administrativo, habituados al uso de registros manuales o herramientas tradicionales, muestren renuencia a adoptar la nueva plataforma, lo que podría ralentizar la fase de implementación o provocar un uso incorrecto de la misma.

Errores en la carga inicial y migración de datos: El traspaso de la información histórica desde soportes físicos o planillas dispersas hacia el nuevo sistema conlleva un riesgo elevado de omisión de datos, duplicados o errores de transcripción, afectando la calidad de la información registrada desde el inicio.

Modificaciones en el marco regulatorio: Cambios imprevistos en la normativa legal y fiscal vigente en materia de salud mental (como regulaciones sobre el manejo de historias clínicas) o variaciones en los requerimientos de las obras sociales podrían exigir modificaciones estructurales no planificadas en la lógica del sistema.

Escalabilidad desalineada con el MVP: Un crecimiento acelerado del consultorio o la incorporación de nuevas dinámicas comerciales podrían demandar de forma inmediata funcionalidades complejas (como facturación electrónica o integraciones externas) que no están contempladas dentro del alcance de esta primera versión.

Pérdida de información crítica por fallas de respaldo: Al centralizar datos sensibles (clínicos y financieros), la falta de políticas estrictas o fallas en los mecanismos de copias de seguridad automáticas ante un incidente de infraestructura representa un riesgo crítico para la continuidad del negocio.

Inconsistencia operativa por errores continuos de carga: La introducción de datos erróneos o incompletos de forma recurrente por parte de los usuarios (por ejemplo, en los estados de pago o datos de DNI) puede corromper la integridad de la base de datos, restándole confiabilidad a los reportes administrativos generados.

10. Próximas Etapas

Próximas etapas
Este análisis del negocio representa el punto de partida y la base sólida sobre la cual se construirá todo el proyecto. Al haber definido con claridad qué hace el consultorio, cuáles son sus reglas y qué problemas se necesitan resolver, es momento de avanzar hacia el diseño técnico y la construcción de la solución. A partir de este documento, el proyecto seguirá un camino estructurado que transformará estos requerimientos en un sistema real y funcional a través de los siguientes pasos:

Elaboración del modelo conceptual de datos (DER): Crear un diagrama visual que represente cómo se relacionan entre sí los elementos principales del negocio (pacientes, profesionales, turnos, etc.).

Construcción del modelo relacional: Traducir ese diagrama visual a una estructura de tablas, definiendo cómo se organizará la información internamente.

Elaboración del diccionario de datos: Crear un documento guía que detalle las características específicas de cada dato que se guardará (por ejemplo, si el DNI es un número, qué longitud tiene, etc.).

Implementación de la base de datos en PostgreSQL: Crear de forma real la base de datos en el servidor utilizando este motor de almacenamiento.

Desarrollo de consultas, vistas y funciones: Programar los mecanismos internos para que la base de datos pueda buscar, filtrar y procesar la información de manera rápida y eficiente.

Diseño de la arquitectura de la aplicación: Planificar la estructura técnica y los componentes de software que darán soporte al sistema.

Desarrollo del backend: Programar el "cerebro" del sistema, es decir, la lógica interna que procesará las solicitudes, validará las reglas de negocio y conectará la pantalla con la base de datos.

Desarrollo del frontend: Diseñar y construir las pantallas, botones y la interfaz visual con la que interactuarán los secretarios, psicólogos y administradores.

Pruebas funcionales y validación con usuarios: Poner a prueba el sistema en escenarios reales para asegurar que funcione sin errores y que realmente resuelva los problemas identificados.

Preparación de la primera versión estable del sistema: Realizar los ajustes finales y dejar la plataforma lista para su puesta en marcha oficial en el consultorio.