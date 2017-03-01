var Game = function(args) {
    
    var graphics = new Graphics('canvas');
    var self = this;
    
    this.initialize = function() {
        this.hangman = $('#' + args.hangman);
        this.statsContainer = $('#' + args.statsContainer);
        this.gameContainer = $('#' + args.gameContainer);
        this.lettersContainer = $('#' + args.lettersContainer);
        this.letterButtonsContainer = $('#' + args.letterButtonsContainer)
        this.wins = $('#' + args.wins);
        this.losses = $('#' + args.losses);
        this.newGameButton = $('#' + args.newGame)
        
        this.newGameButton.click(function(e) {
            self.startNewGame();
        });
        
        this.letterButtonsContainer.find('button').click(function(e) {
            self.selectLetter(e);
        });
        
        this.loadGame();
    }

    this.initLetters = function(numLetters) {
        var str = '';
        for (var i = 0; i < numLetters; i++) {
            str += '_ ';
        }
        self.lettersContainer.text(str);
    }
    
    this.initHangman = function() {
        this.hangman.text('10');
    }
    
    this.updateHangman = function(number, drawAll) {
        this.hangman.text(number);
        // If were loading a game that's in progress, we need to draw the
        // parts of the hangman corresponding to the number of lives left
        if (drawAll) {
            for (var i = 9; i > number-1; i--) {
                graphics.animate(i);
            }
        } else {
            graphics.animate(number);
        }
    }
    
    this.startNewGame = function() {
        var self = this;
        $.get('/newgame', function(result) {
            var gameData = JSON.parse(result);
            
            self.initLetters(gameData.letters.length);
            self.initHangman();
            
            graphics.clear();
            
            // Hide stats and show game controls.
            self.statsContainer.hide();
            self.gameContainer.show();
        });
    }
    
    this.updateLetters = function(letters) {
        var str = letters.map(function(x) { 
            return x ? x : '_' 
        }).join(' ');
        
        this.lettersContainer.text(str);
    }
    
    this.updateRecord = function(wins, losses) {
        this.wins.text(wins);
        this.losses.text(losses);
    }
    
    this.selectLetter = function(e) {
        var letter = $(e.target).text();
        $(e.target).prop('disabled', true);
        
        var callBack = function (res) {
            var result = JSON.parse(res);
            if (result.game_over) {
                if (result.win) {
                    alert('You won!!');
                } else {
                    alert('Game Over.  You lost. Word was: ' + result.word);
                }
                self.updateRecord(result.wins, result.losses)
                self.statsContainer.show();
                self.gameContainer.hide();
                self.resetButtons();
            } else {
                if (!result.miss) {
                    self.updateLetters(result.letters);
                } else {
                    self.updateHangman(result.lives);
                }
            }
        }
        
        var postData = { letter: letter };
        $.post('tryletter', postData, callBack);
    }
    
    this.resetButtons = function() {
        this.letterButtonsContainer.find('button').prop('disabled', false);
    }
    
    this.setButtons = function(letters) {
        for (var i = 0; i < letters.length; i++) {
            this.letterButtonsContainer.find('button:contains(' + letters[i] + ')').prop('disabled', true);
        }
    }
    
    this.loadGame = function() {
        $.get('/getgame', function(result) {
            var game = JSON.parse(result);
            
            if (!game.game_over) {
                self.updateLetters(game.letters);
                self.updateHangman(game.lives, true);
                self.setButtons(game.letters_guessed);
                self.statsContainer.hide();
                self.gameContainer.show();
            } else {
                self.updateRecord(game.wins, game.losses);
            }
        });
    }
    
    this.initialize();
}

$(document).ready(function(e) {
    var args = {
        hangman: 'hangman',
        statsContainer: 'stats-container',
        gameContainer: 'game-container',
        lettersContainer: 'letter-container',
        wins: 'wins',
        losses: 'losses',
        letterButtonsContainer: 'letter-buttons-container',
        newGame: 'new-game'
    }
    
    var g = new Game(args);
});