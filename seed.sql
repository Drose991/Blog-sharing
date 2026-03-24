INSERT INTO users (username, email) VALUES
('ali', 'ali@mail.com'),
('ayse', 'ayse@mail.com'),
('mehmet', 'mehmet@mail.com'),
('zeynep', 'zeynep@mail.com'),
('can', 'can@mail.com'),
('elif', 'elif@mail.com'),
('mert', 'mert@mail.com'),
('sena', 'sena@mail.com'),
('burak', 'burak@mail.com'),
('derya', 'derya@mail.com');

INSERT INTO categories (name) VALUES
('Technology'),
('Education'),
('Travel'),
('Health'),
('Sports'),
('Music'),
('Science'),
('Food'),
('Lifestyle'),
('Business');

INSERT INTO blogs (user_id, category_id, title, content) VALUES
(1, 1, 'Flask Basics', 'Introduction to Flask framework.'),
(2, 2, 'Study Tips', 'Useful tips for studying efficiently.'),
(3, 3, 'Trip to Norway', 'My travel experience in Norway.'),
(4, 4, 'Healthy Living', 'How to stay healthy every day.'),
(5, 5, 'Football News', 'Latest football updates.'),
(6, 6, 'Learning Guitar', 'Beginner guide for guitar.'),
(7, 7, 'Space Discoveries', 'Recent discoveries in space.'),
(8, 8, 'Best Pasta Recipe', 'Easy and delicious pasta recipe.'),
(9, 9, 'Daily Routine', 'A productive daily routine.'),
(10, 10, 'Startup Ideas', 'Simple startup ideas for students.');

INSERT INTO comments (blog_id, user_id, content) VALUES
(1, 2, 'Great post!'),
(2, 3, 'Very helpful, thanks.'),
(3, 4, 'Nice travel story.'),
(4, 5, 'Good advice.'),
(5, 6, 'Interesting update.'),
(6, 7, 'I want to learn too.'),
(7, 8, 'Amazing topic.'),
(8, 9, 'Looks delicious.'),
(9, 10, 'Very relatable.'),
(10, 1, 'Nice business ideas.');
