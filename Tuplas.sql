-- =========================================
-- AUTH_USER
-- =========================================

INSERT INTO auth_user
(id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
VALUES
(2,'pbkdf2_sha256$600000$hash1',NULL,false,'juanperez','Juan','Pérez','juan1@gmail.com',false,true,NOW()),
(3,'pbkdf2_sha256$600000$hash2',NULL,false,'mariagarcia','Maria','García','maria2@gmail.com',false,true,NOW()),
(4,'pbkdf2_sha256$600000$hash3',NULL,false,'carlosruiz','Carlos','Ruiz','carlos3@gmail.com',false,true,NOW()),
(5,'pbkdf2_sha256$600000$hash4',NULL,false,'laurasanchez','Laura','Sánchez','laura4@gmail.com',false,true,NOW()),
(6,'pbkdf2_sha256$600000$hash5',NULL,false,'pedromartin','Pedro','Martín','pedro5@gmail.com',false,true,NOW()),
(7,'pbkdf2_sha256$600000$hash6',NULL,false,'lucialopez','Lucía','López','lucia6@gmail.com',false,true,NOW()),
(8,'pbkdf2_sha256$600000$hash7',NULL,false,'davidfernandez','David','Fernández','david7@gmail.com',false,true,NOW()),
(9,'pbkdf2_sha256$600000$hash8',NULL,false,'elenagomez','Elena','Gómez','elena8@gmail.com',false,true,NOW()),
(10,'pbkdf2_sha256$600000$hash9',NULL,false,'jorgejimenez','Jorge','Jiménez','jorge9@gmail.com',false,true,NOW()),
(11,'pbkdf2_sha256$600000$hash10',NULL,false,'saradiaz','Sara','Díaz','sara10@gmail.com',false,true,NOW()),

(12,'pbkdf2_sha256$600000$hash11',NULL,false,'alvaronieto','Álvaro','Nieto','alvaro11@gmail.com',false,true,NOW()),
(13,'pbkdf2_sha256$600000$hash12',NULL,false,'patriciaromo','Patricia','Romo','patricia12@gmail.com',false,true,NOW()),
(14,'pbkdf2_sha256$600000$hash13',NULL,false,'rubencastro','Rubén','Castro','ruben13@gmail.com',false,true,NOW()),
(15,'pbkdf2_sha256$600000$hash14',NULL,false,'martaalonso','Marta','Alonso','marta14@gmail.com',false,true,NOW()),
(16,'pbkdf2_sha256$600000$hash15',NULL,false,'sergiotorres','Sergio','Torres','sergio15@gmail.com',false,true,NOW()),
(17,'pbkdf2_sha256$600000$hash16',NULL,false,'nuriavargas','Nuria','Vargas','nuria16@gmail.com',false,true,NOW()),
(18,'pbkdf2_sha256$600000$hash17',NULL,false,'pabloramos','Pablo','Ramos','pablo17@gmail.com',false,true,NOW()),
(19,'pbkdf2_sha256$600000$hash18',NULL,false,'irenemolina','Irene','Molina','irene18@gmail.com',false,true,NOW()),
(20,'pbkdf2_sha256$600000$hash19',NULL,false,'adriangil','Adrián','Gil','adrian19@gmail.com',false,true,NOW()),
(21,'pbkdf2_sha256$600000$hash20',NULL,false,'claudianavarro','Claudia','Navarro','claudia20@gmail.com',false,true,NOW()),

(22,'pbkdf2_sha256$600000$hash21',NULL,false,'raullorenzo','Raúl','Lorenzo','raul21@gmail.com',false,true,NOW()),
(23,'pbkdf2_sha256$600000$hash22',NULL,false,'silviaprieto','Silvia','Prieto','silvia22@gmail.com',false,true,NOW()),
(24,'pbkdf2_sha256$600000$hash23',NULL,false,'miguelortega','Miguel','Ortega','miguel23@gmail.com',false,true,NOW()),
(25,'pbkdf2_sha256$600000$hash24',NULL,false,'beatrizflores','Beatriz','Flores','beatriz24@gmail.com',false,true,NOW()),
(26,'pbkdf2_sha256$600000$hash25',NULL,false,'oscarmendez','Óscar','Méndez','oscar25@gmail.com',false,true,NOW());



-- =========================================
-- USUARIO
-- =========================================

INSERT INTO usuario
(user_id, apellidos, fecha_nac, dni, saldo)
VALUES
(2,'Pérez García','1995-03-12','11111111A',1200.50),
(3,'García López','1998-07-22','22222222B',845.20),
(4,'Ruiz Martín','1992-11-05','33333333C',430.00),
(5,'Sánchez Torres','1997-01-14','44444444D',1500.75),
(6,'Martín Díaz','1999-06-18','55555555E',620.90),
(7,'López Romero','1994-02-27','66666666F',980.10),
(8,'Fernández Gil','1991-09-10','77777777G',305.40),
(9,'Gómez Navarro','1996-04-03','88888888H',765.00),
(10,'Jiménez Castro','1993-12-30','99999999I',2100.25),
(11,'Díaz Ortega','1998-08-09','10101010J',540.60),

(12,'Nieto Ramos','1995-05-21','11112222K',875.00),
(13,'Romo Flores','1990-10-13','12121212L',1320.40),
(14,'Castro Prieto','1997-07-01','13131313M',690.90),
(15,'Alonso Vargas','1992-01-17','14141414N',455.30),
(16,'Torres Molina','1999-09-29','15151515O',1780.80),
(17,'Vargas Ruiz','1994-03-08','16161616P',999.99),
(18,'Ramos Pérez','1991-06-11','17171717Q',250.00),
(19,'Molina Gómez','1996-11-23','18181818R',1345.45),
(20,'Gil Sánchez','1993-04-06','19191919S',870.00),
(21,'Navarro Jiménez','1998-12-15','20202020T',615.15),

(22,'Lorenzo Martín','1995-08-19','21212121U',420.75),
(23,'Prieto Díaz','1990-02-25','22223333V',2300.00),
(24,'Ortega López','1997-05-30','23232323W',760.40),
(25,'Flores Castro','1992-09-07','24242424X',510.25),
(26,'Méndez Romero','1999-01-28','25252525Y',1890.60);

-- =========================================
-- HIPODROMO
-- =========================================

INSERT INTO hipodromo (nombre,direccion)VALUES
('Hipódromo de la Zarzuela','Madrid, España'),
('Hipódromo de San Sebastián','San Sebastián, España'),
('Hipódromo de Dos Hermanas','Sevilla, España'),
('Hipódromo de Son Pardo', 'Palma de Mallorca, España');

-- =========================================
-- PISTA
-- =========================================

INSERT INTO pista (tipo)
VALUES
('Arena'),
('Hierba'),
('Sintetica'),
('Arena Humeda'),
('Hierba Mojada'),
('Tierra'),
('Tierra Compacta'),
('Arena Seca'),
('Hierba Rapida'),
('Sintetica Premium');

-- =========================================
-- ESTADO PISTA
-- =========================================

INSERT INTO estado_pista (tipo)
VALUES
('Seca'),
('Humeda'),
('Rapida'),
('Mojada'),
('Pesada'),
('Lenta'),
('Compacta'),
('Perfecta'),
('Dura'),
('Blanca');


INSERT INTO tipos_apuesta (nombre)
VALUES
('Ganador'), 
('Colocado'), 
('Exacta'), 
('Trifecta'), 
('Quiniela');

-- =====================================
-- 15 CARRERAS DESDE EL 24 DE MAYO 2026
-- =====================================

INSERT INTO carrera
(id_carrera, enlace, nombre, fecha, hora, distancia, orden, estado,
 id_hipodromo, id_pista, id_estado_pista, tipo, categoria)
VALUES
(1,  'zarzuela-20260524-c1',  'Premio Primavera',        '2026-05-24', '11:30:00', 1200, 1, 'Pendiente', 1, 1, 1, 'Plano', 'C'),
(2,  'zarzuela-20260524-c2',  'Premio Castilla',         '2026-05-24', '12:15:00', 1400, 2, 'Pendiente', 1, 1, 1, 'Plano', 'B'),
(3,  'zarzuela-20260524-c3',  'Premio Duero',            '2026-05-24', '13:00:00', 1600, 3, 'Pendiente', 1, 1, 1, 'Plano', 'A'),

(4,  'sevilla-20260525-c1',   'Premio Andalucía',        '2026-05-25', '11:45:00', 1500, 1, 'Pendiente', 2, 1, 1, 'Plano', 'D'),
(5,  'sevilla-20260525-c2',   'Premio Guadalquivir',     '2026-05-25', '12:30:00', 1800, 2, 'Pendiente', 2, 1, 1, 'Plano', 'B'),
(6,  'sevilla-20260525-c3',   'Gran Premio Sevilla',     '2026-05-25', '13:15:00', 2000, 3, 'Pendiente', 2, 1, 1, 'Plano', 'D'),

(7,  'madrid-20260526-c1',    'Premio Madrid',           '2026-05-26', '16:00:00', 1400, 1, 'Pendiente', 1, 1, 1, 'Plano', 'C'),
(8,  'madrid-20260526-c2',    'Premio Chamartín',        '2026-05-26', '16:45:00', 1700, 2, 'Pendiente', 1, 1, 1, 'Plano', 'B'),
(9,  'madrid-20260526-c3',    'Premio Castellana',       '2026-05-26', '17:30:00', 2100, 3, 'Pendiente', 1, 1, 1, 'Plano', 'D'),

(10, 'valencia-20260527-c1',  'Premio Mediterráneo',     '2026-05-27', '11:20:00', 1300, 1, 'Pendiente', 3, 1, 1, 'Plano', 'D'),
(11, 'valencia-20260527-c2',  'Premio Turia',            '2026-05-27', '12:05:00', 1600, 2, 'Pendiente', 3, 1, 1, 'Plano', 'C'),
(12, 'valencia-20260527-c3',  'Gran Premio Valencia',    '2026-05-27', '12:50:00', 2200, 3, 'Pendiente', 3, 1, 1, 'Plano', 'C'),

(13, 'bilbao-20260528-c1',    'Premio Euskadi',          '2026-05-28', '15:30:00', 1500, 1, 'Pendiente', 4, 1, 1, 'Plano', 'B'),
(14, 'bilbao-20260528-c2',    'Premio Cantábrico',       '2026-05-28', '16:15:00', 1900, 2, 'Pendiente', 4, 1, 1, 'Plano', 'C'),
(15, 'bilbao-20260528-c3',    'Gran Premio Norte',       '2026-05-28', '17:00:00', 2400, 3, 'Pendiente', 4, 1, 1, 'Plano', 'D');

INSERT INTO participante
(id_participante, id_caballo, id_carrera, id_jinete, numero_salida, retirado)
VALUES
(1, 226, 1, 49, 1, FALSE),
(2, 225, 1, 48, 2, FALSE),
(3, 224, 1, 47, 3, FALSE),
(4, 223, 1, 46, 4, FALSE),
(5, 222, 1, 45, 5, FALSE),
(6, 221, 1, 44, 6, FALSE),

(7, 220, 2, 43, 1, FALSE),
(8, 219, 2, 42, 2, FALSE),
(9, 218, 2, 41, 3, FALSE),
(10, 217, 2, 40, 4, FALSE),
(11, 216, 2, 39, 5, FALSE),
(12, 215, 2, 38, 6, FALSE),
(13, 214, 2, 37, 7, FALSE),

(14, 213, 3, 36, 1, FALSE),
(15, 212, 3, 35, 2, FALSE),
(16, 211, 3, 34, 3, FALSE),
(17, 210, 3, 33, 4, FALSE),
(18, 209, 3, 32, 5, FALSE),
(19, 208, 3, 31, 6, FALSE),
(20, 207, 3, 30, 7, FALSE),
(21, 206, 3, 29, 8, FALSE),

(22, 205, 4, 28, 1, FALSE),
(23, 204, 4, 27, 2, FALSE),
(24, 203, 4, 26, 3, FALSE),
(25, 202, 4, 25, 4, FALSE),
(26, 201, 4, 24, 5, FALSE),
(27, 200, 4, 23, 6, FALSE),
(28, 199, 4, 22, 7, FALSE),
(29, 198, 4, 21, 8, FALSE),
(30, 197, 4, 20, 9, FALSE),

(31, 196, 5, 19, 1, FALSE),
(32, 195, 5, 18, 2, FALSE),
(33, 194, 5, 17, 3, FALSE),
(34, 193, 5, 16, 4, FALSE),
(35, 192, 5, 15, 5, FALSE),
(36, 191, 5, 14, 6, FALSE),
(37, 190, 5, 13, 7, FALSE),
(38, 189, 5, 12, 8, FALSE),
(39, 188, 5, 11, 9, FALSE),
(40, 187, 5, 10, 10, FALSE),

(41, 186, 6, 9, 1, FALSE),
(42, 185, 6, 8, 2, FALSE),
(43, 184, 6, 7, 3, FALSE),
(44, 183, 6, 6, 4, FALSE),
(45, 182, 6, 5, 5, FALSE),
(46, 181, 6, 4, 6, FALSE),
(47, 180, 6, 3, 7, FALSE),
(48, 179, 6, 2, 8, FALSE),
(49, 178, 6, 1, 9, FALSE),
(50, 177, 6, 49, 10, FALSE),
(51, 176, 6, 48, 11, FALSE),

(52, 175, 7, 47, 1, FALSE),
(53, 174, 7, 46, 2, FALSE),
(54, 173, 7, 45, 3, FALSE),
(55, 172, 7, 44, 4, FALSE),
(56, 171, 7, 43, 5, FALSE),
(57, 170, 7, 42, 6, FALSE),
(58, 169, 7, 41, 7, FALSE),
(59, 168, 7, 40, 8, FALSE),
(60, 167, 7, 39, 9, FALSE),
(61, 166, 7, 38, 10, FALSE),
(62, 165, 7, 37, 11, FALSE),
(63, 164, 7, 36, 12, FALSE),

(64, 163, 8, 35, 1, FALSE),
(65, 162, 8, 34, 2, FALSE),
(66, 161, 8, 33, 3, FALSE),
(67, 160, 8, 32, 4, FALSE),
(68, 159, 8, 31, 5, FALSE),

(69, 158, 9, 30, 1, FALSE),
(70, 157, 9, 29, 2, FALSE),
(71, 156, 9, 28, 3, FALSE),
(72, 155, 9, 27, 4, FALSE),
(73, 154, 9, 26, 5, FALSE),
(74, 153, 9, 25, 6, FALSE),

(75, 152, 10, 24, 1, FALSE),
(76, 151, 10, 23, 2, FALSE),
(77, 150, 10, 22, 3, FALSE),
(78, 149, 10, 21, 4, FALSE),
(79, 148, 10, 20, 5, FALSE),
(80, 147, 10, 19, 6, FALSE),
(81, 146, 10, 18, 7, FALSE),

(82, 145, 11, 17, 1, FALSE),
(83, 144, 11, 16, 2, FALSE),
(84, 143, 11, 15, 3, FALSE),
(85, 142, 11, 14, 4, FALSE),
(86, 141, 11, 13, 5, FALSE),
(87, 140, 11, 12, 6, FALSE),
(88, 139, 11, 11, 7, FALSE),
(89, 138, 11, 10, 8, FALSE),

(90, 137, 12, 9, 1, FALSE),
(91, 136, 12, 8, 2, FALSE),
(92, 135, 12, 7, 3, FALSE),
(93, 134, 12, 6, 4, FALSE),
(94, 133, 12, 5, 5, FALSE),
(95, 132, 12, 4, 6, FALSE),
(96, 131, 12, 3, 7, FALSE),
(97, 130, 12, 2, 8, FALSE),
(98, 129, 12, 1, 9, FALSE),

(99, 128, 13, 49, 1, FALSE),
(100, 127, 13, 48, 2, FALSE),
(101, 126, 13, 47, 3, FALSE),
(102, 125, 13, 46, 4, FALSE),
(103, 124, 13, 45, 5, FALSE),
(104, 123, 13, 44, 6, FALSE),
(105, 122, 13, 43, 7, FALSE),
(106, 121, 13, 42, 8, FALSE),
(107, 120, 13, 41, 9, FALSE),
(108, 119, 13, 40, 10, FALSE),

(109, 118, 14, 39, 1, FALSE),
(110, 117, 14, 38, 2, FALSE),
(111, 116, 14, 37, 3, FALSE),
(112, 115, 14, 36, 4, FALSE),
(113, 114, 14, 35, 5, FALSE),
(114, 113, 14, 34, 6, FALSE),
(115, 112, 14, 33, 7, FALSE),
(116, 111, 14, 32, 8, FALSE),
(117, 110, 14, 31, 9, FALSE),
(118, 109, 14, 30, 10, FALSE),
(119, 108, 14, 29, 11, FALSE),

(120, 107, 15, 28, 1, FALSE),
(121, 106, 15, 27, 2, FALSE),
(122, 105, 15, 26, 3, FALSE),
(123, 104, 15, 25, 4, FALSE),
(124, 103, 15, 24, 5, FALSE),
(125, 102, 15, 23, 6, FALSE),
(126, 101, 15, 22, 7, FALSE),
(127, 100, 15, 21, 8, FALSE),
(128, 99, 15, 20, 9, FALSE),
(129, 98, 15, 19, 10, FALSE),
(130, 97, 15, 18, 11, FALSE),
(131, 96, 15, 17, 12, FALSE);

SELECT setval(
    'carrera_id_carrera_seq',
    (SELECT MAX(id_carrera) FROM carrera)
);

SELECT setval(
    'participante_id_participante_seq',
    COALESCE((SELECT MAX(id_participante) FROM participante), 1)
);
