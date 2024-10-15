"""
database.py

The database works with sqlite3 to store the game data. The database is created
if it does not exist and the tables are created if they do not exist. The database
contains tables for players, weapons, cosmetics, game setup, player cosmetics, player
weapons, and friends. The tables are created with the STRICT keyword to enforce strict
data types.

The passwords are hashed using the werkzeug.security module. The Database class contains

This file contains the Database class and the Player, Weapon, and Cosmetic classes.
The Database class is used to interact with the database, while the Player, Weapon,
and Cosmetic classes are used to represent the data stored in the database.

The Database class contains methods to execute queries on the database, create the
database tables, add a player, and login a player.

The Player class represents a player in the game. It has properties for the player's
username, email, balance, weapons, cosmetics, and friends. It also has methods to add
and remove friends, weapons, and cosmetics.

The Weapon class represents a weapon in the game. It has properties for the weapon's
price, amo, cool_down, reach, velocity, and motion_type.

The Cosmetic class represents a cosmetic item in the game. It has properties for the
cosmetic's name, price, and path.
"""
from __future__ import annotations

import sqlite3 # sqlite3 is a built-in module in Python that allows you to interact with SQLite databases
from werkzeug.security import generate_password_hash, check_password_hash # werkzeug.security is a module that provides password hashing utilities

