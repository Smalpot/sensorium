-- ========================================================================
-- Script de inicialización de la base de datos SENSORIUM
-- SQL Server
-- ========================================================================

-- Crear la base de datos si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'SENSORIUM')
BEGIN
    CREATE DATABASE SENSORIUM;
    PRINT '✓ Base de datos SENSORIUM creada';
END
GO

USE SENSORIUM;
GO

-- ========================================================================
-- TABLA: USUARIO
-- Almacena los usuarios del sistema (administradores y psicólogos)
-- ========================================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[USUARIO]') AND type in (N'U'))
BEGIN
    CREATE TABLE USUARIO (
        IDusuario INT IDENTITY(1,1) PRIMARY KEY,
        nombre VARCHAR(40) NOT NULL,
        correo VARCHAR(40) NOT NULL UNIQUE,
        contraseña VARCHAR(100) NOT NULL,
        rol VARCHAR(20) NOT NULL CHECK (rol IN ('administrador', 'psicologo')),
        fecha_regist DATE NOT NULL DEFAULT GETDATE()
    );
    PRINT '✓ Tabla USUARIO creada';
END
GO

-- ========================================================================
-- TABLA: PSICOLOGOS
-- Almacena información adicional de los psicólogos
-- ========================================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[PSICOLOGOS]') AND type in (N'U'))
BEGIN
    CREATE TABLE PSICOLOGOS (
        IDpsicologo INT IDENTITY(1,1) PRIMARY KEY,
        IDusuario INT NOT NULL,
        especialidad VARCHAR(40) NOT NULL,
        experiencia VARCHAR(150),
        cedula VARCHAR(20) NOT NULL UNIQUE,
        FOREIGN KEY (IDusuario) REFERENCES USUARIO(IDusuario) ON DELETE CASCADE
    );
    PRINT '✓ Tabla PSICOLOGOS creada';
END
GO

-- ========================================================================
-- TABLA: PACIENTES
-- Almacena información de los pacientes
-- ========================================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[PACIENTES]') AND type in (N'U'))
BEGIN
    CREATE TABLE PACIENTES (
        IDpaciente INT IDENTITY(1,1) PRIMARY KEY,
        nombre VARCHAR(40) NOT NULL,
        correo VARCHAR(40),
        telefono VARCHAR(15) NOT NULL,
        direccion VARCHAR(80),
        fecha_regist DATE NOT NULL DEFAULT GETDATE()
    );
    PRINT '✓ Tabla PACIENTES creada';
END
GO

-- ========================================================================
-- TABLA: CITAS
-- Almacena las citas programadas entre pacientes y psicólogos
-- ========================================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CITAS]') AND type in (N'U'))
BEGIN
    CREATE TABLE CITAS (
        IDcita INT IDENTITY(1,1) PRIMARY KEY,
        IDpaciente INT NOT NULL,
        IDpsicologo INT NOT NULL,
        fecha DATE NOT NULL,
        hora TIME NOT NULL,
        modalidad VARCHAR(20) NOT NULL CHECK (modalidad IN ('Presencial', 'Virtual')),
        estado VARCHAR(20) NOT NULL DEFAULT 'Programada' CHECK (estado IN ('Programada', 'Completada', 'Cancelada')),
        FOREIGN KEY (IDpaciente) REFERENCES PACIENTES(IDpaciente) ON DELETE CASCADE,
        FOREIGN KEY (IDpsicologo) REFERENCES PSICOLOGOS(IDpsicologo) ON DELETE NO ACTION
    );
    PRINT '✓ Tabla CITAS creada';
END
GO

-- ========================================================================
-- TABLA: CONSULTAS
-- Almacena el registro de las consultas realizadas
-- ========================================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CONSULTAS]') AND type in (N'U'))
BEGIN
    CREATE TABLE CONSULTAS (
        IDconsulta INT IDENTITY(1,1) PRIMARY KEY,
        IDcita INT NOT NULL UNIQUE,
        notas VARCHAR(200),
        duracion INT,  -- Duración en minutos
        diagnostico VARCHAR(150),
        recomend VARCHAR(150),
        FOREIGN KEY (IDcita) REFERENCES CITAS(IDcita) ON DELETE CASCADE
    );
    PRINT '✓ Tabla CONSULTAS creada';
END
GO

-- ========================================================================
-- TABLA: PAGOS
-- Almacena los pagos realizados por las consultas
-- ========================================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[PAGOS]') AND type in (N'U'))
BEGIN
    CREATE TABLE PAGOS (
        IDpago INT IDENTITY(1,1) PRIMARY KEY,
        IDconsulta INT NOT NULL,
        monto DECIMAL(10,2) NOT NULL CHECK (monto > 0),
        metodo VARCHAR(20) NOT NULL CHECK (metodo IN ('Efectivo', 'Tarjeta', 'Transferencia')),
        fecha_pago DATE NOT NULL DEFAULT GETDATE(),
        estatus_pago VARCHAR(20) NOT NULL DEFAULT 'Pendiente' CHECK (estatus_pago IN ('Pendiente', 'Pagado', 'Cancelado')),
        FOREIGN KEY (IDconsulta) REFERENCES CONSULTAS(IDconsulta) ON DELETE CASCADE
    );
    PRINT '✓ Tabla PAGOS creada';
