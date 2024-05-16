#--------- DRTP Application --------#

# Some of this code is copyd from or based on my previouse assignemts/Obligs.

import argparse
import sys
import ast
import InputValidation
import client
import server

# Creates a parser.
parser = argparse.ArgumentParser(prog='Optional arguments', description='DRTP file transfere application arguments', epilog= 'End of help text')

# Adds arguments
parser.add_argument('-s', '--server', action= 'store_true',  help='Enable the server mode')
parser.add_argument('-c', '--client', action= 'store_true',  help='Enable the client mode')
parser.add_argument('-p', '--port', type=InputValidation.check_port, default=8088, help='Sets the port adress the server will listen to, must be integer and in the range [1024,65535]')
parser.add_argument('-i', '--ip', default='10.0.1.2', type=InputValidation.check_ip, help='Sets the the ip adress the server in run from/the client want to connect to')
parser.add_argument('-f', '--filename', type=InputValidation.check_filename, default='image.jpg', help='The filepath to the file you want to tranfere')
parser.add_argument('-w', '--windowsize', type=InputValidation.check_window, default = 3 , help='Sets the sliding window size')
parser.add_argument('-d', '--discard', type=InputValidation.check_discard_packet, default=-1, help='Sets the sequence number for the packet to be discarded on the server side')

# Parses the arguments set by user and calls input validation functions.
args = parser.parse_args()

# This code inform the user on wheter the server or client is running and what IP adress and portnumber is set.

if not args.server and not args.client:
    print('You should run either in server or client mode')
    exit(1)
if args.server and args.client:
    print('You cannot start server and client at the same time')
    exit(1)

# Description:
#   Main function of the application, calls either the client or server function
# Parameters:
#   server_ip: IP adress set by user using commandline arguments.
#   server_port: Port number set by user using commandline arguments
#   filename: File to send on the client side, and sets the name of the recived file on server end.
#   windowsize: How many packets that are sent from client before it needs an acknoledgment from server to continue.
#   discard_packet: Sequance number of the packet that should be discarded and resent.
# Returns:
#   none
def main():

    if(args.client):
        client.client(args.ip, args.port, args.filename, args.windowsize)
    if(args.server):
        server.server(args.ip, args.port, args.discard, args.filename)

# Starts the main function
if __name__ == '__main__':
        main() # Calls the function main, with arguents for ip, portnumer and filname.
