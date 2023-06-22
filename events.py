from flask import request,render_template,redirect,url_for
from flask_socketio import emit,join_room,leave_room
from flask_login import login_required,current_user
from extensions import socketio


users = {}

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("user_join")
def handle_user_join(username):
    print(f"User {username} joined!")
    users[username] = request.sid

@socketio.on("new_message")
def handle_new_message(message):
    print(f"New message: {message}")
    username = None 
    for user in users:
        if  users[user] == request.sid:
            username = user
    emit("chat", {"message": message, "username": username}, broadcast=True)
    #emit("chat", {"message": message, "username": username}, broadcast=False)


#Joining a room.
roomMap = {}
@socketio.on('join_room')
@login_required
def handle_join_room(data):
    global roomMap
    room = data['room']
    print('Room joining')
    join_room(room)
    print('Joined room:', room)
    # if len(socketio.server.eio.sockets) == 1:
    #     socketio.start_background_task(redirect_user, delay=5, url=('/lobby/'+room))
    # else:
    #     socketio.start_background_task(redirect_user, delay=5, url='/match/'+room)
    #socketio.start_background_task(redirect_user, delay=5, url=('/lobby/'+room))
    # socketio.
    #print(len(socketio.server.eio.sockets))
    num_clients = len(socketio.server.manager.rooms['/'][room]) 
    print(num_clients)
    if (num_clients)==1:
        roomMap[room]= current_user.name
        
        #emit('lobby_redirect', {'url': ('/lobby/')})
    if num_clients == 2:
        newUser = current_user.name 
        clients = [roomMap[room],newUser,room]
        
        
        roomMap[room]= clients
        print(roomMap)
        emit('redirect', {'url': ('/waitRoom/'),'params':roomMap},broadcast= True)
        #emit('new_user',broadcast= True)
    
    # else:
    #     socketio.start_background_task(redirect_user, delay=2, url='/match/'+room)
    #emit('redirect', {'url': ('/lobby/'+room)})
    # userName = current_user
    # editToggleBid = ''
    # playerName = 'Kohli'
    #bid()
    #return render_template('chatPage.html')
    #return redirect(url_for('auth.signup'))


    #return render_template('bidPlayer.html',userName=userName,playerName=playerName,editToggleBid=editToggleBid)




# #Leaving a room
# @socketio.on('leave_room')
# def handle_leave_room(data):
#     room = data['room']
#     leave_room(room)
#     print('Left room:', room)

def testFunc():
    print('Test function is invoked')

def redirect_user(delay, url):
    socketio.sleep(delay)
    emit('redirect', {'url': url}) 