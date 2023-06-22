from flask import Flask, render_template,request,url_for,redirect
# app = Flask(__name__)
#E

from flask_dance.contrib.google import make_google_blueprint, google
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from events import socketio

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__) # creates the Flask instance, __name__ is the name of the current Python module
    app.config['SECRET_KEY'] = 'secret-key-goes-here' # it is used by Flask and extensions to keep data safe
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #it is the path where the SQLite database file will be saved
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # deactivate Flask-SQLAlchemy track modifications
    db.init_app(app) # Initialiaze sqlite database
    # The login manager contains the code that lets your application and Flask-Login work together
    login_manager = LoginManager() # Create a Login Manager instance
    login_manager.login_view = 'auth.login' # define the redirection path when login required and we attempt to access without being logged in
    login_manager.init_app(app) # configure it for login
    from models import User
    @login_manager.user_loader
    def load_user(user_id): #reload user object from the user ID stored in the session
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    # blueprint for auth routes in our app
    # blueprint allow you to orgnize your flask app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # blueprint for non-auth parts of app
    # from main import main as main_blueprint
    # app.register_blueprint(main_blueprint)
    from bidPlayer import bPlayer as bidPlayer_blueprint
    app.register_blueprint(bidPlayer_blueprint)
    from basicPages import basicPages as basicPayes_blueprint
    app.register_blueprint(basicPayes_blueprint)
    from gameModule import gameModule as gameModule_blueprint
    app.register_blueprint(gameModule_blueprint) 
    blueprint = make_google_blueprint(
    client_id="73547651310-kefolrirmich6ai1hrfd19c6edpc0cfc.apps.googleusercontent.com",
    client_secret="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",
    redirect_url="/google-login"
    )
    app.register_blueprint(blueprint, url_prefix="/google_login")
    socketio.init_app(app)
    return app



    

    return app
# @app.route('/hello/<user>')
# def hello_name(user):
#    return render_template('hello.html', name = user)

# # @app.route('/')
# # def home_page():
# #    return 'Hello World'

# @app.route('/bid/<user>/<player>/<bidvalue>')
# def bidForPlayer(user,player,bidvalue):
#     if request.method == 'POST':
#         print('POST Method is invoked - Bid Player')
        
#         #return render_template('login.html')
#         if user_name == 'jeff':
#             user_name = 'Matt'
#             player_name = 'Kohli'
#             bidValue = request.form['vb']
#             return render_template('bidPlayer.html',bid = bidValue,userName = user_name,playerName = player_name,nextUser=user_name)
#         #return redirect(url_for('success', name = user))
#     #print('Else is invoked')
         
#     current_bid = bidvalue
#     user_name = user
        
#     player_name = player
#     return render_template('bidPlayer.html',bid = current_bid,userName = user_name,playerName = player_name,nextUser = user_name)
        


# @app.route('/success/<name>')
# def success(name):
#    return render_template('hello.html', name = name)

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         print('POST Method is invoked')
#         user = request.form['nm']
#         #return render_template('login.html')
#         return redirect(url_for('success', name = user))
#     #print('Else is invoked')
#     return render_template('login.html')

# @app.route('/bid', methods=['POST', 'GET'])
# def bid():
#     if request.method == 'POST':
#         print('POST Method is invoked')
#         newBid = request.form['vb']
#         #nxtPlayerBtn = request.form['nxtPlayerBtn']
#         print(request.form)
#       #   print(nxtPlayerBtn)
      
#         if newBid == '':
#             newBid = 10
#         userName = request.form['Current User']
#         if userName=='jeff':
#             userName = 'Enzio'
#         else:
#             userName = 'jeff'
#         playerName = request.form['Current Player']
#         if 'nxtPlayerVal' in request.form:
#             global playerIdx,playerList
#             playerIdx+=1
#             if playerIdx>=len(playerList):
#                 playerIdx -=1
#             playerName = playerList[playerIdx]
#         #return render_template('login.html')
        
#         return redirect(url_for('bidForPlayer',user=userName,player=playerName,bidvalue = newBid ))
#     #print('Else is invoked')
    
#     return render_template('bidPlayer.html',bid = 1,userName = 'jeff',playerName = 'Kohli',nextUser = 'Matt')


# playerList = ['Kohli','Dhoni','Sachin','Gill']
# playerIdx=0
# if __name__ == '__main__':
#    #app.run(host="127.0.0.1")
#    #app.run(host='0.0.0.0')
#    #app.run()
#    #app.run(host="0.0.0.0",port=5050, threaded=True)
   
#    app.run(host='127.0.0.1', port=5052,debug=True)