import sqlite3 as lite
import pdb
from game import Game

## Constants
DB_NAME = 'hangman.db'
GET_GAME_QUERY = 'SELECT * FROM Games WHERE user_id = (?)'
ADD_GAME_QUERY = 'INSERT INTO Games VALUES (?, ?, ?, ?, ?, ?)'
UPDATE_GAME_QUERY =  '''
    UPDATE Games SET 
        word = ?,
        letters = ?,
        status = ?,
        lives = ?,
        guessed_letters = ?
    WHERE user_id = ?
    '''
UPDATE_WINS = 'UPDATE Users SET Wins = ? WHERE username = ?'
UPDATE_LOSSES = 'UPDATE Users SET Losses = ? WHERE username = ?'
GET_RECORD = 'SELECT Wins, Losses FROM Users WHERE username = ?'
ADD_USER = 'INSERT INTO Users VALUES (?, ?, 0, 0)'
GET_USER = 'SELECT * FROM Users WHERE username = ?'

## Initialize database
def create():
    with lite.connect(DB_NAME) as con:
        cmd = open('SQL/Create.sql').read()
        con.executescript(cmd)
    
## Retrieve a game by ID.
def get_game(user_id):
    with lite.connect(DB_NAME) as con:
        cursor = con.cursor()
        row = cursor.execute(GET_GAME_QUERY, [user_id]).fetchone()
    
        if not row:
            # Create an entry in the Game table for this user.
            # We just stub out the values for now, the /newgame 
            # request will actually set everything.
            g = Game(user_id, None, [], True, 10, '')
            save_game(g)
            return g
        else:
            (wins, losses) = get_stats(user_id)
            return create_game(row, wins, losses)
    
## Convert dbRow -> Game object
def create_game(row, wins, losses):
    user_id = row[0]
    word = row[1]
    cur_letters = string_to_letters(row[2])
    status = bit_to_status(row[3])
    lives = row[4]
    guessed_letters = row[5]
   
    game = Game(user_id, word, cur_letters, status, lives, guessed_letters)
    game.wins = wins
    game.losses = losses
    
    return game
    
## Get a users stats
def get_stats(user_id):
    with lite.connect(DB_NAME) as con:
        cursor = con.cursor()
        row = cursor.execute(GET_RECORD, [user_id]).fetchone()
        return (row[0], row[1])


## Insert a new game.
def save_game(game):
    with lite.connect(DB_NAME) as con:
        cursor = con.cursor()
        
        status = status_to_bit(game.game_over)
        letters = letters_to_string(game.letters)
        params = (game.user_id, game.word, letters, status, game.lives, game.letters_guessed)
        
        cursor.execute(ADD_GAME_QUERY, params)
        con.commit()
        
## Update a user's game
def update_game(game):
    with lite.connect(DB_NAME) as con:
        cursor = con.cursor()
        
        status = status_to_bit(game.game_over)
        letters = letters_to_string(game.letters)
        params = (game.word, letters, status, game.lives, game.letters_guessed, game.user_id)
        
        cursor.execute(UPDATE_GAME_QUERY, params)
        con.commit()
        
## Update a users wins or losses.
def update_record(user_id, num, win):
    with lite.connect(DB_NAME) as con:
        cursor = con.cursor()
        params = (num, user_id)
        if win:
            cursor.execute(UPDATE_WINS, params)
        else:
            cursor.execute(UPDATE_LOSSES, params)
        
## Return username & password from username
def get_user(username):
    with lite.connect(DB_NAME) as con:
        cursor = con.cursor()
        
        cursor.execute(GET_USER, (username,))
        res = cursor.fetchone()
        
        if not res:
            return None
            
        return (res[0], res[1])
        
## Return username & password from username. In a production application,
## passwords should be halt.
def add_user(username, password):
    with lite.connect(DB_NAME) as con:
        cursor = con.cursor()
        existingUser = get_user(username)
        
        if not existingUser:
            params = (username, password)
            cursor.execute(ADD_USER, params)
            return True
        else:
            return False
            
            
## Helper functions for converting SQL to python types. ##

def letters_to_string(letters):
    return ''.join([x if x != None else '_' for x in letters])
    
def status_to_bit(status):
    return 1 if status else 0
    
def bit_to_status(bit):
    return True if bit == 1 else False 
    
def string_to_letters(string):
    return ['_' if x == None else x for x in string]
    
# Convert dbRow -> Game object
def create_game(row, wins, losses):
    user_id = row[0]
    word = row[1]
    cur_letters = string_to_letters(row[2])
    status = bit_to_status(row[3])
    lives = row[4]
    guessed_letters = row[5]
   
    game = Game(user_id, word, cur_letters, status, lives, guessed_letters)
    game.wins = wins
    game.losses = losses
    
    return game
 