#!/usr/bin/env python3

# button_server_v7
# 2020-09-30

from flask import Flask, render_template
import socketIO_client
import flask_socketio

web = Flask(__name__)
web.config[ 'SECRET_KEY' ] = 'vnxxxxxjknfl1232#'
server = flask_socketio.SocketIO( web )

dgrey  = '#404040'
grey   = '#808080'
green  = '#66ff66'
yellow = '#ffff00'
red    = '#ff0000'
but = { 'b0' : { 'b0' : green, 'b1' : dgrey, 'b2' : dgrey, 'b3' : dgrey },
        'b1' : { 'b0' : dgrey, 'b1' : yellow, 'b2' : dgrey, 'b3' : dgrey },
        'b2' : { 'b0' : dgrey, 'b1' : dgrey, 'b2' : red, 'b3' : dgrey },
        'b3' : { 'b0' : dgrey, 'b1' : dgrey, 'b2' : dgrey, 'b3' : grey }}
lit = { 'b0' : {'i':'b0', 'r': 10, 'g': 255, 'b': 10},
        'b1' : {'i':'b1', 'r': 0, 'g': 255, 'b': 255},
        'b2' : {'i':'b2', 'r': 255, 'g': 0, 'b': 0},
        'b3' : {'i':'b3', 'r': 0, 'g': 0, 'b': 0}}
data = but['b3'] #{i,r,g,b}

@web.route("/")
def main():
    return render_template('buttons.html')

@server.on( 'click' )
def click( btn, methods = ['GET', 'POST'] ):
    global data
    server.emit('state', but[btn])
    blinkt.emit( 'change', lit[btn] )
    data = but[btn]
    #blinkt.wait( seconds = 1)

@server.on('connect')
def web_connect():
    blinkt.emit('ask')
    blinkt.wait( seconds = 1 )

#blinkt.return_state
def return_state( rgb, methods = ['GET', 'POST'] ):
    server.emit('state', but[rgb['i']] )

if __name__ == "__main__":
    blinkt = socketIO_client.SocketIO( '192.168.1.190', 8000 )
    blinkt.on( 'return_state', return_state )
    server.run( web, host = '0.0.0.0', port=5000, debug=True )
