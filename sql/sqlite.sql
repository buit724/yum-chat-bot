CREATE TABLE user (
    id INTEGER PRIMARY KEY,
    display_name TEXT NOT NULL
);

CREATE table game (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL
);

CREATE TABLE moment (
	id INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	description TEXT NOT NULL,
	game_id INTEGER,
	start_time TEXT NOT NULL,
	end_time TEXT NOT NULL,
	
	FOREIGN KEY(game_id) REFERENCES game(id) ON DELETE CASCADE
);

CREATE TABLE user_moment_assoc (
	id INTEGER PRIMARY KEY,
	user_id INTEGER NOT NULL,
	moment_id INTEGER NOT NULL,
	claimed_time TEXT NOT NULL,
	
	FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
	FOREIGN KEY(moment_id) REFERENCES moment(id) ON DELETE CASCADE
);