class Database:
    """
    The Database class is used to interact with the database. It contains methods to execute queries on the database,
    create the database tables, add a player, and login a player.
    
    Attributes:
    - path:str - The path to the database file

    Methods:
    - execute(query:str, args:tuple) -> sqlite3.Cursor - Executes a query on the database
    - create_database() - Creates the database tables
    - add_player(username:str, email:str, password:str) - Adds a player to the database
    - login(email:str, password:str) -> Player - Logs in a player and returns the Player object
    """
    def __init__(self, db_name:str='data.db') -> None:
        """
        The constructor for the Database class. It initializes the path attribute with the path to the database file
        and creates the database tables.
        
        Parameters:
        - db_name:str - The path to the database file
        """
        self.path:str = db_name
        self.create_database()

    def execute(self, query:str, args:tuple=tuple()) -> sqlite3.Cursor:
        """
        Executes a query on the database.

        ## Arguments:
        - query:str - The SQL query to execute
        - args:tuple - The arguments to pass to the query

        ## Returns:
        - sqlite3.Cursor - The cursor object

        WARNING: This method is vulnerable to SQL injection attacks. You should use parameterized queries to prevent SQL injection.
        SELECT * FROM players WHERE id = 1 should be SELECT * FROM players WHERE id = ? and (1,) should be passed as the args parameter.
        """
        with sqlite3.connect(self.path) as conn: # open a contex manager for extra safety
            cursor = conn.cursor() # create a cursor object
            cursor.execute(query, args) # execute the query
            conn.commit() # commit the changes to the database
            return cursor # return the cursor object
        
    def create_database(self):
        """
        Creates the database tables if they do not exist
        
        The tables created are:

        - players: Contains the player data
        - weapons: Contains the weapon data
        - cosmetics: Contains the cosmetic data
        - game_setup: Contains the game setup data
        - player_cosmetics: Contains the player cosmetics data
        - player_weapons: Contains the player weapons data
        - friends: Contains the friend

        The tables are created with the STRICT keyword to enforce strict data types.

        The players table contains the following columns:
        - id: The player's ID
        - username: The player's username
        - email: The player's email
        - password: The player's password
        - balance: The player's balance
        
        The weapons table contains the following columns:
        - id: The weapon's ID
        - name: The weapon's name
        - price: The weapon's price
        - damage: The weapon's damage
        - radius: The weapon's radius
        - cool_down: The weapon's cool down
        - reach: The weapon's reach
        - velocity: The weapon's velocity
        - motion_type: The weapon's motion type

        The cosmetics table contains the following columns:
        - id: The cosmetic's ID
        - name: The cosmetic's name
        - price: The cosmetic's price

        The game_setup table contains the following columns:
        - id: The game setup's ID
        - player_id: The player's ID
        - skin_id: The skin's ID
        - id_weapon_1: The ID of the player's first weapon
        - id_weapon_2: The ID of the player's second weapon
        - id_weapon_3: The ID of the player's third weapon

        The player_cosmetics table contains the following columns:
        - id: The player cosmetic's ID
        - id_player: The player's ID
        - id_cosmetic: The cosmetic's ID

        The player_weapons table contains the following columns:
        - id: The player weapon's ID
        - id_player: The player's ID
        - id_weapon: The weapon's ID

        The friends table contains the following columns:
        - id: The friend's ID
        - id_player_a: The ID of player A
        - id_player_b: The ID of player B
        """

        # Create the table players if it does not exist
        self.execute('''
            CREATE TABLE IF NOT EXISTS `players` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
                `username` TEXT UNIQUE NOT NULL,
                `email` TEXT UNIQUE NOT NULL, 
                `password` TEXT NOT NULL,
                `balance` INTEGER
            ) STRICT
        ''')

        # Create the table weapons if it does not exist
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

        # Create the table cosmetics if it does not exist
        self.execute('''
            CREATE TABLE IF NOT EXISTS `cosmetics` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                `name` TEXT,
                `price` INTEGER,
                `path` TEXT
            ) STRICT
        ''')

        # Create the table game_setup if it does not exist
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

        # Create the table player_cosmetics if it does not exist
        self.execute('''
            CREATE TABLE IF NOT EXISTS `player_cosmetics` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                `id_player` INTEGER REFERENCES `players`(`id`),
                `id_cosmetic` INTEGER REFERENCES `cosmetics`(`id`)
            ) STRICT
        ''')

        # Create the table player_weapons if it does not exist
        self.execute('''
            CREATE TABLE IF NOT EXISTS `player_weapons` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                `id_player` INTEGER REFERENCES `players`(`id`),
                `id_weapon` INTEGER REFERENCES `weapons`(`id`)
            ) STRICT
        ''')

        # Create the table friends if it does not exist
        self.execute('''
            CREATE TABLE IF NOT EXISTS `friends` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                `id_player_a` INTEGER REFERENCES `players`(`id`),
                `id_player_b` INTEGER REFERENCES `players`(`id`)
            ) STRICT   
        ''')
    
    def add_player(self, username:str, email:str, password:str) -> None:
        """
        Adds a player to the database
        
        ## Arguments:
        - username:str - The player's username
        - email:str - The player's email
        - password:str - The player's password
        """
        # add the player to the players table
        self.execute('INSERT INTO players (username, email, password) VALUES (?, ?, ?)', (username, email, generate_password_hash(password)))
        # get the player's ID
        player = self.login(email, password)
        # add the player's weapons to the player_weapons table
        player.balance = 0
        player.add_weapon(Weapon(0, self))
        player.add_weapon(Weapon(1, self))
        player.add_weapon(Weapon(2, self))

        # add the player's cosmetics to the player_cosmetics table
        player.add_cosmetic(Cosmetic(0, self))

        # ? add the player to the game_setup table
        self.execute('INSERT INTO game_setup (player_id) VALUES ((SELECT id FROM players WHERE email = ?))', (email,))
        print(f'[DBG] from database.py.Database.add_player : {player=}')
        print(f'[DBG] from database.py.Database.add_player : players={self.execute("SELECT * FROM players").fetchall()}')

    def login(self, email:str, password:str) -> 'Player'|int:
        """ 
        Logs in a player and returns the Player object

        ## Arguments:
        - email:str - The player's email
        - password:str - The player's password

        ## Returns:
        - Player - The Player object associated with the given email and password
        - int - -1 if the email and password do not match
        """

        user = self.execute('SELECT * FROM players WHERE email = ?', (email,)).fetchone()
        print(f'[DBG] from database.py.Database.login :  {user=}')
        if user and check_password_hash(user[3], password):
            return Player(user[0], self)
        return -1

