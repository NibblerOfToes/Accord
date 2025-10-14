-- database: c:\Users\adamc\Desktop\hello-world\database\database.db

--CREATE TABLE users (
    userID INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    password TEXT
);

--CREATE TABLE classes (
    classID INTEGER PRIMARY KEY,
    subject TEXT,
    teacher TEXT
);

--CREATE TABLE userClasses (
    userID INTEGER,
    classID INTEGER,
    PRIMARY KEY (userID, classID),
    FOREIGN KEY (userID) REFERENCES users(userID),
    FOREIGN KEY (classID) REFERENCES classes(classID)
);

--CREATE TABLE messages (
    messageID INTEGER PRIMARY KEY,
    userID INTEGER,
    text TEXT,
    date TEXT,
    time TEXT,
    name TEXT,
    FOREIGN KEY (userID) REFERENCES users(userID)
);

--CREATE TABLE timetable (
    timetableID INTEGER PRIMARY KEY,
    classID INTEGER,
    class TEXT,
    period INTEGER,
    time TEXT,
    FOREIGN KEY (classID) REFERENCES classes(classID)
);

--INSERT INTO users (userID, name, email, password) VALUES
(1, 'Lena Marquez', 'lena.marquez@email.com', 'T!g3rWind92'),
(2, 'Darius Chen', 'darius.chen@email.com', 'Vx7$Moonlight'),
(3, 'Isabelle Thornton', 'isabelle.thornton@email.com', 'R3dFox!2025'),
(4, 'Mateo Rossi', 'mateo.rossi@email.com', 'Bl@zeC0ast88'),
(5, 'Aisha Campbell', 'aisha.campbell@email.com', 'S!lkShadow77'),
(6, 'Noah Takahashi', 'noah.takahashi@email.com', 'Qu!ckWave19'),
(7, 'Freya Lindström', 'freya.lindstrom@email.com', 'St@rrySky#6'),
(8, 'Jamal Rivers', 'jamal.rivers@email.com', 'D3epF!eld42'),
(9, 'Sophie Delgado', 'sophie.delgado@email.com', 'Gl!mm3rPath'),
(10, 'Eliot McAllister', 'eliot.mcallister@email.com', 'N!ghtFalcon73');

--INSERT INTO classes (classID, subject, teacher) VALUES
(1, 'Maths', 'Anna Ngo'),
(2, 'English', 'Amelia Lawson'),
(3, 'Science', 'Gabriel Guy'),
(4, 'PDHPE', 'Edmund Feng'),
(5, 'CPT', 'Benjamin Clark'),
(6, 'French', 'Arkady Dejong'),
(7, 'Food Technology', 'Julie Meissner'),
(8, 'Drama', 'Evelyn Harper'),
(9, 'Art', 'Thomas Nguyen'),
(10, 'Engineering', 'Priya Desai'),
(11, 'German', 'Marcus Bell'),
(12, 'Chinese', 'Clara Jensen'),
(13, 'Japanese', 'Leo Romano');

--INSERT INTO userClasses (userID, classID) VALUES
(1, 7), (1, 3), (1, 12), (1, 1), (1, 9), (1, 5),
(2, 11), (2, 2), (2, 8), (2, 13), (2, 6), (2, 4),
(3, 10), (3, 3), (3, 7), (3, 1), (3, 12), (3, 9),
(4, 6), (4, 2), (4, 11), (4, 8), (4, 5), (4, 13),
(5, 4), (5, 10), (5, 7), (5, 3), (5, 12), (5, 1),
(6, 9), (6, 6), (6, 2), (6, 11), (6, 8), (6, 5);

