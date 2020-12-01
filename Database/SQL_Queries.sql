-- display courses from a specific major
SELECT DISTINCT concat(co.coursenumber, ' ', co.coursesubject) as Course, co.Name
FROM course co, majorprogram mp, majorcourses mc
WHERE co.courseid = mc.courseid
AND mp.majorid = mc.majorid
AND mp.majorid = 'CSCI';

-- display courses from a specific minor
SELECT DISTINCT concat(co.coursenumber, ' ', co.coursesubject) as Course, co.Name
FROM course co, minorprogram mp, minorcourses mc
WHERE co.courseid = mc.courseid
AND mp.minorid = mc.minorid
AND mp.minorid = 'CSEC';

-- display classes that contain a keyword
SELECT DISTINCT c.Classid, co.Name, c.Day, c.StartTime, c.EndTime, c.Semester, c.Session, concat(f.FName, ' ', f.LName) as Instructor, c.Building, c.Room
FROM class c, course co, faculty f
WHERE c.instructorid = f.facultyid
AND c.courseid = co.courseid
AND co.name LIKE '%Cyber%';

-- display prerequisite courses for a course with a keyword
SELECT DISTINCT concat(co1.coursenumber, ' ', co1.coursesubject) as 'Desired Course ID', co1.Name AS 'Desired Course Name', concat(co2.coursenumber, ' ', co2.coursesubject) as 'Requisite Course ID', co2.Name as 'Requisite Course Name', r.requirement as 'Pre/Co'
FROM course co1, course co2, requisite r
WHERE co1.courseID = r.courseID
AND co2.courseID = r.requisiteID
AND co1.name LIKE '%Cyber Security%';

-- show drop dates
SELECT DISTINCT d.name, d.date, d.description
FROM date d
WHERE name LIKE '%Deadline%';

-- show credit hours taken
SELECT DISTINCT concat(s.fname, ' ', s.lname) AS Student, s.CreditsTaken
FROM student s
WHERE s.studentID = 1794794;

-- show degree plan of student
SELECT DISTINCT concat(s.major, ' ', ma.name) as Major, concat(s.minor, ' ', mi.name) as Minor
FROM student s, majorprogram ma, minorprogram mi
WHERE s.studentID = 1794794
AND s.major = ma.majorid
AND s.minor = mi.minorid;

-- show all degree plans
SELECT ID, Name, Type
FROM
(SELECT DISTINCT ma.majorid as ID, ma.Name, 'Major' as Type
FROM majorprogram ma
UNION
SELECT DISTINCT mi.minorid as ID, mi.Name, 'Minor' as Type
FROM minorprogram mi) degrees;

-- show student enrollment
SELECT DISTINCT c.Classid, co.Name
FROM class c, course co, faculty f, enroll e
WHERE c.instructorid = f.facultyid
AND c.courseid = co.courseid
AND e.classid = c.classid
AND e.studentid = '1794794';

-- show student major
SELECT DISTINCT concat(s.major, ' ', ma.name) as Major
FROM student s, majorprogram ma
WHERE s.studentID = 1794794
AND s.major = ma.majorid;

-- show student minor
SELECT DISTINCT concat(s.minor, ' ', mi.name) as Minor
FROM student s, minorprogram mi
WHERE s.studentID = 1794794
AND s.minor = mi.minorid;

-- show course names that match input course number
SELECT DISTINCT concat(co.coursesubject, ' ', co.coursenumber, ' ', co.name) as Course
FROM course co
WHERE co.coursenumber LIKE '%4388%'
AND co.coursesubject LIKE '%ITEC%';

-- show course names that are similar to user input
SELECT DISTINCT concat(co.coursesubject, ' ', co.coursenumber, ' ', co.name) as Course
FROM course co
WHERE co.coursenumber LIKE '%4388%'
OR co.coursesubject LIKE '%ITEC%';