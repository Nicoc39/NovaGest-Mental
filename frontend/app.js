const API_URL = "https://novagest-mental-api.onrender.com";


/* AUTENTICACIÓN */

const login = document.getElementById("login");

const btnCerrarSesion = document.getElementById("btnCerrarSesion");

const formLogin = document.getElementById("formLogin");

const mensajeLogin = document.getElementById("mensajeLogin");

const usuarioConectado =
    document.getElementById("usuarioConectado");

const consultorioPaciente = document.getElementById("idConsultorioPaciente");

const consultorioProfesional = document.getElementById("idConsultorioProfesional");

const tokenGuardado = localStorage.getItem("token");

const usuarioGuardado =
    localStorage.getItem("usuario");

function obtenerToken() {
    return localStorage.getItem("token");
}

btnCerrarSesion.addEventListener("click", () => {

    localStorage.removeItem("token");
    localStorage.removeItem("usuario");
    localStorage.removeItem("rol");

    mostrarLogin();

});



async function cargarConsultorios() {

    try {
        const respuesta = await apiFetch(
            "/consultorios"
        );

        const consultorios = await respuesta.json();

        consultorioPaciente.innerHTML =
            '<option value="">Seleccione un consultorio</option>';

        consultorioProfesional.innerHTML =
            '<option value="">Seleccione un consultorio</option>';

        consultorios.forEach(consultorio => {

            const opcionPaciente = document.createElement("option");

            opcionPaciente.value = consultorio.id_consultorio;
            opcionPaciente.textContent = consultorio.nombre;

            consultorioPaciente.appendChild(opcionPaciente);


            const opcionProfesional = document.createElement("option");

            opcionProfesional.value = consultorio.id_consultorio;
            opcionProfesional.textContent = consultorio.nombre;

            consultorioProfesional.appendChild(opcionProfesional);
        });

    } catch (error) {
        console.error("Error al cargar consultorios:", error);
    }
}

async function apiFetch(url, opciones = {}) {

    const token = obtenerToken();

    const headers = {
        ...(opciones.headers || {})
    };

    if (token) {
        headers["Authorization"] = "Bearer " + token;
    }

    const respuesta = await fetch(API_URL + url, {
        ...opciones,
        headers
    });

    if (respuesta.status === 401) {
        localStorage.removeItem("token");

        if (login) {
            login.classList.remove("oculto");
        }

        throw new Error("Sesión expirada");
    }

    return respuesta;
}


function mostrarAplicacion() {

    document.getElementById("login").classList.add("oculto");

    document.getElementById("aplicacion").classList.remove("oculto");

}


function mostrarLogin() {

    login.classList.remove("oculto");

    document.getElementById("aplicacion").classList.add("oculto");

}


formLogin.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const email = document.getElementById("emailLogin").value;
    const password = document.getElementById("passwordLogin").value;

    mensajeLogin.textContent = "";

    try {

        const respuesta = await fetch(API_URL + "/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const datos = await respuesta.json();

        if (!respuesta.ok) {
            mensajeLogin.textContent =
                datos.detail || "Email o contraseña incorrectos";
            return;
        }

        localStorage.setItem("token", datos.access_token);
        localStorage.setItem("rol", datos.usuario.rol);

        localStorage.setItem(
            "usuario",
            JSON.stringify(datos.usuario)
        );

        usuarioConectado.textContent =
            datos.usuario.nombre + " " +
            datos.usuario.apellido + " — " +
            datos.usuario.rol;

        const rolUsuario = datos.usuario.rol;

        document.querySelectorAll(".opcion-menu").forEach(opcion => {

            if (opcion.textContent.trim() === "Consultorios") {

                if (rolUsuario !== "SUPERADMIN") {
                    opcion.classList.add("oculto");
                } else {
                    opcion.classList.remove("oculto");
                }
            }
        });

        btnNuevoProfesional.classList.remove("oculto");

        if (
            rolUsuario !== "SUPERADMIN" &&
            rolUsuario !== "ADMINISTRADOR"
        ) {
            btnNuevoProfesional.classList.add("oculto");
        }

        mostrarAplicacion();

        cargarConsultorios();
        cargarListaConsultorios();
        cargarPacientes();
        cargarProfesionales();
        cargarTurnos();
        cargarSesiones();
        cargarPagos();
        cargarObrasSociales();
        cargarHistorias();

    } catch (error) {

        console.error(error);

        mensajeLogin.textContent =
            "No se pudo conectar con el servidor.";
    }
});


/* PACIENTES */

