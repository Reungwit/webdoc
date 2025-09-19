-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 10, 2025 at 08:15 AM
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
-- Table structure for table `ref_website`
--

CREATE TABLE `ref_website` (
  `id` bigint NOT NULL COMMENT 'PK: รหัสรายการอ้างอิงเว็บไซต์',
  `user_id` bigint NOT NULL COMMENT 'FK: อ้างอิงผู้ใช้ (backend_customuser.user_id)',
  `batch_id` varchar(36) NOT NULL COMMENT 'รหัสชุดบันทึก (กลุ่มรายการที่บันทึกพร้อมกัน)',
  `number` int DEFAULT NULL COMMENT 'ลำดับการอ้างอิง [1], [2], [3] ... (ไว้จัดเรียงตอนออกรายการ)',
  `authors_th_json` json NOT NULL COMMENT 'ผู้แต่งภาษาไทย (JSON array เช่น ["สมชาย","สมหญิง"])',
  `authors_en_json` json NOT NULL COMMENT 'ผู้แต่งภาษาอังกฤษ (JSON array เช่น ["Somchai","Somsri"])',
  `title_th` varchar(500) NOT NULL COMMENT 'ชื่อเรื่องภาษาไทย',
  `title_en` varchar(500) NOT NULL COMMENT 'ชื่อเรื่องภาษาอังกฤษ',
  `site_name_th` varchar(255) DEFAULT NULL COMMENT 'ชื่อเว็บไซต์หลักภาษาไทย เช่น "กรมอนามัย"',
  `site_name_en` varchar(255) DEFAULT NULL COMMENT 'ชื่อเว็บไซต์หลักภาษาอังกฤษ เช่น "WHO"',
  `year` smallint DEFAULT NULL COMMENT 'ปีที่เผยแพร่',
  `month` tinyint DEFAULT NULL COMMENT 'เดือนที่เผยแพร่ (1-12)',
  `day` tinyint DEFAULT NULL COMMENT 'วันที่เผยแพร่',
  `url` varchar(1000) NOT NULL COMMENT 'URL ของหน้าเว็บ',
  `accessed_date` date DEFAULT NULL COMMENT 'วันที่เข้าถึงข้อมูล (YYYY-MM-DD)',
  `notes` text COMMENT 'บันทึกเพิ่มเติม (ถ้ามี)',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'เวลาที่สร้างข้อมูล',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'เวลาที่อัปเดตล่าสุด'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='ตารางเก็บบรรณานุกรมประเภทเว็บไซต์ (ไทย-อังกฤษ)';

--
-- Dumping data for table `ref_website`
--

INSERT INTO `ref_website` (`id`, `user_id`, `batch_id`, `number`, `authors_th_json`, `authors_en_json`, `title_th`, `title_en`, `site_name_th`, `site_name_en`, `year`, `month`, `day`, `url`, `accessed_date`, `notes`, `created_at`, `updated_at`) VALUES
(1, 1, '', NULL, '[\"มงลง\"]', '[]', 'การศึกษา', '', NULL, NULL, NULL, NULL, NULL, 'https://www.youtube.com/', '2025-09-07', NULL, '2025-09-07 07:56:04', '2025-09-07 07:56:04');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ref_website`
--
ALTER TABLE `ref_website`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_web_user` (`user_id`),
  ADD KEY `idx_ref_website_user_batch` (`user_id`,`batch_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ref_website`
--
ALTER TABLE `ref_website`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'PK: รหัสรายการอ้างอิงเว็บไซต์', AUTO_INCREMENT=12;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ref_website`
--
ALTER TABLE `ref_website`
  ADD CONSTRAINT `fk_web_user` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
