#!/usr/bin/env python3

# blinkt_server_v7
# 2020-09-30

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import blinkt

light = { 'i':'b3', 'r': 0, 'g': 0, 'b': 0 }
web = Flask(__name__)
web.config[ 'SECRET_KEY' ] = 'vnkdjnfjknfl1232#'
server = SocketIO( web )

@web.route( '/' )
def default_route():
    return render_template( 'state.html')

@server.on('connect')
def web_connect():
    server.emit( 'state', str(light) )

@server.on( 'change' ) # { 'r':'0', 'g':'0', 'b':'0' }
def change( rgb, methods = ['GET', 'POST'] ):
    global light
    if rgb != light:
        blinkt.set_all( rgb['r'], rgb['g'], rgb['b'] )
        blinkt.show()
        light = rgb.copy()
        server.emit( 'state', str(light) )


@server.on('ask')
def ask():
    server.emit( 'return_state',  light )


if __name__ == "__main__":
    server.run( web, host = '0.0.0.0', port=8000, debug=True )
