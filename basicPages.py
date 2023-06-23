from flask import Blueprint, render_template, session, copy_current_request_context
from flask_login import login_required, current_user
from __init__ import create_app, db
from flask_socketio import SocketIO, emit, join_room, leave_room,disconnect


# app = create_app() # we initialize our flask app using the __init__.py function
# async_mode = None
# socket_ = SocketIO(app, async_mode=async_mode)
# socketio = SocketIO(app)
basicPages = Blueprint('basicPages', __name__)


@basicPages.route('/home')
def index():
    return render_template('index.html')

@basicPages.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@basicPages.route('/chat')
def chat():
    return render_template('chatPage.html')