const formulario = document.getElementById("formulario");
const btnNuevo = document.getElementById("btnNuevo");
const btnCancelar = document.getElementById("btnCancelar");
const formPaciente = document.getElementById("formPaciente");
const listaPacientes = document.getElementById("listaPacientes");
const obraSocialPaciente = document.getElementById("obraSocialPaciente");
const numeroAfiliado = document.getElementById("numeroAfiliado");

btnNuevo.addEventListener("click", async () => {
    formulario.classList.remove("oculto");

    await cargarObrasSocialesEnPaciente();
});


btnCancelar.addEventListener("click", () => {
    formulario.classList.add("oculto");
    formPaciente.reset();
});


async function cargarPacientes() {

    try {

        const respuesta = await apiFetch("/pacientes");

        if (!respuesta.ok) {
            throw new Error("No se pudieron cargar los pacientes");
        }

        const pacientes = await respuesta.json();

        listaPacientes.innerHTML = "";

        if (pacientes.length === 0) {
            listaPacientes.innerHTML =
                "<p>No hay pacientes registrados.</p>";
            return;
        }

        pacientes.forEach(paciente => {

            const elemento = document.createElement("div");

            elemento.classList.add("tarjeta", "paciente");

            elemento.innerHTML = `
                <h3>${paciente.nombre} ${paciente.apellido}</h3>
                <p><strong>DNI:</strong> ${paciente.dni}</p>
                <p><strong>Teléfono:</strong> ${paciente.telefono || "No registrado"}</p>
                <p><strong>Email:</strong> ${paciente.email || "No registrado"}</p>
                <p><strong>Obra social:</strong> ${paciente.obra_social || "Sin obra social"}</p>
                <p><strong>Afiliado:</strong> ${paciente.numero_afiliado || "No registrado"}</p>

                <div class="acciones">

                    <button onclick="editarPaciente(${paciente.id_paciente})">
                        Editar
                    </button>

                    <button onclick="eliminarPaciente(${paciente.id_paciente})">
                        Eliminar
                    </button>

                </div>
            `;

            listaPacientes.appendChild(elemento);
        });

    } catch (error) {

        console.error(error);

        listaPacientes.innerHTML =
            "<p>No se pudieron cargar los pacientes.</p>";
    }
}


async function cargarObrasSocialesEnPaciente() {

    try {

        const respuesta = await apiFetch("/obras-sociales");

        const obrasSociales = await respuesta.json();

        obraSocialPaciente.innerHTML =
            '<option value="">Sin obra social</option>';

        obrasSociales.forEach(obraSocial => {

            if (obraSocial.activo) {

                obraSocialPaciente.innerHTML += `
                    <option value="${obraSocial.id_obra_social}">
                        ${obraSocial.nombre}
                    </option>
                `;
            }
        });

    } catch (error) {

        console.error(error);
    }
}


formPaciente.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    const idObraSocial = obraSocialPaciente.value;

    if (
        idObraSocial &&
        !numeroAfiliado.value.trim()
    ) {

        alert(
            "Ingresá el número de afiliado para la obra social seleccionada."
        );

        return;
    }

    const paciente = {

        id_consultorio: parseInt(
            consultorioPaciente.value
        ),
        nombre: document.getElementById("nombre").value,
        apellido: document.getElementById("apellido").value,
        dni: document.getElementById("dni").value,
        fecha_nacimiento:
            document.getElementById("fecha_nacimiento").value || null,
        telefono:
            document.getElementById("telefono").value || null,
        email:
            document.getElementById("email").value || null
    };

    try {

        const respuesta = await apiFetch("/pacientes", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(paciente)
        });

        if (!respuesta.ok) {

            const error = await respuesta.json();

            alert(error.detail || "No se pudo crear el paciente.");

            return;
        }

        const pacienteCreado = await respuesta.json();

        if (idObraSocial) {

            const relacion = {

                id_paciente: pacienteCreado.id_paciente,
                id_obra_social: Number(idObraSocial),
                numero_afiliado:
                    numeroAfiliado.value.trim()
            };

            const respuestaRelacion =
                await apiFetch("/pacientes-obras-sociales", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify(relacion)
                });

            if (!respuestaRelacion.ok) {

                const error = await respuestaRelacion.json();

                alert(
                    error.detail ||
                    "No se pudo asociar la obra social."
                );

                return;
            }
        }

        formPaciente.reset();

        formulario.classList.add("oculto");

        cargarPacientes();

    } catch (error) {

        console.error(error);

        alert("No se pudo guardar el paciente.");
    }
});


