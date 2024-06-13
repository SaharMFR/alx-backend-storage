-- Creates a table `users` following these requirements:
--   1. With these attributes:
--     * `id`, integer, never null, auto increment and primary key.
--     * `email`, string (255 chars), never null and unique.
--     * `name`, string (255 chars).
--   2. If the table already exists, the script should not fail.
--   3. The script can be executed on any database.
DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255)
);
