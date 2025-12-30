/* Relational Schemas (Corrected & Normalized)
01. Person(aadhar, name, age, dob, mobile, address)
02. Hosteller(aadhar, guardian_mob, join_date)
03. Guardian(guardian_mob, guardian_name)
04. Staff(aadhar, role)
05. Building(building_id, building_name, total_rooms)
06. Room(Room_no, building_no, floor, bed_count, wifi_available, bath_attached, ac_available)
07. Gets(aadhar, room_no, building_no)
08. Bill(Bill_no, amount, issue_date, paid_date)
09. Bill_Issue(issue_date, due_date)
10. Pays(Bill_no, aadhar)
11. Complaint(Complaint_no, Date, Status, Message)
12. MessageType(Message, type)
13. Raises(Complaint_no, aadhar)
14. Deals_with(complaint_no, aadhar)
15. Mess(Food_id, Food_name, Food_type)
16. Attends(aadhar, Food_id, Date, time)
17. Notice(notice_no, message, date)
18. Issues(notice_no, aadhar)
19. Login(username, person_type, password, last_login)
20. Access(aadhar, username)
*/

--CREATE DATABASE hostel_mgmt;

--Queries to create the required tables

-- 01
CREATE TABLE Person (
    aadhar CHAR(12) PRIMARY KEY CHECK(aadhar BETWEEN '100000000000' AND '999999999999'),
    name VARCHAR(60) NOT NULL,
    age SMALLINT CHECK (age >= 0),
    dob DATE NOT NULL,
    mobile CHAR(10) NOT NULL CHECK(mobile BETWEEN '1000000000' AND '9999999999'),
    address TEXT NOT NULL
);

INSERT INTO Person VALUES
	('123456789012', 'John Doe', 25, '1999-03-14', '9876543210', '12, Green Villa, MG Road, 680001'),
	('123456789013', 'Jane Smith', 28, '1996-06-11', '9867543211', '13, Sunshine, Church Road, 680002'),
	('123456789014', 'Mohammad Rizwan', 22, '2002-01-05', '9856543212', '14, Lakshmi Bhavan, Temple Road, 682001'),
	('123456789015', 'Amit Sharma', 24, '2000-05-17', '9846543213', '15, Roses, Hilltop Road, 682002'),
	('123456789016', 'Ravi Kumar', 21, '2003-12-10', '9836543214', '16, Oceanview, Seaside Road, 673001'),
	('123456789017', 'Sneha Verma', 23, '2001-04-09', '9826543215', '17, Breezy Cottage, Park Avenue, 673002'),
	('123456789018', 'Rohit Patel', 27, '1997-09-13', '9816543216', '18, Silver Nest, High Street, 676001'),
	('123456789019', 'Nina Nair', 29, '1995-11-22', '9806543217', '19, Pearl Mansion, College Road, 676002'),
	('123456789020', 'Vijay Menon', 24, '2000-02-28', '9796543218', '20, Lotus, Main Road, 688001'),
	('123456789021', 'Isha Rao', 26, '1998-07-15', '9786543219', '21, Maple House, Railway Road, 688002'),
	('123456789022', 'Deepak Jain', 23, '2001-10-08', '9776543220', '22, Jasmine, Market Street, 686001'),
	('123456789023', 'Lakshmi Iyer', 25, '1999-08-25', '9766543221', '23, Daffodil, Station Road, 686002')
;

-- 03
CREATE TABLE Guardian (
    guardian_mob CHAR(10) PRIMARY KEY,
    guardian_name VARCHAR(90) NOT NULL
);

INSERT INTO Guardian VALUES
	('9123456789', 'Kumar Nair'),
	('9123456790', 'Shiva Varma'),
	('9123456792', 'Vishnu Iyer'),
	('9123456795', 'Ram Mohan'),
	('9123456796', 'Kiran K'),
	('9123456799', 'Suresh N'),
	('9123456700', 'Suma M')
;

