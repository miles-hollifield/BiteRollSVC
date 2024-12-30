/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `firstname` varchar(100) NOT NULL,
  `lastname` varchar(100) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `avatar` mediumtext DEFAULT NULL,
  `salt` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `restaurants` (
  `restaurant_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `restaurant_name` varchar(100) NOT NULL,
  `restaurant_cuisine` varchar(100) DEFAULT NULL,
  `restaurant_website` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`restaurant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `sets` (
  `set_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `set_name` varchar(100) NOT NULL,
  `user_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`set_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `favorites` (
  `favorite_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` int(10) unsigned NOT NULL,
  `restaurant_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`favorite_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`restaurant_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `set_entries` (
  `set_entry_id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `set_id` int(10) unsigned NOT NULL,
  `restaurant_id` int(10) unsigned NOT NULL,
  PRIMARY KEY (`set_entry_id`),
  FOREIGN KEY (`set_id`) REFERENCES `sets` (`set_id`) ON DELETE CASCADE,
  FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`restaurant_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Inserting test data into `users`
INSERT INTO `users` (firstname, lastname, username, email, avatar, salt, password) VALUES
('Stu', 'Dent', 'student', 'stu.dent@example.com', '', '48c8947f69c054a5caa934674ce8881d02bb18fb59d5a63eeaddff735b0e9', '83d9bdb5e20f3571b087db9aabf190a296741c3e864d7742f35658cfccc1b79c4599aad25084aa9a28c649a50c92244227b3e53e197621301d619d1ea01873c4'),
('Jane', 'Doe', 'janedoe', 'jane.doe@example.com', 'path/to/avatar2.jpg', 'randomsalt2', 'hashedpassword2');

-- Inserting test data into `restaurants`
INSERT INTO `restaurants` (restaurant_name, restaurant_cuisine, restaurant_website) VALUES
('Pasta Place', 'Italian', 'http://pastaplace.com'),
('Curry Corner', 'Indian', 'http://currycorner.com'),
('Grill House', 'American', 'http://grillhouse.com'),
('Taco Tower', 'Mexican', 'http://tacotower.com'),
('Pho Real', 'Vietnamese', 'http://phoreal.com'),
('Burger Bonanza', 'American', 'http://burgerbonanza.com'),
('Sushi Sun', 'Japanese', 'http://sushisun.com'),
('Beijing Bites', 'Chinese', 'http://beijingbites.com'),
('Mamma Mia', 'Italian', 'http://mammamia.com'),
('Delhi Delights', 'Indian', 'http://delhidelights.com');

-- Inserting test data into `sets`
INSERT INTO `sets` (set_name, user_id) VALUES
('Italian Nights', 1),
('Indian Adventures', 1),
('American Grills', 1),
('Mexican Delights', 1),
('Vietnamese Vibes', 1),
('Fast Food Fun', 1),
('Sushi Specials', 1),
('Chinese Choices', 1),
('Italian Indulgence', 2),
('Indian Inspirations', 2);

-- Inserting test data into `favorites`
INSERT INTO `favorites` (user_id, restaurant_id) VALUES
(1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
(1, 6), (1, 7), (1, 8), (2, 9), (2, 10);

-- Inserting test data into `set_entries`
INSERT INTO `set_entries` (set_id, restaurant_id) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5),
(6, 6), (7, 7), (8, 8), (9, 9), (10, 10);


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET SQL_NOTES=@OLD_SQL_NOTES */;