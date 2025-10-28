-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 27, 2025 at 10:26 AM
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
-- Table structure for table `abstract`
--

CREATE TABLE `abstract` (
  `abstract_id` int NOT NULL,
  `author1_th` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `author1_en` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `author2_th` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `author2_en` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `project_name_th` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `project_name_en` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `major_th` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `major_en` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `advisor_th` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `advisor_en` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `coadvisor_th` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `coadvisor_en` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `academic_year_th` int DEFAULT NULL,
  `academic_year_en` int DEFAULT NULL,
  `abstract_th_para1` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `abstract_th_para2` text COLLATE utf8mb4_general_ci,
  `abstract_en_para1` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `abstract_en_para2` text COLLATE utf8mb4_general_ci,
  `keyword_th` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `keyword_en` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `acknow_para1` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'ย่อหน้าแรกของกิตติกรรมประกาศ',
  `acknow_para2` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'ย่อหน้า2กิตติกรรมประกาศ',
  `acknow_name1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'ชื่อผู้จัดทำกิตติกรรมคนที่1',
  `acknow_name2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'ชื่อผู้จัดทำกิตติกรรมคนที่2',
  `user_id` bigint DEFAULT NULL,
  `total_pages` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `abstract`
--

INSERT INTO `abstract` (`abstract_id`, `author1_th`, `author1_en`, `author2_th`, `author2_en`, `project_name_th`, `project_name_en`, `major_th`, `major_en`, `advisor_th`, `advisor_en`, `coadvisor_th`, `coadvisor_en`, `academic_year_th`, `academic_year_en`, `abstract_th_para1`, `abstract_th_para2`, `abstract_en_para1`, `abstract_en_para2`, `keyword_th`, `keyword_en`, `acknow_para1`, `acknow_para2`, `acknow_name1`, `acknow_name2`, `user_id`, `total_pages`) VALUES
(1, 'นายเศรษฐพงศ์ จังเลิศคณาพงศ์', 'Mr. Settapong Junglerdkanapong', 'นายสุรเกียรติ สุนทราวิรัตน์', 'Mr. Surakiat Suntrawirat', 'การพัฒนาเว็บแอปพลิเคชันคัดกรองและประเมินความเสี่ยง โรคสมองเสื่อมด้วยแบบประเมิน MoCA Check', 'Developing an web application to screen and assess dementia risk with the MoCA Check assessment.', 'เทคโนโลยีสารสนเทศ', 'Information Technology', 'รองศาสตราจารย์ ดร.ยุพิน สรรพคุณ', 'Associate Professor Dr.Yupins Suppakhun', '', '', 2567, 2024, 'งานวิจัยนี้นำเสนอการพัฒนาเว็บแอปพลิเคชันเพื่อคัดกรองและประเมินความเสี่ยงของโรคสมองเสื่อมโดยใช้แบบประเมิน MoCA Check ซึ่งมีวัตถุประสงค์หลักเพื่อให้ผู้สูงอายุสามารถประเมินสมรรถภาพทางสติปัญญาของตนเอง ผ่านการทดสอบความจำ ภาษา และการประมวลผลข้อมูลต่างๆผ่านแพลตฟอร์มดิจิทัล โดยแอปพลิเคชันนี้ใช้เครื่องมือ MoCA ซึ่งได้รับการยอมรับในวงการการแพทย์ในการคัดกรองผู้ที่มีความเสี่ยงต่อโรคสมองเสื่อมในระยะเริ่มต้น', 'นอกจากนี้ยังมีฟังก์ชันการฝึกสมอง เช่น การฝึกความจำ เพื่อเสริมสร้างและรักษาสมรรถภาพ ทางสติปัญญา แอปพลิเคชันนี้จึงมีเป้าหมายในการป้องกันโรคสมองเสื่อม โดยการเพิ่มความตระหนักรู้ ในการดูแลสุขภาพสมองและการส่งเสริมพฤติกรรมสุขภาพที่ดีในผู้สูงอายุ', 'This research presents the development of a web application for screeningand assessing dementia risk using the MoCA Check assessment. The primary objectiveof the application is to enable elderly users to assess their cognitive functions,including memory, language, and information processing abilities, through a digitalplatform. The app utilizes the MoCA tool, which is widely accepted in the medicalfield for screening individuals at risk of dementia in its early stages.', 'In addition, the application includes cognitive exercises, such as memory training, to enhance and maintain cognitive abilities. This application aims to serve as a preventive tool for dementia and to raise awareness about brain health management, encouraging elderly users to adopt healthy habits and take proactive steps in maintaining their brain health.', 'โรคสมองเสื่อม เว็บแอปพลิเคชัน แบบประเมิน', 'Dementia, Web Application, Assessment', 'การทำปริญญานิพนธ์นี้สำเร็จลุล่วงไปได้ด้วยดีเนื่องจากได้รับความอนุเคราะห์และความช่วยเหลือจากบุคคลหลายท่าน ทางคณะผู้จัดทำขอขอบพระคุณ รองศาสตราจารย์ ดร.ยุพิน สรรพคุณอาจารย์ที่ปรึกษาที่ได้ให้คำปรึกษาต่าง ๆ ในการทำโครงงานพิเศษ ตลอดจนคณะอาจารย์ประจำภาควิชา เทคโนโลยีสารสนเทศทุกท่านที่ได้อบรมสั่งสอนและมอบความรู้ความสามารถในการจัดทำโครงงานพิเศษ ที่ได้ช่วยชี้แนะและแนวทาง ตลอดจนให้คำปรึกษาเกี่ยวกับเรื่องของการจัดทำโครงงานพิเศษนี้', 'สุดท้ายนี้ขอกราบขอบพระคุณผู้จัดทำขอขอบพระคุณผู้มีส่วนเกี่ยวข้องทุกท่านที่ได้ให้การปรึกษา ทำให้โครงงานพิเศษนี้สำเร็จลุล่วงไปด้วยดี และขอขอบพระคุณบิดา มารดา และครอบครัวที่ให้ความอนุเคราะห์ด้านต่าง ๆ ไม่ว่าจะเป็นค่าเบี้ยเลี้ยง และค่าใช้จ่าย รวมทั้งเป็นขวัญและกำลังใจในการทำให้โครงงานพิเศษนี้สำเร็จลุล่วงไปได้ด้วยดี', 'เศรษฐพงศ์ จังเลิศคณาพงศ์', 'สุรเกียรติ สุนทราวิรัตน์', 1, 172);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `abstract`
--
ALTER TABLE `abstract`
  ADD PRIMARY KEY (`abstract_id`),
  ADD KEY `fk_user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `abstract`
--
ALTER TABLE `abstract`
  MODIFY `abstract_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `abstract`
--
ALTER TABLE `abstract`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
