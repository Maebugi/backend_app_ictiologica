-- =========================================================
-- BASE DE DATOS APP ICTIOLÓGICA
-- PostgreSQL DDL
-- =========================================================

CREATE TABLE roles (
    rol_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_rol VARCHAR(100),
    descripcion TEXT
);

CREATE TABLE usuarios (
    usuario_id UUID PRIMARY KEY,
    rol_id INTEGER NOT NULL,
    nombre VARCHAR(150),
    correo VARCHAR(150) UNIQUE,
    contrasena VARCHAR(255),
    institucion VARCHAR(150),
    fecha_registro TIMESTAMPTZ,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_usuarios_roles
        FOREIGN KEY (rol_id)
        REFERENCES roles (rol_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE especies (
    especie_id UUID PRIMARY KEY,
    nombre_cientifico VARCHAR(150),
    nombre_comun VARCHAR(100),
    orden VARCHAR(80),
    familia VARCHAR(80),
    longitud_estandar DOUBLE PRECISION,
    talla_maxima DOUBLE PRECISION,
    peso_maximo DOUBLE PRECISION,
    longevidad INTEGER,
    habito_alimenticio VARCHAR(100),
    reproductivo VARCHAR(100),
    periodo_reproductivo VARCHAR(100),
    estado_conservacion VARCHAR(50),
    descripcion TEXT
);
CREATE TABLE salidas (
    salida_id UUID PRIMARY KEY,
    id_usuario UUID NOT NULL,
    fecha_inicio TIMESTAMPTZ,
    fecha_fin TIMESTAMPTZ,
    observaciones TEXT,
    nombre_lugar VARCHAR(150),
    nombre_proyecto VARCHAR(150),
    estado VARCHAR(20) NOT NULL DEFAULT 'abierta',
    CONSTRAINT fk_salidas_usuarios
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios (usuario_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT chk_salidas_fechas
        CHECK (fecha_inicio IS NULL OR fecha_fin IS NULL OR fecha_fin >= fecha_inicio),
    CONSTRAINT chk_salidas_estado
        CHECK (estado IN ('abierta','cerrada'))
);

CREATE TABLE estaciones (
    estacion_id UUID PRIMARY KEY,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    nombre VARCHAR(150) NOT NULL,
    cuerpo_agua VARCHAR(150) NOT NULL,
    latitud DOUBLE PRECISION NOT NULL,
    longitud DOUBLE PRECISION NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE
);



CREATE TABLE ocurrencias (
    id_ocurrencia UUID PRIMARY KEY,
    id_especie UUID NOT NULL,
    salida_id UUID NOT NULL,
    fecha_hora TIMESTAMPTZ,
    coordenadas VARCHAR(50),
    altitud DOUBLE PRECISION,
    esfuerzo DOUBLE PRECISION,
    cpue DOUBLE PRECISION,
    longitud_pez DOUBLE PRECISION,
    peso DOUBLE PRECISION,
    sexo VARCHAR(20),
    estado_ontogenetico VARCHAR(30),
    estadio_vida VARCHAR(30),
    condicion_reproductiva VARCHAR(30),
    comportamiento VARCHAR(50),
    anomalias TEXT,
    mortalidad VARCHAR(30),
    vouchers VARCHAR(100),
    nivel_certeza INTEGER,
    ancho_cauce DOUBLE PRECISION,
    profundidad_media DOUBLE PRECISION,
    profundidad_maxima DOUBLE PRECISION,
    caudal_velocidad DOUBLE PRECISION,
    tipo_habitat VARCHAR(50),
    microhabitat VARCHAR(50),
    cobertura_dosel DOUBLE PRECISION,
    uso_suelo_ribereno VARCHAR(50),
    estabilidad_orillas VARCHAR(50),
    sustrato VARCHAR(50),
    clima VARCHAR(50),
    metodo_captura VARCHAR(50),
    arte_pesca VARCHAR(50),
    codigo_muestreo VARCHAR(50),
    datum VARCHAR(20),
    observaciones TEXT,
    dinamica_agua VARCHAR(30),
    latitud DOUBLE PRECISION,
    longitud DOUBLE PRECISION,
    estacion_id UUID,
    CONSTRAINT fk_ocurrencias_especies FOREIGN KEY (id_especie)
        REFERENCES especies(especie_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_ocurrencias_salidas FOREIGN KEY (salida_id)
        REFERENCES salidas(salida_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_ocurrencia_estacion FOREIGN KEY (estacion_id)
        REFERENCES estaciones(estacion_id)
);

CREATE TABLE mediciones (
    medicion_id UUID PRIMARY KEY,
    ocurrencia_id UUID NOT NULL UNIQUE,
    ph NUMERIC(4,2),
    observaciones TEXT,
    CONSTRAINT fk_mediciones_ocurrencias
        FOREIGN KEY (ocurrencia_id)
        REFERENCES ocurrencias(id_ocurrencia)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE evidencia_ocurrencia (
    id_foto UUID PRIMARY KEY,
    id_ocurrencia UUID NOT NULL,
    ruta VARCHAR(255),
    observaciones TEXT,
    CONSTRAINT fk_evidencia_ocurrencia
        FOREIGN KEY (id_ocurrencia)
        REFERENCES ocurrencias(id_ocurrencia)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE fotos (
    id_foto UUID PRIMARY KEY,
    id_especie UUID NOT NULL,
    ruta VARCHAR(255),
    descripcion TEXT,
    CONSTRAINT fk_especie
        FOREIGN KEY (id_especie)
        REFERENCES especies(especie_id)
        ON DELETE CASCADE
);

CREATE TABLE salida_evidencia (
    id_foto UUID PRIMARY KEY,
    salida_id UUID NOT NULL,
    ruta VARCHAR(255),
    tipo_archivo VARCHAR(20),
    observaciones TEXT,
    CONSTRAINT fk_salida_evidencia
        FOREIGN KEY (salida_id)
        REFERENCES salidas(salida_id)
        ON DELETE CASCADE
);
