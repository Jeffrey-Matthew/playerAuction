from flask import Blueprint, render_template,redirect,url_for,request,flash,jsonify
#from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import emit,join_room,leave_room
from flask_login import login_user, login_required, logout_user,current_user
from models import User
from __init__ import db,socketio
bPlayer = Blueprint('bPlayer', __name__)


@bPlayer.route('/bid/<user>/<player>/<bidvalue>') #Here you didn't provide action methods (POST or get , thats why it didn't work)
def bidForPlayer(user,player,bidvalue):
    # if request.method == 'POST':
    #     print('POST Method is invoked - Bid Player')
        
    #     #return render_template('login.html')
    #     if user_name == 'jeff':
    #         user_name = 'Matt'
    #         player_name = 'Kohli'
    #         bidValue = request.form['vb']
    #         return render_template('bidPlayer.html',bid = bidValue,userName = user_name,playerName = player_name,nextUser=user_name)
        #return redirect(url_for('success', name = user))
    #print('Else is invoked')
         
    current_bid = bidvalue
    user_name = user
        
    player_name = player
    logged_user_name = current_user.name 
    userActionPrompt= ''
    editToggleBid = ''
    if logged_user_name == user:
        userActionPrompt = 'It\'s your Turn'
        editToggleBid = ''
    else:
        userActionPrompt = 'Please Wait!!'
        editToggleBid = 'readonly'
    return render_template('bidPlayer.html',bid = current_bid,userName = user_name,playerName = player_name,nextUser = user_name,userActionPrompt=userActionPrompt,editToggleBid=editToggleBid)
        




@bPlayer.route('/success/<name>')
def success(name):
   return render_template('hello.html', name = name)

# @bPlayer.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         print('POST Method is invoked')
#         user = request.form['nm']
#         #return render_template('login.html')
#         return redirect(url_for('bPlayer.success', name = user))
#     #print('Else is invoked')
#     return render_template('login.html')

@bPlayer.route('/bid', methods=['POST', 'GET'])
@login_required
def bid():
    if request.method == 'POST':
        print('POST Method is invoked')
        newBid = request.form['vb']
        #nxtPlayerBtn = request.form['nxtPlayerBtn']
        print(request.form)
      #   print(nxtPlayerBtn)
      
        if newBid == '':
            newBid = 10
        userName = request.form['Current User']
        if userName=='jeff':
            userName = 'Enzio'
        else:
            userName = 'jeff'
        playerName = request.form['Current Player']
        if 'nxtPlayerVal' in request.form:
            global playerIdx,playerList
            playerIdx+=1
            if playerIdx>=len(playerList):
                playerIdx -=1
            playerName = playerList[playerIdx]
        #return render_template('login.html')
        
        return redirect(url_for('bPlayer.bidForPlayer',user=userName,player=playerName,bidvalue = newBid ))
    #print('Else is invoked')
    print('Current User',current_user.name)
    return render_template('bidPlayer.html',bid = 5,userName = 'jeff',playerName = 'Kohli',nextUser = 'Matt')


# playerList = ['Kohli','Dhoni','Sachin','Gill','steveSmith','yuvraj','brettLee','mikeHussey','ponting','abd','mccullum','root','sanga','dravid','jimmy']
playerList  = ['Ajmal','Yomi','Andrew','Aravind','Maddy','Rajesh','Rajil','Reva','Rohit','Sanjeevi','Sanjith','Sijin','Tezan','Vasu','Venky']
playerIdx=0
userPlayers = {}

roomMap = {}
playerMap = {}

@bPlayer.route('/lobby/', methods=['POST', 'GET'])
@login_required
def lobbyRoom():
    return render_template('lobby.html')

@bPlayer.route('/waitRoom/', methods=['POST', 'GET'])
@login_required
def waitRoom():
    global roomMap
    # cur_user = current_user.name
    # if roomId in roomMap:
    #     user1 = roomMap[roomId]
    #     user2 = cur_user
    #     cur_user = user1+'   VS      '+user2
    #     roomMap[roomId] = [user1,user2]
    #     return redirect(url_for('bPlayer.playGame',roomId=roomId))
    #     #return redirect(url_for('bPlayer.playGame',roomId=roomId)) and render_template('lobby.html',cur_user=cur_user)
        
    # else:
        
    #     roomMap[roomId] = cur_user
    #print(roomMap)
    params = request.args.to_dict()
    # Retrieve the dictionary values from the URL parameters
    
    # Do something with the values...
    # Example: Print the dictionary values
    roomId=''
    values = ''
    for key, value in params.items():
        
        #roomMap[roomId] = [value[0],value[1]]
        
        print(f"{key}: {value}")
        values = value.split(',') 
        if len(values) == 3:
            roomId = key
            roomMap[roomId] = [values[0],values[1],True]
            playerMap[roomId] = 0 
    #return render_template('index.html')
    return redirect(url_for('bPlayer.playGame',roomId=roomId))
    #return render_template('lobby.html',cur_user=cur_user)