-- 02
CREATE TABLE Hosteller (
    aadhar CHAR(12) PRIMARY KEY,
    guardian_mob CHAR(10),
    join_date DATE NOT NULL,
    FOREIGN KEY (aadhar) REFERENCES Person(aadhar),
    FOREIGN KEY (guardian_mob) REFERENCES Guardian(guardian_mob)
);

INSERT INTO Hosteller VALUES
	('123456789012', '9123456789', '2021-06-01'),
	('123456789013', '9123456790', '2020-08-15'),
	('123456789015', '9123456792', '2019-12-12'),
	('123456789018', '9123456795', '2021-09-20'),
	('123456789019', '9123456796', '2020-11-25'),
	('123456789020', '9123456789', '2022-05-18'),
	('123456789022', '9123456799', '2019-10-30'),
	('123456789023', '9123456700', '2021-02-22')
;

-- 04
CREATE TABLE Staff (
    aadhar CHAR(12) PRIMARY KEY,
    role VARCHAR(50) NOT NULL,
    FOREIGN KEY (aadhar) REFERENCES Person(aadhar)
);

INSERT INTO Staff VALUES
    ('123456789014', 'Cook'),
    ('123456789016', 'Electrician'),
    ('123456789017', 'Plumber'),
    ('123456789021', 'Security')
;

-- 06
CREATE TABLE Room (
    Room_no CHAR(3) NOT NULL,
    building_no CHAR(1) NOT NULL,
    floor SMALLINT NOT NULL CHECK(floor BETWEEN 1 AND 3),
    bed_count SMALLINT CHECK (bed_count BETWEEN 1 AND 3),
    wifi_available BOOLEAN NOT NULL,
    bath_attached BOOLEAN NOT NULL,
    ac_available BOOLEAN NOT NULL,
    PRIMARY KEY (Room_no, building_no)
);

INSERT INTO Room VALUES
	('101', '1', 1, 3, TRUE, TRUE, TRUE),
	('102', '1', 1, 2, TRUE, TRUE, TRUE),
	('103', '1', 1, 3, TRUE, TRUE, TRUE),
	('104', '1', 1, 2, TRUE, TRUE, TRUE),
	('105', '1', 1, 3, TRUE, TRUE, TRUE),
	('106', '1', 1, 2, TRUE, TRUE, TRUE),
	('107', '1', 2, 3, TRUE, TRUE, TRUE),
	('108', '1', 2, 2, TRUE, TRUE, TRUE),
	('109', '1', 2, 3, TRUE, TRUE, TRUE),
	('110', '1', 2, 2, TRUE, TRUE, TRUE),
	('111', '1', 2, 3, TRUE, TRUE, TRUE),
	('112', '1', 2, 2, TRUE, TRUE, TRUE),
	('201', '2', 1, 3, TRUE, TRUE, TRUE),
	('202', '2', 1, 2, TRUE, TRUE, TRUE),
	('203', '2', 1, 3, TRUE, TRUE, TRUE),
	('204', '2', 1, 2, TRUE, TRUE, TRUE),
	('205', '2', 2, 3, TRUE, TRUE, TRUE),
	('206', '2', 2, 2, TRUE, TRUE, TRUE),
	('207', '2', 2, 3, TRUE, TRUE, TRUE),
	('208', '2', 2, 2, TRUE, TRUE, TRUE),
	('209', '2', 3, 3, TRUE, TRUE, TRUE),
	('210', '2', 3, 2, TRUE, TRUE, TRUE),
	('211', '2', 3, 3, TRUE, TRUE, TRUE),
	('212', '2', 3, 2, TRUE, TRUE, TRUE)

;

-- 07
CREATE TABLE Gets (
    aadhar CHAR(12) NOT NULL,
    room_no CHAR(3) NOT NULL,
    building_no CHAR(1) NOT NULL,
    PRIMARY KEY (aadhar),
    FOREIGN KEY (aadhar) REFERENCES Person(aadhar),
    FOREIGN KEY (room_no, building_no) REFERENCES Room(Room_no, building_no)
);

