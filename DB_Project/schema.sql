-- CAMPUS SOCIAL DATABASE - Team Info Hacker_2021331002_2021331006_2021331012
-- SQLite compatible version

-- USER TABLE
CREATE TABLE IF NOT EXISTS User (
    user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    password    VARCHAR(255) NOT NULL,
    role        VARCHAR(50)  NOT NULL,
    profile_pic VARCHAR(255)
);

-- POST TABLE
CREATE TABLE IF NOT EXISTS Post (
    post_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL,
    media_url VARCHAR(255),
    content   VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- COMMENT TABLE
CREATE TABLE IF NOT EXISTS Comment (
    comment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id      INTEGER NOT NULL,
    user_id      INTEGER NOT NULL,
    comment_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES Post(post_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- LIKES TABLE
-- (one like per user per post; enforce with UNIQUE)
CREATE TABLE IF NOT EXISTS Likes (
    like_id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES Post(post_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    UNIQUE(post_id, user_id)
);

-- MESSAGE TABLE
CREATE TABLE IF NOT EXISTS Message (
    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id  INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    content    TEXT NOT NULL,
    is_read    BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES User(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES User(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- RESOURCES TABLE
CREATE TABLE IF NOT EXISTS Resources (
    resource_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    file_url    VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- EVENTS TABLE
CREATE TABLE IF NOT EXISTS Events (
    event_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    event_date  DATE NOT NULL,
    image       VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
        ON UPDATE CASCADE ON DELETE CASCADE
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_post_user ON Post(user_id);
CREATE INDEX IF NOT EXISTS idx_likes_post ON Likes(post_id);
CREATE INDEX IF NOT EXISTS idx_likes_user ON Likes(user_id);
CREATE INDEX IF NOT EXISTS idx_comment_post ON Comment(post_id);
CREATE INDEX IF NOT EXISTS idx_message_sender ON Message(sender_id);
CREATE INDEX IF NOT EXISTS idx_message_receiver ON Message(receiver_id);

-- SAMPLE DATA
-- USERS (passwords are hashed using SHA-256)
INSERT OR IGNORE INTO User (name, email, password, role, profile_pic) VALUES
('Abdullah Rahman',  'abdullah500@gmail.com',  'c19944c0714bd49b5567ee99964ff25df4ab09354921bf7877ce59a46dc1c653',  'student', 'abdullah.jpg'),
('Zubayer Hossain',   'zubayer22@gmail.com',    'a1d061e5feef79bf7eea73a98fe603398ed515c323e9b7d896fa4cb9ba6d8728',    'student', 'zubayer.jpg'),
('Ishtiaque Zahid', 'ishtiaque-cse@sust.edu','cde383eee8ee7a4400adf7a15f716f179a2eb97646b37e089eb8d6d04e663416','teacher', 'Istiaque.png'),
('Tanzim Hasan',    'tanzimp6@gmail.com',  '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9',  'admin',   'admin.jpg');

-- POSTS
INSERT OR IGNORE INTO Post (user_id, media_url, content) VALUES
(1, 'images/post1.png', 'Excited for the new semester!'),
(2, NULL,               'Sharing slides for today''s DBMS lecture.'),
(3, 'images/post3.jpg', 'Anyone joining the coding contest this week?');

-- COMMENTS
INSERT OR IGNORE INTO Comment (post_id, user_id, comment_text) VALUES
(1, 3, 'Same here, can''t wait!'),
(2, 1, 'Thanks for the slides, very helpful.'),
(3, 2, 'I will be there as a judge!');

-- LIKES
INSERT OR IGNORE INTO Likes (post_id, user_id) VALUES
(1, 2),
(1, 3),
(3, 1);

-- MESSAGES
INSERT OR IGNORE INTO Message (sender_id, receiver_id, content, is_read) VALUES
(1, 2, 'Sir, could you please share the assignment details?', 0),
(2, 1, 'Sure, I have posted it in the course group.', 1),
(3, 1, 'Hi Alice, want to work together on the project?', 0);

-- RESOURCES
INSERT OR IGNORE INTO Resources (user_id, title, description, file_url) VALUES
(2, 'DBMS Lecture 1 Slides', 'Introduction to relational databases.', 'files/dbms_lec1.pdf'),
(2, 'ER Diagram Examples', 'Sample ER diagrams for practice.', 'files/er_examples.pdf'),
(4, 'Lab Rules', 'Guidelines for using the lab PCs.', 'files/lab_rules.docx');

-- EVENTS
INSERT OR IGNORE INTO Events (user_id, title, description, event_date, image) VALUES
(4, 'Welcome Orientation', 'Orientation for first year students.', '2025-01-10', 'images/orientation.jpg'),
(3, 'Coding Contest', 'Inter-university programming contest.', '2025-02-05', 'images/contest.png'),
(1, 'Study Group Meetup', 'Informal group study session for DBMS.', '2025-01-20', 'images/studygroup.jpg');
