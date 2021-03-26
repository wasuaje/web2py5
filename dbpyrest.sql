-- MySQL dump 10.13  Distrib 5.5.29, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: dbPyRest
-- ------------------------------------------------------
-- Server version	5.5.29-0ubuntu0.12.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_cas`
--

DROP TABLE IF EXISTS `auth_cas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_cas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `service` varchar(255) DEFAULT NULL,
  `ticket` varchar(255) DEFAULT NULL,
  `renew` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_cas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_cas`
--

LOCK TABLES `auth_cas` WRITE;
/*!40000 ALTER TABLE `auth_cas` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_cas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_event`
--

DROP TABLE IF EXISTS `auth_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time_stamp` datetime DEFAULT NULL,
  `client_ip` varchar(255) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `origin` varchar(255) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_event_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_event`
--

LOCK TABLES `auth_event` WRITE;
/*!40000 ALTER TABLE `auth_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(255) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_membership`
--

DROP TABLE IF EXISTS `auth_membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_membership` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_membership_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `auth_membership_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_membership`
--

LOCK TABLES `auth_membership` WRITE;
/*!40000 ALTER TABLE `auth_membership` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `table_name` varchar(255) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `registration_key` varchar(255) DEFAULT NULL,
  `reset_password_key` varchar(255) DEFAULT NULL,
  `registration_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'Duducoma','Popapomo','mamacesa@example.com','','Concluding this energy which two of the eyes. Girdled about. ','Wasted. It forms of unexhausted possibilities of damp meadow. in. ','Butterfly kallima inachis from water from the waves 1 of the. '),(2,'Dacosamo','Dasococe','madutadu@example.com','','Empire. he shows the greek meaning of the fox or feelings. ','Shore-pool. sec. All the habit of evolution going on up. ','Gr granules. from the length of neck and eventually to strike. '),(3,'Pamadamo','Sapocopo','somasaco@example.com','','1869 that they differ as we must be several more. . ','Iron-forming bacteria of this made a profound calm of the surroundings. ','Figures--bison reindeer and concise view of pithecanthropus the solar spectrum. . '),(4,'Sasasota','Cotoduce','posodusa@example.com','','Aesop prawn takes at each other growths on one which tackle. ','Ulna of man with the field. Had a bell is. ','Engrain capacities but it has instruments of the seven two very. '),(5,'Cocesoco','Potasopo','tasapopo@example.com','','Violates the past; it is independent lives at the man. ','Excessively minute in the use part with the finest gold has. ','Trundles about six meant the bat the surface or zoophyte. . '),(6,'Pomoceda','Motopopo','pomamosa@example.com','','Wires as walt whitman took longer than they are going on. ','Trilobite 90 days of the surface is as the constitution of. ','Jaws of teeth which circulate round about 9 inches below the. '),(7,'Tacoposo','Podacema','patadumo@example.com','','Protoplasm flowing through them insulators because of slits the spineless cactus. ','Distinctions except that walks slowly on a large number of migration.. ','Lethargic state of its typical districts. The energy disappears from. '),(8,'Dusosoce','Ducomama','papacedu@example.com','','286 transformation such time immemorial and sheep. The photograph. . ','Refinements are just a tube. New view of the project. ','Happened to do not very literal blood-relationship between shadow across the. '),(9,'Pamodada','Pacetata','tapopota@example.com','','Most of the stick it feeds on its partner s sons. ','Want. illustration: harvard college observatory. a common foraminifer polystomella showing. ','Heidelbergensis discovered in the earth it collects pollen from fossil horses. '),(10,'Tosasosa','Cepacomo','satotoso@example.com','','Terra firma and sponges jellyfish it often got the sake professor. ','Killdeer plover has to depress one of trekking to charge on. ','Lessen the stars the conclusion what the atoms and saltatory display. ');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cf_cliente`
--

DROP TABLE IF EXISTS `cf_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cf_cliente` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `razon_social` varchar(255) DEFAULT NULL,
  `direccion` longtext,
  `rif` varchar(255) DEFAULT NULL,
  `nit` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `tlf` varchar(255) DEFAULT NULL,
  `fax` varchar(255) DEFAULT NULL,
  `ruta_foto` varchar(255) DEFAULT NULL,
  `juridico` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cf_cliente`
--