--INSERT INTO messages (messageID, userID, text, date, time, name) VALUES
(1, 4, 'Hey, just checking in—how’s everything going?', '2025-04-12', '09:47:00', 'Mateo Rossi'),
(2, 7, 'Can you send me the notes from class today?', '2025-05-03', '14:22:00', 'Freya Lindström'),
(3, 8, 'I’m running a bit late, sorry! Be there soon.', '2025-03-27', '18:05:00', 'Jamal Rivers'),
(4, 3, 'That movie last night was wild, we need to talk about it.', '2025-06-15', '11:36:00', 'Isabelle Thornton'),
(5, 1, 'Do you want to grab coffee after school tomorrow?', '2025-04-29', '08:13:00', 'Lena Marquez'),
(6, 6, 'I finally finished the project—remind me to show you.', '2025-05-21', '16:50:00', 'Noah Takahashi'),
(7, 5, 'You free this weekend? Thinking of doing something chill.', '2025-06-08', '10:04:00', 'Aisha Campbell'),
(8, 9, 'Lol I can’t believe that actually happened', '2025-03-30', '19:27:00', 'Eliot McAllister'),
(9, 2, 'Thanks again for helping me out earlier', '2025-04-18', '13:15:00', 'Darius Chen'),
(10, 10, 'I’ve been meaning to ask—how did your presentation go?', '2025-05-10', '17:42:00', 'Sophie Delgado'),
(11, 1, 'Let me know if you need anything, I’m around', '2025-06-01', '07:58:00', 'Lena Marquez'),
(12, 4, 'I saw something that reminded me of you today', '2025-04-05', '12:33:00', 'Mateo Rossi'),
(13, 7, 'Can’t stop thinking about that conversation we had', '2025-05-26', '15:09:00', 'Freya Lindström'),
(14, 3, 'You crushed it today, seriously', '2025-06-20', '20:45:00', 'Isabelle Thornton'),
(15, 8, 'Sorry if I seemed off earlier, just had a lot on my mind', '2025-03-22', '09:01:00', 'Jamal Rivers'),
(16, 5, 'We should hang out more, I miss talking to you', '2025-04-25', '18:30:00', 'Aisha Campbell'),
(17, 2, 'That playlist you sent? Fire.', '2025-05-14', '10:56:00', 'Darius Chen'),
(18, 10, 'I’m proud of you, even if you don’t hear it enough', '2025-06-11', '14:18:00', 'Sophie Delgado'),
(19, 6, 'Want to study together for the exam?', '2025-04-08', '08:39:00', 'Noah Takahashi'),
(20, 9, 'Just wanted to say hi—hope your day’s going okay', '2025-05-30', '11:11:00', 'Eliot McAllister');

--INSERT INTO timetable (timetableID, classID, class, period, time) VALUES
(1, 1, 'Maths', 4, '09:12:00'),
(2, 2, 'English', 2, '13:47:00'),
(3, 3, 'Science', 5, '10:05:00'),
(4, 4, 'PDHPE', 1, '11:33:00'),
(5, 5, 'CPT', 3, '12:18:00'),
(6, 6, 'French', 2, '09:59:00'),
(7, 7, 'Food Technology', 4, '13:04:00'),
(8, 8, 'Drama', 5, '10:42:00'),
(9, 9, 'Art', 1, '11:07:00'),
(10, 10, 'Engineering', 3, '12:55:00'),
(11, 11, 'German', 2, '09:26:00'),
(12, 12, 'Chinese', 5, '13:21:00'),
(13, 13, 'Japanese', 4, '10:16:00');

-- 1. Show all users
--SELECT * FROM users;

-- 2. Show all classes
--SELECT * FROM classes;

-- 3. Find which classes a specific user is taking
--SELECT subject
--FROM classes
--JOIN userClasses ON classes.classID = userClasses.classID
--WHERE userClasses.userID = 1;

-- 4. See all messages sent by a user
--SELECT text, date, time
--FROM messages
--WHERE userID = 4;

-- 5. View the timetable for a class
--SELECT subject, period, time
--FROM classes
--JOIN timetable ON classes.classID = timetable.classID
--WHERE classes.classID = 3;