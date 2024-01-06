DELETE FROM messages;
DELETE FROM chats;
DELETE FROM users;

INSERT INTO users(id, username, pass_hash, salt) VALUES
(1, 'Tarnished', decode('123ABC', 'hex'), convert_to('salt', 'utf-8')),
(2, 'Radahn', decode('123ABC', 'hex'), convert_to('salt', 'utf-8')),
(3, 'Malenia', decode('123ABC', 'hex'), convert_to('salt', 'utf-8')),
(4, 'Melina', decode('123ABC', 'hex'), convert_to('salt', 'utf-8')),
(5, 'Morgott', decode('123ABC', 'hex'), convert_to('salt', 'utf-8'));

ALTER SEQUENCE users_id_seq RESTART 6;

INSERT INTO chats(id, chatname) VALUES
(1, 'Erdtree Sanctuary'),
(2, 'Grand Study Hall'),
(3, 'Radahns Battlefield');

ALTER SEQUENCE chats_id_seq RESTART 4;

INSERT INTO messages(id, user_id, chat_id, message, edited, timestamp) VALUES
(1, 5, 1, 'Fools emboldened by the flame of ambition.', False, '2012-7-17 10:00:00'),
(2, 1, 1, 'My brother in Marika you wear rags and you call yourself "King".', False, '2012-7-17 10:00:10'),
(3, 1, 1, '*Bodies Morgott*', False, '2012-7-17 10:03:00'),
(4, 5, 1, 'Literally how. Nah he hacking get him out.', False, '2012-7-17 10:03:15'),
(5, 1, 1, 'L Bozo + mad + skill issue + golden order fell off + go back to the sewers', False, '2012-7-17 10:03:20'),
(6, 2, 3, 'GRARARRHRHHRHHR', False, '2012-7-23 13:00:00'),
(7, 1, 3, 'Bro why is he growling. Ur not him', False, '2012-7-23 13:00:05'),
(8, 2, 3, 'GUH!!!', False, '2012-7-23 13:02:12'),
(9, 1, 3, '*Bodies Radahn*', False, '2012-7-23 13:05:32'),
(10, 1, 3, 'Imagine learning gravity magic just to be beat by a guy with a stick.', False, '2012-7-23 13:05:45');

ALTER SEQUENCE messages_id_seq RESTART 11;
