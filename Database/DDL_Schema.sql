-- Create the UHCL Database

-- Reset database
DROP DATABASE IF EXISTS c438820fa01g1;
CREATE DATABASE c438820fa01g1;
USE c438820fa01g1;

SET foreign_key_checks = 0;
-- Drop tables for housekeeping
DROP TABLE IF EXISTS Student;
DROP TABLE IF EXISTS Class;
DROP TABLE IF EXISTS Course;
DROP TABLE IF EXISTS Enroll;
DROP TABLE IF EXISTS MajorProgram;
DROP TABLE IF EXISTS MinorProgram;
DROP TABLE IF EXISTS Faculty;
DROP TABLE IF EXISTS MajorCourses;
DROP TABLE IF EXISTS MinorCourses;
DROP TABLE IF EXISTS Requisite;
DROP TABLE IF EXISTS LoginInfo;
DROP TABLE IF EXISTS Date;
DROP TABLE IF EXISTS College;

-- Create new tables
CREATE TABLE IF NOT EXISTS College (
	Code				CHAR(3) NOT NULL,
	Name				VARCHAR(42) NOT NULL,
	CONSTRAINT			PK_College PRIMARY KEY (Code),
	CONSTRAINT			CK_College_Name UNIQUE (Name)
);

CREATE TABLE IF NOT EXISTS Course (
	CourseID			INT NOT NULL,
	CourseSubject		CHAR(4) NOT NULL,
	CourseNumber		INT(4) NOT NULL,
	Name				VARCHAR(80) NOT NULL,
	Credits				TINYINT(1) NOT NULL,
	CONSTRAINT			PK_Course PRIMARY KEY (CourseID),
	CONSTRAINT			CK_Course_Name UNIQUE (Name)
);

CREATE TABLE IF NOT EXISTS MajorProgram (
	MajorID				CHAR(4) NOT NULL,
	Name				VARCHAR(64) NOT NULL,
	CreditsRequired		INT(3) NOT NULL,
	College				CHAR(3)NOT NULL,
	Plan				VARCHAR(128) NOT NULL,	
	CONSTRAINT			PK_Major PRIMARY KEY (MajorID),
	CONSTRAINT			FK_Major_College FOREIGN KEY (College)
		REFERENCES		College(Code) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT			CK_Major UNIQUE (Name)
);

CREATE TABLE IF NOT EXISTS MinorProgram (
	MinorID				CHAR(4) NOT NULL,
	Name				VARCHAR(64) NOT NULL,
	CreditsRequired		INT(3) NOT NULL,
	College				CHAR(3) NOT NULL,
	Plan				VARCHAR(128) NOT NULL,
	CONSTRAINT			PK_Minor PRIMARY KEY (MinorID),
	CONSTRAINT			FK_Minor_College FOREIGN KEY (College)
		REFERENCES		College(Code) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT			CK_Minor UNIQUE (Name)	
);

CREATE TABLE IF NOT EXISTS Faculty (
	FacultyID			INT NOT NULL,
	FName				VARCHAR(35) NOT NULL,
	LName				VARCHAR(35) NOT NULL,
	Email				VARCHAR(45) NOT NULL,
	Phone				VARCHAR(12) NOT NULL,
	Office				VARCHAR(6) NOT NULL,
	Bio					VARCHAR(128) NOT NULL,
	CONSTRAINT			PK_Faculty PRIMARY KEY (FacultyID)
);

