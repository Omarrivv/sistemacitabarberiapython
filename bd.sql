-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 28-06-2024 a las 01:15:33
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `barberiamacha`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `id_cita` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time NOT NULL,
  `nota` text DEFAULT NULL,
  `estado` enum('pendiente','cancelado','terminado') NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_barbero` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `citas`
--

INSERT INTO `citas` (`id_cita`, `fecha`, `hora`, `nota`, `estado`, `id_cliente`, `id_barbero`) VALUES
(1, '2024-04-25', '15:00:00', 'Corte clásico', 'terminado', 3, 2),
(2, '2024-05-04', '15:55:00', 'un taper fade', 'terminado', 19, 15),
(3, '2024-05-05', '20:30:00', 'un mullet ', 'terminado', 4, 17),
(4, '2024-05-03', '21:30:00', 'clasico ', 'terminado', 20, 18),
(5, '2024-05-07', '11:30:00', 'un taper fade con mullet', 'terminado', 4, 15),
(6, '2024-05-05', '21:16:00', 'jdhd yutr', 'terminado', 4, 16),
(7, '2024-05-12', '22:18:00', 'clasico mullet', 'pendiente', 4, 15),
(8, '2024-05-04', '20:50:00', 'un clasico', 'terminado', 21, 2),
(9, '2024-05-12', '01:15:00', 'taper', 'pendiente', 6, 17),
(10, '2024-04-01', '13:29:00', 'corte cero', 'terminado', 22, 17),
(11, '2024-05-12', '14:40:00', 'clasico fade hongo', 'terminado', 5, 16),
(12, '2024-05-05', '03:30:00', 'taper mullet', 'terminado', 3, 18),
(13, '2024-05-19', '03:10:00', 'hydydyd', 'pendiente', 3, 15),
(14, '2024-05-05', '20:30:00', 'un clasico fade mullet', 'pendiente', 23, 15),
(15, '2024-05-08', '15:40:00', 'un fade clasico', 'terminado', 24, 18),
(16, '2024-05-11', '15:30:00', 'byuuu', 'terminado', 25, 27),
(17, '2024-05-11', '20:15:00', 'un clasico', 'terminado', 29, 17),
(18, '2024-06-27', '21:13:00', 'un corte', 'pendiente', 31, 15);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `id_pago` int(11) NOT NULL,
  `id_cita` int(11) NOT NULL,
  `corteRealizado` varchar(100) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fechaPago` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`id_pago`, `id_cita`, `corteRealizado`, `monto`, `fechaPago`) VALUES
(1, 1, 'Corte clásico', 25.50, '2024-04-25'),
(2, 2, 'Corte moderno', 30.00, '2024-05-04'),
(3, 1, 'Corte clásico', 25.50, '2024-04-25'),
(5, 3, 'un taper fade', 37.00, '2024-05-04'),
(6, 3, 'un taper fade con mullet adicionales', 56.00, '2024-05-04'),
(7, 1, 'fade mullet y colorimetria', 60.00, '2024-05-05'),
(8, 1, 'corte atrsasdo 2', 40.00, '2024-05-05'),
(9, 1, 'corte atrsasdo 3', 89.00, '2024-05-05'),
(10, 8, 'faqde ddd', 98.00, '2024-05-05'),
(11, 8, 'faqde ddd', 98.00, '2024-05-05'),
(12, 14, 'un clasico fade mullet', 35.00, '2024-05-05'),
(13, 15, 'un fade clasico', 27.00, '2024-05-08'),
(14, 16, 'un fade mas barba', 30.00, '2024-05-11'),
(15, 15, 'un clasico + extra', 25.00, '2024-05-11');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `imagen`, `nombre`, `descripcion`, `precio`) VALUES
(1, 'https://plazavea.vteximg.com.br/arquivos/ids/25856086-450-450/20181614.jpg', 'Shampoo', 'Shampoo anti caspa', 10.99);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_usuario` int(11) NOT NULL,
  `tipoDeDocumento` enum('DNI','CNE') NOT NULL,
  `numeroDeDocumento` varchar(15) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `celular` varchar(20) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `rol` enum('cliente','admin','barbero') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_usuario`, `tipoDeDocumento`, `numeroDeDocumento`, `nombre`, `apellido`, `celular`, `email`, `password`, `rol`) VALUES