INSERT INTO Gets VALUES
	('123456789012', '101', '1'),
	('123456789013', '102', '1'),
	('123456789014', '103', '1'),
	('123456789015', '104', '1'),
	('123456789016', '105', '1'),
	('123456789017', '106', '1'),
	('123456789018', '201', '2'),
	('123456789019', '202', '2'),
	('123456789020', '203', '2'),
	('123456789021', '204', '2'),
	('123456789022', '205', '2')
;

-- 09
CREATE TABLE Bill_Issue (
    issue_date DATE PRIMARY KEY,
    due_date DATE NOT NULL
);

INSERT INTO Bill_Issue VALUES
	('2024-01-05', '2024-01-20'),
	('2024-02-10', '2024-02-25'),
	('2024-03-05', '2024-03-20'),
	('2024-04-10', '2024-04-25'),
	('2024-05-05', '2024-05-20'),
	('2024-06-10', '2024-06-25'),
	('2024-07-05', '2024-07-20'),
	('2024-08-10', '2024-08-25'),
	('2024-09-05', '2024-09-20'),
	('2024-10-10', '2024-10-25')
;

-- 08
CREATE TABLE Bill (
    Bill_no CHAR(8) PRIMARY KEY,
    amount DECIMAL(6,2) CHECK (amount >= 0),
    issue_date DATE NOT NULL,
    paid_date DATE,
    FOREIGN KEY (issue_date) REFERENCES Bill_Issue(issue_date)
);

INSERT INTO Bill VALUES
	('BIL001', 1500.00, '2024-01-05', '2024-01-18'),
	('BIL002', 1800.00, '2024-02-10', '2024-02-22'),
	('BIL003', 2000.00, '2024-03-05', '2024-03-28'),
	('BIL004', 1700.00, '2024-04-10', '2024-04-10'),
	('BIL005', 1900.00, '2024-05-05', '2024-05-17'),
	('BIL006', 2200.00, '2024-06-10', '2024-06-23'),
	('BIL007', 2100.00, '2024-07-05', '2024-07-29'),
	('BIL008', 2300.00, '2024-08-10', '2024-08-19'),
	('BIL009', 1600.00, '2024-09-05', '2024-09-23'),
	('BIL010', 2500.00, '2024-10-10', '2024-10-27')
;

-- 10
CREATE TABLE Pays (
    Bill_no CHAR(8) PRIMARY KEY,
    aadhar CHAR(12) NOT NULL,
    FOREIGN KEY (Bill_no) REFERENCES Bill(Bill_no),
    FOREIGN KEY (aadhar) REFERENCES Hosteller(aadhar)
);

INSERT INTO Pays (Bill_no, aadhar) VALUES
	('BIL001', '123456789012'),
	('BIL002', '123456789013'),
	('BIL003', '123456789015'),
	('BIL004', '123456789018'),
	('BIL005', '123456789019'),
	('BIL006', '123456789020'),
	('BIL007', '123456789022'),
	('BIL008', '123456789023')
;

-- 11
CREATE TABLE Complaint (
    Complaint_no CHAR(8) PRIMARY KEY,
    Date DATE NOT NULL,
    Status VARCHAR(8) CHECK (Status IN ('resolved', 'pending')),
    Message TEXT NOT NULL
);

INSERT INTO Complaint VALUES
	('CMP001', '2024-02-01', 'resolved', 'Wi-Fi not working in Room 101'),
	('CMP002', '2024-02-15', 'pending', 'AC malfunction in Room 202'),
	('CMP003', '2024-03-05', 'resolved', 'Leaky faucet in Room 302'),
	('CMP004', '2024-03-20', 'pending', 'Broken bed in Room 401'),
	('CMP005', '2024-04-10', 'resolved', 'Power outage in Building B'),
	('CMP006', '2024-04-25', 'pending', 'Bathroom drain clogged in Room 501'),
	('CMP007', '2024-05-10', 'resolved', 'No hot water in Room 102'),
	('CMP008', '2024-05-30', 'pending', 'Electrical issue in Room 301'),
	('CMP009', '2024-06-10', 'resolved', 'Wi-Fi down in Room 201'),
	('CMP010', '2024-06-25', 'pending', 'AC not cooling in Room 502')
;

