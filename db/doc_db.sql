-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 27, 2025 at 05:56 AM
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
-- Table structure for table `abstract`
--

CREATE TABLE `abstract` (
  `abstract_id` int NOT NULL,
  `author1_th` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `author1_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `author2_th` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `author2_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `project_name_th` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `project_name_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `major_th` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `major_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `advisor_th` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `advisor_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `coadvisor_th` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `coadvisor_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `academic_year_th` int DEFAULT NULL,
  `academic_year_en` int DEFAULT NULL,
  `abstract_th_para1` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `abstract_en_para1` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `keyword_th` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `keyword_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `acknow_para1` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'ย่อหน้าแรกของกิตติกรรมประกาศ',
  `acknow_para2` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT 'ย่อหน้า2กิตติกรรมประกาศ',
  `acknow_name1` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'ชื่อผู้จัดทำกิตติกรรมคนที่1',
  `acknow_name2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'ชื่อผู้จัดทำกิตติกรรมคนที่2',
  `user_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `abstract`
--

INSERT INTO `abstract` (`abstract_id`, `author1_th`, `author1_en`, `author2_th`, `author2_en`, `project_name_th`, `project_name_en`, `major_th`, `major_en`, `advisor_th`, `advisor_en`, `coadvisor_th`, `coadvisor_en`, `academic_year_th`, `academic_year_en`, `abstract_th_para1`, `abstract_en_para1`, `keyword_th`, `keyword_en`, `acknow_para1`, `acknow_para2`, `acknow_name1`, `acknow_name2`, `user_id`) VALUES
(1, 'นายเศรษฐพงศ์ จังเลิศคณาพงศ์', 'Mr. Settapong Junglerdkanapong', '', '', 'การพัฒนาเว็บแอป โรคประสาท', 'Developing an web application to screen and assess dementia risk with the MoCA Check assessment.', 'เทคโนโลยีสารสนเทศ มหาวิทยาลัยเทคโน', 'Information Technology King Mongkut’s University of Technology North Bangkok', 'รองศาสตราจารย์ ดร.ยุพิน สรรพคุณ', 'Associate Professor Dr.Yupins Suppakhun', '', '', 2567, 2024, 'งานวิจัยนี้นำเสนอการพัฒนาเว็บแอปพลิเคชันเพื่อคัดกรองและประเมินความเสี่ยงของโรคสมองเสื่อมโดยใช้แบบประเมิน MoCA Check ซึ่งมีวัตถุประสงค์หลักเพื่อให้ผู้สูงอายุสามารถประเมินสมรรถภาพทางสติปัญญาของตนเอง ผ่านการทดสอบความจำ ภาษา และการประมวลผลข้อมูลต่างๆผ่านแพลตฟอร์มดิจิทัล โดยแอปพลิเคชันนี้ใช้เครื่องมือ MoCA ซึ่งได้รับการยอมรับในวงการการแพทย์ในการคัดกรองผู้ที่มีความเสี่ยงต่อโรคสมองเสื่อมในระยะเริ่มต้น', 'This research presents the development of a web application for screeningand assessing dementia risk using the MoCA Check assessment. The primary objectiveof the application is to enable elderly users to assess their cognitive functions,including memory, language, and information processing abilities, through a digitalplatform. The app utilizes the MoCA tool, which is widely accepted in the medicalfield for screening individuals at risk of dementia in its early stages.', 'โรคสมองเสื่อม เว็บแอปพลิเคชัน แบบประเมิน', 'Dementia, Web Application, Assessment', 'การทำปริญญานิพนธ์นี้สำเร็จลุล่วงไปได้ด้วยดีเนื่องจากได้รับความอนุเคราะห์และความช่วยเหลือจากบุคคลหลายท่าน ทางคณะผู้จัดทำขอขอบพระคุณ รองศาสตราจารย์ ดร.ยุพิน สรรพคุณอาจารย์ที่ปรึกษาที่ได้ให้คำปรึกษาต่าง ๆ ในการทำโครงงานพิเศษ ตลอดจนคณะอาจารย์ประจำภาควิชา เทคโนโลยีสารสนเทศทุกท่านที่ได้อบรมสั่งสอนและมอบความรู้ความสามารถในการจัดทำโครงงานพิเศษ ที่ได้ช่วยชี้แนะและแนวทาง ตลอดจนให้คำปรึกษาเกี่ยวกับเรื่องของการจัดทำโครงงานพิเศษนี้', 'สุดท้ายนี้ขอกราบขอบพระคุณผู้จัดทำขอขอบพระคุณผู้มีส่วนเกี่ยวข้องทุกท่านที่ได้ให้การปรึกษา ทำให้โครงงานพิเศษนี้สำเร็จลุล่วงไปด้วยดี และขอขอบพระคุณบิดา มารดา และครอบครัวที่ให้ความอนุเคราะห์ด้านต่าง ๆ ไม่ว่าจะเป็นค่าเบี้ยเลี้ยง และค่าใช้จ่าย รวมทั้งเป็นขวัญและกำลังใจในการทำให้โครงงานพิเศษนี้สำเร็จลุล่วงไปได้ด้วยดี', 'เศรษฐพงศ์ จังเลิศคณาพงศ์', 'สุรเกียรติ สุนทราวิรัตน์', 1);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_customuser'),
(22, 'Can change user', 6, 'change_customuser'),
(23, 'Can delete user', 6, 'delete_customuser'),
(24, 'Can view user', 6, 'view_customuser'),
(25, 'Can add sp project', 7, 'add_spproject'),
(26, 'Can change sp project', 7, 'change_spproject'),
(27, 'Can delete sp project', 7, 'delete_spproject'),
(28, 'Can view sp project', 7, 'view_spproject'),
(29, 'Can add sp project author', 8, 'add_spprojectauthor'),
(30, 'Can change sp project author', 8, 'change_spprojectauthor'),
(31, 'Can delete sp project author', 8, 'delete_spprojectauthor'),
(32, 'Can view sp project author', 8, 'view_spprojectauthor');

-- --------------------------------------------------------

--
-- Table structure for table `backend_customuser`
--

CREATE TABLE `backend_customuser` (
  `user_id` bigint NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `is_active` tinyint NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `email` varchar(254) NOT NULL,
  `full_name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `backend_customuser`
--

INSERT INTO `backend_customuser` (`user_id`, `password`, `last_login`, `is_superuser`, `is_active`, `username`, `first_name`, `last_name`, `is_staff`, `date_joined`, `email`, `full_name`) VALUES
(1, 'pbkdf2_sha256$870000$kBh9QE2VrV9CBGBTobhxHz$Lkd2/zbMenIpTPk9QV32loYJQmUZWLn/RaDDPokd4XY=', '2025-08-06 08:04:59.773340', 1, 1, 'admin', '', '', 1, '2025-07-13 05:06:37.253416', 'admin@gmail.com', ''),
(2, 'pbkdf2_sha256$870000$O10Of0E6RmlMPPsYBCOSol$p+bus7K12Z4+qHFcduQpsvtGaFYducHVJsTNjyEWST4=', '2025-08-27 02:34:33.346403', 0, 1, 'BossReungwit', '', '', 0, '2025-07-13 05:28:03.461600', 'singlaboss@gmail.com', 'ZA'),
(4, 'pbkdf2_sha256$870000$RdkraQ3A6nbkI9mJgK5OnM$rbDGJ77Uo0TpfQC8PS+2uWfHFy1Ovdlh78Maq2Xmd74=', NULL, 0, 1, 'test', '', '', 0, '2025-07-18 03:35:54.750817', 'test@gmail.com', 'test'),
(6, 'pbkdf2_sha256$870000$DYOn2AU52ffoHSvsp5FJbz$iHtyKDdSMUgjFgEVv8iAJsro8UPJY7Bedy/fsY/ssoI=', '2025-07-25 14:41:40.237073', 0, 1, 'test1', '', '', 0, '2025-07-25 14:41:39.728345', 'test1@gmail.com', 'ZA');

-- --------------------------------------------------------

--
-- Table structure for table `backend_customuser_groups`
--

CREATE TABLE `backend_customuser_groups` (
  `id` bigint NOT NULL,
  `customuser_id` bigint NOT NULL,
  `group_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `backend_customuser_user_permissions`
--

CREATE TABLE `backend_customuser_user_permissions` (
  `id` bigint NOT NULL,
  `customuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL
) ;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(6, 'backend', 'customuser'),
(7, 'backend', 'spproject'),
(8, 'backend', 'spprojectauthor'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-07-13 05:05:56.178215'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-07-13 05:05:56.227453'),
(3, 'auth', '0001_initial', '2025-07-13 05:05:56.371239'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-07-13 05:05:56.406224'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-07-13 05:05:56.410335'),
(6, 'auth', '0004_alter_user_username_opts', '2025-07-13 05:05:56.415335'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-07-13 05:05:56.419444'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-07-13 05:05:56.420745'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-07-13 05:05:56.425757'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-07-13 05:05:56.429759'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-07-13 05:05:56.434757'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-07-13 05:05:56.444882'),
(13, 'auth', '0011_update_proxy_permissions', '2025-07-13 05:05:56.450004'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-07-13 05:05:56.454004'),
(15, 'backend', '0001_initial', '2025-07-13 05:05:56.633282'),
(16, 'admin', '0001_initial', '2025-07-13 05:05:56.713800'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-07-13 05:05:56.719933'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-07-13 05:05:56.724933'),
(19, 'sessions', '0001_initial', '2025-07-13 05:05:56.745980'),
(20, 'backend', '0002_spproject_spprojectauthor', '2025-07-27 03:54:26.871014');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('49qrs07dynexh8hpdymi3v1i579fbso8', '.eJxVizsOAyEMRO9CHa3AJoudMlLOgYwBscqnCLtVlLvnI4qkm5k372GibGuLWy_3uGRzMGB2v1sSPZfbB4w0fdkofTpdZbkcx-nPbNLbW_Oca_ahirfZpoAlw8zkiWbHwBAIS90jIKIrmqx6ZmEgq6rOWSbzfAEbHjRU:1ufeZV:SY1SdF0G4mNQXioqpef2W2y68MFtEVERYkxGOewcDVI', '2025-08-09 13:04:17.518052'),
('9i0yn5ufbr0r73dwaypc5bbfwcou5exu', 'e30:1uaovv:8lutfgnT3_ORdoaPfHiEye8y_3n798y41el-NahXeAs', '2025-07-27 05:07:27.713320'),
('jbwpe3nxqallot4k533hfkwwolhpkd71', '.eJxVizsOAyEMRO9CHa3AJoudMlLOgYwBscqnCLtVlLvnI4qkm5k372GibGuLWy_3uGRzMGB2v1sSPZfbB4w0fdkofTpdZbkcx-nPbNLbW_Oca_ahirfZpoAlw8zkiWbHwBAIS90jIKIrmqx6ZmEgq6rOWSbzfAEbHjRU:1ufeg7:QCCqJkebRKoSPi6SBeCIWMQiENlnsva-Ot9O71ab5EU', '2025-08-09 13:11:07.840171'),
('orwc9gs7h2423gbt3hrul23nz6x5fztd', 'e30:1ufJZn:V0C31YNWlrZgBlrbJ7uGjjT8zlizqV8Q4ss152Ilk9s', '2025-08-08 14:39:11.966251'),
('u9dze1aoy51z4ks0545dshbvas6f1oe0', '.eJxVjL0OwjAMhN8lM6qaxNQOIxLPETm2USp-BkInxLtXrTLAdnff3X1c5uVd89LslWd1J-fd4TcrLDd7bqCrYWfdtOHy4Pl-7qW_ZeVWtz8UNpowXQ18ID-qSpCiRILgcRoLcEygUMAXtKBGcpRkbMwxIrnvCjlQNcQ:1ujZ8t:oSW64YALFnAmW3EoOWafUF2uVjzENSkF2OkBsVZJeaE', '2025-08-20 08:04:59.776339'),
('vq3w1ecq34694ot5ig7qnqur7pzdszr1', 'e30:1ucbn2:7faVuZa-IAuaqSyPQuoUxbb0NvyDi0m5gxPNGZcGybU', '2025-08-01 03:29:40.543057'),
('wpjhggmnryvlh8dwjkfotcdpkdwjlm7x', 'e30:1uaowt:xDpWe91KBstbfQPRahJFExy_LQpTsovMWMqDFwWneGs', '2025-07-27 05:08:27.607318'),
('yoafkwocgfgyqk3ey76qtik10n8tzh2p', '.eJxVizsOAyEMRO9CHa3AJoudMlLOgYwBscqnCLtVlLvnI4qkm5k372GibGuLWy_3uGRzMGB2v1sSPZfbB4w0fdkofTpdZbkcx-nPbNLbW_Oca_ahirfZpoAlw8zkiWbHwBAIS90jIKIrmqx6ZmEgq6rOWSbzfAEbHjRU:1ur5zd:_qhYiEJUYacBDgypmRiNeTix1NDmN0TDwQjPDojS-zA', '2025-09-10 02:34:33.353406');

-- --------------------------------------------------------

--
-- Table structure for table `doc_cover`
--

CREATE TABLE `doc_cover` (
  `cover_id` int NOT NULL,
  `project_name_th` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `project_name_en` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `author1_name_th` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `author2_name_th` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `author1_name_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `author2_name_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `academic_year` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doc_cover`
--

INSERT INTO `doc_cover` (`cover_id`, `project_name_th`, `project_name_en`, `author1_name_th`, `author2_name_th`, `author1_name_en`, `author2_name_en`, `academic_year`, `user_id`) VALUES
(6, '', '', '', '', '', '', '', 2);

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
(17, 'ระบบสนับสนุนการจัดทำเล่มโครงงานพิเศษ', 'Special Project Formatting Assistant', 'ไม่มี', '2', '2567', 'ผศ.จสต.นพเก้า ทองใบ', '', 'การพัฒนาวิทยาศาสตร์ เทคโนโลยี การวิจัย และ นวัตกรรมระดับขั้นแนวหน้าที่ก้าวหน้าล้ำยุค เพื่อสร้างโอกาสใหม่ และความพร้อมของประเทศในอนาคต', '20 พัฒนาโครงสร้างพื้นฐาน ด้านวิทยาศาสตร์ วิจัย และนวัตกรรมและโครงสร้าง พื้นฐานทางคุณภาพของประเทศที่รองรับการวิจัยขั้นแนวหน้า และการพัฒนาเทคโนโลยีและนวัตกรรมสู่อนาคต', 'ประเทศไทยมีโครงสร้างพื้นฐานด้านวิทยาศาสตร์ วิจัย นวัตกรรมที่สำคัญ\r\nเทคโนโลยีพื้นฐาน และโครงสร้างพื้นฐานทางคุณภาพสำหรับการวิจัยขั้นแนวหน้าที่ทัดเทียมมาตรฐานสากลและสามารถรองรับการพัฒนาอย่างก้าวกระโดดสู่อนาคต\r\n', 'การจัดทำเล่มปริญญานิพนธ์เป็นขั้นตอนที่สำคัญสำหรับนักศึกษาในการแสดงศักยภาพและความรู้ที่ได้สั่งสมมาตลอดระยะเวลาการศึกษา กระบวนการนี้เกี่ยวข้องกับการนำเสนอเนื้อหาการวิจัย การรวบรวมข้อมูล และการทำเล่มปริญญานิพนธ์ให้ตรงตามรูปแบบที่กำหนด ซึ่งถือเป็นมาตรฐานที่ช่วยยกระดับคุณภาพของผลงานวิจัย อีกทั้งการจัดรูปเล่มที่ถูกต้องยังสะท้อนถึงความเป็นมืออาชีพและความเอาใจใส่ในรายละเอียดของนักศึกษา', 'ในปัจจุบัน นักศึกษามักพบอุปสรรคในการจัดรูปเล่มปริญญานิพนธ์ เนื่องจากมีเวลาที่จำกัด ซึ่งต้องจัดทำงานวิจัยและเตรียมตัวสอบในหลายวิชา การตรวจสอบความถูกต้องของรูปแบบจึงมีโอกาสเกิดข้อผิดพลาด เช่น การจัดหน้า การเว้นวรรค หรือการละเลยรายละเอียดที่สำคัญ ปัญหาเหล่านี้ทำให้งานวิจัยที่ควรแสดงถึงคุณภาพอาจไม่สมบูรณ์ตามที่คาดหวังไว้', 'เพื่อแก้ไขปัญหาเหล่านี้ ทางคณะผู้จัดทำจึงได้พัฒนาระบบช่วยจัดทำเล่มปริญญานิพนธ์ที่สามารถสร้างรูปแบบมาตรฐานได้โดยอัตโนมัติผ่านเว็บเบราว์เซอร์ ระบบจะช่วยจัดทำรูปแบบเล่ม การจัดหน้า การตัดคำ ผู้ใช้งานสามารถใส่ข้อมูลที่เตรียมไว้ลงในระบบเพื่อให้ระบบประมวลผลและสร้างเล่มปริญญานิพนธ์ที่สมบูรณ์ตรงตามมาตรฐานที่กำหนด ช่วยลดข้อผิดพลาดและเพิ่มความสะดวกสบายในการทำงานได้อย่างมีประสิทธิภาพ', 'เพื่อพัฒนาระบบสนับสนุนการจัดทำเล่ม ทก. และ โครงงานพิเศษ', '', '', '\"[{\\\"main\\\": \\\"สามารถจัดรูปแบบเล่มปริญญานิพนธ์ผ่านเว็บบราวเซอร์\\\", \\\"subs\\\": [\\\"การจัดทำระบบบนเว็บแอปพลิเคชัน\\\"]}]\"', 2);

-- --------------------------------------------------------

--
-- Table structure for table `sp_project_author`
--

CREATE TABLE `sp_project_author` (
  `id` bigint NOT NULL,
  `name` varchar(100) NOT NULL,
  `userid` bigint NOT NULL,
  `sp_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `sp_project_author`
--

INSERT INTO `sp_project_author` (`id`, `name`, `userid`, `sp_id`) VALUES
(40, 'นายเรืองวิชญ์  สิงห์หล้า', 1, 11),
(41, 'นางสาวสุกฤตา  กาหาวงศ์', 1, 11),
(395, 'นายเรืองวิชญ์  สิงห์หล้า', 2, 17),
(396, 'นางสาวสุกฤตา  กาหาวงศ์', 2, 17);

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
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `backend_customuser`
--
ALTER TABLE `backend_customuser`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `backend_customuser_groups`
--
ALTER TABLE `backend_customuser_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `backend_customuser_groups_customuser_id_group_id_a4f8c55e_uniq` (`customuser_id`,`group_id`),
  ADD KEY `backend_customuser_groups_group_id_5fab7100_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `backend_customuser_user_permissions`
--
ALTER TABLE `backend_customuser_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `backend_customuser_user__customuser_id_permission_ca2b53b6_uniq` (`customuser_id`,`permission_id`),
  ADD KEY `backend_customuser_u_permission_id_9e1b6f57_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_backend_customuser_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `doc_cover`
--
ALTER TABLE `doc_cover`
  ADD PRIMARY KEY (`cover_id`),
  ADD KEY `userid_doccover` (`user_id`);

--
-- Indexes for table `sp_project`
--
ALTER TABLE `sp_project`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `sp_project_author`
--
ALTER TABLE `sp_project_author`
  ADD PRIMARY KEY (`id`),
  ADD KEY `userid` (`userid`),
  ADD KEY `sp_id` (`sp_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `abstract`
--
ALTER TABLE `abstract`
  MODIFY `abstract_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `backend_customuser`
--
ALTER TABLE `backend_customuser`
  MODIFY `user_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `backend_customuser_groups`
--
ALTER TABLE `backend_customuser_groups`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `backend_customuser_user_permissions`
--
ALTER TABLE `backend_customuser_user_permissions`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `doc_cover`
--
ALTER TABLE `doc_cover`
  MODIFY `cover_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `sp_project`
--
ALTER TABLE `sp_project`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `sp_project_author`
--
ALTER TABLE `sp_project_author`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=397;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `abstract`
--
ALTER TABLE `abstract`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `backend_customuser_groups`
--
ALTER TABLE `backend_customuser_groups`
  ADD CONSTRAINT `backend_customuser_g_customuser_id_a9d2181c_fk_backend_c` FOREIGN KEY (`customuser_id`) REFERENCES `backend_customuser` (`user_id`),
  ADD CONSTRAINT `backend_customuser_groups_group_id_5fab7100_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `backend_customuser_user_permissions`
--
ALTER TABLE `backend_customuser_user_permissions`
  ADD CONSTRAINT `backend_customuser_u_customuser_id_44346a50_fk_backend_c` FOREIGN KEY (`customuser_id`) REFERENCES `backend_customuser` (`user_id`),
  ADD CONSTRAINT `backend_customuser_u_permission_id_9e1b6f57_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_backend_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`);

--
-- Constraints for table `doc_cover`
--
ALTER TABLE `doc_cover`
  ADD CONSTRAINT `userid_doccover` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `sp_project`
--
ALTER TABLE `sp_project`
  ADD CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

--
-- Constraints for table `sp_project_author`
--
ALTER TABLE `sp_project_author`
  ADD CONSTRAINT `sp_id` FOREIGN KEY (`sp_id`) REFERENCES `sp_project` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `userid` FOREIGN KEY (`userid`) REFERENCES `backend_customuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
