-- Table: public.especies

-- DROP TABLE IF EXISTS public.especies;

CREATE TABLE IF NOT EXISTS public.especies
(
    especie_id uuid NOT NULL,
    nombre_cientifico character varying(150) COLLATE pg_catalog."default",
    nombre_comun character varying(100) COLLATE pg_catalog."default",
    orden character varying(80) COLLATE pg_catalog."default",
    familia character varying(80) COLLATE pg_catalog."default",
    longitud_estandar double precision,
    talla_maxima double precision,
    peso_maximo double precision,
    longevidad integer,
    habito_alimenticio character varying(100) COLLATE pg_catalog."default",
    reproductivo character varying(100) COLLATE pg_catalog."default",
    periodo_reproductivo character varying(100) COLLATE pg_catalog."default",
    estado_conservacion character varying(50) COLLATE pg_catalog."default",
    descripcion text COLLATE pg_catalog."default",
    CONSTRAINT especies_pkey PRIMARY KEY (especie_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.especies
    OWNER to postgres;

-- Table: public.estaciones

-- DROP TABLE IF EXISTS public.estaciones;

CREATE TABLE IF NOT EXISTS public.estaciones
(
    estacion_id uuid NOT NULL,
    codigo character varying(50) COLLATE pg_catalog."default" NOT NULL,
    nombre character varying(150) COLLATE pg_catalog."default" NOT NULL,
    cuerpo_agua character varying(150) COLLATE pg_catalog."default" NOT NULL,
    latitud double precision NOT NULL,
    longitud double precision NOT NULL,
    activo boolean NOT NULL DEFAULT true,
    CONSTRAINT estaciones_pkey PRIMARY KEY (estacion_id),
    CONSTRAINT estaciones_codigo_key UNIQUE (codigo)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.estaciones
    OWNER to postgres;

-- Table: public.evidencia_ocurrencia

-- DROP TABLE IF EXISTS public.evidencia_ocurrencia;

CREATE TABLE IF NOT EXISTS public.evidencia_ocurrencia
(
    id_foto uuid NOT NULL,
    id_ocurrencia uuid NOT NULL,
    ruta character varying(255) COLLATE pg_catalog."default",
    observaciones text COLLATE pg_catalog."default",
    CONSTRAINT evidencia_ocurrencia_pkey PRIMARY KEY (id_foto),
    CONSTRAINT fk_evidencia_ocurrencia FOREIGN KEY (id_ocurrencia)
        REFERENCES public.ocurrencias (id_ocurrencia) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.evidencia_ocurrencia
    OWNER to postgres;
-- Index: idx_evidencia_id_ocurrencia

-- DROP INDEX IF EXISTS public.idx_evidencia_id_ocurrencia;

CREATE INDEX IF NOT EXISTS idx_evidencia_id_ocurrencia
    ON public.evidencia_ocurrencia USING btree
    (id_ocurrencia ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.fotos

-- DROP TABLE IF EXISTS public.fotos;

CREATE TABLE IF NOT EXISTS public.fotos
(
    id_foto uuid NOT NULL,
    id_especie uuid NOT NULL,
    ruta character varying(255) COLLATE pg_catalog."default",
    descripcion text COLLATE pg_catalog."default",
    CONSTRAINT fotos_pkey PRIMARY KEY (id_foto),
    CONSTRAINT fk_especie FOREIGN KEY (id_especie)
        REFERENCES public.especies (especie_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.fotos
    OWNER to postgres;
-- Index: idx_fotos_id_especie

-- DROP INDEX IF EXISTS public.idx_fotos_id_especie;

CREATE INDEX IF NOT EXISTS idx_fotos_id_especie
    ON public.fotos USING btree
    (id_especie ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.mediciones

-- DROP TABLE IF EXISTS public.mediciones;

CREATE TABLE IF NOT EXISTS public.mediciones
(
    medicion_id uuid NOT NULL,
    ocurrencia_id uuid NOT NULL,
    oxigeno_disuelto_mg_l numeric(8,2),
    ph numeric(4,2),
    turbidez_ntu numeric(8,2),
    conductividad_us_cm numeric(10,2),
    tds_mg_l numeric(10,2),
    temperatura_c numeric(5,2),
    transparencia_secchi_cm numeric(8,2),
    nivel_estado_agua character varying(50) COLLATE pg_catalog."default",
    orp_mv numeric(8,2),
    alcalinidad_mg_l numeric(10,2),
    dureza_mg_l numeric(10,2),
    salinidad numeric(8,2),
    amonio_mg_l numeric(10,2),
    fosforo_metales_mg_l numeric(10,2),
    nitratos_mg_l numeric(10,2),
    nitritos_mg_l numeric(10,2),
    fosfatos_mg_l numeric(10,2),
    clorofila_a_ug_l numeric(10,2),
    sst_mg_l numeric(10,2),
    coliformes_fecales_ufc integer,
    observaciones text COLLATE pg_catalog."default",
    CONSTRAINT mediciones_pkey PRIMARY KEY (medicion_id),
    CONSTRAINT mediciones_ocurrencia_id_key UNIQUE (ocurrencia_id),
    CONSTRAINT fk_mediciones_ocurrencias FOREIGN KEY (ocurrencia_id)
        REFERENCES public.ocurrencias (id_ocurrencia) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT chk_mediciones_ph CHECK (ph IS NULL OR ph >= 0::numeric AND ph <= 14::numeric)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.mediciones
    OWNER to postgres;
-- Index: idx_mediciones_ocurrencia_id

-- DROP INDEX IF EXISTS public.idx_mediciones_ocurrencia_id;

CREATE INDEX IF NOT EXISTS idx_mediciones_ocurrencia_id
    ON public.mediciones USING btree
    (ocurrencia_id ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.ocurrencias

-- DROP TABLE IF EXISTS public.ocurrencias;

CREATE TABLE IF NOT EXISTS public.ocurrencias
(
    id_ocurrencia uuid NOT NULL,
    id_especie uuid NOT NULL,
    salida_id uuid NOT NULL,
    fecha_hora timestamp with time zone,
    coordenadas character varying(50) COLLATE pg_catalog."default",
    altitud double precision,
    esfuerzo double precision,
    cpue double precision,
    longitud_pez double precision,
    peso double precision,
    sexo character varying(20) COLLATE pg_catalog."default",
    estado_ontogenetico character varying(30) COLLATE pg_catalog."default",
    estadio_vida character varying(30) COLLATE pg_catalog."default",
    condicion_reproductiva character varying(30) COLLATE pg_catalog."default",
    comportamiento character varying(50) COLLATE pg_catalog."default",
    anomalias text COLLATE pg_catalog."default",
    mortalidad character varying(30) COLLATE pg_catalog."default",
    vouchers character varying(100) COLLATE pg_catalog."default",
    nivel_certeza integer,
    ancho_cauce double precision,
    profundidad_media double precision,
    profundidad_maxima double precision,
    caudal_velocidad double precision,
    tipo_habitat character varying(50) COLLATE pg_catalog."default",
    microhabitat character varying(50) COLLATE pg_catalog."default",
    cobertura_dosel double precision,
    uso_suelo_ribereno character varying(50) COLLATE pg_catalog."default",
    estabilidad_orillas character varying(50) COLLATE pg_catalog."default",
    sustrato character varying(50) COLLATE pg_catalog."default",
    clima character varying(50) COLLATE pg_catalog."default",
    metodo_captura character varying(50) COLLATE pg_catalog."default",
    arte_pesca character varying(50) COLLATE pg_catalog."default",
    codigo_muestreo character varying(50) COLLATE pg_catalog."default",
    datum character varying(20) COLLATE pg_catalog."default",
    observaciones text COLLATE pg_catalog."default",
    dinamica_agua character varying(30) COLLATE pg_catalog."default",
    latitud double precision,
    longitud double precision,
    estacion_id uuid,
    CONSTRAINT ocurrencias_pkey PRIMARY KEY (id_ocurrencia),
    CONSTRAINT fk_ocurrencia_estacion FOREIGN KEY (estacion_id)
        REFERENCES public.estaciones (estacion_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_ocurrencias_especies FOREIGN KEY (id_especie)
        REFERENCES public.especies (especie_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT fk_ocurrencias_salidas FOREIGN KEY (salida_id)
        REFERENCES public.salidas (salida_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.ocurrencias
    OWNER to postgres;
-- Index: idx_ocurrencias_fecha_hora

-- DROP INDEX IF EXISTS public.idx_ocurrencias_fecha_hora;

CREATE INDEX IF NOT EXISTS idx_ocurrencias_fecha_hora
    ON public.ocurrencias USING btree
    (fecha_hora ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_ocurrencias_id_especie

-- DROP INDEX IF EXISTS public.idx_ocurrencias_id_especie;

CREATE INDEX IF NOT EXISTS idx_ocurrencias_id_especie
    ON public.ocurrencias USING btree
    (id_especie ASC NULLS LAST)
    TABLESPACE pg_default;
-- Index: idx_ocurrencias_salida_id

-- DROP INDEX IF EXISTS public.idx_ocurrencias_salida_id;

CREATE INDEX IF NOT EXISTS idx_ocurrencias_salida_id
    ON public.ocurrencias USING btree
    (salida_id ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.roles

-- DROP TABLE IF EXISTS public.roles;

CREATE TABLE IF NOT EXISTS public.roles
(
    rol_id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    nombre_rol character varying(100) COLLATE pg_catalog."default",
    descripcion text COLLATE pg_catalog."default",
    CONSTRAINT roles_pkey PRIMARY KEY (rol_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.roles
    OWNER to postgres;

-- Table: public.salida_evidencia

-- DROP TABLE IF EXISTS public.salida_evidencia;

CREATE TABLE IF NOT EXISTS public.salida_evidencia
(
    id_foto uuid NOT NULL,
    salida_id uuid NOT NULL,
    ruta character varying(255) COLLATE pg_catalog."default",
    tipo_archivo character varying(20) COLLATE pg_catalog."default",
    observaciones text COLLATE pg_catalog."default",
    CONSTRAINT salida_evidencia_pkey PRIMARY KEY (id_foto),
    CONSTRAINT fk_salida_evidencia FOREIGN KEY (salida_id)
        REFERENCES public.salidas (salida_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.salida_evidencia
    OWNER to postgres;

-- Table: public.salidas

-- DROP TABLE IF EXISTS public.salidas;

CREATE TABLE IF NOT EXISTS public.salidas
(
    salida_id uuid NOT NULL,
    id_usuario uuid NOT NULL,
    fecha_inicio timestamp with time zone,
    fecha_fin timestamp with time zone,
    observaciones text COLLATE pg_catalog."default",
    nombre_lugar character varying(150) COLLATE pg_catalog."default",
    estado character varying(20) COLLATE pg_catalog."default" NOT NULL DEFAULT 'abierta'::character varying,
    nombre_proyecto character varying(150) COLLATE pg_catalog."default",
    CONSTRAINT salidas_pkey PRIMARY KEY (salida_id),
    CONSTRAINT fk_salidas_usuarios FOREIGN KEY (id_usuario)
        REFERENCES public.usuarios (usuario_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT chk_salidas_estado CHECK (estado::text = ANY (ARRAY['abierta'::character varying, 'cerrada'::character varying]::text[])),
    CONSTRAINT chk_salidas_fechas CHECK (fecha_inicio IS NULL OR fecha_fin IS NULL OR fecha_fin >= fecha_inicio)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.salidas
    OWNER to postgres;
-- Index: idx_salidas_id_usuario

-- DROP INDEX IF EXISTS public.idx_salidas_id_usuario;

CREATE INDEX IF NOT EXISTS idx_salidas_id_usuario
    ON public.salidas USING btree
    (id_usuario ASC NULLS LAST)
    TABLESPACE pg_default;

-- Table: public.usuarios

-- DROP TABLE IF EXISTS public.usuarios;

CREATE TABLE IF NOT EXISTS public.usuarios
(
    usuario_id uuid NOT NULL,
    rol_id integer NOT NULL,
    nombre character varying(150) COLLATE pg_catalog."default",
    correo character varying(150) COLLATE pg_catalog."default",
    contrasena character varying(255) COLLATE pg_catalog."default",
    institucion character varying(150) COLLATE pg_catalog."default",
    fecha_registro timestamp with time zone,
    activo boolean NOT NULL DEFAULT true,
    CONSTRAINT usuarios_pkey PRIMARY KEY (usuario_id),
    CONSTRAINT usuarios_correo_key UNIQUE (correo),
    CONSTRAINT fk_usuarios_roles FOREIGN KEY (rol_id)
        REFERENCES public.roles (rol_id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.usuarios
    OWNER to postgres;
-- Index: idx_usuarios_rol_id

-- DROP INDEX IF EXISTS public.idx_usuarios_rol_id;

CREATE INDEX IF NOT EXISTS idx_usuarios_rol_id
    ON public.usuarios USING btree
    (rol_id ASC NULLS LAST)
    TABLESPACE pg_default;