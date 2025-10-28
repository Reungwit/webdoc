-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 01, 2025 at 06:51 PM
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
(2, 'pbkdf2_sha256$870000$8qwcUeeABxi9GgqY2tD2Li$/0ddq45eRFqPjahVOLkuO3HyKXEiUGiM7KiiCdlgR/U=', '2025-09-27 15:16:39.106346', 0, 1, 'BossReungwit', '', '', 0, '2025-07-13 05:28:03.461600', 'singlaboss@gmail.com', 'ZA');

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
-- Table structure for table `chapter5`
--

CREATE TABLE `chapter5` (
  `doc_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `intro_th` longtext,
  `sections_json` json NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `chapter5`
--

INSERT INTO `chapter5` (`doc_id`, `user_id`, `intro_th`, `sections_json`, `created_at`, `updated_at`) VALUES
(1, 2, 'ทดสอบ', '[{\"body\": \"uuuuu\", \"title\": \"สรุปผลการดำเนินงาน\", \"points\": [{\"main\": \"yyyyy\", \"subs\": []}]}, {\"body\": \"rrrrr\", \"title\": \"อภิปรายผล\", \"points\": [{\"main\": \"eeeee\", \"subs\": []}]}, {\"body\": \"wwwww\", \"title\": \"ข้อเสนอแนะ\", \"points\": [{\"main\": \"eeeee\", \"subs\": []}]}]', NULL, '2025-09-23 05:18:55');

-- --------------------------------------------------------

--
-- Table structure for table `chapter_1`
--

CREATE TABLE `chapter_1` (
  `chapter_id` int UNSIGNED NOT NULL COMMENT 'PK: รหัสรายการ (อัตโนมัติ)',
  `sec11_p1` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '1.1 ย่อหน้า 1: ข้อความความเป็นมาและความสำคัญของปัญหา (ย่อหน้า 1)',
  `sec11_p2` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '1.1 ย่อหน้า 2: ข้อความความเป็นมาและความสำคัญของปัญหา (ย่อหน้า 2)',
  `sec11_p3` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '1.1 ย่อหน้า 3: ข้อความความเป็นมาและความสำคัญของปัญหา (ย่อหน้า 3)',
  `purpose_count` tinyint UNSIGNED NOT NULL DEFAULT '0' COMMENT 'จำนวนวัตถุประสงค์ที่ผู้ใช้กรอก (0–3)',
  `purpose_1` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'วัตถุประสงค์ ข้อที่ 1 (1.2.1)',
  `purpose_2` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'วัตถุประสงค์ ข้อที่ 2 (1.2.2)',
  `purpose_3` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT 'วัตถุประสงค์ ข้อที่ 3 (1.2.3)',
  `hypo_paragraph` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci COMMENT '1.3 ย่อหน้า (มีได้ 0 หรือ 1 ย่อหน้า ตาม UI)',
  `hypo_items_json` json DEFAULT NULL COMMENT '1.3.x รายการสมมติฐานย่อย (JSON array ของ string)',
  `scope_json` json DEFAULT NULL COMMENT '1.4 ขอบเขต (JSON array ของ object: [{"main":"...","subs":["..."]}])',
  `para_premise` json DEFAULT NULL,
  `premise_json` json DEFAULT NULL COMMENT '1.5 ข้อตกลงเบื้องต้น (JSON array ของ object แบบเดียวกับ scope_json)',
  `def_items_json` json DEFAULT NULL COMMENT '1.6.x รายการนิยามศัพท์ (JSON array ของ string)',
  `benefit_items_json` json DEFAULT NULL COMMENT '1.7.x รายการประโยชน์ (JSON array ของ string)',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'เวลาที่สร้างข้อมูล',
  `user_id` bigint NOT NULL COMMENT 'FK: อ้างอิง backend_customuser.user_id'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ฟอร์มบทที่ 1 ต่อผู้ใช้ 1 คน 1 แถว; รายการหลายข้อเก็บเป็น JSON';

--
-- Dumping data for table `chapter_1`
--

INSERT INTO `chapter_1` (`chapter_id`, `sec11_p1`, `sec11_p2`, `sec11_p3`, `purpose_count`, `purpose_1`, `purpose_2`, `purpose_3`, `hypo_paragraph`, `hypo_items_json`, `scope_json`, `para_premise`, `premise_json`, `def_items_json`, `benefit_items_json`, `created_at`, `user_id`) VALUES
(3, 'การจัดทำเล่มปริญญานิพนธ์เป็นขั้นตอนที่สำคัญสำหรับนักศึกษาในการแสดงศักยภาพและความรู้ที่ได้สั่งสมมาตลอดระยะเวลาการศึกษา กระบวนการนี้เกี่ยวข้องกับการนำเสนอเนื้อหาการวิจัย การรวบรวมข้อมูล และการทำเล่มปริญญานิพนธ์ให้ตรงตามรูปแบบที่กำหนด ซึ่งถือเป็นมาตรฐานที่ช่วยยกระดับคุณภาพของผลงานวิจัย อีกทั้งการจัดรูปเล่มที่ถูกต้องยังสะท้อนถึงความเป็นมืออาชีพและความเอาใจใส่ในรายละเอียดของนักศึกษา', 'ในปัจจุบัน นักศึกษามักพบอุปสรรคในการจัดรูปเล่มปริญญานิพนธ์ เนื่องจากมีเวลาที่จำกัด ซึ่งต้องจัดทำงานวิจัยและเตรียมตัวสอบในหลายวิชา การตรวจสอบความถูกต้องของรูปแบบจึงมีโอกาสเกิดข้อผิดพลาด เช่น การจัดหน้า การเว้นวรรค หรือการละเลยรายละเอียดที่สำคัญ ปัญหาเหล่านี้ทำให้งานวิจัยที่ควรแสดงถึงคุณภาพอาจไม่สมบูรณ์ตามที่คาดหวังไว้', 'เพื่อแก้ไขปัญหาเหล่านี้ ทางคณะผู้จัดทำจึงได้พัฒนาระบบช่วยจัดทำเล่มปริญญานิพนธ์ที่สามารถสร้างรูปแบบมาตรฐานได้โดยอัตโนมัติผ่านเว็บเบราว์เซอร์ ระบบจะช่วยจัดทำรูปแบบเล่ม การจัดหน้า การตัดคำ ผู้ใช้งานสามารถใส่ข้อมูลที่เตรียมไว้ลงในระบบเพื่อให้ระบบประมวลผลและสร้างเล่มปริญญานิพนธ์ที่สมบูรณ์ตรงตามมาตรฐานที่กำหนด ช่วยลดข้อผิดพลาดและเพิ่มความสะดวกสบายในการทำงานได้อย่างมีประสิทธิภาพ', 3, 'เพื่อพัฒนาระบบสนับสนุนการจัดทำเล่ม ทก. และ โครงงานพิเศษ', 'เพื่อส่งเสริมการใช้เทคโนโลยีในการพัฒนาคุณภาพและมาตรฐานงานวิชาการของนักศึกษา', 'เพื่อให้ผู้ใช้สามารถใช้งานผ่านเว็บเบราว์เซอร์ได้โดยไม่ต้องติดตั้งซอฟต์แวร์เพิ่มเติม', 'การออกแบบและการพัฒนาระบบตรวจจับการล้มมีสมมุติฐานของการวิจัยเพื่อที่จะสร้างระบบ\r\nใหม่ที่มีเสถียรภาพเข้ามาทดแทนระบบงานเดิมซึ่งมีความล่าช้า มีการศึกษาค้นคว้าโดยอ้างอิงจาก\r\nงานวิจัยที่ใกล้เคียง กรณีศึกษา เครื่องตรวจจับการล้ม มีตัวแปรที่เกี่ยวข้องดังนี้', '[\"ตัวแปรต้น คือ ระบบตรวจจับการล้มต้องมีอุปกรณ์ติดตัวผู้ที่ต้องการตรวจจับได้เพียง เครื่องละ 1 คน และหากมีการสั่นสะเทือนเกิดขึ้นอาจจะให้ระบบตรวจจับผิดพลาดได้ ระบบเดิมจึงมี ความแม่นยำและยังต้องมีอุปกรณ์ติดตัวตลอดเวลาอีกด้วย\", \"ตัวแปรตาม คือ ประสิทธิภาพของระบบตรวจจับการล้มตรวจจับได้อย่างแม่นยำมากขึ้น และไม่มีสิ่งของติดอยู่ตามร่างกายหรือเสื้อผ้า\"]', '[{\"main\": \"สามารถจัดรูปแบบเล่มปริญญานิพนธ์ผ่านเว็บบราวเซอร์\", \"subs\": [\"การจัดทำระบบบนเว็บแอปพลิเคชัน\"]}, {\"main\": \"สามารถจัดรูปแบบของเอกสาร\", \"subs\": [\"การจัดรูปแบบตัวอักษรหัวข้อ หัวข้อย่อย และเนื้อหาได้\"]}]', '\"ทดสอบ\"', '[{\"main\": \"สามารถเข้าถึงข้อมูลที่มีการอัพเดตได้ก็ต่อเมื่อมีสัญญาณอินเตอร์เน็ต\", \"subs\": []}, {\"main\": \"ระบบจะต้องออนไลน์อยู่ตลอดเวลา\", \"subs\": []}, {\"main\": \"การติดตั้งกล้องที่ขนาดของห้องที่ได้ผลลัพธ์ที่ดีที่สุดขณะทดลองสูง 3 เมตร กว้าง 5 เมตร ยาว 5 เมตร\", \"subs\": []}]', '[\"แจ้งเตือน หมายถึง การเตือนหรือการแจ้งให้ทราบเมื่อมีอุบัติเหตุเกิดขึ้น\", \"GPS คือ ระบบระบุตำแหน่งบนพื้นโลก ย่อมาจากคำว่า Global Positioning System\"]', '[\"ได้รับระบบที่ช่วยแจ้งเตือนเกี่ยวกับการล้มในที่พักอาศัย\", \"ได้ระบบที่ให้ความช่วยเหลือเกี่ยวกับอุบัติเหตจากการล้มได้ทันท่วงที\", \"ช่วยลดอัตราการบาดเจ็บจากการล้มในผู้สูงอายุ\"]', '2025-09-03 04:57:52', 2);

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
('r4892tpziskcr71l3c8pda3w85mbuxpf', '.eJxVi0sOwjAMRO-SNaoSN65rlkicI3IcV6n4LAhdIe7OR1nAbmbevIdLst1r2prd0lrc3oHb_W5Z9GTXD-hp-LJe2nC8yHo-9NOfWaXVt0YyaWZbZgmescQwQ1bjAIF0HCUTEtDChuQj5hiweGXmwioGE4J7vgAsrTTg:1v2Wf9:NFCDp3kybgassELHVmkglY_v4Kx4eFDY6kLFdEZwydY', '2025-10-11 15:16:39.114121'),
('u9dze1aoy51z4ks0545dshbvas6f1oe0', '.eJxVjL0OwjAMhN8lM6qaxNQOIxLPETm2USp-BkInxLtXrTLAdnff3X1c5uVd89LslWd1J-fd4TcrLDd7bqCrYWfdtOHy4Pl-7qW_ZeVWtz8UNpowXQ18ID-qSpCiRILgcRoLcEygUMAXtKBGcpRkbMwxIrnvCjlQNcQ:1ujZ8t:oSW64YALFnAmW3EoOWafUF2uVjzENSkF2OkBsVZJeaE', '2025-08-20 08:04:59.776339'),
('vq3w1ecq34694ot5ig7qnqur7pzdszr1', 'e30:1ucbn2:7faVuZa-IAuaqSyPQuoUxbb0NvyDi0m5gxPNGZcGybU', '2025-08-01 03:29:40.543057'),
('wpjhggmnryvlh8dwjkfotcdpkdwjlm7x', 'e30:1uaowt:xDpWe91KBstbfQPRahJFExy_LQpTsovMWMqDFwWneGs', '2025-07-27 05:08:27.607318');

-- --------------------------------------------------------

--
-- Table structure for table `doc_abstract`
--

CREATE TABLE `doc_abstract` (
  `doc_id` int NOT NULL,
  `user_id` bigint NOT NULL,
  `total_pages` int NOT NULL,
  `keyword_th` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `keyword_en` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `abstract_th_json` json NOT NULL,
  `abstract_en_json` json DEFAULT NULL,
  `acknow_json` json DEFAULT NULL COMMENT 'กิตติกรรมประกาศ'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `doc_abstract`
--

INSERT INTO `doc_abstract` (`doc_id`, `user_id`, `total_pages`, `keyword_th`, `keyword_en`, `abstract_th_json`, `abstract_en_json`, `acknow_json`) VALUES
(1, 2, 10, '', '', '[\"ทดสอบ1\", \"ทดสอบ2\"]', '[\"Test1\", \"Test2\"]', '[\"ทดสอบ1\", \"ทดสอบ2\"]');

-- --------------------------------------------------------

--
-- Table structure for table `doc_introduction`
--

CREATE TABLE `doc_introduction` (
  `doc_id` int NOT NULL,
  `name_pro_th` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name_pro_en` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `student_name` json DEFAULT NULL,
  `school_y_BE` int DEFAULT NULL COMMENT 'พ.ศ',
  `school_y_AD` int DEFAULT NULL COMMENT 'ค.ศ',
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
  `user_id` bigint NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `doc_introduction`
--

INSERT INTO `doc_introduction` (`doc_id`, `name_pro_th`, `name_pro_en`, `student_name`, `school_y_BE`, `school_y_AD`, `comm_dean`, `comm_prathan`, `comm_first`, `comm_sec`, `advisor_th`, `advisor_en`, `coadvisor_th`, `coadvisor_en`, `dep_th`, `dep_en`, `user_id`, `created_at`, `updated_at`) VALUES
(3, 'ตตตต', 'Special Project Formatting Assistant', '{\"en\": [\"Reungwit Singla\", \"test\"], \"th\": [\"นายเรืองวิชญ์  สิงห์หล้า\", \"นางสาวสุกฤตา  กาหาวงศ์\"]}', 2568, 2025, 'test', 'test', 'test', 'test', 'รองศาสตราจารย์ ดร.ยุพิน สรรพคุณ', '', '\"ไม่มี\"', '\"None\"', 'คณะเทคโนโลยีสารสนเทศ', 'Faculty of Information Technology', 2, '2025-09-27 06:59:40', '2025-10-01 09:47:03');

-- --------------------------------------------------------

--
-- Table structure for table `doc_ref_book`
--

CREATE TABLE `doc_ref_book` (
  `ref_book_id` int NOT NULL COMMENT 'รหัสหนังสือ',
  `book_authors_en` json DEFAULT NULL,
  `book_authors_th` json NOT NULL,
  `book_title_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `book_title_th` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `book_print_count_en` int DEFAULT NULL,
  `book_print_count_th` int NOT NULL,
  `book_city_print_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `book_city_print_th` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `book_publisher_en` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `book_publisher_th` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `book_y_print_en` int DEFAULT NULL,
  `book_y_print_th` int NOT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doc_ref_book`
--

INSERT INTO `doc_ref_book` (`ref_book_id`, `book_authors_en`, `book_authors_th`, `book_title_en`, `book_title_th`, `book_print_count_en`, `book_print_count_th`, `book_city_print_en`, `book_city_print_th`, `book_publisher_en`, `book_publisher_th`, `book_y_print_en`, `book_y_print_th`, `user_id`) VALUES
(3, NULL, '[\"ผต 1หนังสือ\"]', NULL, 'หหหห', NULL, 1, NULL, 'ดดดด', NULL, 'พพพ', NULL, 2568, 2);

-- --------------------------------------------------------

--
-- Table structure for table `doc_ref_web`
--

CREATE TABLE `doc_ref_web` (
  `ref_web_id` int NOT NULL,
  `ref_no` varchar(10) NOT NULL,
  `ref_web_authors_th` json NOT NULL,
  `ref_web_authors_en` json NOT NULL,
  `ref_web_title_th` varchar(255) NOT NULL,
  `ref_web_title_en` varchar(255) NOT NULL,
  `ref_url` varchar(255) NOT NULL,
  `ref_date_access` date NOT NULL,
  `user_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `doc_ref_web`
--

INSERT INTO `doc_ref_web` (`ref_web_id`, `ref_no`, `ref_web_authors_th`, `ref_web_authors_en`, `ref_web_title_th`, `ref_web_title_en`, `ref_url`, `ref_date_access`, `user_id`) VALUES
(1, '1', '[]', '[\"Eng\", \"Eng2\"]', '', 'uuuuqqqq', 'https://www.ukukeng.com', '2025-09-19', 2),
(2, '2', '[\"ไทย1\", \"ไทย2\"]', '[]', 'ชื่อเรื่องไทย', '', 'https://www.ukukthai.com', '2025-09-19', 2);

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
(17, 'ระบบสนับสนุนการจัดทำเล่มโครงงานพิเศษ', 'Special Project Formatting Assistant', 'ไม่มี', '2', '2567', 'ผศ.จสต.นพเก้า ทองใบ', 'ไม่มี', 'การพัฒนาวิทยาศาสตร์ เทคโนโลยี การวิจัย และ นวัตกรรมระดับขั้นแนวหน้าที่ก้าวหน้าล้ำยุค เพื่อสร้างโอกาสใหม่ และความพร้อมของประเทศในอนาคต', '20 พัฒนาโครงสร้างพื้นฐาน ด้านวิทยาศาสตร์ วิจัย และนวัตกรรมและโครงสร้าง พื้นฐานทางคุณภาพของประเทศที่รองรับการวิจัยขั้นแนวหน้า และการพัฒนาเทคโนโลยีและนวัตกรรมสู่อนาคต', 'ประเทศไทยมีโครงสร้างพื้นฐานด้านวิทยาศาสตร์ วิจัย นวัตกรรมที่สำคัญ\r\nเทคโนโลยีพื้นฐาน และโครงสร้างพื้นฐานทางคุณภาพสำหรับการวิจัยขั้นแนวหน้าที่ทัดเทียมมาตรฐานสากลและสามารถรองรับการพัฒนาอย่างก้าวกระโดดสู่อนาคต\r\n', 'การจัดทำเล่มปริญญานิพนธ์เป็นขั้นตอนที่สำคัญสำหรับนักศึกษาในการแสดงศักยภาพและความรู้ที่ได้สั่งสมมาตลอดระยะเวลาการศึกษา กระบวนการนี้เกี่ยวข้องกับการนำเสนอเนื้อหาการวิจัย การรวบรวมข้อมูล และการทำเล่มปริญญานิพนธ์ให้ตรงตามรูปแบบที่กำหนด ซึ่งถือเป็นมาตรฐานที่ช่วยยกระดับคุณภาพของผลงานวิจัย อีกทั้งการจัดรูปเล่มที่ถูกต้องยังสะท้อนถึงความเป็นมืออาชีพและความเอาใจใส่ในรายละเอียดของนักศึกษา', 'ในปัจจุบัน นักศึกษามักพบอุปสรรคในการจัดรูปเล่มปริญญานิพนธ์ เนื่องจากมีเวลาที่จำกัด ซึ่งต้องจัดทำงานวิจัยและเตรียมตัวสอบในหลายวิชา การตรวจสอบความถูกต้องของรูปแบบจึงมีโอกาสเกิดข้อผิดพลาด เช่น การจัดหน้า การเว้นวรรค หรือการละเลยรายละเอียดที่สำคัญ ปัญหาเหล่านี้ทำให้งานวิจัยที่ควรแสดงถึงคุณภาพอาจไม่สมบูรณ์ตามที่คาดหวังไว้', 'เพื่อแก้ไขปัญหาเหล่านี้ ทางคณะผู้จัดทำจึงได้พัฒนาระบบช่วยจัดทำเล่มปริญญานิพนธ์ที่สามารถสร้างรูปแบบมาตรฐานได้โดยอัตโนมัติผ่านเว็บเบราว์เซอร์ ระบบจะช่วยจัดทำรูปแบบเล่ม การจัดหน้า การตัดคำ ผู้ใช้งานสามารถใส่ข้อมูลที่เตรียมไว้ลงในระบบเพื่อให้ระบบประมวลผลและสร้างเล่มปริญญานิพนธ์ที่สมบูรณ์ตรงตามมาตรฐานที่กำหนด ช่วยลดข้อผิดพลาดและเพิ่มความสะดวกสบายในการทำงานได้อย่างมีประสิทธิภาพ', '', '', '', '\"[{\\\"main\\\": \\\"\\\", \\\"subs\\\": []}]\"', 2);

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
(397, 'นายเรืองวิชญ์  สิงห์หล้า', 2, 17),
(398, 'นางสาวสุกฤตา  กาหาวงศ์', 2, 17);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_certificate`
-- (See below for the actual view)
--
CREATE TABLE `v_certificate` (
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_doc_abstract`
-- (See below for the actual view)
--
CREATE TABLE `v_doc_abstract` (
);

-- --------------------------------------------------------

--
-- Stand-in structure for view `v_doc_cover`
-- (See below for the actual view)
--
CREATE TABLE `v_doc_cover` (
);

-- --------------------------------------------------------

--
-- Structure for view `v_certificate`
--
DROP TABLE IF EXISTS `v_certificate`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_certificate`  AS SELECT `i`.`doc_id` AS `doc_id`, `i`.`user_id` AS `user_id`, `i`.`name_pro_th` AS `name_pro_th`, `i`.`name_pro_en` AS `name_pro_en`, `i`.`student_name` AS `student_name`, `i`.`school_y_BE` AS `school_y_BE`, `i`.`school_y_AD` AS `school_y_AD`, `i`.`dep_th` AS `dep_th`, `i`.`dep_en` AS `dep_en`, `i`.`advisor_th` AS `advisor_th`, `i`.`advisor_en` AS `advisor_en`, `i`.`coadvisor_th` AS `coadvisor_th`, `i`.`coadvisor_en` AS `coadvisor_en`, `i`.`certificate_options` AS `certificate_options`, `i`.`comm_dean` AS `comm_dean`, `i`.`comm_prathan` AS `comm_prathan`, `i`.`comm_first` AS `comm_first`, `i`.`comm_sec` AS `comm_sec` FROM `doc_introduction` AS `i` ;

-- --------------------------------------------------------

--
-- Structure for view `v_doc_abstract`
--
DROP TABLE IF EXISTS `v_doc_abstract`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_doc_abstract`  AS SELECT `i`.`doc_id` AS `doc_id`, `i`.`user_id` AS `user_id`, `i`.`name_pro_th` AS `project_name_th`, `i`.`name_pro_en` AS `project_name_en`, `i`.`dep_th` AS `major_th`, `i`.`dep_en` AS `major_en`, `i`.`advisor_th` AS `advisor_th`, `i`.`advisor_en` AS `advisor_en`, `i`.`coadvisor_th` AS `coadvisor_th`, `i`.`coadvisor_en` AS `coadvisor_en`, `i`.`school_y_BE` AS `academic_year_th`, `i`.`school_y_AD` AS `academic_year_en`, `a`.`abstract_th` AS `abstract_th`, `a`.`abstract_en` AS `abstract_en`, `a`.`acknow` AS `acknow`, `a`.`acknow_name1` AS `acknow_name1`, `a`.`acknow_name2` AS `acknow_name2` FROM (`doc_introduction` `i` left join `doc_abstract` `a` on((`a`.`doc_id` = `i`.`doc_id`))) ;

-- --------------------------------------------------------

--
-- Structure for view `v_doc_cover`
--
DROP TABLE IF EXISTS `v_doc_cover`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_doc_cover`  AS SELECT `i`.`doc_id` AS `doc_id`, `i`.`user_id` AS `user_id`, `i`.`name_pro_th` AS `name_pro_th`, `i`.`name_pro_en` AS `name_pro_en`, `i`.`student_name` AS `student_name`, `i`.`school_y_BE` AS `school_y_BE`, `i`.`school_y_AD` AS `school_y_AD`, `i`.`dep_th` AS `dep_th`, `i`.`dep_en` AS `dep_en`, `i`.`advisor_th` AS `advisor_th`, `i`.`advisor_en` AS `advisor_en`, `i`.`coadvisor_th` AS `coadvisor_th`, `i`.`coadvisor_en` AS `coadvisor_en`, `i`.`cover_options` AS `cover_options` FROM `doc_introduction` AS `i` ;

--
-- Indexes for dumped tables
--

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
-- Indexes for table `chapter5`
--
ALTER TABLE `chapter5`
  ADD PRIMARY KEY (`doc_id`),
  ADD KEY `fk_user_ct5` (`user_id`);

--
-- Indexes for table `chapter_1`
--
ALTER TABLE `chapter_1`
  ADD PRIMARY KEY (`chapter_id`),
  ADD UNIQUE KEY `uq_chapter_1_user` (`user_id`) COMMENT 'บังคับให้ 1 ผู้ใช้มีบทที่ 1 ได้ 1 แถว';

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
-- Indexes for table `doc_abstract`
--
ALTER TABLE `doc_abstract`
  ADD PRIMARY KEY (`doc_id`),
  ADD UNIQUE KEY `uq_abs_doc` (`doc_id`),
  ADD KEY `fk_abs_user` (`user_id`);

--
-- Indexes for table `doc_introduction`
--
ALTER TABLE `doc_introduction`
  ADD PRIMARY KEY (`doc_id`),
  ADD UNIQUE KEY `uq_intro_user` (`user_id`);

--
-- Indexes for table `doc_ref_book`
--
ALTER TABLE `doc_ref_book`
  ADD PRIMARY KEY (`ref_book_id`),
  ADD KEY `userid_refbook` (`user_id`);

--
-- Indexes for table `doc_ref_web`
--
ALTER TABLE `doc_ref_web`
  ADD PRIMARY KEY (`ref_web_id`),
  ADD KEY `user_id_ref_web` (`user_id`);

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
  MODIFY `user_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

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
-- AUTO_INCREMENT for table `chapter5`
--
ALTER TABLE `chapter5`
  MODIFY `doc_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `chapter_1`
--
ALTER TABLE `chapter_1`
  MODIFY `chapter_id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'PK: รหัสรายการ (อัตโนมัติ)', AUTO_INCREMENT=4;

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
-- AUTO_INCREMENT for table `doc_abstract`
--
ALTER TABLE `doc_abstract`
  MODIFY `doc_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `doc_introduction`
--
ALTER TABLE `doc_introduction`
  MODIFY `doc_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `doc_ref_book`
--
ALTER TABLE `doc_ref_book`
  MODIFY `ref_book_id` int NOT NULL AUTO_INCREMENT COMMENT 'รหัสหนังสือ', AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `doc_ref_web`
--
ALTER TABLE `doc_ref_web`
  MODIFY `ref_web_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `sp_project`
--
ALTER TABLE `sp_project`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `sp_project_author`
--
ALTER TABLE `sp_project_author`
  MODIFY `id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=399;

--
-- Constraints for dumped tables
--

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
-- Constraints for table `chapter5`
--
ALTER TABLE `chapter5`
  ADD CONSTRAINT `fk_user_ct5` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `chapter_1`
--
ALTER TABLE `chapter_1`
  ADD CONSTRAINT `fk_chapter_1_user` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_backend_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`);

--
-- Constraints for table `doc_abstract`
--
ALTER TABLE `doc_abstract`
  ADD CONSTRAINT `fk_abs_user` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `doc_introduction`
--
ALTER TABLE `doc_introduction`
  ADD CONSTRAINT `fk_intro_user` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `doc_ref_book`
--
ALTER TABLE `doc_ref_book`
  ADD CONSTRAINT `userid_refbook` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `doc_ref_web`
--
ALTER TABLE `doc_ref_web`
  ADD CONSTRAINT `user_id_ref_web` FOREIGN KEY (`user_id`) REFERENCES `backend_customuser` (`user_id`) ON DELETE RESTRICT ON UPDATE RESTRICT;

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
