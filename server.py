'#This is the server side of the file transfere application. The following code'


'#copied from safiqul UDP code.'

from socket import *
import header
import os
from datetime import datetime
import time

# Description:
#   Server side of the application. For adding reliablity to UDP transfere, it implements a tree-way handshake.
#
# Parameters:
#   server_ip: IP adress set by user using commandline arguments
#   server_port: Port number set by user using commandline arguments
#   windowsize: How many packets that are sent from client before it needs an acknoledgment from server to continue.
#   filename: File to send on the client side, and sets the name of the recived file on server end.
# Returns:
#   none
def server(server_ip, server_port, discard_packet, filename):

    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', server_port))
    print(f'Server is ready to recive a connection. Ip adress = {server_ip} and port number =  {server_port}\n\n')

    #Threeway handshake

    packet_recived, clientAddress = serverSocket.recvfrom(2048)
    syn, ack, fin = header.parse_packet(packet_recived)

    if (syn, ack, fin) == (1, 0, 0):
        print('SYN packet is recived')

        SYN_ACK_packet = header.create_packet(0, 0, 12, b'')
        serverSocket.sendto(SYN_ACK_packet, clientAddress)
        print('SYN-ACK packet is sent')

    else:
        print('SYN is not recived')
        exit(1)

    packet_recived, clientAddress = serverSocket.recvfrom(2048)
    syn, ack, fin = header.parse_packet(packet_recived)

    if (syn, ack, fin) == (0, 1, 0):
        print('ACK packet is recived\nConnection established')
        start_time = time.time()

    else:
        print('ACK is not recived')
        exit(1)

    # Recive packets from client.
    if filename == None:
        filename = 'image.jpg'

    #Filname is recived and the path is removed to create a copy of the file and save it in the application.
    filename = os.path.basename(filename)
    counter = 1
    discard = True
    total_data_recived =b''

    #Opens a file with the filename choosen, if it already excist it overwrites it.
    with open(filename, 'wb') as f:

        while True:
            data_recived, clientAddress = serverSocket.recvfrom(2048)
            header_msg = data_recived[:6]
            seq, ack, flag = header.parse_header(header_msg)


            if seq == discard_packet and discard:
                discard = False

            elif seq == counter:
                f.write(data_recived[6:])
                print(datetime.now().time(),f' -- packet {seq} is received')
                counter += 1
                total_data_recived += data_recived

                ACK_packet = header.create_packet(0, seq, 4, b'')
                serverSocket.sendto(ACK_packet, clientAddress)
                print(datetime.now().time(), f' -- sending ack packet for recived packet {seq}')

            elif seq == 0 and ack == 0 and flag == 2:

                print('FIN packet is recived')
                end_time = time.time()
                FIN_ACK_packet = header.create_packet(0, 0, 6, b'')
                serverSocket.sendto(FIN_ACK_packet, clientAddress)
                print('FIN-ACK packet is sent')
                print('Connection closes')
                serverSocket.close()
                break

            else: print(datetime.now().time(), f' -- out-of-order packet {seq} is recived')


    # Calculating througput:

    total_time = end_time - start_time
    file_size = len(total_data_recived) / (1000 * 1000) # Converts to Mega bytes

    througput = (file_size / total_time) * 8 # Througout calculated in Mega bits per second includes all data recivded, also header.
    print(f'The througput is {througput} Mbps')
#Denne Socketen er ikke blitt lukket og er klar for å taimot flere forespørsler.