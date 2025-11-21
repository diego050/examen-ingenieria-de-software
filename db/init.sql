-- db/init.sql

-- Creamos la tabla para los personajes
CREATE TABLE IF NOT EXISTS personajes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    aldea VARCHAR(100),
    jutsu_principal VARCHAR(100)
);

-- Creamos la tabla para los comentarios
CREATE TABLE IF NOT EXISTS comentarios (
    id SERIAL PRIMARY KEY,
    personaje_id INTEGER NOT NULL,
    autor VARCHAR(100) NOT NULL,
    texto TEXT NOT NULL,
    -- Creamos una relación con la tabla personajes
    CONSTRAINT fk_personaje
        FOREIGN KEY(personaje_id) 
        REFERENCES personajes(id)
        ON DELETE CASCADE -- Si un personaje se borra, sus comentarios también.
);

-- Insertamos algunos datos de prueba para que la aplicación no empiece vacía
INSERT INTO personajes (nombre, aldea, jutsu_principal) VALUES
('Naruto Uzumaki', 'Konoha', 'Rasengan'),
('Sasuke Uchiha', 'Konoha', 'Chidori'),
('Gaara', 'Sunagakure', 'Ataúd de Atadura de Arena');