import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self, db_name='data.db'):
        self.path = db_name
        self.create_database()

    def execute(self, query, args=()):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, args)
            conn.commit()
            return cursor
        
    def create_database(self):
        self.execute('''
            CREATE TABLE IF NOT EXISTS `players` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
                `username` TEXT UNIQUE NOT NULL,
                `email` TEXT UNIQUE NOT NULL, 
                `password` TEXT NOT NULL,
                `balance` INTEGER
            ) STRICT
        ''')
        self.execute('''
            CREATE TABLE IF NOT EXISTS `weapons` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                `name` TEXT,
                `price` INTEGER,
                `damage` INTEGER,
                `radius` INTEGER,
                `cool_down` INTEGER,
                `reach` INTEGER,
                `velocity` INTEGER,
                `motion_type` TEXT,
                `path` TEXT
            ) STRICT
        ''')
        self.execute('''
            CREATE TABLE IF NOT EXISTS `cosmetics` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                `name` TEXT,
                `price` INTEGER,
                `path` TEXT
            ) STRICT
        ''')
        self.execute('''
            CREATE TABLE IF NOT EXISTS `game_setup` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                `player_id` INTEGER REFERENCES `players`(`id`),
                `skin_id` INTEGER REFERENCES `cosmetics`(`id`),
                `id_weapon_1` INTEGER REFERENCES "weapons"(`id`), 
                `id_weapon_2` INTEGER REFERENCES "weapons"(`id`),
                `id_weapon_3` INTEGER REFERENCES "weapons"(`id`)
            ) STRICT
        ''')
        self.execute('''
            CREATE TABLE IF NOT EXISTS `player_cosmetics` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                `id_player` INTEGER REFERENCES `players`(`id`),
                `id_cosmetic` INTEGER REFERENCES `cosmetics`(`id`)
            ) STRICT
        ''')
        self.execute('''
            CREATE TABLE IF NOT EXISTS `player_weapons` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                `id_player` INTEGER REFERENCES `players`(`id`),
                `id_weapon` INTEGER REFERENCES `weapons`(`id`)
            ) STRICT
        ''')
        self.execute('''
            CREATE TABLE IF NOT EXISTS `friends` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                `id_player_a` INTEGER REFERENCES `players`(`id`),
                `id_player_b` INTEGER REFERENCES `players`(`id`)
            ) STRICT   
        ''')
    
    def add_player(self, username, email, password):
        self.execute('INSERT INTO players (username, email, password) VALUES (?, ?, ?)', (username, email, generate_password_hash(password)))
        player = self.login(email, password)
        player.balance = 0
        player.add_weapon(Weapon(0))
        player.add_weapon(Weapon(1))
        player.add_weapon(Weapon(2))
        player.add_cosmetic(Cosmetic(0))
        self.execute('INSERT INTO game_setup (player_id) VALUES ((SELECT id FROM players WHERE email = ?))', (email,))


    def login(self, email, password):
        user = self.execute('SELECT * FROM players WHERE email = ?', (email,)).fetchone()
        print(f'[DBG] from database.py.l93 :  {user=}')
        if user and check_password_hash(user[3], password):
            return Player(user[0])
        return -1

