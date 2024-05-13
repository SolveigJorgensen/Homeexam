#---------DRTP Application--------#

#Tar imot argparse

import argparse
import sys
import ast
import InputValidation
import client
import server

#Creates a parser.
parser = argparse.ArgumentParser(prog='Optional arguments', description='Optional arguments', epilog= 'Good luck!')

#Adds arguments
parser.add_argument('-s', '--server', action= 'store_true',  help='if True it enable the server mode')
parser.add_argument('-c', '--client', action= 'store_true',  help='if True it enable the client mode')
parser.add_argument('-p', '--port', type=InputValidation.valid_port, default=8088, help='Please provide the port adress the server will listen to, must be int and in the range [1024,65535]')
parser.add_argument('-i', '--ip', default='127.0.0.1', type=InputValidation.valid_ip, help='if True it enable the server mode')
parser.add_argument('-f', '--filename', type=str, help='enter webpage')
parser.add_argument('-w', '--windowsize', type=InputValidation.valid_window, default = 3 , help='Please provide sliding window size')
parser.add_argument('-d', '--discard', type=str, default= 0, help='Provide packet to be discarded')

#Runs the parser and get the data.
args = parser.parse_args()

# This code inform the user on wheter the server or client is running and what IP adress and portnumber is entered.
# The input is checked when the user use the arguments.
if args.server and not args.client:
    print('The server is running with IP adresse = ', args.ip, ' and port adress = ', args.port)

if args.client and not args.server:
    print('The client is running with IP adresse = ', args.ip, ' and port adress = ', args.port)
if not args.server and not args.client:
    print('You should run either in server or client mode')
    exit(1)
if args.server and args.client:
    print('You cannot use both at the same time')
    exit(1)

def main(server_ip, server_port, filename, windowsize, discard_packet):

    if(args.client):
        client.client(server_ip, server_port, filename, windowsize)
    if(args.server):
        server.server(server_ip, server_port, discard_packet)

if __name__ == '__main__':
        main(args.ip, int(args.port), args.filename, args.windowsize, int(args.discard))  # Calls the function main, with arguents for ip, portnumer and filname.