LOCK TABLES `cf_cliente` WRITE;
/*!40000 ALTER TABLE `cf_cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `cf_cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cf_empresa`
--

DROP TABLE IF EXISTS `cf_empresa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cf_empresa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `razon_social` varchar(255) DEFAULT NULL,
  `rif` varchar(255) DEFAULT NULL,
  `nit` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `tlf` varchar(255) DEFAULT NULL,
  `fax` varchar(255) DEFAULT NULL,
  `ruta_foto` varchar(255) DEFAULT NULL,
  `direccion` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cf_empresa`
--

LOCK TABLES `cf_empresa` WRITE;
/*!40000 ALTER TABLE `cf_empresa` DISABLE KEYS */;
INSERT INTO `cf_empresa` VALUES (1,'Restaurant 1','Restaurant 1','J-1234569-2','','resta@gmail.com','58412-3659899','','cf_empresa.ruta_foto.b764f92bb1f67f9d.69636f2d696e6475636f6d2e706e67.png','La Candelaria Esq. de Animas');
/*!40000 ALTER TABLE `cf_empresa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cf_mesa`
--

DROP TABLE IF EXISTS `cf_mesa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cf_mesa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(255) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `ruta_foto` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cf_mesa`
--

LOCK TABLES `cf_mesa` WRITE;
/*!40000 ALTER TABLE `cf_mesa` DISABLE KEYS */;
INSERT INTO `cf_mesa` VALUES (1,'00','Cliente de Contado',''),(2,'01','Mesa 01',''),(3,'02','Mesa 02',''),(4,'03','Mesa 03',''),(5,'04','Mesa 04',''),(6,'05','Mesa 05','');
/*!40000 ALTER TABLE `cf_mesa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cf_proveedor`
--

DROP TABLE IF EXISTS `cf_proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cf_proveedor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) DEFAULT NULL,
  `razon_social` varchar(255) DEFAULT NULL,
  `direccion` longtext,
  `rif` varchar(255) DEFAULT NULL,
  `nit` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `tlf` varchar(255) DEFAULT NULL,
  `fax` varchar(255) DEFAULT NULL,
  `ruta_foto` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cf_proveedor`
--

LOCK TABLES `cf_proveedor` WRITE;
/*!40000 ALTER TABLE `cf_proveedor` DISABLE KEYS */;
/*!40000 ALTER TABLE `cf_proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fc_orden`
--

DROP TABLE IF EXISTS `fc_orden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fc_orden` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `numero` varchar(255) DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `cliente_id` int(11) DEFAULT NULL,
  `closed` char(1) DEFAULT NULL,
  `delivery` char(1) DEFAULT NULL,
  `delivered` char(1) DEFAULT NULL,
  `delivery_paid` char(1) DEFAULT NULL,
  `facturada` char(1) DEFAULT NULL,
  `num_fact` varchar(255) DEFAULT NULL,
  `fecha_fac` date DEFAULT NULL,
  `mesa_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fc_orden`
--

LOCK TABLES `fc_orden` WRITE;
/*!40000 ALTER TABLE `fc_orden` DISABLE KEYS */;
INSERT INTO `fc_orden` VALUES (13,NULL,'2013-03-05',0,'F','F','F','F','F',NULL,NULL,1);
/*!40000 ALTER TABLE `fc_orden` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fc_orden_det`
--

DROP TABLE IF EXISTS `fc_orden_det`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fc_orden_det` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `producto_id` int(11) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `importe` float DEFAULT NULL,
  `iva` float DEFAULT NULL,
  `imp1` float DEFAULT NULL,
  `imp2` float DEFAULT NULL,
  `descuento` float DEFAULT NULL,
  `total` float DEFAULT NULL,
  `orden_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fc_orden_det`
--

LOCK TABLES `fc_orden_det` WRITE;
/*!40000 ALTER TABLE `fc_orden_det` DISABLE KEYS */;
INSERT INTO `fc_orden_det` VALUES (13,1,1,80,12,0,0,0,89.6,13),(14,1,1,80,12,0,0,0,89.6,13),(16,1,1,80,12,0,0,0,89.6,13),(24,1,1,80,12,0,0,0,89.6,13),(25,1,1,80,12,0,0,0,89.6,13);
/*!40000 ALTER TABLE `fc_orden_det` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `in_categoria`
--

DROP TABLE IF EXISTS `in_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `in_categoria` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(255) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `show_in_menu` char(1) DEFAULT NULL,
  `ruta_foto` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `in_categoria`
--

LOCK TABLES `in_categoria` WRITE;
/*!40000 ALTER TABLE `in_categoria` DISABLE KEYS */;
INSERT INTO `in_categoria` VALUES (1,'01','Entradas','T','in_categoria.ruta_foto.83ef17064ea81c18.656e73616c616461732e6a7067.jpg'),(2,'02','Desayunos','T','in_categoria.ruta_foto.8e7d22a98bb4df19.6465736179756e6f2e6a706567.jpeg'),(3,'03','Almuerzos','T','in_categoria.ruta_foto.a012d0a7ab68f864.6361726e65732e6a706567.jpeg'),(4,'04','Licores','T','in_categoria.ruta_foto.b2fe9358bac2d0b0.6c69636f7265732e6a706567.jpeg'),(5,'05','Bebidas','T','in_categoria.ruta_foto.98d873102435a558.626562696461732e6a7067.jpg');
/*!40000 ALTER TABLE `in_categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `in_producto`
--

DROP TABLE IF EXISTS `in_producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `in_producto` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(255) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `show_in_menu` char(1) DEFAULT NULL,
  `ruta_foto` varchar(255) DEFAULT NULL,
  `categoria_id` int(11) DEFAULT NULL,
  `imp2` float DEFAULT NULL,
  `imp1` float DEFAULT NULL,
  `iva` float DEFAULT NULL,
  `descuento` float DEFAULT NULL,
  `costo` float DEFAULT NULL,
  `importe` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `in_producto`
--

LOCK TABLES `in_producto` WRITE;
/*!40000 ALTER TABLE `in_producto` DISABLE KEYS */;
INSERT INTO `in_producto` VALUES (1,'01','Ensalada Cesar','T','in_producto.ruta_foto.96470f0367149164.656e7472616461312e6a7067.jpg',1,0,0,12,0,60,80),(2,'02','Sopa','T','in_producto.ruta_foto.91a952c9c0d1965b.656e7472616461322e6a706567.jpeg',1,NULL,NULL,NULL,NULL,NULL,NULL),(3,'03','Tortilla Española','T','in_producto.ruta_foto.a1120636a01924a9.656e7472616461332e6a706567.jpeg',1,NULL,NULL,NULL,NULL,NULL,NULL),(4,'04','Huevos con pan','T','in_producto.ruta_foto.a536de1e9e4c42f4.6465736179756e6f322e6a706567.jpeg',2,NULL,NULL,NULL,NULL,NULL,NULL),(5,'05','Torta de jamon','T','in_producto.ruta_foto.a6f5a94858a49a55.6465736179756e6f332e6a706567.jpeg',2,NULL,NULL,NULL,NULL,NULL,NULL),(6,'06','Panquecas','T','in_producto.ruta_foto.8b13a71b00b1b6cd.6465736179756e6f312e6a7067.jpg',2,NULL,NULL,NULL,NULL,NULL,NULL),(7,'07','Shawarma','T','in_producto.ruta_foto.ac1c7441862c1835.616c6d7565727a6f312e6a7067.jpg',3,NULL,NULL,NULL,NULL,NULL,NULL),(8,'08','Carne Guisada','T','in_producto.ruta_foto.aae05b44b0851646.616c6d7565727a6f322e6a7067.jpg',3,NULL,NULL,NULL,NULL,NULL,NULL),(9,'09','Submarino','T','in_producto.ruta_foto.a424ea41cd8d0aba.616c6d7565727a6f332e6a7067.jpg',3,NULL,NULL,NULL,NULL,NULL,NULL),(10,'10','whisky','T','in_producto.ruta_foto.a393121e2144dffd.776869736b792e6a7067.jpg',4,NULL,NULL,NULL,NULL,NULL,NULL),(11,'11','Vino Tinto','T','in_producto.ruta_foto.99027ac42a7e1da4.76696e6f74696e746f2e6a7067.jpg',4,NULL,NULL,NULL,NULL,NULL,NULL),(12,'12','Vino Blanco','T','in_producto.ruta_foto.9a422bcc9b5aac51.76696e6f626c616e636f2e6a7067.jpg',4,NULL,NULL,NULL,NULL,NULL,NULL),(13,'13','Pepsi light','T','in_producto.ruta_foto.98d221226484a40f.676173656f7361342e6a7067.jpg',5,NULL,NULL,NULL,NULL,NULL,NULL),(14,'14','Coca Cola','T','in_producto.ruta_foto.8f746a6836bbe19c.676173656f7361322e6a7067.jpg',5,NULL,NULL,NULL,NULL,NULL,NULL),(15,'15','Sprite','T','in_producto.ruta_foto.b032c799ff03f011.676173656f7361332e6a7067.jpg',5,NULL,NULL,NULL,NULL,NULL,NULL),(16,'16','Agua mineral','T','in_producto.ruta_foto.aae4c25c3ef119b2.676173656f7361352e6a7067.jpg',5,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `in_producto` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2013-04-10 15:35:06
