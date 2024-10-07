# Microtroopers

A game in python, made to learn about server-client relation in a web socket protocol.

This game is a derivative of whorms.

## Basics

The player begin with a login to the server.
If he has an auto login on his device, he lands on the home page, else, he has to login or signup into the game.

Then, the server check for any updates, and modifications to the game files.

If needed, the server may order a download of the missings or broken parts of the game.

This may took a while, since all the assets must be checked.

If the server cannot be found, the app will show the player the link of the github page where he can report any incidents or bugs.

The player is in his own page, where he can see his stats, his cosmetics, his status and his datas.

He has some options available from this main menu:

1. Play
2. Shop
3. Settings
4. Inventory

### 1. Play

This feature is the core of the game.

Base on the game [whorms](https://en.wikipedia.org/wiki/Worms_(series)), it keep the purpose of shoot at others on a 2D destructible map, but, instead of a turn-to-turn game, this one will be a real time game, where all players can play simultanously.

The play button puts the player on a file, which is used to creates lobbies with 2, 4 or 6 players.

In teams or in solo mode, the main goal is either to kill of to make fall all the enemies under the void that's under the map

The player can control your character's motion with your keyboard (WASD), and the aiming and shooting with his mouse.

There is some objects that the player can own, and some will be added if I am still motivated.

*A beginner account will only have a gun, and will need to purchase new weapons.*

there are the objects:

1. Gun : Fast reload, small damage, small reach
2. Shotgun : Medium reload, high damage at short distance, medium reach
3. Sniper : Slow reload, high damage, long reach
4. RPG : Slow reload, high damage, also damage the terrain
5. Buildings : 5 in inventory (use wisely), add a protection layer
6. ? LandMines ?
7. ? Drill ?

Amo, shields, heal and building materials will randomly spawn onto the map.

The winner (or the winnng team) is the last to stay alive.

A kill grant the player some coins, and a soul.

The player can use souls to buy collectibles, and coins to buy and upgrade weapons.

Here are the coin chart:

| Action                     | Coins earned                                                 |
| -------------------------- | ------------------------------------------------------------ |
| Kill players in a game     | 25 + (25*number of kills)                                    |
| Win a game                 | 25                                                           |
| Lose a game                | 5                                                            |
| Randomly spawning in lobby | 2~5                                                          |
| In free offers             | 2~30 (The chances are getting lower the higher the prize is) |

### 2. Shop

The shop is a place where the player can find offers to buy collectibles, weapons, and ?some perks?

All the offers are availlable in coins or in souls (no real monney)

The offers will be reset daily, and it will be the same for all the players.

### 3. Settings

In this place, the player can modify his in-game settings:

| Setting         | Default value      | Available value      |
| --------------- | ------------------ | -------------------- |
| Direction keys  | WASD/ZQSD (French) | Any keys             |
| In game options | `<esc>`          | Na                   |
| Use item        | `<left click>`   | Any key/mouse button |
| Aiming          | Mouse              | Na                   |
| Zoom +/-        | Mouse wheel        | Na                   |
| Select item     | digit keys         | Any keys             |

The player can also set his username, his icon, his pseudo color, and manage his account settings.

### 4. Inventory

The player can see here all the items he owns, and he can upgrade and equip some weapons.

## Server

The server is a multithreading program that can handle players connexions, host games, and manage shop.

### Player connexion

When the player tries to connect, the server will check into its database many things:

Is this player banned ?

Does the player need an update or a re-download ?

If the player is banned, the used wi-fi will be added to the blacklist, and the connexion will be canceled.

If the player needs an update, or a re-download, the server will ask the client if he consents to a download, and will launch the download.

Then, the server will create a thread for the player, which will handle his main page.

### Shop managing

The shop is managed by a json file, listed in a database.

the database check which offers each player bought, in order to prevent overbuying or claiming twice the same offer.

### Game hosting

Each game is host in a single thread, which can holp up to 6 players.

The thread will handle the input events, the outputs, the updates of the map, and the random spawn of AMOs, build, shield and heal


### Server logic

start

wait for players

infinite:

get inputs

handle input

return data (positions and explosions)

:

close connections

end

## Also

the server will have a sqlite database to handle connections and manage passwords and ownership of cosmetics.

the game will be clock base and not fps based. 

the player will always be at the center of ths screen

## Modules

pygame
sys
os
pillow
pytmx
pyscroll
sockets
threading
sqlite
requests
dataclasses

