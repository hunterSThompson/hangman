from flask import Flask, Response, request, send_from_directory, redirect
from flask import render_template
from game import Game
from user import User
import model
import os

from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user

app = Flask(__name__)

# Configure login manager
login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)
            
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
    
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)
    
## Serve game page
@app.route('/')
@login_required
def test():
    return render_template('game.html', username=current_user.username)
    
## AJAX request for loading the current game.
@app.route('/getgame')
@login_required
def get_game():
    g = model.get_game(current_user.username)
    return g.serialize()

## Request to start a new game.
@app.route('/newgame')
@login_required
def newgame():
    game = model.get_game(current_user.username)
    
    if not game.game_over:
        raise Exception('The game isn\'t over yet so you can\'t start a new one. Quit cheating.')
        
    game.start_new_game()
    model.update_game(game)
    
    return game.serialize()
    
## Reqeust to try a letter. Could potentially lead to a win or loss.
@app.route('/tryletter', methods=['POST'])
@login_required
def try_letter():
    game = model.get_game(current_user.username)
    
    print 'WORD: ' + game.word
    if game.game_over:
        raise Exception('The game is over, you can\'t try anymore letters. Quit cheating.')
        
    letter = request.form['letter']
    
    game.tryLetter(letter)
    model.update_game(game)
    
    # If the game is over update the record in both the DB and the response object.
    if game.game_over:
        num = (game.wins if game.win else game.losses) + 1
        if game.win:
            game.wins = num
        else:
            game.losses = num
        model.update_record(current_user.username, num, game.win)
        # Important: We only want to include the answer if the games over.
        # Otherwise user could cheat.
        return game.serialize(removeWord=False)
    
    return game.serialize()
    
    
# Tell flask-login how to pull the user using from the auth token.
@login_manager.user_loader
def load_user(username):
    return User.get(username)
    
# Register a new user. Reloads page if username is already taken.
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        result = model.add_user(username, password)
        if result:
            user = User.get(username)
            login_user(user)
            return redirect("/")
        else:
            return render_template("register.html", error=True)
    else:
        return render_template('register.html')
    

# Log user in. Reload /login page if credentials are invalid
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # pull username via params
        username = request.form['username']
        password = request.form['password']        
        user = User.get(username)
        # validate password. if valid redirect to /game page, otherwise 
        # reload login page w/ error
        if user and user.password == password:
            login_user(user)
            return redirect("/")
        else:
            return render_template('login.html', Error=True)
    else:
        return render_template('login.html')
        
# Logout the current user.
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/login')
    
    
## For running on cloud9.
host = os.getenv('IP', '0.0.0.0')
port = int(os.getenv('PORT', 8080))

# Need to set the secret key so flask-login can write to session.
# In a production application this should never be in source control.
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Initialize the model.
model.create()

# Start the app.
app.run(host=host, port=port)