END
GO

-- ========================================================================
-- TABLA: HISTORIAL
-- Almacena el historial clínico de los pacientes
-- ========================================================================
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[HISTORIAL]') AND type in (N'U'))
BEGIN
    CREATE TABLE HISTORIAL (
        IDhistorial INT IDENTITY(1,1) PRIMARY KEY,
        IDpaciente INT NOT NULL UNIQUE,
        antecedentes VARCHAR(150),
        alergias VARCHAR(100),
        tratamientos VARCHAR(200),
        fecha_creacion DATE NOT NULL DEFAULT GETDATE(),
        FOREIGN KEY (IDpaciente) REFERENCES PACIENTES(IDpaciente) ON DELETE CASCADE
    );
    PRINT '✓ Tabla HISTORIAL creada';
END
GO

-- ========================================================================
-- ÍNDICES para mejorar el rendimiento
-- ========================================================================

-- Índice para búsqueda de usuarios por correo
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_USUARIO_Correo')
BEGIN
    CREATE INDEX IX_USUARIO_Correo ON USUARIO(correo);
    PRINT '✓ Índice IX_USUARIO_Correo creado';
END
GO

-- Índice para búsqueda de psicólogos por especialidad
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_PSICOLOGOS_Especialidad')
BEGIN
    CREATE INDEX IX_PSICOLOGOS_Especialidad ON PSICOLOGOS(especialidad);
    PRINT '✓ Índice IX_PSICOLOGOS_Especialidad creado';
END
GO

-- Índice para búsqueda de citas por fecha
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_CITAS_Fecha')
BEGIN
    CREATE INDEX IX_CITAS_Fecha ON CITAS(fecha, hora);
    PRINT '✓ Índice IX_CITAS_Fecha creado';
END
GO

-- Índice para búsqueda de citas por estado
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'IX_CITAS_Estado')
BEGIN
    CREATE INDEX IX_CITAS_Estado ON CITAS(estado);
    PRINT '✓ Índice IX_CITAS_Estado creado';
END
GO

-- ========================================================================
-- DATOS INICIALES - Usuario administrador por defecto
-- Contraseña: admin123 (encriptada en SHA256)
-- ========================================================================
IF NOT EXISTS (SELECT * FROM USUARIO WHERE correo = 'admin@sensorium.com')
BEGIN
    INSERT INTO USUARIO (nombre, correo, contraseña, rol)
    VALUES (
        'Administrador', 
        'admin@sensorium.com', 
        '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',  -- admin123 en SHA256
        'administrador'
    );
    PRINT '✓ Usuario administrador creado';
    PRINT '   Usuario: admin@sensorium.com';
    PRINT '   Contraseña: admin123';
END
GO

-- ========================================================================
-- VISTAS útiles para consultas comunes
-- ========================================================================

-- Vista de citas con información completa
IF EXISTS (SELECT * FROM sys.views WHERE name = 'V_CITAS_COMPLETAS')
    DROP VIEW V_CITAS_COMPLETAS;
GO

CREATE VIEW V_CITAS_COMPLETAS AS
SELECT 
    c.IDcita,
    c.fecha,
    c.hora,
    c.modalidad,
    c.estado,
    p.IDpaciente,
    p.nombre AS nombre_paciente,
    p.telefono AS telefono_paciente,
    ps.IDpsicologo,
    u.nombre AS nombre_psicologo,
    ps.especialidad
FROM CITAS c
INNER JOIN PACIENTES p ON c.IDpaciente = p.IDpaciente
INNER JOIN PSICOLOGOS ps ON c.IDpsicologo = ps.IDpsicologo
INNER JOIN USUARIO u ON ps.IDusuario = u.IDusuario;
GO

PRINT '✓ Vista V_CITAS_COMPLETAS creada';
GO

-- Vista de consultas con información de pago
IF EXISTS (SELECT * FROM sys.views WHERE name = 'V_CONSULTAS_PAGOS')
    DROP VIEW V_CONSULTAS_PAGOS;
GO

CREATE VIEW V_CONSULTAS_PAGOS AS
SELECT 
    co.IDconsulta,
    co.notas,
    co.diagnostico,
    co.duracion,
    c.fecha AS fecha_consulta,
    p.nombre AS nombre_paciente,
    u.nombre AS nombre_psicologo,
    pg.IDpago,
    pg.monto,
    pg.metodo,
    pg.estatus_pago,
    pg.fecha_pago
FROM CONSULTAS co
INNER JOIN CITAS c ON co.IDcita = c.IDcita
INNER JOIN PACIENTES p ON c.IDpaciente = p.IDpaciente
INNER JOIN PSICOLOGOS ps ON c.IDpsicologo = ps.IDpsicologo
INNER JOIN USUARIO u ON ps.IDusuario = u.IDusuario
LEFT JOIN PAGOS pg ON co.IDconsulta = pg.IDconsulta;
GO

PRINT '✓ Vista V_CONSULTAS_PAGOS creada';
GO

-- ========================================================================
PRINT '';
PRINT '========================================';
PRINT 'Base de datos SENSORIUM inicializada correctamente';
PRINT 'Todas las tablas, índices y vistas han sido creadas';
PRINT '========================================';