CREATE TABLE IF NOT EXISTS MajorCourses (
	MajorID				CHAR(4) NOT NULL,
	CourseID			INT NOT NULL,
	CONSTRAINT			PK_MajorCourses PRIMARY KEY (MajorID, CourseID),
	CONSTRAINT			FK_MajorCourses_Major FOREIGN KEY (MajorID)
		REFERENCES		MajorProgram(MajorID) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT			FK_MajorCourses_Courses FOREIGN KEY (CourseID)
		REFERENCES		Course(CourseID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS MinorCourses (
	MinorID				CHAR(4) NOT NULL,
	CourseID			INT NOT NULL,
	CONSTRAINT			PK_MinorCourses PRIMARY KEY (MinorID, CourseID),
	CONSTRAINT			FK_MinorCourses_Minor FOREIGN KEY (MinorID)
		REFERENCES		MinorProgram(MinorID) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT			FK_MinorCourses_Courses FOREIGN KEY (CourseID)
		REFERENCES		Course(CourseID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Requisite (
	CourseID			INT NOT NULL,
	RequisiteID			INT NOT NULL,
	Requirement			CHAR(14) NOT NULL,
	CONSTRAINT			PK_Requisite PRIMARY KEY (CourseID, RequisiteID),
	CONSTRAINT			FK_Requisite_Course FOREIGN KEY (CourseID)
		REFERENCES		Course(CourseID) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT			FK_Requisite_Requisite FOREIGN KEY (RequisiteID)
		REFERENCES		Course(CourseID) ON DELETE CASCADE ON UPDATE CASCADE    
);

CREATE TABLE IF NOT EXISTS Date (
	DateID				INT NOT NULL,				
	Name				VARCHAR(64) NOT NULL,
	Date				DATE NOT NULL,
	Description			VARCHAR(64) NOT NULL,
	CONSTRAINT			PK_Date PRIMARY KEY (DateID)
);

CREATE TABLE IF NOT EXISTS Student (
	StudentID			INT NOT NULL,
	FName				VARCHAR(35) NOT NULL,
	LName				VARCHAR(35) NOT NULL,
	Email				VARCHAR(45),
	CreditsTaken		INT(3) DEFAULT 0,
	Major				VARCHAR(4),
	Minor				VARCHAR(4),
	CONSTRAINT			PK_Student PRIMARY KEY (StudentID),
	CONSTRAINT			FK_Student_Major FOREIGN KEY (Major)
		REFERENCES		MajorProgram(MajorID),
	CONSTRAINT			FK_Student_Minor FOREIGN KEY (Minor)
		REFERENCES		MinorProgram(MinorID)
);

CREATE TABLE IF NOT EXISTS Class (
	ClassID				INT NOT NULL,
	CourseID			INT NOT NULL,
	Day					VARCHAR(15) NOT NULL,
	StartTime			TIME NOT NULL,
    EndTime				TIME NOT NULL,
    Semester			VARCHAR(6) NOT NULL,
	Session				VARCHAR(30) NOT NULL,
	InstructorID		INT NOT NULL,
	Building			VARCHAR(20) NOT NULL,
	Room				VARCHAR(6),
	CONSTRAINT			PK_Class PRIMARY KEY (ClassID),
	CONSTRAINT			FK_Class_Course FOREIGN KEY (CourseID)
		REFERENCES		Course(CourseID) ON DELETE CASCADE ON UPDATE CASCADE,
	CONSTRAINT			FK_Class_Instructor FOREIGN KEY (InstructorID)
		REFERENCES		Faculty(FacultyID)
);

CREATE TABLE IF NOT EXISTS Enroll (
	StudentID			INT NOT NULL,
	ClassID				INT NOT NULL,
	CONSTRAINT			PK_Enroll PRIMARY KEY (StudentID, ClassID),
	CONSTRAINT			FK_Enroll_Student FOREIGN KEY (StudentID)
		REFERENCES		Student(StudentID) ON DELETE CASCADE ON UPDATE CASCADE,	
	CONSTRAINT			FK_Enroll_Class FOREIGN KEY (ClassID)
		REFERENCES		Class(ClassID) ON DELETE CASCADE ON UPDATE CASCADE		
);

CREATE TABLE IF NOT EXISTS LoginInfo (
	StudentID			INT NOT NULL,
	Password			VARCHAR(32) NOT NULL,
	CONSTRAINT			PK_Login PRIMARY KEY (StudentID),
	CONSTRAINT			FK_Login_Student FOREIGN KEY (StudentID)
		REFERENCES		Student(StudentID) ON DELETE CASCADE ON UPDATE CASCADE
);
-- Populate tables with values
INSERT INTO Student VALUES
	(0000000, 'Guest', 'User', NULL, NULL, NULL, NULL),
	(1794794, 'John', 'Naisbitt', 'NaisbittJ4859@UHCL.edu', 121, 'ITEC', 'CSEC'),
    (1594057, 'Richard', 'Fly', 'FlyR7169@UHCL.edu', 120, 'ITEC', 'CSEC'),
	(1132784, 'Jane', 'Doe', 'DoeJ5763@UHCL.edu', 65, 'CSCI', NULL),
    (1535670, 'Thy', 'Le', 'LeP3495@uhcl.edu', 120, 'ITEC', 'CSEC');
INSERT INTO Class VALUES
	(21842, 9000, 'Mo', '19:00:00', '21:50:00', 'Fall', 'Regular Academic Section', 1000, 'Delta Building', 'D241'),
	(21844, 9000, 'Tu', '19:00:00', '21:50:00', 'Fall', 'Regular Academic Section', 1000, 'Delta Building', 'D242'),
	(21819, 9003, 'Mo', '16:00:00', '18:50:00', 'Fall', 'Regular Academic Section', 1005, 'Delta Building', 'D201'),
	(21808, 9006, 'We', '13:00:00', '15:50:00', 'Fall', 'Regular Academic Section', 1002, 'Online', NULL),
	(27219, 9004, 'We', '16:00:00', '18:50:00', 'Fall', 'Regular Academic Section', 1002, 'Delta Building', 'D204'),
	(27218, 9008, 'Th', '16:00:00', '18:50:00', 'Fall', 'Regular Academic Section', 1002, 'Online', NULL),
	(26317, 9005, 'We', '16:00:00', '18:50:00', 'Fall', 'Regular Academic Section', 1004, 'Online', NULL),
	(21823, 9009, 'We', '19:00:00', '21:50:00', 'Fall', 'Regular Academic Section', 1005, 'Delta Building', 'D201'),
	(21827, 9001, 'Mo', '19:00:00', '21:50:00', 'Fall', 'Regular Academic Section', 1005, 'Delta Building', 'D201'),
	(27244, 9011, 'Mo', '19:00:00', '21:50:00', 'Fall', 'Regular Academic Section', 1002, 'Online', NULL),
	(21834, 9018, 'We', '16:00:00', '18:50:00', 'Fall', 'Regular Academic Section', 1006, 'Delta Building' , 'D242'),
	(21837, 9013, 'We', '16:00:00', '18:50:00', 'Fall', 'Regular Academic Section', 1005, 'Delta Building' , 'D201'),
	(21840, 9002, 'Tu', '19:00:00', '21:50:00', 'Fall', 'Regular Academic Section', 1001, 'Online', NULL),
	(21694, 8000, 'TuTh', '10:00:00', '11:50:00', 'Fall', 'Regular Academic Section', 1007, 'Online', NULL),
	(21702, 8000, 'TuTh', '11:30:00', '13:20:00', 'Fall', 'Regular Academic Section', 1008, 'Delta Building', 'D202'),
	(21703, 8001, 'TuTh', '10:00:00', '11:50:00', 'Fall', 'Regular Academic Section', 1001, 'Online', NULL),
	(21705, 8001, 'TuTh', '13:00:00', '14:50:00', 'Fall', 'Regular Academic Section', 1001, 'Online', NULL),
	(21706, 8003, 'TuTh', '11:30:00', '12:50:00', 'Fall', 'Regular Academic Section', 1011, 'Delta Building', 'D241'),
	(21708, 8003, 'TuTh', '16:00:00', '17:20:00', 'Fall', 'Regular Academic Section', 1001, 'Online', NULL),
	(28358, 8003, 'TuTh', '10:00:00', '11:20:00', 'Fall', 'Regular Academic Section', 1011, 'Delta Building', 'D241'),
	(21712, 8002, 'Tu', '13:00:00', '15:50:00', 'Fall', 'Regular Academic Section', 1003, 'Online', NULL),
	(21736, 8005, 'MoWe', '13:00:00', '14:20:00', 'Fall', 'Regular Academic Section', 1010, 'Online', NULL),
	(21738, 8005, 'MoWe', '16:00:00', '17:20:00', 'Fall', 'Regular Academic Section', 1010, 'Online', NULL),
	(21741, 8010, 'Mo', '16:00:00', '18:50:00', 'Fall', 'Regular Academic Section', 1006, 'Delta Building', 'D136'),
	(21849, 8008, 'Mo', '19:00:00', '21:50:00', 'Fall', 'Regular Academic Section', 1000, 'Delta Building', 'D241'),
	(21850, 8008, 'Tu', '19:00:00', '21:50:00', 'Fall', 'Regular Academic Section', 1000, 'Delta Building', 'D242'),
	(21739, 8007, 'TuTh', '17:30:00', '18:50:00', 'Fall', 'Regular Academic Section', 1008, 'Delta Building', 'D202');
INSERT INTO Course VALUES
	(9000, 'ITEC', 4388, 'Senior Project in Information Technology', 3),
    (9001, 'ITEC', 3388, 'Cyber Security 1', 3),
    (9002, 'ITEC', 4383, 'Cyber Security 2', 3),
	(9003, 'ITEC', 2381, 'Forensic Fundamentals', 3),
	(9004, 'ITEC', 2313, 'Scripting 1', 3),
	(9005, 'ITEC', 3335, 'Database Development', 3),
	(9006, 'ITEC', 1310, 'Introduction to Information Technology', 3),
	(9007, 'ITEC', 3312, 'Scripting 2', 3),
	(9008, 'ITEC', 2351, 'Web Fundamentals', 3),
	(9009, 'ITEC', 3365, 'Network Fundamentals', 3),
	(9010, 'ITEC', 4313, 'Emerging Information Technology', 3),
	(9011, 'ITEC', 4342, 'IT Project Management', 3),
	(9012, 'ITEC', 4379, 'Internship or Approved Elective', 3),
	(9013, 'ITEC', 4381, 'Computer Forensics', 3),
	(9014, 'ITEC', 4382, 'Registry & Internet Forensics', 3),
	(9015, 'ITEC', 4351, 'Web Design', 3),
	(9016, 'ITEC', 4352, 'Backend Web Development', 3),
	(9017, 'ITEC', 4335, 'Database Administration', 3),
	(9018, 'ITEC', 4365, 'Network Administration', 3),
	(9019, 'ITEC', 4366, 'Computer Security and Disaster Recovery', 3),
	(8000, 'CSCI', 1470, 'Computer Science 1', 4),
	(8001, 'CSCI', 1471, 'Computer Science 2', 4),
	(8002, 'CSCI', 2331, 'Computer Organization and Assembly Language', 3),
	(8003, 'CSCI', 2315, 'Data Structures', 3),
	(8004, 'CSCI', 3352, 'Advanced Data Structures and Algorithms', 3),
	(8005, 'CSCI', 4333, 'Design of Database Systems', 3),
	(8006, 'CSCI', 3321, 'Numerical Methods', 3),
	(8007, 'CSCI', 4354, 'Operating Systems', 3),
	(8008, 'CSCI', 4388, 'Senior Project in Computer Science', 3),
	(8009, 'CSCI', 3311, 'Programming with Visual Basic', 3),
	(8010, 'CSCI', 4364, 'Computer Systems Administration', 3),
	(1100, 'CRIM', 4330, 'Criminal Investigation', 3),
	(5000, 'ARTS', 2371, 'Digital Photography', 3),
	(5001, 'ARTS', 3360, 'Graphic Design', 3),
    (2000, 'CHEM', 1311, 'General Chemistry', 3),
    (2001, 'CHEM', 1111, 'General Chemistry Lab', 1),
    (3000, 'MATH', 2305, 'Discrete Math', 3),
    (3001, 'MATH', 2318, 'Linear Algebra', 3),
    (3002, 'MATH', 2414, 'Calculus 2', 3),
    (3003, 'MATH', 2320, 'Differential Equations', 3),
    (3004, 'MATH', 2413, 'Calculus 1', 3),
	(1000, 'STAT', 3334, 'Probability and Statistics for Scientists & Engineers', 3),
    (1001, 'STAT', 3334, 'Computational Statistics', 3),
    (6000, 'CENG', 2312, 'Digital Circuits', 3),
    (6001, 'CENG', 2112, 'Digital Circuits Lab', 1),
    (6002, 'CENG', 3331, 'Introduction to Telecommunications and Networks', 3),
    (6003, 'CENG', 3131, 'Introduction to Telecommunications and Networks Lab', 3),
    (6004, 'CENG', 3351, 'Computer Architecture', 3),
    (6005, 'CENG', 3351, 'Computer Architecture Lab', 1),
    (4000, 'SWEN', 4342, 'Software Engineering', 3),
    (0000, 'WRIT', 3315, 'Advanced Technical Writing', 3);
INSERT INTO Enroll VALUES
	(1794794, 21844),
	(1794794, 21819),
	(1794794, 21736),
	(1132784, 21849),
	(1132784, 21736),
	(1132784, 21741),
	(1132784, 21739),
    (1535670, 21844);
INSERT INTO MajorProgram VALUES
	('ITEC', 'Information Technology', 120, 'CSE', 'https://www.uhcl.edu/academics/degrees/documents/cse/wbs-informationtechnology.pdf'),
    ('CINF', 'Computer Information Systems', 120, 'CSE', 'https://www.uhcl.edu/academics/degrees/documents/cse/wbs-computerinformationsystems.pdf'),
	('CSCI', 'Computer Science', 120, 'CSE', 'https://www.uhcl.edu/academics/degrees/documents/cse/wbs-computerscience.pdf'),
    ('MENG', 'Mechanical Engineering', 120, 'CSE', 'https://www.uhcl.edu/academics/degrees/documents/cse/wbs-mechanical-engineering.pdf');
INSERT INTO MinorProgram VALUES
	('CSEC', 'Cyber Security', 15, 'CSE', 'https://catalog.uhcl.edu/current/undergraduate/degrees-and-programs/minors/cybersecurity-minor');
INSERT INTO Faculty VALUES
	(1000, 'Alfredo', 'Perez-Davila', 'perezd@uhcl.edu', '281-283-3863', 'D167', 'https://www.uhcl.edu/science-engineering/faculty/perez-davila-alfredo'),
	(1001, 'Charles', 'Phillips', 'phillips@uhcl.edu', '281-283-3837', 'B3128', 'https://www.uhcl.edu/science-engineering/faculty/phillips-charles'),
	(1002, 'Lisa', 'Lacher', 'lacher@uhcl.edu', '281-283-3885', 'D161', 'https://www.uhcl.edu/science-engineering/faculty/lacher-lisa'),
	(1003, 'Hisham', 'Al-Mubaid', 'hisham@uhcl.edu', '281-283-3802', 'D168', 'https://www.uhcl.edu/science-engineering/faculty/al-mubaid'),
	(1004, 'Khondker', 'Hasan', 'hasank@uhcl.edu', '281-283-3842', 'D224', 'https://www.uhcl.edu/science-engineering/faculty/khondker-hasan'),
	(1005, 'Joshua', 'Baker', 'bakerjo@uhcl.edu', '281-283-3887', 'D227', 'https://www.uhcl.edu/science-engineering/faculty/baker-josh'),
	(1006, 'Krishani', 'Abeysekera', 'abeysekera@uhcl.edu', '281-283-3831', 'D165', 'https://www.uhcl.edu/science-engineering/faculty/abeysekera-krishani'),
	(1007, 'Sadegh', 'Davari', 'davari@uhcl.edu', '281-283-3865', 'D153', 'https://www.uhcl.edu/science-engineering/faculty/davari-sadegh'),
	(1008, 'Sharon', 'Hall', 'perkins@uhcl.edu', '281-283-3868', 'D115', 'https://www.uhcl.edu/science-engineering/faculty/hall-sharon'),
	(1009, 'Wei', 'Wei', 'wei@uhcl.edu', '281-283-3732', 'D175', 'https://www.uhcl.edu/science-engineering/faculty/wei-wei'),
	(1010, 'Bun', 'Yue', 'yue@uhcl.edu', '281-283-3864', 'D163', 'https://www.uhcl.edu/science-engineering/faculty/yue-bun'),
	(1011, 'Ahmed', 'Abukmail', 'abukmail@uhcl.edu', '281-283-3888', 'D169', 'https://www.uhcl.edu/science-engineering/faculty/abukmail-ahmed');
INSERT INTO MajorCourses VALUES
	('ITEC', 9000),
    ('ITEC', 9001),
	('ITEC', 9003),
	('ITEC', 9004),
	('ITEC', 9005),
	('ITEC', 9006),
	('ITEC', 9007),
	('ITEC', 9008),
	('ITEC', 9009),
	('ITEC', 9010),
	('ITEC', 9011),
	('ITEC', 9012),
	('ITEC', 9013),
	('ITEC', 9014),
	('ITEC', 9015),
	('ITEC', 1100),
	('ITEC', 5000),
	('ITEC', 5001),
	('ITEC', 9016),
    ('ITEC', 0000),
	('CSCI', 8000),
	('CSCI', 8001),
	('CSCI', 8002),
	('CSCI', 8003),
	('CSCI', 8004),
	('CSCI', 8005),
	('CSCI', 8006),
	('CSCI', 8007),
	('CSCI', 8008),
	('CSCI', 8009),
	('CSCI', 8010),
    ('CSCI', 0000),
	('CSCI', 2000),
    ('CSCI', 2001),
    ('CSCI', 3000),
    ('CSCI', 3001),
    ('CSCI', 3002),
    ('CSCI', 3003),
    ('CSCI', 1000),
    ('CSCI', 6000),
    ('CSCI', 6001),
    ('CSCI', 6002),
    ('CSCI', 6003),
    ('CSCI', 6004),
    ('CSCI', 6005),
    ('CSCI', 4000);
INSERT INTO MinorCourses VALUES
	('CSEC', 9001),
    ('CSEC', 9002),
	('CSEC', 8000),
	('CSEC', 8001),
	('CSEC', 9019);
INSERT INTO Requisite VALUES
	(9002, 9001, 'Prerequisite'),
    (9007, 9004, 'Prerequisite'),
	(9005, 9007, 'Prerequisite'),
	(9001, 9009, 'Prerequisite'),
	(9001, 8001, 'Prerequisite'),
	(9017, 9005, 'Prerequisite'),
	(9011, 9007, 'Prerequisite'),
	(9015, 9008, 'Prerequisite'),
	(9016, 9015, 'Prerequisite'),
	(9016, 9005, 'Prerequisite'),
	(9018, 9009, 'Prerequisite'),
	(9013, 9003, 'Prerequisite'),
	(9014, 9003, 'Prerequisite'),
    (8001, 8000, 'Prerequisite'),
	(8003, 8001, 'Prerequisite'),
	(8002, 8001, 'Prerequisite'),
	(8002, 3004, 'Prerequisite'),
	(8006, 3001, 'Prerequisite'),
	(8006, 3002, 'Prerequisite'),
	(8006, 8001, 'Prerequisite'),
	(8004, 8003, 'Prerequisite'),
	(8004, 3000, 'Prerequisite'),
	(8004, 3002, 'Prerequisite'),
	(8005, 8003, 'Prerequisite'),
	(8007, 8003, 'Prerequisite'),
	(8007, 8002, 'Prerequisite'),
	(8007, 6004, 'Corequisite'),
	(8010, 8003, 'Prerequisite'),
	(8008, 8004, 'Prerequisite'),
	(8008, 4000, 'Prerequisite');
INSERT INTO LoginInfo VALUES
	(1794794, 'secret'),
    (1594057, 'test123'),
    (1132784, 'test123'),
	(1535670, 'password');
INSERT INTO Date VALUES
	(10, 'Drop Date Fall 2020', '2020-11-09', 'Last day to Drop/Withdraw'),
    (11, 'Last Class Day Fall 2020 Regular Session', '2020-12-05', 'Last day of classes'),
    (12, 'Early Registration Open Spring 2021', '2020-11-02', 'Early registration begins for Spring 2021'),
    (13, 'Early Registration Close Spring 2021', '2020-11-12', 'Early registration ends for Spring 2021'),
    (14, 'End of Fall 2020 Semester', '2020-12-12', 'Official Closing of Fall Semester'),
    (15, 'Payment Deadline 1 Fall 2020', '2020-8-21', 'Due date for payment installment 1'),
    (16, 'Payment Deadline 2 Fall 2020', '2020-9-24', 'Due date for payment installment 2'),
    (17, 'Payment Deadline 3 Fall 2020', '2020-10-26', 'Due date for payment installment 3'),
    (18, 'Payment Deadline 4 Fall 2020', '2020-11-24', 'Due date for payment installment 4');
	
INSERT INTO College VALUES
	('CSE', 'College of Science and Engineering'),
    ('BUS', 'College of Business'),
    ('EDU', 'College of Education'),
    ('HSH', 'College of Human Sciences and Humanities');