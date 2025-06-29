CREATE DATABASE `db_reserva_cabeleireiro`;
/*DROP DATABASE IF EXISTS `db_reserva_cabeleireiro`;*/

USE `db_reserva_cabeleireiro`;

CREATE TABLE `tb_usuarios` (
	`usu_id` INT AUTO_INCREMENT PRIMARY KEY,
    `usu_name` VARCHAR(200),
    `uso_contato` VARCHAR(200),
    `usu_tipo` ENUM('cliente', 'profissional'),
    `usu_email` VARCHAR(200) UNIQUE,
    `usu_senha` VARCHAR(200)
);

CREATE TABLE `tb_clientes` (
	`cli_id` INT AUTO_INCREMENT PRIMARY KEY,
    `cli_nome` VARCHAR(200),
    `cli_contato` VARCHAR(200),
    `cli_email` VARCHAR(200) UNIQUE,
    `cli_usu_id` INT,
    FOREIGN KEY (`cli_usu_id`) REFERENCES `tb_usuarios`(`usu_id`)
);

CREATE TABLE `tb_profissionais` (
	`pro_id` INT AUTO_INCREMENT PRIMARY KEY,
    `pro_nome` VARCHAR(200),
    `pro_email` VARCHAR(200),
    `pro_contato` VARCHAR(200),
    `pro_horario` DATETIME,
    `pro_usu_id` INT,
    FOREIGN KEY (`pro_usu_id`) REFERENCES `tb_usuarios`(`usu_id`)
);

CREATE TABLE `tb_servicos` (
	`ser_id` INT AUTO_INCREMENT PRIMARY KEY,
    `ser_categoria` ENUM(
    'Corte Masculino', 'Corte Feminino', 'Corte Infantil',
    'Hidratação', 'Escova', 'Progressiva', 
    'Coloração', 'Luzes', 'Mechas', 
    'Penteado', 'Maquiagem', 'Design de Sobrancelhas', 
    'Manicure', 'Pedicure', 'Depilação') NOT NULL,
    `ser_descricao` VARCHAR(600),
    `ser_duracao` TIME,
    `ser_preco` FLOAT,
    `ser_pro_id` INT,
    FOREIGN KEY (`ser_pro_id`) REFERENCES `tb_profissionais`(`pro_id`)
);

CREATE TABLE `tb_agendamentos` (
	`age_id` INT AUTO_INCREMENT PRIMARY KEY,
    `age_cli_id` INT,
    FOREIGN KEY (`age_cli_id`) REFERENCES `tb_clientes`(`cli_id`),
    `age_pro_id` INT,
    FOREIGN KEY (`age_pro_id`) REFERENCES `tb_profissionais`(`pro_id`),
    `age_ser_id` INT,
    FOREIGN KEY (`age_ser_id`) REFERENCES `tb_servicos`(`ser_id`),
    `age_data_hora` DATETIME,
    `age_status` ENUM('pendente', 'confirmado', 'cancelado'),
    `age_criacao` DATETIME
);