@bPlayer.route('/match/<roomId>',methods=['POST','GET'])
@login_required
def playGame(roomId):
    global roomMap
    print('Play Game invoked!,now')
    if request.method=='POST':
        # print('POST Method is invoked for RoomID')
        # newBid = request.form['vb']
        # user1 = request.form['curUser']
        # user2 = request.form['nxtUser']
        # roomId = request.form['roomNo'] 
        # print(roomId)
        
        data = request.get_json()
        value_from_js = data['data']
        #print(value_from_js)
        roomId = data['data']
        user2 = data['curUser']
        user1 = data['nextUser']
        newBid = data['newBid']
        #userActionPrompt  = ''
        if user1 == current_user.name:
            editToggleBid = ''
         #   userActionPrompt  = 'Please wait for the other user'
        else:
            editToggleBid ='readonly'
        #handle_refresh_page(roomId)
        #socketio.emit('refresh', {'url': ('/match/'),'roomId':roomId},broadcast= True)
        
        response_data = {'bid': newBid,'userName':user1,'nextUser':user2,'curPlayer':playerList[playerMap[roomId]]}
        return jsonify(response_data)
        #return render_template('bidPlayer.html',bid = newBid,userName = user1,playerName = 'Kohli',nextUser = user2,editToggleBid=editToggleBid,roomNo=roomId)
    else:
        print(roomId,roomMap,'Here is it')
        if (roomMap[roomId][2]) :
            user1 = roomMap[roomId][0]
            user2 = roomMap[roomId][1]
            # if roomMap[roomId][2] == 0:
            #     roomMap[roomId][2] = -1
            # else:
            #     roomMap[roomId][2] = int(roomMap[roomId][2]) - int(roomMap[roomId][2])
            curBid = 5
            #userActionPrompt = ''
            newBid = curBid
            if user1 == current_user.name:
                editToggleBid = ''
                userActionPrompt = 'Play On'
            else:
                editToggleBid ='disabled'
                userActionPrompt = 'Let the other Player play!'
        #     print(request.form)
        # if not 'bidBtn' in request.form:
        #     return render_template('bidPlayer.html',bid = newBid,userName = user1,playerName = 'Kohli',nextUser = user2,editToggleBid=editToggleBid,roomNo=roomId)
        # else:
        #     newBid = request.form['vb']
        #     user1 = request.form['curUser']
        #     user2 = request.form['nxtUser']
        #     roomId = request.form['roomNo'] 
        #     print(roomId)
        #     if user1 == current_user.name:
        #         editToggleBid = ''
        #     else:
        #         editToggleBid ='readonly'
            logged_user = current_user.name
            return render_template('bidPlayer.html',bid = newBid,userName = user1,playerName = playerList[playerMap[roomId]],nextUser = user2,editToggleBid=editToggleBid,roomNo=roomId,logged_user=logged_user,userActionPrompt = userActionPrompt,remainingPlayers= playerList[playerMap[roomId]+1:])
        else:
            # if user1 == current_user.name:
            #     editToggleBid = ''
            # else:
            #     editToggleBid ='readonly'
            user1 = roomMap[roomId][0]
            user2 = roomMap[roomId][1]
            # if roomMap[roomId][2] == 0:
            #     roomMap[roomId][2] = -1
            # else:
            #     roomMap[roomId][2] = int(roomMap[roomId][2]) - int(roomMap[roomId][2])
            curBid = 5
        
            newBid = curBid
            if user1 == current_user.name:
                editToggleBid = ''
            else:
                editToggleBid ='readonly'
            return render_template('bidPlayer.html',bid = newBid,userName = user2,playerName = playerList[playerMap[roomId]],nextUser = user1,editToggleBid=editToggleBid,roomNo=roomId,remainingPlayers= playerList[playerMap[roomId]+1:])



