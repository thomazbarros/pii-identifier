create database  store;

use store;

-- Table for storing categories
CREATE TABLE categories (
  category_id INT PRIMARY KEY,
  category_name VARCHAR(50) NOT NULL
);

-- Table for storing customers
CREATE TABLE customers (
  customer_id INT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(100),
  phone_number VARCHAR(20),
  address VARCHAR(100)
);

CREATE TABLE products (
  product_id INT PRIMARY KEY,
  product_name VARCHAR(100) NOT NULL,
  category_id INT,
  price DECIMAL(10, 2),
  stock_quantity INT,
  FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Table for storing orders
CREATE TABLE orders (
  order_id INT PRIMARY KEY,
  customer_id INT,
  order_date DATE,
  total_amount DECIMAL(10, 2),
  FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Table for storing order items
CREATE TABLE order_items (
  order_item_id INT PRIMARY KEY,
  order_id INT,
  product_id INT,
  quantity INT,
  unit_price DECIMAL(10, 2),
  FOREIGN KEY (order_id) REFERENCES orders(order_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Table for storing payments
CREATE TABLE payments (
  payment_id INT PRIMARY KEY,
  order_id INT,
  payment_date DATE,
  payment_amount DECIMAL(10, 2),
  payment_method VARCHAR(50),
  card_token VARCHAR(100), -- Tokenized card information
  FOREIGN KEY (order_id) REFERENCES orders(order_id)
);
