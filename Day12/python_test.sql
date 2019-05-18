/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.2.114
 Source Server Type    : MySQL
 Source Server Version : 50726
 Source Host           : 192.168.2.114:3306
 Source Schema         : python_test

 Target Server Type    : MySQL
 Target Server Version : 50726
 File Encoding         : 65001

 Date: 18/05/2019 15:53:55
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for course
-- ----------------------------
DROP TABLE IF EXISTS `course`;
CREATE TABLE `course`  (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`cid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of course
-- ----------------------------
INSERT INTO `course` VALUES (1, 'A');
INSERT INTO `course` VALUES (2, 'B');
INSERT INTO `course` VALUES (3, 'C');
INSERT INTO `course` VALUES (4, 'D');

-- ----------------------------
-- Table structure for record
-- ----------------------------
DROP TABLE IF EXISTS `record`;
CREATE TABLE `record`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cid` int(11) NULL DEFAULT NULL,
  `uid` int(11) NULL DEFAULT NULL,
  `score` smallint(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `cid`(`cid`) USING BTREE,
  INDEX `uid`(`uid`) USING BTREE,
  CONSTRAINT `record_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `course` (`cid`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `record_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `student` (`std_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of record
-- ----------------------------
INSERT INTO `record` VALUES (1, 1, 1, 90);
INSERT INTO `record` VALUES (2, 2, 1, 88);
INSERT INTO `record` VALUES (3, 3, 1, 80);
INSERT INTO `record` VALUES (4, 4, 1, 99);
INSERT INTO `record` VALUES (5, 1, 2, 78);
INSERT INTO `record` VALUES (6, 2, 2, 67);
INSERT INTO `record` VALUES (7, 3, 2, 59);
INSERT INTO `record` VALUES (8, 4, 2, 88);
INSERT INTO `record` VALUES (9, 1, 3, 99);
INSERT INTO `record` VALUES (10, 2, 3, 100);

-- ----------------------------
-- Table structure for score
-- ----------------------------
DROP TABLE IF EXISTS `score`;
CREATE TABLE `score`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NULL DEFAULT NULL,
  `score` smallint(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `uid`(`uid`) USING BTREE,
  CONSTRAINT `score_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `student` (`std_id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of score
-- ----------------------------
INSERT INTO `score` VALUES (1, 1, 68);
INSERT INTO `score` VALUES (2, 2, 59);
INSERT INTO `score` VALUES (3, 3, 100);
INSERT INTO `score` VALUES (4, 6, 98);
INSERT INTO `score` VALUES (5, 7, 89);
INSERT INTO `score` VALUES (6, 8, 75);

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `std_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sex` varchar(32) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `age` smallint(6) NULL DEFAULT NULL,
  PRIMARY KEY (`std_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (1, 'Tommy', 'M', 28);
INSERT INTO `student` VALUES (2, 'Jack', 'M', 20);
INSERT INTO `student` VALUES (3, 'Simmons', 'F', 22);
INSERT INTO `student` VALUES (6, 'Fitz', 'M', 25);
INSERT INTO `student` VALUES (7, 'Phil', 'M', 44);
INSERT INTO `student` VALUES (8, 'Daisy', 'F', 26);

SET FOREIGN_KEY_CHECKS = 1;
