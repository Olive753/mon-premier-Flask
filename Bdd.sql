CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  role VARCHAR(255) NOT NULL,
  registration_date DATE NOT NULL,
  token VARCHAR(255) NOT NULL,
  expiration_date DATETIME NOT NULL,
  validation_date DATETIME
);
