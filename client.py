#Client side
#This is the client side of the UDP file transfere application. The following code
#copied from safiqul UDP code. https://github.com/safiqul/2410/blob/main/udp/udpserver.py

## IP SKAL ALLTID FØRST

import socket
import header
from datetime import datetime


def client(server_ip, server_port, filename, windowsize):

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print('Connection Establisht Phase: \n')
    #Three-way handshake, creates a packet with every variable set to null. Just values for the flags are set to establish a connection
    SYN_packet = header.create_packet(0, 0, 8, b'')
    syn, ack, fin = header.parse_packet(SYN_packet)

    clientSocket.sendto(SYN_packet, (server_ip, server_port))
    print('SYN packet is sent')

    packet_recived, serverAddress = clientSocket.recvfrom(2048)
    syn, ack, fin = header.parse_packet(packet_recived)

    if (syn, ack, fin) == (1, 1, 0):
        print(' SYN-ACK packet is recived')

        ACK_packet = header.create_packet(0, 0, 4, b'')
        clientSocket.sendto(ACK_packet, serverAddress)
        print('ACK packet is sent\nConnection established\n')

    else:
        print('Connection failed')
        exit(1)

    clientSocket.sendto(filename.encode(), serverAddress)

#Sending packets
    print('Data Transfer: \n')
    packets = {}
    seq_sent = []
    ack_recived = []
    sequence_number = 1
    clientSocket.settimeout(0.5)

    with open(filename,'rb') as file:

        while True:
            bytes_read = file.read(994)

            if not bytes_read:
                clientSocket.sendto(b'', serverAddress)
                print('DATA finished\n')
                break # If there is no bytes to read, the loop exit.
            packets[sequence_number] = bytes_read

            packet = header.create_packet(sequence_number, 0, 0, bytes_read)
            clientSocket.sendto(packet, serverAddress)
            seq_sent.append(sequence_number)
            print(datetime.now().time(),f' -- packet with seq = {sequence_number} is sent, sliding window = {seq_sent[-windowsize:]}')
            sequence_number += 1


            if(len(packets) >= windowsize):
                while seq_sent != ack_recived:
                    try:
                        ack_packet_recived, serverAddress = clientSocket.recvfrom(2048)
                        header_msg = ack_packet_recived[:6]
                        seq, ack, flag = header.parse_header(header_msg)
                        print(datetime.now().time(),f' -- Ack for packet {ack} is recived')
                        ack_recived.append(ack)


                    except socket.timeout:
                        print(datetime.now().time(),' -- RTO occured')

                        for i in seq_sent:
                            if i not in ack_recived:
                                packet = header.create_packet(i, 0, 0, packets[i])
                                clientSocket.sendto(packet, serverAddress)
                                print(datetime.now().time(), f' -- retransmitting packet with seq = {i}')


    print('Connection Teardown\n')
    FIN_packet = header.create_packet(0, 0, 2, b'')
    clientSocket.sendto(FIN_packet, serverAddress)
    print('FIN packet is sent')

    packet_recived, serverAddress = clientSocket.recvfrom(2048)
    syn, ack, fin = header.parse_packet(packet_recived)

    if (syn, ack, fin) == (0, 1, 1):
        print('FIN-ACK packet is recived')
        print('Connection closes')
        clientSocket.close()
    else: print('FIN-ACK is not recived.')