-- 12
CREATE TABLE MessageType (
    Message TEXT PRIMARY KEY,
    type VARCHAR(20)
);

INSERT INTO MessageType VALUES
	('Wi-Fi not working in Room 101', 'Technical'),
	('AC malfunction in Room 202', 'Maintenance'),
	('Leaky faucet in Room 202', 'Plumbing'),
	('Broken bed in Room 111', 'Furniture'),
	('Power outage in Block B', 'Electrical'),
	('Bathroom drain clogged in Room 107', 'Plumbing'),
	('No hot water in Room 210', 'Plumbing'),
	('Electrical issue in Room 103', 'Electrical'),
	('Wi-Fi down in Room 200', 'Technical'),
	('AC not cooling in Room 109', 'Maintenance')
;

-- 13
CREATE TABLE Raises (
    Complaint_no CHAR(8) NOT NULL,
    aadhar CHAR(12) NOT NULL,
    PRIMARY KEY (Complaint_no),
    FOREIGN KEY (Complaint_no) REFERENCES Complaint(Complaint_no),
    FOREIGN KEY (aadhar) REFERENCES Hosteller(aadhar)
);

INSERT INTO Raises VALUES
	('CMP001', '123456789012'),
	('CMP002', '123456789013'),
	('CMP003', '123456789015'),
	('CMP004', '123456789018'),
	('CMP005', '123456789020'),
	('CMP006', '123456789022'),
	('CMP007', '123456789023'),
	('CMP008', '123456789013')
;

-- 14
CREATE TABLE Deals_with (
    Complaint_no CHAR(8) NOT NULL,
    aadhar CHAR(12) NOT NULL,
    PRIMARY KEY (Complaint_no),
    FOREIGN KEY (Complaint_no) REFERENCES Complaint(Complaint_no),
    FOREIGN KEY (aadhar) REFERENCES Staff(aadhar)
);

INSERT INTO Deals_with VALUES
	('CMP001', '123456789014'),
	('CMP002', '123456789014'),
	('CMP003', '123456789016'),
	('CMP004', '123456789017'),
	('CMP005', '123456789021'),
	('CMP006', '123456789017'),
	('CMP007', '123456789016'),
	('CMP008', '123456789021')
;

-- 15
CREATE TABLE Mess (
    Food_id CHAR(5) PRIMARY KEY,
    Food_name VARCHAR(90) NOT NULL,
    Food_type VARCHAR(90)
);

INSERT INTO Mess VALUES
	('F001', 'Idli','Breakfast'),
	('F002', 'Dosa','Breakfast'),
	('F003', 'Upma','Breakfast'),
	('F004', 'Rice and Curry','Lunch'),
	('F005', 'Chappati','Dinner'),
	('F006', 'Puri','Lunch'),
	('F007', 'Fried Rice','Lunch'),
	('F008', 'Biriyani','Lunch'),
	('F009', 'Pasta','Dinner'),
	('F010', 'Sandwich','Dinner')
;

-- 16
CREATE TABLE Attends (
    aadhar CHAR(12) NOT NULL,
    Food_id CHAR(5) NOT NULL,
    date_and_time TIMESTAMP NOT NULL,
    PRIMARY KEY (aadhar, Food_id),
    FOREIGN KEY (Food_id) REFERENCES Mess(Food_id),
    FOREIGN KEY (aadhar) REFERENCES Person(aadhar)
);

INSERT INTO Attends VALUES
	('123456789012', 'F001', '2024-01-01 08:00:00'),
	('123456789013', 'F002', '2024-01-01 08:30:00'),
	('123456789014', 'F003', '2024-01-02 08:00:00'),
	('123456789015', 'F004', '2024-01-02 12:30:00'),
	('123456789016', 'F005', '2024-01-03 13:00:00'),
	('123456789017', 'F006', '2024-01-03 13:30:00'),
	('123456789018', 'F007', '2024-01-04 12:00:00'),
	('123456789019', 'F008', '2024-01-04 12:30:00'),
	('123456789020', 'F009', '2024-01-05 19:00:00'),
	('123456789021', 'F010', '2024-01-05 19:30:00')
