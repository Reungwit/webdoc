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
-- Table structure for table `ref_book`
--

CREATE TABLE `ref_book` (
  `id` bigint NOT NULL COMMENT 'PK: รหัสรายการอ้างอิงหนังสือ',
  `user_id` bigint NOT NULL COMMENT 'FK: อ้างอิงผู้ใช้ (backend_customuser.user_id)',
  `batch_id` varchar(36) NOT NULL COMMENT 'รหัสชุดบันทึก (กลุ่มรายการที่บันทึกพร้อมกัน)',
  `number` int DEFAULT NULL COMMENT 'ลำดับการอ้างอิง [1], [2], [3] ... (ไว้จัดเรียงตอนออกรายการ)',
  `authors_th_json` json NOT NULL COMMENT 'ผู้แต่งภาษาไทย (JSON array เช่น ["สมชาย","สมหญิง"])',
  `authors_en_json` json NOT NULL COMMENT 'ผู้แต่งภาษาอังกฤษ (JSON array เช่น ["Somchai","Somsri"])',
  `title_th` varchar(500) NOT NULL COMMENT 'ชื่อหนังสือภาษาไทย',
  `title_en` varchar(500) NOT NULL COMMENT 'ชื่อหนังสือภาษาอังกฤษ',
  `edition_th` varchar(50) DEFAULT NULL COMMENT 'ครั้งที่พิมพ์ (ไทย) เช่น "พิมพ์ครั้งที่ 2"',
  `edition_en` varchar(50) DEFAULT NULL COMMENT 'Edition (EN) เช่น "2nd ed."',
  `publisher_place_th` varchar(255) DEFAULT NULL COMMENT 'สถานที่พิมพ์ภาษาไทย',
  `publisher_place_en` varchar(255) DEFAULT NULL COMMENT 'สถานที่พิมพ์ภาษาอังกฤษ',
  `publisher_th` varchar(255) DEFAULT NULL COMMENT 'สำนักพิมพ์ภาษาไทย',
  `publisher_en` varchar(255) DEFAULT NULL COMMENT 'Publisher ภาษาอังกฤษ',
  `year` smallint DEFAULT NULL COMMENT 'ปีที่พิมพ์',
  `doi` varchar(255) DEFAULT NULL COMMENT 'DOI (ถ้ามี)',
  `url` varchar(1000) DEFAULT NULL COMMENT 'URL (ถ้าเป็น e-book/online)',
  `notes` text COMMENT 'บันทึกเพิ่มเติม (ถ้ามี)',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'เวลาที่สร้างข้อมูล',
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'เวลาที่อัปเดตล่าสุด'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='ตารางเก็บบรรณานุกรมประเภทหนังสือ (ไทย-อังกฤษ)';

--
-- Dumping data for table `ref_book`
--

INSERT INTO `ref_book` (`id`, `user_id`, `batch_id`, `number`, `authors_th_json`, `authors_en_json`, `title_th`, `title_en`, `edition_th`, `edition_en`, `publisher_place_th`, `publisher_place_en`, `publisher_th`, `publisher_en`, `year`, `doi`, `url`, `notes`, `created_at`, `updated_at`) VALUES
(1, 1, '', 2, '[]', '[\"Mr.Monaree\"]', '', 'abcde', '', '112', '', 'newword', '', 'Qa', 2003, NULL, NULL, NULL, '2025-09-07 08:21:20', '2025-09-07 08:21:20');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ref_book`
--
ALTER TABLE `ref_book`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_book_user` (`user_id`),
  ADD KEY `idx_book_year` (`year`),
  ADD KEY `idx_ref_book_user_batch` (`user_id`,`batch_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ref_book`
--
ALTER TABLE `ref_book`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT COMMENT 'PK: รหัสรายการอ้างอิงหนังสือ', AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ref_book`
--
ALTER TABLE `ref_book`
  ADD CONSTRAINT `fk_book_user` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
