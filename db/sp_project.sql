-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 06, 2025 at 06:07 AM
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
-- Table structure for table `sp_project`
--

CREATE TABLE `sp_project` (
  `id` int NOT NULL,
  `name_pro_th` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `name_pro_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `case_stu` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `term` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `school_y` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `adviser` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `co_advisor` varchar(255) DEFAULT NULL,
  `strategic` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `plan` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `key_result` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `bg_and_sig_para1` longtext NOT NULL,
  `bg_and_sig_para2` longtext NOT NULL,
  `bg_and_sig_para3` longtext NOT NULL,
  `purpose_1` varchar(255) NOT NULL,
  `purpose_2` varchar(255) NOT NULL,
  `purpose_3` varchar(255) NOT NULL,
  `scope_json` json NOT NULL,
  `user_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `sp_project`
--

INSERT INTO `sp_project` (`id`, `name_pro_th`, `name_pro_en`, `case_stu`, `term`, `school_y`, `adviser`, `co_advisor`, `strategic`, `plan`, `key_result`, `bg_and_sig_para1`, `bg_and_sig_para2`, `bg_and_sig_para3`, `purpose_1`, `purpose_2`, `purpose_3`, `scope_json`, `user_id`) VALUES
(11, 'ัระบบสนับสนุนการจัดทำเล่มโครงงานพิเศษ', 'Special Project Formatting Assistant', 'ไม่มี', '2', '2567', 'ผศ.จสต.นพเก้า ทองใบ', 'ไม่มี', '', '', '', '', '', '', '', '', '', 'null', 1),
(17, 'ระบบสนับสนุนการจัดทำเล่มโครงงานพิเศษ', 'Special Project Formatting Assistant', 'ไม่มี', '2', '2567', 'ผศ.จสต.นพเก้า ทองใบ', 'ไม่มี', '', '', '', '', '', '', 'เพื่อพัฒนาระบบสนับสนุนการจัดทำเล่ม ทก. และ โครงงานพิเศษ', 'เพื่อส่งเสริมการใช้เทคโนโลยีในการพัฒนาคุณภาพและมาตรฐานงานวิชาการของนักศึกษา', 'เพื่อให้ผู้ใช้สามารถใช้งานผ่านเว็บเบราว์เซอร์ได้โดยไม่ต้องติดตั้งซอฟต์แวร์เพิ่มเติม', '\"[{\\\"main\\\": \\\"สามารถจัดรูปแบบเล่มปริญญานิพนธ์ผ่านเว็บบราวเซอร์\\\", \\\"subs\\\": [\\\"การจัดทำระบบบนเว็บแอปพลิเคชัน\\\"]}]\"', 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sp_project`
--
ALTER TABLE `sp_project`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `sp_project`
--
ALTER TABLE `sp_project`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `sp_project`
--
ALTER TABLE `sp_project`
  ADD CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