async function eliminarPaciente(id) {

    const confirmar =
        confirm("¿Querés eliminar este paciente?");

    if (!confirmar) {
        return;
    }

    try {

        const respuesta =
            await apiFetch("/pacientes/" + id, {
                method: "DELETE"
            });

        if (!respuesta.ok) {

            const error = await respuesta.json();

            alert(
                error.detail ||
                "No se pudo eliminar el paciente."
            );

            return;
        }

        cargarPacientes();

    } catch (error) {

        console.error(error);

        alert("No se pudo eliminar el paciente.");
    }
}


async function editarPaciente(id) {

    const nombre = prompt("Nuevo nombre:");

    if (nombre === null || nombre.trim() === "") {
        return;
    }

    const apellido = prompt("Nuevo apellido:");

    if (apellido === null || apellido.trim() === "") {
        return;
    }

    try {

        const respuestaPaciente =
            await apiFetch("/pacientes/" + id);

        if (!respuestaPaciente.ok) {

            const error = await respuestaPaciente.json();

            alert(
                error.detail ||
                "No se pudo consultar el paciente."
            );

            return;
        }

        const paciente =
            await respuestaPaciente.json();

        paciente.nombre = nombre;
        paciente.apellido = apellido;

        const respuesta =
            await apiFetch("/pacientes/" + id, {

                method: "PUT",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(paciente)
            });

        console.log("Método enviado:", "PUT");
        console.log("URL:", API_URL + "/pacientes/" + id);
        console.log("Respuesta:", respuesta.status);

        if (!respuesta.ok) {

            const error = await respuesta.json();

            alert(
                error.detail ||
                "No se pudo modificar el paciente."
            );

            return;
        }

        cargarPacientes();

    } catch (error) {

        console.error(error);

        alert("No se pudo modificar el paciente.");
    }
}


/* HISTORIAS CLÍNICAS */

const formularioHistoria =
    document.getElementById("formularioHistoria");

const btnNuevaHistoria =
    document.getElementById("btnNuevaHistoria");

const btnCancelarHistoria =
    document.getElementById("btnCancelarHistoria");

const formHistoria =
    document.getElementById("formHistoria");

const listaHistorias =
    document.getElementById("listaHistorias");

const pacienteHistoria =
    document.getElementById("pacienteHistoria");


btnNuevaHistoria.addEventListener("click", async () => {

    formularioHistoria.classList.remove("oculto");

    await cargarPacientesEnHistoria();
});


btnCancelarHistoria.addEventListener("click", () => {

    formularioHistoria.classList.add("oculto");

    formHistoria.reset();
});


async function cargarPacientesEnHistoria() {

    try {

        const respuesta =
            await apiFetch("/pacientes");

        const pacientes =
            await respuesta.json();

        pacienteHistoria.innerHTML =
            '<option value="">Seleccionar paciente</option>';

        pacientes.forEach(paciente => {

            pacienteHistoria.innerHTML += `
                <option value="${paciente.id_paciente}">
                    ${paciente.nombre} ${paciente.apellido}
                </option>
            `;
        });

    } catch (error) {

        console.error(error);
    }
}


async function cargarHistorias() {

    try {

        const respuesta =
            await apiFetch("/historias-clinicas");

        const historias =
            await respuesta.json();

        listaHistorias.innerHTML = "";

        if (historias.length === 0) {

            listaHistorias.innerHTML =
                "<p>No hay historias clínicas registradas.</p>";

            return;
        }

        historias.forEach(historia => {

            const elemento =
                document.createElement("div");

            elemento.classList.add("tarjeta", "tarjeta-historia");

            elemento.innerHTML = `
                <h3>${historia.paciente}</h3>
                <p><strong>Fecha de apertura:</strong> ${historia.fecha_apertura}</p>
                <p><strong>Observaciones:</strong> ${historia.observaciones || "Sin observaciones"}</p>
            `;

            listaHistorias.appendChild(elemento);
        });

    } catch (error) {

        console.error(error);

        listaHistorias.innerHTML =
            "<p>No se pudieron cargar las historias clínicas.</p>";
    }
}


formHistoria.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    const historia = {

        id_paciente:
            Number(pacienteHistoria.value),

        fecha_apertura:
            document.getElementById("fechaAperturaHistoria").value,

        observaciones:
            document.getElementById("observacionesHistoria").value ||
            null
    };

    try {

        const respuesta =
            await apiFetch("/historias-clinicas", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(historia)
            });

        if (!respuesta.ok) {

            const error =
                await respuesta.json();

            alert(
                error.detail ||
                "No se pudo crear la historia clínica."
            );

            return;
        }

        formHistoria.reset();

        formularioHistoria.classList.add("oculto");

        cargarHistorias();

    } catch (error) {

        console.error(error);

        alert(
            "No se pudo guardar la historia clínica."
        );
    }
});


