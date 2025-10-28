-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 27, 2025 at 07:44 AM
-- Server version: 8.0.42
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `doc_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `doc_introduction`
--

CREATE TABLE `doc_introduction` (
  `doc_id` int NOT NULL,
  `name_pro_th` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name_pro_en` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `student_name` json NOT NULL,
  `school_y_BE` int NOT NULL COMMENT 'พ.ศ',
  `school_y_AD` int NOT NULL COMMENT 'ค.ศ',
  `comm_dean` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comm_prathan` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comm_first` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `comm_sec` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `advisor_th` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `advisor_en` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `coadvisor_th` json DEFAULT NULL,
  `coadvisor_en` json DEFAULT NULL,
  `dep_th` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `dep_en` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cover_options` json DEFAULT NULL COMMENT 'ยังไม่ได้ใช้',
  `certificate_options` json DEFAULT NULL COMMENT 'ยังไม่ได้ใช้',
  `user_id` bigint NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `doc_introduction`
--
ALTER TABLE `doc_introduction`
  ADD PRIMARY KEY (`doc_id`),
  ADD UNIQUE KEY `uq_intro_user` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `doc_introduction`
--
ALTER TABLE `doc_introduction`
  MODIFY `doc_id` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `doc_introduction`
--
ALTER TABLE `doc_introduction`
  ADD CONSTRAINT `fk_intro_user` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