class Player:
    """
    The Player class represents a player in the game. It has properties for the player's
    username, email, balance, weapons, cosmetics, and friends. It also has methods to add
    and remove friends, weapons, and cosmetics.
    
    ## Attributes:
    - db:Database - The Database object
    - id:int - The player's ID
    - inventory:list - The player's inventory
    
    ## Properties
    - username:str - The player's username
    - mail:str - The player's email
    - balance:int - The player's balance
    - weapons:list - The player's weapons
    - cosmetics:list - The player's cosmetics
    - friends:list - The player's friends

    ## Methods
    - add_friend(friend:Player) - Adds a friend to the player's friends list
    - remove_friend(friend:Player) - Removes a friend from the player's friends list
    - add_weapon(weapon:Weapon) - Adds a weapon to the player's inventory
    - remove_weapon(weapon:Weapon) - Removes a weapon from the player's inventory
    - add_cosmetic(cosmetic:Cosmetic) - Adds a cosmetic to the player's inventory

    """
    def __init__(self, id_:int, database:Database) -> None:
        """
        The constructor for the Player class. It initializes the db attribute with a Database object
        and the id attribute with the player's ID.

        ## Arguments:
        - id_:int - The player's ID
        """
        self.db = database
        self.id = id_
        self.inventory:list["Weapon"] = []

    def __getittem__(self, key: int) -> "Weapon":
        if key not in range(3):
            raise ValueError("Key must be in range 0-2")
        return self.inventory[key]
    
    def __setitem__(self, key: int, value: "Weapon") -> None:
        if not isinstance(value, Weapon):
            raise TypeError("Value must be a Weapon object")
        elif key not in range(3):
            raise ValueError("Key must be in range 0-2")
        elif value not in self.weapons:
            raise ValueError("Player does not have this weapon")
        else:
            self.inventory[key] = value

    @property
    def username(self) -> str:
        return self.db.execute('SELECT username FROM players WHERE id = ?', (self.id,)).fetchone()[0]

    @username.setter
    def username(self, username:str) -> None:
        self.db.execute('UPDATE players SET username = ? WHERE id = ?', (username, self.id))

    @property
    def mail(self) -> str:
        return self.db.execute('SELECT email FROM players WHERE id = ?', (self.id,)).fetchone()[0]
    
    @mail.setter
    def mail(self, email:str) -> None:
        self.db.execute('UPDATE players SET email = ? WHERE id = ?', (email, self.id))

    @property
    def balance(self) -> int:
        return self.db.execute('SELECT balance FROM players WHERE id = ?', (self.id,)).fetchone()[0]
    
    @balance.setter
    def balance(self, balance:int) -> None:
        self.db.execute('UPDATE players SET balance = ? WHERE id = ?', (balance, self.id))


    @property
    def weapons(self) -> list["Weapon"]:
        return [Weapon(weapon[0], self.db) for weapon in self.db.execute('SELECT id_weapon FROM player_weapons WHERE id_player = ?', (self.id,)).fetchall()]
    
    @property
    def cosmetics(self) -> list["Cosmetic"]:
        return [Cosmetic(cosmetic[0], self.bd) for cosmetic in self.db.execute('SELECT id_cosmetic FROM player_cosmetics WHERE id_player = ?', (self.id,)).fetchall()]
    
    @property
    def friends(self) -> list["Player"]:
        return [Player(friend[0], self.bd) for friend in self.db.execute('SELECT id_player_b FROM friends WHERE id_player_a = ?', (self.id,)).fetchall()]

    def add_friend(self, friend: 'Player') -> None:
        self.db.execute('INSERT INTO friends (id_player_a, id_player_b) VALUES (?, ?)', (self.id, friend.id))

    def remove_friend(self, friend: 'Player') -> None:
        self.db.execute('DELETE FROM friends WHERE id_player_a = ? AND id_player_b = ?', (self.id, friend.id))

    def add_weapon(self, weapon: 'Weapon') -> None:
        self.db.execute('INSERT INTO player_weapons (id_player, id_weapon) VALUES (?, ?)', (self.id, weapon.id))
    
    def remove_weapon(self, weapon: 'Weapon') -> None:
        self.db.execute('DELETE FROM player_weapons WHERE id_player = ? AND id_weapon = ?', (self.id, weapon.id))

    def add_cosmetic(self, cosmetic: 'Cosmetic') -> None:
        self.db.execute('INSERT INTO player_cosmetics (id_player, id_cosmetic) VALUES (?, ?)', (self.id, cosmetic.id))

    def remove_cosmetic(self, cosmetic: 'Cosmetic') -> None:
        self.db.execute('DELETE FROM player_cosmetics WHERE id_player = ? AND id_cosmetic = ?', (self.id, cosmetic.id))

    

