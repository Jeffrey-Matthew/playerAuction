from flask import Blueprint, render_template, session, copy_current_request_context
from flask_login import login_required, current_user
from __init__ import create_app, db,socketio
from flask_socketio import SocketIO, emit, join_room, leave_room,disconnect


app = create_app() # we initialize our flask app using the __init__.py function
async_mode = None
# socket_ = SocketIO(app)
# socketio = SocketIO(app,async_mode=None)
main = Blueprint('main', __name__)
# main = Blueprint('main', __name__)
# # app.register_blueprint(main)

# @main.route('/')
# def index():
#     return render_template('index.html')

# @main.route('/profile')
# @login_required
# def profile():
#     return render_template('profile.html', name=current_user.name)


# @main.route('/socket')
# def sck_index():
#     return render_template('sck_index.html', async_mode=main.async_mode)


# @socket_.on('my_event', namespace='/test')
# def test_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']})


# @socket_.on('my_broadcast_event', namespace='/test')
# def test_broadcast_message(message):
#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': message['data'], 'count': session['receive_count']},
#          broadcast=True)


# @socket_.on('disconnect_request', namespace='/test')
# def disconnect_request():
#     @copy_current_request_context
#     def can_disconnect():
#         disconnect()

#     session['receive_count'] = session.get('receive_count', 0) + 1
#     emit('my_response',
#          {'data': 'Disconnected!', 'count': session['receive_count']},
#          callback=can_disconnect)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() # create the SQLite database
    
    #socketio.run(app,host='127.0.0.1', port=5053,debug=True)
    socketio.run(app,allow_unsafe_werkzeug=True)
    #socketio.run(app,host='172.20.20.255', port=5053,debug=True)
    #app.run(host='127.0.0.1', port=5052,debug=True) # run the flask app on debug mode



    