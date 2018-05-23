-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: proyectoprueba1
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cambios`
--

DROP TABLE IF EXISTS `cambios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cambios` (
  `idcambios` int(11) NOT NULL AUTO_INCREMENT,
  `fecha` timestamp NULL DEFAULT NULL,
  `porcentaje` float DEFAULT NULL,
  `estatus` varchar(20) NOT NULL,
  `urls_idurls` int(11) NOT NULL,
  PRIMARY KEY (`idcambios`),
  KEY `fk_idurl_cambio` (`urls_idurls`),
  CONSTRAINT `fk_idurl_cambio` FOREIGN KEY (`urls_idurls`) REFERENCES `urls` (`idurls`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cambios`
--

LOCK TABLES `cambios` WRITE;
/*!40000 ALTER TABLE `cambios` DISABLE KEYS */;
INSERT INTO `cambios` VALUES (1,'2018-02-25 07:21:36',100,'Error de Conexion',120),(2,'2018-02-25 07:21:36',100,'Error de Conexion',120),(3,'2018-02-25 07:23:39',100,'Error de Conexion',120),(4,'2018-02-25 07:51:29',2.98913,'ok 200',130),(5,'2018-02-25 07:51:50',2.98913,'ok 200',130),(6,'2018-02-25 08:00:13',2.98913,'ok 200',130),(7,'2018-02-25 08:04:28',2.98913,'ok 200',130),(8,'2018-02-25 08:05:39',2.98913,'ok 200',130),(9,'2018-02-25 08:06:36',2.98913,'ok 200',130),(10,'2018-02-28 01:51:40',2.98913,'hacked',130),(11,'2018-02-28 01:52:02',2.98913,'hacked',130),(12,'2018-02-28 01:52:06',2.98913,'hacked',130),(13,'2018-02-28 01:52:07',2.98913,'hacked',130),(14,'2018-02-28 01:52:07',2.98913,'hacked',130),(15,'2018-02-28 01:52:08',2.98913,'hacked',130),(16,'2018-02-28 01:52:09',2.98913,'hacked',130),(17,'2018-02-28 01:52:18',2.98913,'hacked',130),(18,'2018-02-28 01:52:19',2.98913,'hacked',130),(19,'2018-02-28 01:52:55',2.98913,'hacked',130),(20,'2018-02-28 01:57:03',100,'Error de Conexion',120),(21,'2018-02-28 02:03:28',2.98913,'hacked',130),(22,'2018-02-28 02:10:30',2.98913,'hacked',130),(23,'2018-03-01 03:26:59',25.5132,'ok 200',120),(24,'2018-03-01 03:58:49',2.98913,'hacked',130),(25,'2018-03-01 03:59:26',2.98913,'hacked',130),(26,'2018-03-01 04:00:40',2.98913,'ok 200',130),(27,'2018-03-04 15:59:55',2.98913,'ok 200',130),(28,'2018-03-04 16:02:46',2.98913,'ok 200',130),(29,'2018-03-04 16:03:09',2.98913,'ok 200',130),(30,'2018-03-04 16:03:40',0,'ok 200',130),(31,'2018-03-04 16:06:19',3.26087,'ok 200',130),(32,'2018-03-04 16:06:32',3.26087,'ok 200',130),(33,'2018-03-06 22:39:26',100,'Error de Conexion',120),(34,'2018-03-06 22:39:36',3.26087,'ok 200',130),(35,'2018-03-06 22:40:22',3.26087,'ok 200',130),(36,'2018-03-06 22:43:43',2.98103,'hacked hacked',130);
/*!40000 ALTER TABLE `cambios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entes`
--

DROP TABLE IF EXISTS `entes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entes` (
  `identes` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(80) DEFAULT NULL,
  `ministerios_idministerios` int(11) NOT NULL,
  PRIMARY KEY (`identes`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `fk_idministerios` (`ministerios_idministerios`),
  CONSTRAINT `fk_idministerios` FOREIGN KEY (`ministerios_idministerios`) REFERENCES `ministerios` (`idministerio`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entes`
--

LOCK TABLES `entes` WRITE;
/*!40000 ALTER TABLE `entes` DISABLE KEYS */;
INSERT INTO `entes` VALUES (5,'SUSCERTE',17),(14,'Ente de prueba',24);
/*!40000 ALTER TABLE `entes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ministerios`
--

DROP TABLE IF EXISTS `ministerios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ministerios` (
  `idministerio` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  PRIMARY KEY (`idministerio`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ministerios`
--

LOCK TABLES `ministerios` WRITE;
/*!40000 ALTER TABLE `ministerios` DISABLE KEYS */;
INSERT INTO `ministerios` VALUES (24,'Ministerio de Prueba'),(17,'Ministerio del Poder Popular para la Educación Universitaria, Ciencia y Tecnología'),(19,'Ministerio del Poder Popular para Relaciones Interiores, Justicia y Paz'),(22,'Ministerio del porder popular para la salud');
/*!40000 ALTER TABLE `ministerios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `portales`
--

DROP TABLE IF EXISTS `portales`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `portales` (
  `idportales` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(80) DEFAULT NULL,
  `entes_identes` int(11) NOT NULL,
  `porcDetectarDiferencia` float NOT NULL,
  `porcCambioActual` float NOT NULL,
  PRIMARY KEY (`idportales`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `fk_portales_entes1_idx` (`entes_identes`),
  CONSTRAINT `fk_portales_entes1` FOREIGN KEY (`entes_identes`) REFERENCES `entes` (`identes`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `portales`
--

LOCK TABLES `portales` WRITE;
/*!40000 ALTER TABLE `portales` DISABLE KEYS */;
INSERT INTO `portales` VALUES (98,'SUSCERTE - PORTAL',5,0,100),(101,'LOCALHOST',14,5,1.491),(102,'BCV - PORTAL',14,0,0);
/*!40000 ALTER TABLE `portales` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `urls`
--

DROP TABLE IF EXISTS `urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `urls` (
  `idurls` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `archivo` varchar(500) DEFAULT NULL,
  `md5` varchar(32) NOT NULL,
  `diff` text NOT NULL,
  `ultimo_porcentaje_cambio` float NOT NULL,
  `porcentaje_deteccion_cambio` float NOT NULL,
  `diff_aceptado` tinyint(1) NOT NULL,
  `estatus` varchar(20) NOT NULL,
  `portales_idportales` int(11) NOT NULL,
  PRIMARY KEY (`idurls`),
  UNIQUE KEY `url` (`url`),
  KEY `fk_urls_portales1_idx` (`portales_idportales`),
  CONSTRAINT `fk_urls_portales1` FOREIGN KEY (`portales_idportales`) REFERENCES `portales` (`idportales`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `urls`
--

LOCK TABLES `urls` WRITE;
/*!40000 ALTER TABLE `urls` DISABLE KEYS */;
INSERT INTO `urls` VALUES (120,'http://www.suscerte.gob.ve','portales/SUSCERTE - PORTAL/http___www.suscerte.gob.ve.txt','Error de Conexion','Error de Conexion',100,26,1,'Error de Conexion',98),(130,'http://localhost','portales/LOCALHOST/http___localhost.txt','ff66a3ec398d05eea118dbda045be64b','',2.98103,3.1,1,'hacked hacked',101),(132,'http://localhost/manual','portales/LOCALHOST/http___localhost_manual.txt','d5bcd7e5feb6bc403038709d5205f238','',0,0,1,'ok 200',101);
/*!40000 ALTER TABLE `urls` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-07  7:45:37