/* PROFESIONALES */

const formularioProfesional =
    document.getElementById("formularioProfesional");

const btnNuevoProfesional =
    document.getElementById("btnNuevoProfesional");

const btnCancelarProfesional =
    document.getElementById("btnCancelarProfesional");

const formProfesional =
    document.getElementById("formProfesional");

const listaProfesionales =
    document.getElementById("listaProfesionales");


btnNuevoProfesional.addEventListener("click", () => {

    formularioProfesional.classList.remove("oculto");
});




btnCancelarProfesional.addEventListener("click", () => {

    formularioProfesional.classList.add("oculto");

    formProfesional.reset();
});


async function cargarProfesionales() {

    try {

        const respuesta =
            await apiFetch("/profesionales");

        const profesionales =
            await respuesta.json();

        listaProfesionales.innerHTML = "";

        if (profesionales.length === 0) {

            listaProfesionales.innerHTML =
                "<p>No hay profesionales registrados.</p>";

            return;
        }

        profesionales.forEach(profesional => {

            const elemento =
                document.createElement("div");

            elemento.classList.add("tarjeta", "tarjeta-profesional");

            elemento.innerHTML = `
                <h3>${profesional.nombre} ${profesional.apellido}</h3>
                <p><strong>Matrícula:</strong> ${profesional.matricula}</p>
                <p><strong>Especialidad:</strong> ${profesional.especialidad || "No registrada"}</p>
                <p><strong>Email:</strong> ${profesional.email}</p>
            `;

            listaProfesionales.appendChild(elemento);
        });

    } catch (error) {

        console.error(error);

        listaProfesionales.innerHTML =
            "<p>No se pudo cargar la lista de profesionales.</p>";
    }
}


formProfesional.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    const profesional = {

        nombre:
            document.getElementById("nombreProfesional").value,

        apellido:
            document.getElementById("apellidoProfesional").value,

        email:
            document.getElementById("emailProfesional").value,

        password:
            document.getElementById("passwordProfesional").value,

        matricula:
            document.getElementById("matricula").value,

        especialidad:
            document.getElementById("especialidad").value ||
            null,

        id_consultorio: parseInt(
            consultorioProfesional.value
        )
    };

    try {

        const respuesta =
            await apiFetch("/profesionales", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(profesional)
            });

        if (!respuesta.ok) {

            const error =
                await respuesta.json();

            alert(
                error.detail ||
                "No se pudo crear el profesional."
            );

            return;
        }

        formProfesional.reset();

        formularioProfesional.classList.add("oculto");

        cargarProfesionales();

    } catch (error) {

        console.error(error);

        alert(
            "No se pudo guardar el profesional."
        );
    }
});


/* TURNOS */

const formularioTurno =
    document.getElementById("formularioTurno");

const btnNuevoTurno =
    document.getElementById("btnNuevoTurno");

const btnCancelarTurno =
    document.getElementById("btnCancelarTurno");

const formTurno =
    document.getElementById("formTurno");

const listaTurnos =
    document.getElementById("listaTurnos");

const pacienteTurno =
    document.getElementById("pacienteTurno");

const profesionalTurno =
    document.getElementById("profesionalTurno");


btnNuevoTurno.addEventListener("click", async () => {

    formularioTurno.classList.remove("oculto");

    await cargarPacientesEnTurno();

    await cargarProfesionalesEnTurno();
});


btnCancelarTurno.addEventListener("click", () => {

    formularioTurno.classList.add("oculto");

    formTurno.reset();
});


async function cargarPacientesEnTurno() {

    try {

        const respuesta =
            await apiFetch("/pacientes");

        const pacientes =
            await respuesta.json();

        pacienteTurno.innerHTML =
            '<option value="">Seleccionar paciente</option>';

        pacientes.forEach(paciente => {

            pacienteTurno.innerHTML += `
                <option value="${paciente.id_paciente}">
                    ${paciente.nombre} ${paciente.apellido}
                </option>
            `;
        });

    } catch (error) {

        console.error(error);
    }
}