class Cosmetic:
    """
    The Cosmetic class represents a cosmetic item in the game. It has properties for the
    cosmetic's name, price, and path.
    
    ## Attributes:
    - db:Database - The Database object
    - id:int - The cosmetic's ID
    
    ## Properties:
    - name:str - The cosmetic's name
    - price:int - The cosmetic's price
    
    ## Methods:
    - __init__(id_:int) - The constructor for the Cosmetic class
    """

    def __init__(self, id_:int, database:Database) -> None:
        self.db =database
        self.id = id_
    
    @property
    def name(self) -> str:
        return self.db.execute('SELECT name FROM cosmetics WHERE id = ?', (self.id,)).fetchone()[0]
    
    @name.setter
    def name(self, name:str) -> None:
        self.db.execute('UPDATE cosmetics SET name = ? WHERE id = ?', (name, self.id))

    @property
    def price(self) -> int:
        return self.db.execute('SELECT price FROM cosmetics WHERE id = ?', (self.id,)).fetchone()[0]
    
    @price.setter
    def price(self, price:int) -> None:
        self.db.execute('UPDATE cosmetics SET price = ? WHERE id = ?', (price, self.id))

    @property
    def path(self) -> str:
        return self.db.execute('SELECT path FROM cosmetics WHERE id = ?', (self.id,)).fetchone()[0]
    
    @path.setter
    def path(self, path:str) -> None:
        self.db.execute('UPDATE cosmetics SET path = ? WHERE id = ?', (path, self.id))

class Weapon:
    """
    The Weapon class represents a weapon in the game. It has properties for the weapon's
    price, amo, cool_down, reach, velocity, and motion_type.
    
    ## Attributes:
    - db:Database - The Database object
    - id:int - The weapon's ID
    
    ## Properties:
    - price:int - The weapon's price
    - amo:int - The weapon's amo
    - cool_down:int - The weapon's cool down
    - reach:int - The weapon's reach
    - velocity:int - The weapon's velocity
    - motion_type:str - The weapon's motion type
    
    ## Methods:
    - __init__(id_:int) - The constructor for the Weapon class
    """
    def __init__(self, id_:int, database:Database) -> None:
        self.db = database
        self.id = id_
    
    @property
    def price(self) -> int:
        return self.db.execute('SELECT price FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @price.setter
    def price(self, price:int) -> None:
        self.db.execute('UPDATE weapons SET price = ? WHERE id = ?', (price, self.id))

    @property
    def amo(self) -> int:
        return self.db.execute('SELECT amo FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @amo.setter
    def amo(self, amo:int) -> None:
        self.db.execute('UPDATE weapons SET amo = ? WHERE id = ?', (amo, self.id))

    @property
    def cool_down(self) -> int:
        return self.db.execute('SELECT cool_down FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @cool_down.setter
    def cool_down(self, cool_down:int) -> None:
        self.db.execute('UPDATE weapons SET cool_down = ? WHERE id = ?', (cool_down, self.id))

    @property
    def reach(self) -> int:
        return self.db.execute('SELECT reach FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @reach.setter
    def reach(self, reach:int) -> None:
        self.db.execute('UPDATE weapons SET reach = ? WHERE id = ?', (reach, self.id))

    @property
    def velocity(self) -> int:
        return self.db.execute('SELECT velocity FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @velocity.setter
    def velocity(self, velocity:int) -> None:
        self.db.execute('UPDATE weapons SET velocity = ? WHERE id = ?', (velocity, self.id))

    @property
    def motion_type(self) -> str:
        return self.db.execute('SELECT motion_type FROM weapons WHERE id = ?', (self.id,)).fetchone()[0]
    
    @motion_type.setter
    def motion_type(self, motion_type:str) -> None:
        self.db.execute('UPDATE weapons SET motion_type = ? WHERE id = ?', (motion_type, self.id))


