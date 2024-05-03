#Client side
#This is the client side of the UDP file transfere application. The following code
#copied from safiqul UDP code. https://github.com/safiqul/2410/blob/main/udp/udpserver.py


from socket import *

def client(server_port, server_ip, filename):

    InputFile = filename
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = input('Skriv inn en melding som sendes fra client til server')
    clientSocket.sendto(message.encode(), (server_ip,server_port))
    modifiedMessage, serverAdress = clientSocket.recvfrom(2048)
    print(modifiedMessage.decode())
    clientSocket.close()

