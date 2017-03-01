import json
import random

class Game:
    
    ## Constructor
    def __init__(self, user_id, word, cur_letters, game_over, num_lives, letters_guessed):
        self.user_id = user_id
        self.word = word
        self.lives = num_lives
        self.letters = [None if x == '_' else x for x in cur_letters]
        self.game_over = game_over
        self.letters_guessed = letters_guessed
        
    ## Reset the game with a new word
    def start_new_game(self):
        self.word = self.get_random_word()
        self.letters = [None for x in self.word]
        self.game_over = False
        self.lives = 10
        self.letters_guessed = ''
    
    ## Try a letter. Add it to letters list if it exists, if it doesn't
    ## decrement lives by 1. Update game status either way.
    def tryLetter(self, letter):
        if letter in self.word:
            for i, char in enumerate(self.word):
                if char == letter:
                    self.letters[i] = letter
            self.miss = False
        else:
            self.miss = True
            self.lives -= 1
            
        self.letters_guessed += letter
        self.updateState()
    
    ## Update game status members.
    def updateState(self):
        self.win = all([x != None for x in self.letters])
        self.game_over = self.win or self.lives < 1
            
    ## Serialize object to JSON.
    def serialize(self, removeWord=True):
        dct = self.__dict__
        
        # We only want to include the secret word IF the game is already
        # over. Otherwise user could cheat via looking at the request in dev
        # tools.
        if removeWord:
            dct['word'] = None
        
        return json.dumps(self.__dict__)
        
    ## Return a random english word
    def get_random_word(self):
        words = open('static/words.txt').readlines()
        rand_idx = random.randint(0, len(words))
        word = words[rand_idx]
        # words file has windows line breaks.
        if word.endswith('\n'):
            word = word[:-1]
        return word