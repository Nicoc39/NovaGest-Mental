-- ============================================
-- NovaGest Mental
-- Estructura inicial de la base de datos
-- PostgreSQL
-- ============================================

-- ============================================
-- CONSULTORIO
-- ============================================

CREATE TABLE consultorio (
id_consultorio SERIAL PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
direccion VARCHAR(150),
telefono VARCHAR(30),
email VARCHAR(100),
activo BOOLEAN NOT NULL DEFAULT TRUE
);

-- ============================================
-- USUARIO
-- ============================================

CREATE TABLE usuario (
id_usuario SERIAL PRIMARY KEY,
nombre VARCHAR(100) NOT NULL,
apellido VARCHAR(100) NOT NULL,
email VARCHAR(150) NOT NULL UNIQUE,
password_hash VARCHAR(255) NOT NULL,
rol VARCHAR(30) NOT NULL,
activo BOOLEAN NOT NULL DEFAULT TRUE,

```
CONSTRAINT chk_usuario_rol
    CHECK (rol IN ('ADMINISTRADOR', 'ADMINISTRATIVO', 'PROFESIONAL'))
```

);

-- ============================================
-- PROFESIONAL
-- ============================================

CREATE TABLE profesional (
id_profesional SERIAL PRIMARY KEY,
id_usuario INTEGER NOT NULL UNIQUE,
matricula VARCHAR(50) NOT NULL UNIQUE,
especialidad VARCHAR(100),
activo BOOLEAN NOT NULL DEFAULT TRUE,

```
CONSTRAINT fk_profesional_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES usuario(id_usuario)
```

);

-- ============================================
-- PACIENTE
-- ============================================

CREATE TABLE paciente (
id_paciente SERIAL PRIMARY KEY,
id_consultorio INTEGER NOT NULL,
nombre VARCHAR(100) NOT NULL,
apellido VARCHAR(100) NOT NULL,
dni VARCHAR(20) NOT NULL,
fecha_nacimiento DATE,
telefono VARCHAR(30),
email VARCHAR(150),
activo BOOLEAN NOT NULL DEFAULT TRUE,

```
CONSTRAINT fk_paciente_consultorio
    FOREIGN KEY (id_consultorio)
    REFERENCES consultorio(id_consultorio),

CONSTRAINT uq_paciente_dni_consultorio
    UNIQUE (id_consultorio, dni)
```

);

-- ============================================
-- OBRA SOCIAL
-- ============================================

CREATE TABLE obra_social (
id_obra_social SERIAL PRIMARY KEY,
nombre VARCHAR(100) NOT NULL UNIQUE,
numero_contacto VARCHAR(30),
activo BOOLEAN NOT NULL DEFAULT TRUE
);

-- ============================================
-- CONSULTORIO - USUARIO
-- ============================================

CREATE TABLE consultorio_usuario (
id_consultorio INTEGER NOT NULL,
id_usuario INTEGER NOT NULL,

```
PRIMARY KEY (id_consultorio, id_usuario),

CONSTRAINT fk_consultorio_usuario_consultorio
    FOREIGN KEY (id_consultorio)
    REFERENCES consultorio(id_consultorio)
    ON DELETE CASCADE,

CONSTRAINT fk_consultorio_usuario_usuario
    FOREIGN KEY (id_usuario)
    REFERENCES usuario(id_usuario)
    ON DELETE CASCADE
```

);

-- ============================================
-- CONSULTORIO - PROFESIONAL
-- ============================================

CREATE TABLE consultorio_profesional (
id_consultorio INTEGER NOT NULL,
id_profesional INTEGER NOT NULL,

```
PRIMARY KEY (id_consultorio, id_profesional),

CONSTRAINT fk_consultorio_profesional_consultorio
    FOREIGN KEY (id_consultorio)
    REFERENCES consultorio(id_consultorio)
    ON DELETE CASCADE,

CONSTRAINT fk_consultorio_profesional_profesional
    FOREIGN KEY (id_profesional)
    REFERENCES profesional(id_profesional)
    ON DELETE CASCADE
```

);

