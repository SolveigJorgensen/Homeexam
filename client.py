# ----------- Client side of the DRTP application ---------- #

# The following code include the client side of the DRTP-Application and is based on
# code provided by Safiquel Islam on https://github.com/safiqul/2410

import socket
import header
from datetime import datetime

# Description:
#   Client side of the application. It implements a tree-way handshake before it reads the file, creates packets and
#   sends it to the server. Packets consist of a header of 6 bytes, and the data of 994 bytes, 1000 bytes in total.
#   The function has a timeout and resends packets if it does not recive an acknoledgment from server.
#   For connection teardown it sends an FIN packet and expect a fin-ack from server.
# Parameters:
#   server_ip: IP adress set by user using commandline arguments
#   server_port: Port number set by user using commandline arguments
#   windowsize: How many packets that are sent from client before it needs an acknoledgment from server to continue.
#   filename: File to send on the client side, and sets the name of the recived file on server end.
# Returns:
#   none
def client(server_ip, server_port, filename, windowsize):

    #Creates socket and sets timeout
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    clientSocket.settimeout(0.5)

    #Three-way handshake
    print('Connection Establish Phase: \n')
    try:
        SYN_packet = header.create_packet(0, 0, 8, b'')     # Creates a SYN packet with no data attached.
        clientSocket.sendto(SYN_packet, (server_ip, server_port))               # It only sets the SYN bit in flags.
        print('SYN packet is sent')                                             # Sends SYN packet to server

        packet_recived, serverAddress = clientSocket.recvfrom(2048)             # Recived a packet, server address is stored in Server adress
                                                                                # and packet is storer in packet_recived
        syn, ack, fin = header.parse_packet(packet_recived)                     # Function parse_packet is called. Returns bit set inn flags of the header.

        if (syn, ack, fin) == (1, 1, 0):                                        # If syn and ack bit is set in flags,
            print('SYN-ACK packet is recived')                                  # a syn-ack packet is recived from server.

            ACK_packet = header.create_packet(0, 0, 4, b'') # A ack packet is created
            clientSocket.sendto(ACK_packet, serverAddress)                      # and sent to the server. Connection is sucessfull.
            print('ACK packet is sent\nConnection established\n')

    except socket.timeout:                                                      # If client does not recive a syn ack from server
        print('Connection failed')                                              # before timeout. Connection failed and program exits.
        exit(1)


    #Sending packets
    print('Data Transfer: \n')
    packets = {}                               # Empty dictionary for storing packets with key = sequencenumber of packet
    seq_sent = []                              # Empty list for storing sequence number/packets sent.
    ack_recived = []                           # Empty list for storing acknoledment recived from server.
    sequence_number = 1                        # Sequencenumber for packets sent. Starting at 1.

    with open(filename,'rb') as file:          # Opens file in readmode.

        while True:                            # A loop that sends every packet with sice 1000 (header + data), retransmitt if necessary and sends fin when finnished.
            bytes_read = file.read(994)        # Reads 994 bytes at a time an stores it in bytes_read

            if not bytes_read:                 # If bytes_read is empty, it has reach end of file, and starts connection teardown
                print('DATA finished\n\nConnection Teardown\n')
                FIN_packet = header.create_packet(0, 0, 2, b'')     # Fin packet is sent to server to terminate
                clientSocket.sendto(FIN_packet, serverAddress)                          # connection.
                print('FIN packet is sent')

                while True:
                    try:
                        packet_recived, serverAddress = clientSocket.recvfrom(2048)     # Client waits on respons from server
                        syn, ack, fin = header.parse_packet(packet_recived)             # If it recives a flag with fin and ack bit set
                                                                                        # it closes socket and connection.
                        if (syn, ack, fin) == (0, 1, 1):
                            print('FIN-ACK packet is recived')
                            print('Connection closes')
                            clientSocket.close()
                            break

                    except socket.timeout:                                              # If the does not recive a fin-ack before it time out
                        print('FIN-ACK is not recived.')                                # it prints error.

                break

            packets[sequence_number] = bytes_read                                       # The 964 bytes is stored in packets directory with
                                                                                        # key set to sequence number of the packet.
            packet = header.create_packet(sequence_number, 0, 0, bytes_read)  # Packet with sequence number in header .
            clientSocket.sendto(packet, serverAddress)                                  # and correspoing data is sent to server
            seq_sent.append(sequence_number)                                            # Sequencenumber is stored in sequencenumber/packet sent.
            print(datetime.now().time(),f' -- packet with seq = {sequence_number} is sent, sliding window = {seq_sent[-windowsize:]}')
            sequence_number += 1


            if(len(packets) >= windowsize):                                             # The first packets up to windowsize is sent
                while seq_sent != ack_recived:                                          # Then the client waits for ack before it sends a new packet.
                    try:                                                                # As long as sequnce number sent is not equal to acknoladment recived
                        ack_packet_recived, serverAddress = clientSocket.recvfrom(2048) # the client resends the packet.
                        header_msg = ack_packet_recived[:6]
                        seq, ack, flag = header.parse_header(header_msg)                # If flags in recived packet is set to ack, ack recived is stored.
                        if flag == 4:
                            print(datetime.now().time(),f' -- Ack for packet {ack} is recived')
                            ack_recived.append(ack)

                    except socket.timeout:
                        print(datetime.now().time(),' -- RTO occured')                  # If client does not recice a ack from server and gets a timeout,
                                                                                        # packets has been sendt but have not recived a acknoladment from server
                        for i in seq_sent:                                              # wil be retransmitted until all packets ha recived a ack.
                            if i not in ack_recived:
                                packet = header.create_packet(i, 0, 0, packets[i])
                                clientSocket.sendto(packet, serverAddress)
                                print(datetime.now().time(), f' -- retransmitting packet with seq = {i}')

    exit(1)