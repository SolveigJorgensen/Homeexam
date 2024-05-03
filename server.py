#This is the server side of the file transfere application. The following code
#copied from safiqul UDP code.



from socket import *

def server(server_port, server_ip):

    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', server_port))
    print('Server is ready to recive a connection at port: ', server_port, ' . Ip adress is : ',server_ip)

    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        modifiedMessage = message.decode().upper()
        serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        print("Server has sendt a message back to client.")
        serverSocket.close()
        print("Server er lukket")
        break

#Denne Socketen er ikke blitt lukket og er klar for å taimot flere forespørsler.