async function cargarProfesionalesEnTurno() {

    try {

        const respuesta =
            await apiFetch("/profesionales");

        const profesionales =
            await respuesta.json();

        profesionalTurno.innerHTML =
            '<option value="">Seleccionar profesional</option>';

        profesionales.forEach(profesional => {

            profesionalTurno.innerHTML += `
                <option value="${profesional.id_profesional}">
                    ${profesional.nombre} ${profesional.apellido}
                </option>
            `;
        });

    } catch (error) {

        console.error(error);
    }
}


async function cargarTurnos() {

    try {

        const respuesta =
            await apiFetch("/turnos");

        const turnos =
            await respuesta.json();

        listaTurnos.innerHTML = "";

        if (turnos.length === 0) {

            listaTurnos.innerHTML =
                "<p>No hay turnos registrados.</p>";

            return;
        }

        turnos.forEach(turno => {

            const elemento =
                document.createElement("div");

            elemento.classList.add("tarjeta", "tarjeta-turno");

            elemento.innerHTML = `
                <h3>${turno.paciente}</h3>
                <p><strong>Profesional:</strong> ${turno.profesional}</p>
                <p><strong>Fecha:</strong> ${turno.fecha}</p>
                <p><strong>Horario:</strong> ${turno.hora_inicio} - ${turno.hora_fin}</p>
                <p>
                    <strong>Estado:</strong>
                    <span class="estado-turno estado-${turno.estado.toLowerCase()}">
                        ${turno.estado}
                    </span>
                </p>
                <p><strong>Observaciones:</strong> ${turno.observaciones || "Sin observaciones"}</p>
            `;

            listaTurnos.appendChild(elemento);
        });

    } catch (error) {

        console.error(error);

        listaTurnos.innerHTML =
            "<p>No se pudieron cargar los turnos.</p>";
    }
}


formTurno.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    const turno = {

        id_paciente:
            Number(pacienteTurno.value),

        id_profesional:
            Number(profesionalTurno.value),

        fecha:
            document.getElementById("fechaTurno").value,

        hora_inicio:
            document.getElementById("horaInicio").value,

        hora_fin:
            document.getElementById("horaFin").value,

        estado:
            document.getElementById("estadoTurno").value,

        observaciones:
            document.getElementById("observacionesTurno").value ||
            null
    };

    try {

        const respuesta =
            await apiFetch("/turnos", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(turno)
            });

        if (!respuesta.ok) {

            const error =
                await respuesta.json();

            alert(
                error.detail ||
                "No se pudo crear el turno."
            );

            return;
        }

        formTurno.reset();

        formularioTurno.classList.add("oculto");

        cargarTurnos();

    } catch (error) {

        console.error(error);

        alert("No se pudo guardar el turno.");
    }
});


/* SESIONES */

const formularioSesion =
    document.getElementById("formularioSesion");

const btnNuevaSesion =
    document.getElementById("btnNuevaSesion");

const btnCancelarSesion =
    document.getElementById("btnCancelarSesion");

const formSesion =
    document.getElementById("formSesion");

const listaSesiones =
    document.getElementById("listaSesiones");

const turnoSesion =
    document.getElementById("turnoSesion");


btnNuevaSesion.addEventListener("click", async () => {

    formularioSesion.classList.remove("oculto");

    await cargarTurnosEnSesion();
});


btnCancelarSesion.addEventListener("click", () => {

    formularioSesion.classList.add("oculto");

    formSesion.reset();
});


async function cargarTurnosEnSesion() {

    try {

        const respuestaTurnos =
            await apiFetch("/turnos");

        const turnos =
            await respuestaTurnos.json();

        turnoSesion.innerHTML =
            '<option value="">Seleccionar turno</option>';

        turnos.forEach(turno => {

            turnoSesion.innerHTML += `
                <option value="${turno.id_turno}">
                    ${turno.fecha} - ${turno.paciente} - ${turno.profesional}
                </option>
            `;
        });

        const respuestaObras =
            await apiFetch("/obras-sociales");

        const obrasSociales =
            await respuestaObras.json();

        const obraSocialSesion =
            document.getElementById("obraSocialSesion");

        obraSocialSesion.innerHTML =
            '<option value="">Particular / sin obra social</option>';

        obrasSociales.forEach(obraSocial => {

            if (obraSocial.activo) {

                obraSocialSesion.innerHTML += `
                    <option value="${obraSocial.id_obra_social}">
                        ${obraSocial.nombre}
                    </option>
                `;
            }
        });

    } catch (error) {

        console.error(error);
    }
}