class Player:
    def __init__(self, id_):
        self.db = Database()
        self.id = id_
        self.inventory = []

    def __getittem__(self, key):
        return self.inventory[key]
    
    def __setitem__(self, key: int, value: "Weapon"):
        if not isinstance(value, Weapon):
            raise TypeError("Value must be a Weapon object")
            
        elif key not in range(3):
            raise ValueError("Key must be in range 0-2")
        elif value not in self.weapons:
            raise ValueError("Player does not have this weapon")
        else:
            self.inventory[key] = value
    @property
    def username(self):
        return self.db.execute('SELECT username FROM players WHERE id = ?', (self.id,)).fetchone()[0]

    @username.setter
    def username(self, username):
        self.db.execute('UPDATE players SET username = ? WHERE id = ?', (username, self.id))

    @property
    def mail(self):
        return self.db.execute('SELECT email FROM players WHERE id = ?', (self.id,)).fetchone()[0]
    
    @mail.setter
    def mail(self, email):
        self.db.execute('UPDATE players SET email = ? WHERE id = ?', (email, self.id))

    @property
    def balance(self):
        return self.db.execute('SELECT balance FROM players WHERE id = ?', (self.id,)).fetchone()[0]
    
    @balance.setter
    def balance(self, balance):
        self.db.execute('UPDATE players SET balance = ? WHERE id = ?', (balance, self.id))


    @property
    def weapons(self):
        return [Weapon(weapon[0]) for weapon in self.db.execute('SELECT id_weapon FROM player_weapons WHERE id_player = ?', (self.id,)).fetchall()]
    
    @property
    def cosmetics(self):
        return [Cosmetic(cosmetic[0]) for cosmetic in self.db.execute('SELECT id_cosmetic FROM player_cosmetics WHERE id_player = ?', (self.id,)).fetchall()]
    
    @property
    def friends(self):
        return [Player(friend[0]) for friend in self.db.execute('SELECT id_player_b FROM friends WHERE id_player_a = ?', (self.id,)).fetchall()]

    def add_friend(self, friend):
        self.db.execute('INSERT INTO friends (id_player_a, id_player_b) VALUES (?, ?)', (self.id, friend.id))

    def remove_friend(self, friend):
        self.db.execute('DELETE FROM friends WHERE id_player_a = ? AND id_player_b = ?', (self.id, friend.id))

    def add_weapon(self, weapon):
        self.db.execute('INSERT INTO player_weapons (id_player, id_weapon) VALUES (?, ?)', (self.id, weapon.id))
    
    def remove_weapon(self, weapon):
        self.db.execute('DELETE FROM player_weapons WHERE id_player = ? AND id_weapon = ?', (self.id, weapon.id))

    def add_cosmetic(self, cosmetic):
        self.db.execute('INSERT INTO player_cosmetics (id_player, id_cosmetic) VALUES (?, ?)', (self.id, cosmetic.id))

    def remove_cosmetic(self, cosmetic):
        self.db.execute('DELETE FROM player_cosmetics WHERE id_player = ? AND id_cosmetic = ?', (self.id, cosmetic.id))

    

class Cosmetic:
    def __init__(self, id_):
        self.db = Database()
        self.id = id_
    
    @property
    def name(self):
        return self.db.execute('SELECT name FROM cosmetics WHERE id = ?', (self.id,)).fetchone()[0]
    
    @name.setter
    def name(self, name):
        self.db.execute('UPDATE cosmetics SET name = ? WHERE id = ?', (name, self.id))

    @property
    def price(self):
        return self.db.execute('SELECT price FROM cosmetics WHERE id = ?', (self.id,)).fetchone()[0]
    
    @price.setter
    def price(self, price):
        self.db.execute('UPDATE cosmetics SET price = ? WHERE id = ?', (price, self.id))

    @property
    def path(self):
        return self.db.execute('SELECT path FROM cosmetics WHERE id = ?', (self.id,)).fetchone()[0]
    
    @path.setter
    def path(self, path):
        self.db.execute('UPDATE cosmetics SET path = ? WHERE id = ?', (path, self.id))

class Weapon:
    def __init__(self, id_):
        self.db = Database()
        self.id = id_
    
    @property
    def price(self):
        return self.db.execute('SELECT price FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @price.setter
    def price(self, price):
        self.db.execute('UPDATE weapons SET price = ? WHERE id = ?', (price, self.id))

    @property
    def amo(self):
        return self.db.execute('SELECT amo FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @amo.setter
    def amo(self, amo):
        self.db.execute('UPDATE weapons SET amo = ? WHERE id = ?', (amo, self.id))

    @property
    def cool_down(self):
        return self.db.execute('SELECT cool_down FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @cool_down.setter
    def cool_down(self, cool_down):
        self.db.execute('UPDATE weapons SET cool_down = ? WHERE id = ?', (cool_down, self.id))

    @property
    def reach(self):
        return self.db.execute('SELECT reach FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @reach.setter
    def reach(self, reach):
        self.db.execute('UPDATE weapons SET reach = ? WHERE id = ?', (reach, self.id))

    @property
    def velocity(self):
        return self.db.execute('SELECT velocity FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @velocity.setter
    def velocity(self, velocity):
        self.db.execute('UPDATE weapons SET velocity = ? WHERE id = ?', (velocity, self.id))

    @property
    def motion_type(self):
        return self.db.execute('SELECT motion_type FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @motion_type.setter
    def motion_type(self, motion_type):
        self.db.execute('UPDATE weapons SET motion_type = ? WHERE id = ?', (motion_type, self.id))


database = Database()