@bPlayer.route('/updatePlayerUser',methods=['POST'])
def updatePlayerMap():
    global userPlayers
    data = request.get_json()
    print(data)
    username = data['userName']
    newPlayer = data['newPlayer']
    if username in userPlayers:
        curPlayers = userPlayers[username]
        curPlayers.append(newPlayer)
        userPlayers[username] = curPlayers
    else:
        userPlayers[username] = [newPlayer]
    print('UserPlayer Map',userPlayers)
    return []

maxPlayers = 5
@bPlayer.route('/midGame/',methods=['POST','GET'])
@login_required
def midGameSelection():
    global playerList,playerIdx,maxPlayers
    clickedUser = request.args.get('arg1')
    playerLists = request.args.get('arg2')
    selectedPlayers = [] #Finished player - 5 players
    # print('passedData',clickedUser)
    print('List of players',playerLists.split(','))

    selLimit =maxPlayers -  len(playerLists.split(','))
    logged_user = current_user.name 
    waitToggle,chooseRestToggle = '',''
    # print(type(playerLists))
    presentPlayers = []
    
    for player in playerLists.split(','):
        if not player=='':
            presentPlayers.append(player)
    selLimit =maxPlayers - len(presentPlayers)
    userPlayers[logged_user] = presentPlayers
    if logged_user == clickedUser:
        chooseRestToggle = 'hidden'
        # selectedPlayers = playerLists
        for player in playerLists.split(','):
            selectedPlayers.append(player)
        
    else:
        waitToggle='hidden'
        existPlayerls = playerLists.split(',')
        if not existPlayerls[0] == '':

            for player in playerLists.split(','):
                selectedPlayers.append(player)

    # playerLs = ['Kohli','Dhoni','Hussey','Brett Lee','Steve Smith']
    playerLs = playerList[playerIdx:]
    
    print('Visibilities=waitToggle',waitToggle,'=chooseRestToggle',chooseRestToggle)
    return render_template('midGame.html',players = playerLs,selLimit=selLimit,chooseRestToggle=chooseRestToggle,waitToggle=waitToggle,selectedPlayers=selectedPlayers)

@bPlayer.route('/limitReach',methods=['POST','GET'])
@login_required
def midEndOfGame(data):
    userCompleted = data['username']
    return render_template('bidPlayer.html')
    

@bPlayer.route('/match',methods = ['POST','GET'])
@login_required
def match():
    if request.method == 'POST': 
        print('POST Method is invoked')
        newBid = request.form['vb']
        user1 = request.form['curUser']
        user2 = request.form['nxtUser']
        roomId = request.form['roomNo']
        return redirect(url_for('bPlayer.playGame',roomId=roomId,user1=user2,user2=user1,newBid=newBid))


@socketio.on('restSelected')
def handle_rest_selected(data):
    resList = data['resList']
    userName = current_user.name
    curPlayers = userPlayers[userName]
    for player in resList:
        curPlayers.append(player)
    userPlayers[userName] = curPlayers
    emit('resultsPage',broadcast=True)
    
@bPlayer.route('/midGame/results/')
def resultsPage():
    global roomMap
    users =  []
    for key in userPlayers:
        users.append(key)
    user1,user2 = users[0],users[1]
    user_1_players = []
    user_2_players = []
    for players in userPlayers[user1]:
        user_1_players.append(players)
    for players in userPlayers[user2]:    
        user_2_players.append(players)
    roomMap = {}
    return render_template('results.html',userTwoPlayers =user_2_players,userOnePlayers= user_1_players,user1=user1,user2=user2 )

@socketio.on('refreshPage')
def handle_refresh_page(data):
    print('Handle Refresh Page',data['room'])
    emit('refresh', {'url': ('/match/'),'roomId':data['room'],'newBidValue':data['newBidValue']},broadcast= True) 

@bPlayer.route('/my-route', methods=['POST'])
def my_route():
    data = request.get_json()
    value_from_js = data['data']
    print(value_from_js)
    return None 

@socketio.on('nxtPlayerParent')
def handle_nxtPlayer_master(data):
    global playerIdx
    roomId = data['room']
    print(playerMap,'-----')
    playerMap[roomId]  = playerMap[roomId] + 1
    playerIdx+=1
    emit('nxtPlayerPrompt',{'clickedUserName':data['logged_user']},broadcast = True )

@socketio.on('midGameParent')
def handle_mid_game_master(data):
    arg1 = data['logged_user']
    print('arg1',arg1)
    emit('midGame',{'arg1': arg1},broadcast=True)
     

