CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10, 2) NOT NULL,
    comerciante_id INTEGER NOT NULL
);

-- Opcional: Puedes añadir algunos datos de prueba para que la app no empiece vacía.
INSERT INTO productos (nombre, descripcion, precio, comerciante_id) VALUES
('Polo Básico', 'Polo de algodón con cuello redondo', 35.50, 1),
('Jean Clásico', 'Pantalón jean de corte recto', 90.00, 2);
