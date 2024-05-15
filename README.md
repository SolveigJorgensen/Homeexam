
            elif seq == 0 and ack == 0 and flag == 2:

                print('FIN packet is recived')
                end_time = time.time()
                FIN_ACK_packet = header.create_packet(0, 0, 6, b'')
                serverSocket.sendto(FIN_ACK_packet, clientAddress)
                print('FIN-ACK packet is sent')
                print('Connection closes')
                serverSocket.close()
                break
