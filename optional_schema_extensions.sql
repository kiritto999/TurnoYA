-- OPCIONAL. No se ejecuta automáticamente porque el esquema original no contiene
-- dirección/coordenadas ni tokens de dispositivo.
-- Úsalo si vas a implementar RF11 con mapa y notificaciones push reales.

ALTER TABLE negocio
    ADD COLUMN direccion varchar(255) NULL,
    ADD COLUMN latitud decimal(10,7) NULL,
    ADD COLUMN longitud decimal(10,7) NULL;

-- Para push real, agrega un campo por dispositivo/usuario o crea una tabla de tokens.
-- Ejemplo:
-- CREATE TABLE dispositivo_usuario (
--   id_dispositivo int auto_increment primary key,
--   id_usuario int not null,
--   token varchar(512) not null unique,
--   plataforma varchar(20) not null,
--   foreign key (id_usuario) references usuario(id_usuario)
-- );