;

-- 17
CREATE TABLE Notice (
    notice_no CHAR(8) PRIMARY KEY,
    message VARCHAR(300) NOT NULL,
    date DATE NOT NULL
);

INSERT INTO Notice VALUES
	('NTC001', '123456789014', '2024-02-01'),
	('NTC002', '123456789014', '2024-02-01'),
	('NTC003', '123456789016', '2024-02-01'),
	('NTC004', '123456789017', '2024-02-01'),
	('NTC005', '123456789021', '2024-02-01'),
	('NTC006', '123456789017', '2024-02-01'),
	('NTC007', '123456789016', '2024-02-01'),
	('NTC008', '123456789021', '2024-02-01')
;

-- 18
CREATE TABLE Issues (
    notice_no CHAR(8) PRIMARY KEY,
    aadhar CHAR(12) NOT NULL,
    FOREIGN KEY (notice_no) REFERENCES Notice(notice_no),
    FOREIGN KEY (aadhar) REFERENCES Staff(aadhar)
);

INSERT INTO Issues VALUES
	('NTC001', '123456789014'),
	('NTC002', '123456789014'),
	('NTC003', '123456789014'),
	('NTC004', '123456789016'),
	('NTC005', '123456789021'),
	('NTC006', '123456789017'),
	('NTC007', '123456789014'),
	('NTC008', '123456789017')
;

-- 19
CREATE TABLE Login (
    username VARCHAR(50) PRIMARY KEY,
    person_type VARCHAR(10) NOT NULL CHECK(person_type IN ('staff', 'hosteller')),
    password VARCHAR(50) NOT NULL,
    last_login TIMESTAMP
);

INSERT INTO Login VALUES
	('john_doe', 'staff', 'password123', '2024-09-10 10:05:23'),
	('jane_smith', 'hosteller', 'pass456', '2024-09-09 09:35:45'),
	('mohammed_riz', 'staff', 'admin789', '2024-09-08 08:22:30'),
	('amit_sharma', 'staff', 'secure123', '2024-09-07 12:45:11'),
	('ravi_kumar', 'staff', 'staffpass', '2024-09-06 14:22:55'),
	('sneha_verma', 'hosteller', 'vermapass', '2024-09-05 07:50:02'),
	('rohit_patel', 'staff', 'patelsecure', '2024-09-04 06:11:12'),
	('nina_nair', 'hosteller', 'nairpass', '2024-09-03 18:34:47'),
	('vijay_menon', 'staff', 'menonpass', '2024-09-02 21:14:29'),
	('isha_rao', 'hosteller', 'raosecure', '2024-09-01 23:41:35'),
	('deepak_jain', 'staff', 'deepak123', '2024-08-31 08:11:05'),
	('lakshmi_iyer', 'hosteller', 'iyersecure', '2024-08-30 12:33:20')
;

-- 20
CREATE TABLE Access (
    aadhar CHAR(12) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    FOREIGN KEY (aadhar) REFERENCES Person(aadhar),
    FOREIGN KEY (username) REFERENCES Login(username)
);

INSERT INTO Access VALUES
	('123456789012', 'john_doe'),
	('123456789013', 'jane_smith'),
	('123456789014', 'mohammed_riz'),
	('123456789015', 'amit_sharma'),
	('123456789016', 'ravi_kumar'),
	('123456789017', 'sneha_verma'),
	('123456789018', 'rohit_patel'),
	('123456789019', 'nina_nair'),
	('123456789020', 'vijay_menon'),
	('123456789021', 'isha_rao'),
	('123456789022', 'deepak_jain'),
	('123456789023', 'lakshmi_iyer')
;

-- 05
CREATE TABLE Building (
    building_id SERIAL PRIMARY KEY,
    building_name VARCHAR(50) NOT NULL UNIQUE,
    total_rooms SMALLINT CHECK (total_rooms > 0)
);

-- Sample data entries for Building
INSERT INTO Building (building_name, total_rooms) VALUES
    ('A Block', 10),
    ('B Block', 15),
    ('C Block', 20);