(1, 'DNI', '72681115', 'Omar', 'Rivera Rosas', '930720474', 'or813023@gmail.com', 'omar', 'admin'),
(2, 'CNE', '87654321', 'Carlos', 'Gomez', '966555444', 'carlos.gomez@example.com', 'password123', 'barbero'),
(3, 'DNI', '99900078', 'Luis', 'Jose', '999789000', 'lucas.jose@gmail.com', 'password789', 'cliente'),
(4, 'DNI', '72681115', 'omar felix', 'rivera rosas', '930720474', 'omar.rivera@vallegrande.edu.pe', 'omar', 'cliente'),
(5, 'CNE', '7268111578', 'felipe', 'rojas', '930720473', 'om.re@gmail.com', 'ibarra', 'cliente'),
(6, 'CNE', '7268111578', 'jose', 'rojas', '930720473', 'locos@ede.pe', 'locos', 'cliente'),
(15, 'DNI', '72681115', 'josue', 'Rivera Rosas', '930720474', 'omarweb@gmail.com', 'omarwebtech3450pl', 'barbero'),
(16, 'CNE', '87654321', 'Andrea', 'Gomez', '966555444', 'andrea.gomez@example.com', 'password123', 'barbero'),
(17, 'DNI', '90087652', 'Luci', 'revilla', '999789000', 'luci.jose@gmail.com', 'password789', 'barbero'),
(18, 'DNI', '09876756', 'carla', 'Canto', '999789000', 'carla.jose@gmail.com', 'password789', 'barbero'),
(19, 'DNI', '72726754', 'felipe', 'rojas', '900897234', 'rojas@gmail.com', 'rojas12345', 'cliente'),
(20, 'DNI', '78546734', 'luisbss', 'dggdg', '900876543', 'osi@gamil.com', '900800', 'cliente'),
(21, 'DNI', '87654323', 'webtech', 'olpoil', '900678543', 'webte@gmail.com', 'web123', 'cliente'),
(22, 'CNE', '75093498', 'Ronaldinho Yefferson', 'Ccencho Ramos', '123456789', 'ronaldinho.ccencho@vallegrande.edu.pe', '123456', 'cliente'),
(23, 'DNI', '74565443', 'ronaldiño', 'ccencho', '900765453', 'ccencho@gmail.com', '123123', 'cliente'),
(24, 'DNI', '74565449', 'jose', 'toih', '930720479', 'brendagbarney@gmail.com', '123123', 'cliente'),
(25, 'DNI', '77777777', 'CodeFxRoma', 'Rivera', '930720474', 'omar@edu.pe', '123true', 'cliente'),
(26, 'DNI', '12345678', 'Juan', 'Perez', '999888777', 'jhrt.perez@example.com', 'password123', 'barbero'),
(27, 'DNI', '87654321', 'Carlos', 'Gomez', '666555444', 'bar.gomez@example.com', 'password123', 'barbero'),
(29, 'DNI', '74565449', 'rosaas', 'dsds', '900765453', 'omar1@edu.pe', '123', 'cliente'),
(31, 'CNE', '890765431110', 'omar felix riverass', 'dsds', '930720544', 'or8130sss23@gmail.com', '123', 'cliente');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`id_cita`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_barbero` (`id_barbero`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `id_cita` (`id_cita`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `id_cita` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `usuario` (`id_usuario`),
  ADD CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`id_barbero`) REFERENCES `usuario` (`id_usuario`);

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_cita`) REFERENCES `citas` (`id_cita`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
