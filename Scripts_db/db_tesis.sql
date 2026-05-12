-- =========================================================
-- BASE DE DATOS APP ICTIOLÓGICA
-- PostgreSQL DDL
-- =========================================================

-- =========================================================
-- TABLA: roles
-- =========================================================
CREATE TABLE roles (
    rol_id            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nombre_rol        VARCHAR(100),
    descripcion       TEXT
);

-- =========================================================
-- TABLA: usuarios
-- Validación incluida:
-- - activo con DEFAULT TRUE
-- =========================================================
CREATE TABLE usuarios (
    usuario_id        UUID PRIMARY KEY,
    rol_id            INTEGER NOT NULL,
    nombre            VARCHAR(150),
    correo            VARCHAR(150) UNIQUE,
    contrasena        VARCHAR(255),
    institucion       VARCHAR(150),
    fecha_registro    TIMESTAMPTZ,
    activo            BOOLEAN NOT NULL DEFAULT TRUE,
    

    CONSTRAINT fk_usuarios_roles
        FOREIGN KEY (rol_id)
        REFERENCES roles (rol_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- =========================================================
-- TABLA: especies
-- =========================================================
CREATE TABLE especies (
    especie_id              UUID PRIMARY KEY,
    nombre_cientifico       VARCHAR(150),
    nombre_comun            VARCHAR(100),
    orden                   VARCHAR(80),
    familia                 VARCHAR(80),
    longitud_estandar       DOUBLE PRECISION,
    talla_maxima            DOUBLE PRECISION,
    peso_maximo             DOUBLE PRECISION,
    longevidad              INTEGER,
    habito_alimenticio      VARCHAR(100),
    reproductivo            VARCHAR(100),
    periodo_reproductivo    VARCHAR(100),
    estado_conservacion     VARCHAR(50),
    descripcion             TEXT
);

-- =========================================================
-- TABLA: salidas
-- Validación incluida:
-- - fecha_fin no puede ser menor que fecha_inicio
-- =========================================================
CREATE TABLE salidas (
    salida_id       UUID PRIMARY KEY,
    id_usuario      UUID NOT NULL,
    fecha_inicio    TIMESTAMPTZ,
    fecha_fin       TIMESTAMPTZ,
    observaciones   TEXT,
    nombre_lugar    VARCHAR(150),
    estado          VARCHAR(20) NOT NULL DEFAULT 'abierta',

    CONSTRAINT fk_salidas_usuarios
        FOREIGN KEY (id_usuario)
        REFERENCES usuarios (usuario_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT chk_salidas_fechas
        CHECK (
            fecha_inicio IS NULL
            OR fecha_fin IS NULL
            OR fecha_fin >= fecha_inicio
        ),

    CONSTRAINT chk_salidas_estado
        CHECK (estado IN ('abierta', 'cerrada'))
);

-- =========================================================
-- TABLA: ocurrencias
-- =========================================================
CREATE TABLE ocurrencias (
    id_ocurrencia               UUID PRIMARY KEY,
    id_especie                  UUID NOT NULL,
    salida_id                   UUID NOT NULL,
    fecha_hora                  TIMESTAMPTZ,
    coordenadas                 VARCHAR(50),
    altitud                     DOUBLE PRECISION,
    esfuerzo                    DOUBLE PRECISION,
    cpue                        DOUBLE PRECISION,
    longitud_pez                DOUBLE PRECISION,
    peso                        DOUBLE PRECISION,
    sexo                        VARCHAR(20),
    estado_ontogenetico         VARCHAR(30),
    estadio_vida                VARCHAR(30),
    condicion_reproductiva      VARCHAR(30),
    comportamiento              VARCHAR(50),
    anomalias                   TEXT,
    mortalidad                  VARCHAR(30),
    vouchers                    VARCHAR(100),
    nivel_certeza               INTEGER,
    ancho_cauce                 DOUBLE PRECISION,
    profundidad_media           DOUBLE PRECISION,
    profundidad_maxima          DOUBLE PRECISION,
    caudal_velocidad            DOUBLE PRECISION,
    tipo_habitat                VARCHAR(50),
    microhabitat                VARCHAR(50),
    cobertura_dosel             DOUBLE PRECISION,
    uso_suelo_ribereno          VARCHAR(50),
    estabilidad_orillas         VARCHAR(50),
    sustrato                    VARCHAR(50),
    clima                       VARCHAR(50),
    metodo_captura              VARCHAR(50),
    arte_pesca                  VARCHAR(50),
    codigo_muestreo             VARCHAR(50),
    datum                       VARCHAR(20),
    observaciones               TEXT,

    CONSTRAINT fk_ocurrencias_especies
        FOREIGN KEY (id_especie)
        REFERENCES especies (especie_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,

    CONSTRAINT fk_ocurrencias_salidas
        FOREIGN KEY (salida_id)
        REFERENCES salidas (salida_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- =========================================================
-- TABLA: mediciones
-- Validación incluida:
-- - ph entre 0 y 14
-- =========================================================
CREATE TABLE mediciones (
    medicion_id                     UUID PRIMARY KEY,
    ocurrencia_id                   UUID NOT NULL UNIQUE,
    oxigeno_disuelto_mg_l           NUMERIC(8,2),
    ph                              NUMERIC(4,2),
    turbidez_ntu                    NUMERIC(8,2),
    conductividad_us_cm             NUMERIC(10,2),
    tds_mg_l                        NUMERIC(10,2),
    temperatura_c                   NUMERIC(5,2),
    transparencia_secchi_cm         NUMERIC(8,2),
    nivel_estado_agua               VARCHAR(50),
    orp_mv                          NUMERIC(8,2),
    alcalinidad_mg_l                NUMERIC(10,2),
    dureza_mg_l                     NUMERIC(10,2),
    salinidad                       NUMERIC(8,2),
    amonio_mg_l                     NUMERIC(10,2),
    fosforo_metales_mg_l            NUMERIC(10,2),
    nitratos_mg_l                   NUMERIC(10,2),
    nitritos_mg_l                   NUMERIC(10,2),
    fosfatos_mg_l                   NUMERIC(10,2),
    clorofila_a_ug_l                NUMERIC(10,2),
    sst_mg_l                        NUMERIC(10,2),
    coliformes_fecales_ufc          INTEGER,
    observaciones                   TEXT,

    CONSTRAINT fk_mediciones_ocurrencias
        FOREIGN KEY (ocurrencia_id)
        REFERENCES ocurrencias (id_ocurrencia)
        ON UPDATE CASCADE
        ON DELETE CASCADE,

    CONSTRAINT chk_mediciones_ph
        CHECK (
            ph IS NULL
            OR (ph >= 0 AND ph <= 14)
        )
);

-- =========================================================
-- TABLA: evidencia_ocurrencia
-- =========================================================
CREATE TABLE evidencia_ocurrencia (
    id_foto             UUID PRIMARY KEY,
    id_ocurrencia       UUID NOT NULL,
    ruta                VARCHAR(255),
    observaciones       TEXT,

    CONSTRAINT fk_evidencia_ocurrencia
        FOREIGN KEY (id_ocurrencia)
        REFERENCES ocurrencias (id_ocurrencia)
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

-- =========================================================
-- ÍNDICES RECOMENDADOS
-- =========================================================
CREATE INDEX idx_usuarios_rol_id
    ON usuarios (rol_id);

CREATE INDEX idx_salidas_id_usuario
    ON salidas (id_usuario);

CREATE INDEX idx_ocurrencias_id_especie
    ON ocurrencias (id_especie);

CREATE INDEX idx_ocurrencias_salida_id
    ON ocurrencias (salida_id);

CREATE INDEX idx_ocurrencias_fecha_hora
    ON ocurrencias (fecha_hora);

CREATE INDEX idx_mediciones_ocurrencia_id
    ON mediciones (ocurrencia_id);

CREATE INDEX idx_evidencia_id_ocurrencia
    ON evidencia_ocurrencia (id_ocurrencia);

CREATE INDEX idx_fotos_id_especie
ON fotos (id_especie);