async function cargarSesiones() {

    try {

        const respuesta =
            await apiFetch("/sesiones");

        const sesiones =
            await respuesta.json();

        listaSesiones.innerHTML = "";

        if (sesiones.length === 0) {

            listaSesiones.innerHTML =
                "<p>No hay sesiones registradas.</p>";

            return;
        }

        sesiones.forEach(sesion => {

            const elemento =
                document.createElement("div");

            elemento.classList.add("tarjeta", "tarjeta-sesion");

            elemento.innerHTML = `
                <h3>${sesion.paciente}</h3>
                <p><strong>Profesional:</strong> ${sesion.profesional}</p>
                <p><strong>Fecha:</strong> ${sesion.fecha}</p>
                <p><strong>Observaciones:</strong> ${sesion.observaciones || "Sin observaciones"}</p>
                <p><strong>Obra social:</strong> ${
                    sesion.id_obra_social || "Particular"
                }</p>
            `;

            listaSesiones.appendChild(elemento);
        });

    } catch (error) {

        console.error(error);

        listaSesiones.innerHTML =
            "<p>No se pudieron cargar las sesiones.</p>";
    }
}


formSesion.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    const obraSocial =
        document.getElementById("obraSocialSesion").value;

    const sesion = {

        id_turno:
            Number(turnoSesion.value),

        fecha:
            document.getElementById("fechaSesion").value,

        observaciones:
            document.getElementById("observacionesSesion").value ||
            null,

        id_obra_social:
            obraSocial ? Number(obraSocial) : null
    };

    try {

        const respuesta =
            await apiFetch("/sesiones", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(sesion)
            });

        if (!respuesta.ok) {

            const error =
                await respuesta.json();

            alert(
                error.detail ||
                "No se pudo crear la sesión."
            );

            return;
        }

        formSesion.reset();

        formularioSesion.classList.add("oculto");

        cargarSesiones();

    } catch (error) {

        console.error(error);

        alert("No se pudo guardar la sesión.");
    }
});


/* PAGOS */

const formularioPago =
    document.getElementById("formularioPago");

const btnNuevoPago =
    document.getElementById("btnNuevoPago");

const btnCancelarPago =
    document.getElementById("btnCancelarPago");

const formPago =
    document.getElementById("formPago");

const listaPagos =
    document.getElementById("listaPagos");

const sesionPago =
    document.getElementById("sesionPago");


btnNuevoPago.addEventListener("click", async () => {

    formularioPago.classList.remove("oculto");

    await cargarSesionesEnPago();
});


btnCancelarPago.addEventListener("click", () => {

    formularioPago.classList.add("oculto");

    formPago.reset();
});


async function cargarSesionesEnPago() {

    try {

        const respuesta =
            await apiFetch("/sesiones");

        const sesiones =
            await respuesta.json();

        sesionPago.innerHTML =
            '<option value="">Seleccionar sesión</option>';

        sesiones.forEach(sesion => {

            sesionPago.innerHTML += `
                <option value="${sesion.id_sesion}">
                    ${sesion.fecha} - ${sesion.paciente}
                </option>
            `;
        });

    } catch (error) {

        console.error(error);
    }
}


async function cargarPagos() {

    try {

        const respuesta =
            await apiFetch("/pagos");

        const pagos =
            await respuesta.json();

        listaPagos.innerHTML = "";

        if (pagos.length === 0) {

            listaPagos.innerHTML =
                "<p>No hay pagos registrados.</p>";

            return;
        }

        pagos.forEach(pago => {

            const elemento =
                document.createElement("div");

            elemento.classList.add("tarjeta", "tarjeta-pago");

            elemento.innerHTML = `
                <h3>${pago.paciente}</h3>
                <p><strong>Fecha:</strong> ${pago.fecha}</p>
                <p><strong>Importe:</strong> $${pago.importe}</p>
                <p><strong>Medio de pago:</strong> ${pago.medio_pago}</p>
                <p><strong>Total pagado de la sesión:</strong> $${pago.total_pagado}</p>
            `;

            listaPagos.appendChild(elemento);
        });

    } catch (error) {

        console.error(error);

        listaPagos.innerHTML =
            "<p>No se pudieron cargar los pagos.</p>";
    }
}


formPago.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    const pago = {

        id_sesion:
            Number(sesionPago.value),

        fecha:
            document.getElementById("fechaPago").value,

        importe:
            Number(document.getElementById("importePago").value),

        medio_pago:
            document.getElementById("medioPago").value
    };

    try {

        const respuesta =
            await apiFetch("/pagos", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(pago)
            });

        if (!respuesta.ok) {

            const error =
                await respuesta.json();

            alert(
                error.detail ||
                "No se pudo crear el pago."
            );

            return;
        }

        formPago.reset();

        formularioPago.classList.add("oculto");

        cargarPagos();

    } catch (error) {

        console.error(error);

        alert("No se pudo guardar el pago.");
    }
});


