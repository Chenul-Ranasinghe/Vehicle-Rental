
CREATE DATABASE IF NOT EXISTS car_rental;
USE car_rental;

CREATE TABLE IF NOT EXISTS admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(50) NOT NULL,          
    model VARCHAR(50) NOT NULL,         
    year INT NOT NULL,                   
    color VARCHAR(30),
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    daily_rate DECIMAL(10,2) NOT NULL,  
    status ENUM('available', 'rented', 'maintenance') DEFAULT 'available',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rentals (
    rental_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    vehicle_id INT NOT NULL,
    user_id INT NOT NULL,              
    rental_date DATETIME NOT NULL,
    return_date DATETIME,              
    total_days INT,
    total_cost DECIMAL(10,2),
    status ENUM('active', 'returned', 'cancelled') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO admin (username, password, email) VALUES 
('admin', 'admin123', 'admin@carrentalkw.com');

INSERT INTO users (username, password, email, full_name) VALUES 
('john', 'user123', 'john@carrentalkw.com', 'John Smith'),
('sarah', 'user123', 'sarah@carrentalkw.com', 'Sarah Johnson');

INSERT INTO vehicles (make, model, year, color, license_plate, daily_rate, status) VALUES 
('Toyota', 'Camry', 2023, 'White', 'KWA123', 25.00, 'available'),
('Honda', 'Civic', 2022, 'Black', 'KWB456', 20.00, 'available'),
('Ford', 'Explorer', 2023, 'Blue', 'KWC789', 35.00, 'available'),
('Nissan', 'Altima', 2023, 'Red', 'KWE345', 22.00, 'available');

INSERT INTO customers (full_name, email, phone, address, license_number) VALUES 
('Ahmed Al-Mansour', 'ahmed@email.com', '+965 50012345', 'Kuwait City, Block 5', 'LIC001234'),
('Fatima Al-Sabah', 'fatima@email.com', '+965 50067890', 'Hawalli, Street 15', 'LIC005678'),
('Mohammed Al-Rashid', 'mohammed@email.com', '+965 50011223', 'Salmiya, Block 8', 'LIC009012');