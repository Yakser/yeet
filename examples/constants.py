CREATE_ARTICLES = """
CREATE TABLE IF NOT EXISTS articles (
    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    author int(11) NOT NULL,
    title varchar(255) NOT NULL,
    text TEXT NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
)
ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nickname varchar(128) NOT NULL UNIQUE KEY,
    email varchar(255) NOT NULL UNIQUE KEY,
    is_confirmed tinyint(1) NOT NULL DEFAULT 0,
    role ENUM('admin', 'user') NOT NULL,
    password_hash varchar(255) NOT NULL,
    auth_token varchar(255) NOT NULL,
    created_at datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
)


ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

INIT_QUERIES = [CREATE_USERS, CREATE_ARTICLES]

DB_SETTINGS = {
    'database': 'db',
    'user': 'user',
    'password': 'password1234',
    'host': 'localhost',
}
