CREATE DATABASE IF NOT EXISTS studentdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS studentdb.students (
  id INT PRIMARY KEY AUTO_INCREMENT,
  student_id VARCHAR(10),
  fullname VARCHAR(100),
  dob DATE,
  major VARCHAR(50)
);
-- Synthetic demonstration records; repeatable without deleting existing records.
INSERT INTO studentdb.students (student_id, fullname, dob, major)
SELECT 'DEMO001', 'Nguyễn Minh An', '2003-01-12', 'Information Technology'
WHERE NOT EXISTS (SELECT 1 FROM studentdb.students WHERE student_id = 'DEMO001');
INSERT INTO studentdb.students (student_id, fullname, dob, major)
SELECT 'DEMO002', 'Trần Bảo Bình', '2003-05-20', 'Software Engineering'
WHERE NOT EXISTS (SELECT 1 FROM studentdb.students WHERE student_id = 'DEMO002');
INSERT INTO studentdb.students (student_id, fullname, dob, major)
SELECT 'DEMO003', 'Lê Ngọc Chi', '2003-09-08', 'Computer Science'
WHERE NOT EXISTS (SELECT 1 FROM studentdb.students WHERE student_id = 'DEMO003');