/* OBRAS SOCIALES */

const formularioObraSocial =
    document.getElementById("formularioObraSocial");

const btnNuevaObraSocial =
    document.getElementById("btnNuevaObraSocial");

const btnCancelarObraSocial =
    document.getElementById("btnCancelarObraSocial");

const formObraSocial =
    document.getElementById("formObraSocial");

const listaObrasSociales =
    document.getElementById("listaObrasSociales");


const formularioConsultorio =
    document.getElementById("formularioConsultorio");

const btnNuevoConsultorio =
    document.getElementById("btnNuevoConsultorio");

const btnCancelarConsultorio =
    document.getElementById("btnCancelarConsultorio");

const formConsultorio =
    document.getElementById("formConsultorio");

const listaConsultorios =
    document.getElementById("listaConsultorios");


btnNuevaObraSocial.addEventListener("click", () => {

    formularioObraSocial.classList.remove("oculto");
});


btnCancelarObraSocial.addEventListener("click", () => {

    formularioObraSocial.classList.add("oculto");

    formObraSocial.reset();
});


async function cargarObrasSociales() {

    try {

        const respuesta =
            await apiFetch("/obras-sociales");

        const obrasSociales =
            await respuesta.json();

        listaObrasSociales.innerHTML = "";

        if (obrasSociales.length === 0) {

            listaObrasSociales.innerHTML =
                "<p>No hay obras sociales registradas.</p>";

            return;
        }

        obrasSociales.forEach(obraSocial => {

            const elemento =
                document.createElement("div");

            elemento.classList.add("tarjeta", "tarjeta-obra-social");

            elemento.innerHTML = `
                <h3>${obraSocial.nombre}</h3>

                <p><strong>Contacto:</strong> ${
                    obraSocial.numero_contacto ||
                    "No registrado"
                }</p>

                <p>
                    <strong>Estado:</strong>
                    <span class="estado-obra-social ${
                        obraSocial.activo
                            ? "activa"
                            : "inactiva"
                    }">
                        ${
                            obraSocial.activo
                                ? "Activa"
                                : "Inactiva"
                        }
                    </span>
                </p>
            `;

            listaObrasSociales.appendChild(elemento);
        });

    } catch (error) {

        console.error(error);

        listaObrasSociales.innerHTML =
            "<p>No se pudieron cargar las obras sociales.</p>";
    }
}


formObraSocial.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    const obraSocial = {

        nombre:
            document.getElementById("nombreObraSocial").value,

        numero_contacto:
            document.getElementById("numeroContactoObraSocial").value ||
            null
    };

    try {

        const respuesta =
            await apiFetch("/obras-sociales", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(obraSocial)
            });

        if (!respuesta.ok) {

            const error =
                await respuesta.json();

            alert(
                error.detail ||
                "No se pudo crear la obra social."
            );

            return;
        }

        formObraSocial.reset();

        formularioObraSocial.classList.add("oculto");

        cargarObrasSociales();

    } catch (error) {

        console.error(error);

        alert(
            "No se pudo guardar la obra social."
        );
    }
});

/* CONSULTORIOS */

btnNuevoConsultorio.addEventListener("click", () => {

    formularioConsultorio.classList.remove("oculto");
});


btnCancelarConsultorio.addEventListener("click", () => {

    formularioConsultorio.classList.add("oculto");

    formConsultorio.reset();
});


async function cargarConsultorios() {

    try {
        const respuesta = await apiFetch(
            "/consultorios"
        );

        const consultorios = await respuesta.json();

        consultorioPaciente.innerHTML =
            '<option value="">Seleccione un consultorio</option>';

        consultorioProfesional.innerHTML =
            '<option value="">Seleccione un consultorio</option>';

        consultorios.forEach(consultorio => {

            const opcionPaciente = document.createElement("option");

            opcionPaciente.value = consultorio.id_consultorio;
            opcionPaciente.textContent = consultorio.nombre;

            consultorioPaciente.appendChild(opcionPaciente);


            const opcionProfesional = document.createElement("option");

            opcionProfesional.value = consultorio.id_consultorio;
            opcionProfesional.textContent = consultorio.nombre;

            consultorioProfesional.appendChild(opcionProfesional);
        });

        cargarListaConsultorios();

    } catch (error) {
        console.error("Error al cargar consultorios:", error);
    }
}

