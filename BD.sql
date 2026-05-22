-- =========================================
-- USUARIOS
-- =========================================
CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    fecha_nac DATE NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL
);

-- =========================================
-- ENTRENADORES
-- =========================================
CREATE TABLE entrenador (
    id_entrenador SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    nacionalidad VARCHAR(100)
);

-- =========================================
-- PROPIETARIOS
-- =========================================
CREATE TABLE propietario (
    id_propietario SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    nacionalidad VARCHAR(100),
    equipamiento VARCHAR(150)
);

-- =========================================
-- JINETES
-- =========================================
CREATE TABLE jinete (
    id_jinete SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    peso DECIMAL(5,2),
    nacionalidad VARCHAR(100)
);

-- =========================================
-- CABALLOS
-- =========================================
CREATE TABLE caballo (
    id_caballo SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    nacionalidad VARCHAR(100),
    sexo VARCHAR(20),
    edad INT,

    id_entrenador INT NOT NULL,
    id_propietario INT NOT NULL,

    FOREIGN KEY (id_entrenador)
        REFERENCES entrenador(id_entrenador)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_propietario)
        REFERENCES propietario(id_propietario)
        ON DELETE RESTRICT
);

-- =========================================
-- HIPODROMO
-- =========================================
CREATE TABLE hipodromo (
    id_hipodromo SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    direccion VARCHAR(200)
);

-- =========================================
-- PISTA
-- =========================================
CREATE TABLE pista (
    id_pista SERIAL PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL UNIQUE
);

-- =========================================
-- ESTADO PISTA
-- =========================================
CREATE TABLE estado_pista (
    id_estado_pista SERIAL PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL UNIQUE
);

-- =========================================
-- CARRERA
-- =========================================
CREATE TABLE carrera (
    id_carrera SERIAL PRIMARY KEY,

    enlace VARCHAR(200) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL UNIQUE,

    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    distancia INT NOT NULL, 
    orden INT NOT NULL,

    estado VARCHAR(50),

    id_hipodromo INT NOT NULL,
    id_pista INT,
    id_estado_pista INT,

    tipo VARCHAR(50),
    categoria VARCHAR(50),

    CONSTRAINT unique_carrera
        UNIQUE(enlace, nombre),

    FOREIGN KEY (id_hipodromo)
        REFERENCES hipodromo(id_hipodromo)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_pista)
        REFERENCES pista(id_pista)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_estado_pista)
        REFERENCES estado_pista(id_estado_pista)
        ON DELETE RESTRICT
);

-- =========================================
-- PARTICIPANTE
-- =========================================
CREATE TABLE participante (
    id_participante SERIAL PRIMARY KEY,

    id_caballo INT NOT NULL,
    id_carrera INT NOT NULL,
    id_jinete INT NOT NULL,

    numero_salida INT NOT NULL,
    retirado BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (id_caballo)
        REFERENCES caballo(id_caballo)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_carrera)
        REFERENCES carrera(id_carrera)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_jinete)
        REFERENCES jinete(id_jinete)
        ON DELETE RESTRICT,

    CONSTRAINT unique_jinete_carrera
        UNIQUE (id_jinete, id_carrera),

    CONSTRAINT unique_caballo_carrera
        UNIQUE (id_caballo, id_carrera),

    CONSTRAINT unique_salida_carrera
        UNIQUE (numero_salida, id_carrera)
);

-- =========================================
-- RESULTADO
-- =========================================
CREATE TABLE resultado (
    id_resultado SERIAL PRIMARY KEY,

    id_participante INT UNIQUE NOT NULL,

    posicion INT NOT NULL,
    duracion TIME NOT NULL,
    distancia VARCHAR(20),

    FOREIGN KEY (id_participante)
        REFERENCES participante(id_participante)
        ON DELETE RESTRICT
);

-- =========================================
-- TIPOS APUESTAS
-- =========================================
CREATE TABLE tipos_apuesta (
    id_tipo_apuesta SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
);

-- =========================================
-- APUESTAS
-- =========================================
CREATE TABLE apuesta (
    id_apuesta SERIAL PRIMARY KEY,
    cantidad DECIMAL(10,2) NOT NULL,
    dividendo DECIMAL(10,2),
    estado VARCHAR(20) DEFAULT 'pendiente',

    id_tipo_apuesta INT NOT NULL,
    id_usuario INT NOT NULL,
    id_participante INT NOT NULL,

    FOREIGN KEY (id_tipo_apuesta)
        REFERENCES tipos_apuesta(id_tipo_apuesta)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_usuario)
        REFERENCES usuario(id_usuario)
        ON DELETE RESTRICT,

    FOREIGN KEY (id_participante)
        REFERENCES participante(id_participante)
        ON DELETE RESTRICT,

    CONSTRAINT unique_apuesta_usuario_participante
    UNIQUE (id_participante, id_usuario)
);