-- ============================================
-- HISTORIA CLÍNICA
-- ============================================

CREATE TABLE historia_clinica (
id_historia SERIAL PRIMARY KEY,
id_paciente INTEGER NOT NULL UNIQUE,
fecha_apertura DATE NOT NULL DEFAULT CURRENT_DATE,
observaciones TEXT,

```
CONSTRAINT fk_historia_paciente
    FOREIGN KEY (id_paciente)
    REFERENCES paciente(id_paciente)
    ON DELETE CASCADE
```

);

-- ============================================
-- TURNO
-- ============================================

CREATE TABLE turno (
id_turno SERIAL PRIMARY KEY,
id_paciente INTEGER NOT NULL,
id_profesional INTEGER NOT NULL,
fecha DATE NOT NULL,
hora_inicio TIME NOT NULL,
hora_fin TIME NOT NULL,
estado VARCHAR(20) NOT NULL DEFAULT 'PENDIENTE',
observaciones TEXT,

```
CONSTRAINT fk_turno_paciente
    FOREIGN KEY (id_paciente)
    REFERENCES paciente(id_paciente),

CONSTRAINT fk_turno_profesional
    FOREIGN KEY (id_profesional)
    REFERENCES profesional(id_profesional),

CONSTRAINT chk_turno_horario
    CHECK (hora_fin > hora_inicio),

CONSTRAINT chk_turno_estado
    CHECK (
        estado IN (
            'PENDIENTE',
            'CONFIRMADO',
            'CANCELADO',
            'REPROGRAMADO'
        )
    )
```

);

-- ============================================
-- SESIÓN
-- ============================================

CREATE TABLE sesion (
id_sesion SERIAL PRIMARY KEY,
id_turno INTEGER NOT NULL UNIQUE,
fecha DATE NOT NULL,
observaciones TEXT,

```
CONSTRAINT fk_sesion_turno
    FOREIGN KEY (id_turno)
    REFERENCES turno(id_turno)
```

);

-- ============================================
-- PAGO
-- ============================================

CREATE TABLE pago (
id_pago SERIAL PRIMARY KEY,
id_sesion INTEGER NOT NULL,
fecha DATE NOT NULL DEFAULT CURRENT_DATE,
importe NUMERIC(10,2) NOT NULL,
medio_pago VARCHAR(30),

```
CONSTRAINT fk_pago_sesion
    FOREIGN KEY (id_sesion)
    REFERENCES sesion(id_sesion),

CONSTRAINT chk_pago_importe
    CHECK (importe > 0)
```

);

-- ============================================
-- PACIENTE - OBRA SOCIAL
-- ============================================

CREATE TABLE paciente_obra_social (
id_paciente INTEGER NOT NULL,
id_obra_social INTEGER NOT NULL,
numero_afiliado VARCHAR(50),
activo BOOLEAN NOT NULL DEFAULT TRUE,

```
PRIMARY KEY (id_paciente, id_obra_social),

CONSTRAINT fk_paciente_obra_social_paciente
    FOREIGN KEY (id_paciente)
    REFERENCES paciente(id_paciente)
    ON DELETE CASCADE,

CONSTRAINT fk_paciente_obra_social_obra_social
    FOREIGN KEY (id_obra_social)
    REFERENCES obra_social(id_obra_social)
    ON DELETE CASCADE
```

);

-- ============================================
-- OBRA SOCIAL EN SESIÓN
-- ============================================

ALTER TABLE sesion
ADD COLUMN id_obra_social INTEGER;

ALTER TABLE sesion
ADD CONSTRAINT fk_sesion_obra_social
FOREIGN KEY (id_obra_social)
REFERENCES obra_social(id_obra_social);