async function cargarListaConsultorios() {

    try {

        const respuesta =
            await apiFetch("/consultorios");

        const consultorios =
            await respuesta.json();

        listaConsultorios.innerHTML = "";

        if (consultorios.length === 0) {

            listaConsultorios.innerHTML =
                "<p>No hay consultorios registrados.</p>";

            return;
        }

        consultorios.forEach(consultorio => {

            const elemento =
                document.createElement("div");

            elemento.classList.add("tarjeta", "tarjeta-consultorio");

            elemento.innerHTML = `
                <h3>${consultorio.nombre}</h3>

                <p><strong>Dirección:</strong> ${
                    consultorio.direccion ||
                    "No registrada"
                }</p>

                <p><strong>Teléfono:</strong> ${
                    consultorio.telefono ||
                    "No registrado"
                }</p>

                <p><strong>Email:</strong> ${
                    consultorio.email ||
                    "No registrado"
                }</p>
            `;

            listaConsultorios.appendChild(elemento);
        });

    } catch (error) {

        console.error(error);

        listaConsultorios.innerHTML =
            "<p>No se pudieron cargar los consultorios.</p>";
    }
}


formConsultorio.addEventListener("submit", async (evento) => {

    evento.preventDefault();

    const consultorio = {

        nombre:
            document.getElementById("nombreConsultorio").value,

        direccion:
            document.getElementById("direccionConsultorio").value ||
            null,

        telefono:
            document.getElementById("telefonoConsultorio").value ||
            null,

        email:
            document.getElementById("emailConsultorio").value ||
            null
    };

    try {

        const respuesta =
            await apiFetch("/consultorios", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(consultorio)
            });

        if (!respuesta.ok) {

            const error =
                await respuesta.json();

            alert(
                error.detail ||
                "No se pudo crear el consultorio."
            );

            return;
        }

        formConsultorio.reset();

        formularioConsultorio.classList.add("oculto");

        cargarListaConsultorios();
        cargarConsultorios();

    } catch (error) {

        console.error(error);

        alert(
            "No se pudo guardar el consultorio."
        );
    }
});


function configurarMenuPorRol(rol) {

    const enlacesMenu =
        document.querySelectorAll(".opcion-menu");

    enlacesMenu.forEach(enlace => {

        if (
            enlace.textContent.trim() === "Consultorios"
        ) {

            if (rol !== "SUPERADMIN") {
                enlace.classList.add("oculto");
            } else {
                enlace.classList.remove("oculto");
            }
        }

        if (
            enlace.textContent.trim() === "Historias clínicas"
        ) {

            if (rol === "ADMINISTRATIVO") {
                enlace.classList.add("oculto");
            } else {
                enlace.classList.remove("oculto");
            }
        }
    });
}

/* INICIO */

if (tokenGuardado) {

    if (usuarioGuardado) {
        const usuario = JSON.parse(usuarioGuardado);

        usuarioConectado.textContent =
            usuario.nombre + " " +
            usuario.apellido + " — " +
            usuario.rol;
    }

    mostrarAplicacion();

    const rolGuardado = localStorage.getItem("rol");

    configurarMenuPorRol(rolGuardado);

    cargarConsultorios();
    cargarPacientes();
    cargarProfesionales();
    cargarTurnos();
    cargarSesiones();
    cargarPagos();
    cargarObrasSociales();
    cargarHistorias();

} else {

    mostrarLogin();
}

/* NAVEGACIÓN ENTRE MÓDULOS */

function cambiarModulo(idSeccion) {

    document.getElementById("seccionPacientes").classList.add("oculto");
    document.getElementById("seccionHistorias").classList.add("oculto");
    document.getElementById("seccionProfesionales").classList.add("oculto");
    document.getElementById("seccionTurnos").classList.add("oculto");
    document.getElementById("seccionSesiones").classList.add("oculto");
    document.getElementById("seccionPagos").classList.add("oculto");
    document.getElementById("seccionObrasSociales").classList.add("oculto");
    document.getElementById("seccionConsultorios").classList.add("oculto");

    document.getElementById(idSeccion).classList.remove("oculto");

    document.querySelectorAll(".opcion-menu").forEach(opcion => {
        opcion.classList.remove("activo");
    });

    document.querySelector(
        `.opcion-menu[onclick*="'${idSeccion}'"]`
    ).classList.add("activo");

}

document.addEventListener("DOMContentLoaded", function() {
    cambiarModulo("seccionPacientes");
});