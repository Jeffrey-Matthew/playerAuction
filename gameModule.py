from flask import Blueprint, render_template, session, copy_current_request_context,request,redirect,url_for
from flask_login import login_required, current_user
from __init__ import create_app, db
from flask_socketio import SocketIO, emit, join_room, leave_room,disconnect
import random
from flask_dance.contrib.google import make_google_blueprint, google

gameModule = Blueprint('gameModule', __name__)

@gameModule.route('/create',methods=['POST', 'GET'])
def createGame():
    
    print("Create Button was invoked")
    return render_template('createRoom.html')        
        
    
@gameModule.route('/join',methods=['POST', 'GET'])
def joinGame():
    
    print("Join Game was invoked")
    return render_template('joinRoom.html')
    

@gameModule.route('/session/<session_id>')
def createGameSession(sessionId):
    return "createGameSession function Invoked"+str(sessionId)

@gameModule.route("/google-login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    email = resp.json()["email"]
    # You can now use the email or other user information as needed
    # e.g., authenticate the user or redirect to a specific page
    return f"Logged in as {email}"
