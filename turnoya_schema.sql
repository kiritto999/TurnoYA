
create database if not exists turnoya_db;
use turnoya_db;

create table usuario (
    id_usuario int auto_increment primary key,
    nombre varchar(150) not null,
    email varchar(150) not null unique,
    password_hash varchar(255) not null,
    rol varchar(20) not null,
    estado varchar(20) not null default 'activo',
    fecha_registro datetime not null default current_timestamp
);


create table negocio (
    id_negocio int auto_increment primary key,
    id_dueno int not null,
    nombre varchar(150) not null,
    logo_url varchar(255),
    categoria varchar(100),
    horario varchar(150),
    estado varchar(20) not null default 'activo',
    foreign key (id_dueno) references usuario(id_usuario)
);


create table sector (
    id_sector int auto_increment primary key,
    id_negocio int not null,
    nombre varchar(100) not null,
    descripcion varchar(255),
    foreign key (id_negocio) references negocio(id_negocio)
);

create table empleado_negocio (
    id_empleado_negocio int auto_increment primary key,
    id_usuario int not null,
    id_negocio int not null,
    id_sector int,
    permisos varchar(255),
    estado_invitacion varchar(20) not null default 'pendiente',
    fecha_invitacion datetime not null default current_timestamp,
    foreign key (id_usuario) references usuario(id_usuario),
    foreign key (id_negocio) references negocio(id_negocio),
    foreign key (id_sector) references sector(id_sector)
);

create table catalogo_item (
    id_item int auto_increment primary key,
    id_negocio int not null,
    id_sector int,
    nombre varchar(150) not null,
    descripcion varchar(255),
    precio decimal(10,2),
    tiempo_estimado int,
    estado varchar(20) not null default 'activo',
    foreign key (id_negocio) references negocio(id_negocio),
    foreign key (id_sector) references sector(id_sector)
);

create table codigo_qr (
    id_qr int auto_increment primary key,
    id_negocio int not null,
    id_sector int,
    codigo_unico varchar(64) not null unique,
    url_destino varchar(255) not null,
    fecha_generacion datetime not null default current_timestamp,
    foreign key (id_negocio) references negocio(id_negocio),
    foreign key (id_sector) references sector(id_sector)
);

create table turno (
    id_turno int auto_increment primary key,
    id_cliente int not null,
    id_negocio int not null,
    id_sector int,
    id_item int,
    numero_turno int not null,
    motivo varchar(255),
    estado varchar(20) not null default 'pendiente',
    fecha_solicitud datetime not null default current_timestamp,
    fecha_atencion datetime,
    foreign key (id_cliente) references usuario(id_usuario),
    foreign key (id_negocio) references negocio(id_negocio),
    foreign key (id_sector) references sector(id_sector),
    foreign key (id_item) references catalogo_item(id_item)
);

create table notificacion (
    id_notificacion int auto_increment primary key,
    id_usuario int not null,
    id_turno int,
    id_negocio int,
    tipo varchar(30) not null,
    mensaje varchar(255) not null,
    leido boolean not null default false,
    fecha_envio datetime not null default current_timestamp,
    foreign key (id_usuario) references usuario(id_usuario),
    foreign key (id_turno) references turno(id_turno),
    foreign key (id_negocio) references negocio(id_negocio)
);
