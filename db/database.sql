CREATE DATABASE paySystem;

USE paySystem;

-- CREATE TABLE Employees (
--     id INT NOT NULL AUTO_INCREMENT,
--     full_name VARCHAR(255) NOT NULL,
--     department_id INT NOT NULL,
--     position_id INT NOT NULL,
--     PRIMARY KEY (id)
-- );

-- CREATE TABLE Departments (
--     id INT NOT NULL AUTO_INCREMENT,
--     name VARCHAR(255) NOT NULL,
--     PRIMARY KEY (id)
-- );

-- CREATE TABLE Positions (
--     id INT NOT NULL AUTO_INCREMENT,
--     name VARCHAR(255) NOT NULL,
--     PRIMARY KEY (id)
-- );

-- CREATE TABLE SalaryTypes (
--     id INT NOT NULL AUTO_INCREMENT,
--     name VARCHAR(255) NOT NULL,
--     description VARCHAR(255) NOT NULL,
--     PRIMARY KEY (id)
-- );

-- CREATE TABLE Taxes (
--     id INT NOT NULL AUTO_INCREMENT,
--     name VARCHAR(255) NOT NULL,
--     rate DECIMAL(5,2) NOT NULL,
--     description VARCHAR(255) NOT NULL,
--     PRIMARY KEY (id)
-- );

-- CREATE TABLE TaxPayments (
--     id INT NOT NULL AUTO_INCREMENT,
--     employee_id INT NOT NULL,
--     tax_id INT NOT NULL,
--     year INT NOT NULL,
--     month INT NOT NULL,
--     amount DECIMAL(10,2) NOT NULL,
--     PRIMARY KEY (id),
--     FOREIGN KEY (employee_id) REFERENCES Employees(id),
--     FOREIGN KEY (tax_id) REFERENCES Taxes(id)
-- );

-- CREATE TABLE SalaryPayments (
--     id INT NOT NULL AUTO_INCREMENT,
--     employee_id INT NOT NULL,
--     salary_type_id INT NOT NULL,
--     year INT NOT NULL,
--     month INT NOT NULL,
--     amount DECIMAL(10,2) NOT NULL,
--     PRIMARY KEY (id),
--     FOREIGN KEY (employee_id) REFERENCES Employees(id),
--     FOREIGN KEY (salary_type_id) REFERENCES SalaryTypes(id)
-- );

-- INSERT INTO Departments (name) VALUES ('IT'), ('HR'), ('Finance');

-- INSERT INTO Positions (name) VALUES ('Developer'), ('Designer'), ('Manager');

-- INSERT INTO SalaryTypes (name, description) VALUES ('Base salary', 'Base salary for employees'), ('Bonus', 'Bonus for employees');

-- INSERT INTO Taxes (name, rate, description) VALUES ('Personal income tax', 0.13, 'Personal income tax rate in Russia'), ('Social tax', 0.302, 'Social tax rate in Russia');

-- INSERT INTO Employees (full_name, department_id, position_id) VALUES ('John Smith', 1, 1), ('Jane Doe', 2, 3), ('Bob Johnson', 3, 2);

-- INSERT INTO SalaryPayments (employee_id, salary_type_id, year, month, amount) VALUES (1, 1, 2022, 1, 50000), (2, 1, 2022, 1, 40000), (3, 1, 2022, 1, 45000), (1, 2, 2022, 2, 10000), (2, 2, 2022, 2, 8000);

