'#This is the server side of the file transfere application. The following code'


'#copied from safiqul UDP code.'

from socket import *
import header
import os
from datetime import datetime


def server(server_ip, server_port, discard_packet):

    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', server_port))
    print(f'Server is ready to recive a connection with ip adress = {server_ip} and port number =  {server_port}\n\n')

    #Threeway handshake

    packet_recived, clientAddress = serverSocket.recvfrom(2048)
    syn, ack, fin = header.parse_packet(packet_recived)

    if (syn, ack, fin) == (1, 0, 0):
        print(' SYN packet is recived')

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

    else:
        print('ACK is not recived')
        exit(1)

    # Recive packets from client.

    #Filname is recived and the path is removed to create a copy of the file and save it in the application.
    filename = serverSocket.recvfrom(2048)[0].decode()
    filename = os.path.basename(filename)
    counter = 1
    discard = True

    #Opens a file with the file name, if it already excist it overwrites it.
    with open(filename, 'wb') as f:
        while True:
            data_recived, clientAddress = serverSocket.recvfrom(2048)

            if not data_recived:
                break

            header_msg = data_recived[:6]
            seq, ack, flag = header.parse_header(header_msg)

            if seq == discard_packet and discard:
                discard = False


            elif seq == counter:

                f.write(data_recived[6:])
                print(datetime.now().time(),f' -- packet {seq} is received')
                counter += 1
                ACK_packet = header.create_packet(0, seq, 0, b'')
                serverSocket.sendto(ACK_packet, clientAddress)
                print(datetime.now().time(), f' -- sending ack packet for recived packet {seq}')


            else: print(datetime.now().time(), f' -- out-of-order packet {seq} is recived')


    packet_recived, clientAddress = serverSocket.recvfrom(2048)
    syn, ack, fin = header.parse_packet(packet_recived)

    if (syn, ack, fin) == (0, 0, 1):
        print('FIN packet is recived')

        FIN_ACK_packet = header.create_packet(0, 0, 6, b'')
        serverSocket.sendto(FIN_ACK_packet, clientAddress)
        print('FIN-ACK packet is sent')
        print('Connection closes')
        serverSocket.close()
    else:
        print('FIN is not recived.')

#Denne Socketen er ikke blitt lukket og er klar for å taimot flere forespørsler.