CREATE TABLE products (
    id integer primary key autoincrement,
    url_page TEXT,
    number integer UNIQUE,
    name TEXT,
    cost TEXT,
    image_url TEXT,
    description TEXT,
    timestamp TEXT,
    user_url TEXT
);