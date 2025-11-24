-- db/init.sql

-- Tabla de estudiantes
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    attendance BOOLEAN DEFAULT TRUE
);

-- Tabla de evaluaciones
CREATE TABLE IF NOT EXISTS evaluations (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    score NUMERIC NOT NULL,
    weight NUMERIC NOT NULL,
    CONSTRAINT fk_student
        FOREIGN KEY(student_id)
        REFERENCES students(id)
        ON DELETE CASCADE
);

-- Datos iniciales de ejemplo
INSERT INTO students (code, nombre, attendance) VALUES
('S001', 'Juan Perez', true),
('S002', 'María García', true),
('S003', 'Luis Rodríguez', false);

INSERT INTO evaluations (student_id, score, weight) VALUES
(1, 14, 50),
(1, 16, 50),
(2, 18, 100);