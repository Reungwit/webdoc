-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 05, 2025 at 09:58 AM
-- Server version: 8.0.42
-- PHP Version: 8.1.25

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
-- Table structure for table `certificate`
--

CREATE TABLE `certificate` (
  `id` int NOT NULL,
  `user_id` bigint NOT NULL,
  `topic` varchar(255) NOT NULL COMMENT 'หัวข้อเรื่องของปริญญานิพนธ์',
  `dean` varchar(255) NOT NULL COMMENT 'ชื่อคณบดี',
  `author1` varchar(255) NOT NULL COMMENT 'ผู้จัดทำคนที่ 1',
  `author2` varchar(255) DEFAULT NULL COMMENT 'ผู้จัดทำคนที่ 2 ',
  `chairman` varchar(255) NOT NULL COMMENT 'ชื่อประธานกรรมการ',
  `committee1` varchar(255) NOT NULL COMMENT 'ชื่อกรรมการคนที่ 1',
  `committee2` varchar(255) NOT NULL COMMENT 'ชื่อกรรมการคนที่ 2',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'วันที่-เวลาที่สร้างเรคคอร์ดนี้ขึ้นมา',
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'วันที่-เวลาที่แก้ไขเรคคอร์ดล่าสุด'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `certificate`
--

INSERT INTO `certificate` (`id`, `user_id`, `topic`, `dean`, `author1`, `author2`, `chairman`, `committee1`, `committee2`, `created_at`, `updated_at`) VALUES
(1, 1, 'การพัฒนาเว็บแอปพลิเคชันคัดกรองและประเมินความเสี่ยงโรคสมองเสื่อมด้วยแบบประเมิน MoCA Check', 'ผู้ช่วยศาสตราจารย์ ดร.กฤษฎากร บุตดาจันทร์', 'นายเศรษฐพงศ์ จังเลิศคณาพงศ์', 'นายสุรเกียรติ สุนทราวิรัตน์', 'ผู้ช่วยศาสตราจารย์นิมิต ศรีคำทา', 'ผู้ช่วยศาสตราจารย์นพดล บูรณ์กุศล', 'รองศาสตราจารย์ ดร.ยุพิน สรรพคุณ', NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `certificate`
--
ALTER TABLE `certificate`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_certificate_user` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `certificate`
--
ALTER TABLE `certificate`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `certificate`
--
ALTER TABLE `certificate`
  ADD CONSTRAINT `fk_cert_user` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
