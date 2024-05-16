# ---------- The server side of the DRTP-Application ------------ #

# The following code include the server side of the DRTP-Application and is based on code provided
# by Safiquel Islam on https://github.com/safiqul/2410, lecture slides and my previous assignments/Obligs.

from socket import *
import header
import os
from datetime import datetime
import time

# Description:
#   Server side of the application. It creates a socket and start listening on a set port number for connections.
#   When a client connect they establish the connection with a tree-way handshake. A new file with file name set by user
#   and packets recived from client is written to that file. The function only accepts packets in order, discard
#   packets out of order and sends an ack packet back to client for the recived packet. When it recives a fin packet from
#   client is sends a fin-ack back and closes the connection and socket. Then it calculates the throughput, the amount of
#   successful data transfer during the connection in Mega bits per second, this include the header.
# Parameters:
#   server_ip: IP adress set by user using commandline arguments
#   server_port: Port number the server listens to set by user using commandline arguments
#   filename: Filename set by user for the recived file.
# Returns:
#   none
def server(server_ip, server_port, discard_packet, filename):

    serverSocket = socket(AF_INET, SOCK_DGRAM)                                      # Server creats socket
    serverSocket.bind(('', server_port))                                            # Binds to port
    print(f'Server is ready to recive a connection. Ip adress = {server_ip} and port number =  {server_port}\n\n')

    #Threeway handshake
    packet_recived, clientAddress = serverSocket.recvfrom(2048)                     # Packet recived from client
    syn, ack, fin = header.parse_packet(packet_recived)                             # Parse the flag in the header

    if (syn, ack, fin) == (1, 0, 0):                                                # If the syn flag is set
        print('SYN packet is recived')

        SYN_ACK_packet = header.create_packet(0, 0, 12, b'')    # a syn-ack packet is sent to client
        serverSocket.sendto(SYN_ACK_packet, clientAddress)
        print('SYN-ACK packet is sent')

    else:
        print('SYN is not recived')                                                 # if it does not recive a syn-ack
        exit(1)                                                                     # the program exit

    packet_recived, clientAddress = serverSocket.recvfrom(2048)                     # Packet recived from client
    syn, ack, fin = header.parse_packet(packet_recived)                             # Parse the flag in header

    if (syn, ack, fin) == (0, 1, 0):                                                # If flag is set to ack
        print('ACK packet is recived\nConnection established')                      # Three-way handshake is consider successfuul
        start_time = time.time()                                                    # Current time is stored

    else:
        print('ACK is not recived')                                                 # If the server does not recive a ack
        exit(1)                                                                     # the program exit

    # Recive packets from client.
    if filename == None:                                                            # If filename is not specified by user
        filename = 'recived_image.jpg'                                              # default filename is set.

    filename = os.path.basename(filename)                                           # If the file has a filepath, it stores only the filename
    counter = 1                                                                     # A counter is set to 1. Its used to track packet order
    discard = True                                                                  # Bool for whether a packed should be discarded
    total_data_recived =b''                                                         # Total amount of data recived is stored.

    with open(filename, 'wb') as f:                                                 # Opens a new file with filename set by user or default

        while True:
            data_recived, clientAddress = serverSocket.recvfrom(2048)               # Recived packets from client
            header_msg = data_recived[:6]                                           # Reads header
            seq, ack, flag = header.parse_header(header_msg)                        # Parse header, gets sequence number of packet


            if seq == discard_packet and discard:                                   # If packet sequencenumber is equal to packet to be discarded
                discard = False                                                     # discard is set to false so that the packet is not dropped again

            elif seq == counter:                                                    # If seq equals counter, the packet is in the right order
                f.write(data_recived[6:])                                           # wirtes recived data from packet to file, excluding the header
                print(datetime.now().time(),f' -- packet {seq} is received')
                counter += 1                                                        # Counter is incremented by 1, so it recives the next in order packet
                total_data_recived += data_recived                                  # Data recived is stored in bytes

                ACK_packet = header.create_packet(0, seq, 4, b'')   # Ack packet for recived packet is sent to client
                serverSocket.sendto(ACK_packet, clientAddress)                      # Seq is 0, ack = packet number, and flag set to ack.
                print(datetime.now().time(), f' -- sending ack packet for recived packet {seq}')

            elif seq == 0 and ack == 0 and flag == 2:                               # If packet recived has only set the fin flag

                print('FIN packet is recived')                                      # It communcate end of data transfere
                end_time = time.time()                                              # end time is stored.
                FIN_ACK_packet = header.create_packet(0, 0, 6, b'')
                serverSocket.sendto(FIN_ACK_packet, clientAddress)                  # Fin-ack packet is sent back to client
                print('FIN-ACK packet is sent')
                print('Connection closes')
                serverSocket.close()                                                # Socket closes and connection is terminated
                break

            else: print(datetime.now().time(), f' -- out-of-order packet {seq} is recived') # If packet is out of order


    # Calculating througput:

    total_time = end_time - start_time                      # Total time for data transfere in seconds
    file_size = len(total_data_recived) / (1000 * 1000)     # Converts filesize of data recived including header to Mega bytes

    througput = (file_size / total_time) * 8                # Througput calculated in Mega bits per second
    print(f'The througput is {througput} Mbps')