/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50621
Source Host           : localhost:3306
Source Database       : easy_loan

Target Server Type    : MYSQL
Target Server Version : 50621
File Encoding         : 65001

Date: 2016-09-04 14:01:10
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('47bf951aa9e');

-- ----------------------------
-- Table structure for loan_application
-- ----------------------------
DROP TABLE IF EXISTS `loan_application`;
CREATE TABLE `loan_application` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `apply_name` varchar(20) DEFAULT NULL,
  `gender` smallint(6) DEFAULT NULL,
  `marriage_status` smallint(255) DEFAULT NULL,
  `apply_identi` varchar(20) DEFAULT NULL,
  `bank_name` varchar(128) DEFAULT NULL,
  `bank_account` varchar(30) DEFAULT NULL,
  `company_address` varchar(255) DEFAULT NULL,
  `company_mobile` varchar(255) DEFAULT NULL,
  `urgent_contacter1` varchar(255) DEFAULT NULL,
  `urgent_contacter2` varchar(255) DEFAULT NULL,
  `image1` varchar(255) DEFAULT NULL,
  `image2` varchar(255) DEFAULT NULL,
  `image3` varchar(255) DEFAULT NULL,
  `image4` varchar(255) DEFAULT NULL,
  `apply_status` smallint(255) DEFAULT NULL,
  `loan_amount` int(11) DEFAULT NULL,
  `mobile` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of loan_application
-- ----------------------------
INSERT INTO `loan_application` VALUES ('15', 'jackie123', '0', '1', null, '交通银行', '123456789900', '曹安公路4800号', '1234566', '小明+17812982193821+基友', '小明+17812982193821+基友', null, null, null, null, '1', null, '');
INSERT INTO `loan_application` VALUES ('16', 'jackie123', '0', '1', null, '交通银行', '123456789900', '曹安公路4800号', '1234566', '小明+17812982193821+基友', '小明+17812982193821+基友', '20160904135455671284.png', '20160904135455410597.png', '20160904135455265170.png', '20160904135455502793.png', '0', null, '');
INSERT INTO `loan_application` VALUES ('17', 'jackie123', '0', '1', null, '交通银行', '123456789900', '曹安公路4800号', '1234566', '小明+17812982193821+基友', '小明+17812982193821+基友', '20160904135635756048.png', '20160904135635238745.png', '20160904135635180245.png', '20160904135635327184.png', '0', null, '18918278580');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `withdraw_password` varchar(255) DEFAULT NULL,
  `mobile` varchar(20) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `loan_app_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `mobile` (`mobile`),
  KEY `loan_app_id` (`loan_app_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('1', 'jack', 'pbkdf2:sha1:1000$k35bX1rJ$45eb379eace32709f10d6b83c3bbaa8d10f1fc46', '1234', '18918278580', 'Shanghai tongji', null);
INSERT INTO `users` VALUES ('4', 'Jackie', 'pbkdf2:sha1:1000$ZBoB9Oml$080a6134fdeec056d210312c0a328f7a7c31a100', '12', '18918278581', null, null);
INSERT INTO `users` VALUES ('5', 'jackkk', 'pbkdf2:sha1:1000$OMx5nSqd$80b54e2492f818d85336498b61b3b5f248bd7246', null, '18918278582', null, null);
INSERT INTO `users` VALUES ('8', 'Admin', 'pbkdf2:sha1:1000$Xi8B6KgF$6bfd73e6e041bd88ae4b1062e7e771966bbc047a', null, '18817366807', null, null);
INSERT INTO `users` VALUES ('9', null, 'pbkdf2:sha1:1000$iE7iM76X$723334ad5507a3b53e091e860ba8d24a32c96d57', null, '18817366808', null, null);
