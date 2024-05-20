
# DRTP - Data Reliable Transport Protocol

This application serves as a file transfer application that can transfer jpg files.
It must be run in server or client mode and can be tested in mininet using the simple-topo.py file to create a realistic virtual network. 


### How to run the application

To run det application it must be run in either client or server mode and can be started from the terminal. 
The application accepts the following arguments from command line:

-s --server - Runs the application in server mode  
-c --client - Runs the application in client mode   
-p --port -  Port number the server wil bind to, must be in the range [1024,65535]. Default=8088.  
-i --ip -  Ip address on which the server is running. Default= 10.0.1.2.  
-f --filename - Filename of the file you want to transfer when run in client mode or  
                determine filename of received file in server mode. Default= recived_image.jpg.  
-w --windowsize - Window size in client mode. Default = 3  
-d --discard - Packet to be discarded in server mode.   

#### Server mode:
-s invokes server mode and port number can be set by user to choose which port the  
server should bind/listen to. The ip address (-i) the server is running on can also be set to inform which ip address it runs on.  
The user can use -d with packet number to determine if a packet should be dropped to test
what happens if a packet is not received. The filename of a received file can also be determined with the -f argument and must end with .jpg.  
  
Here is an example on how to run the application in server mode, specifying the IP address, port number, desired filename for the received file,   
and discarding packet number 10.

<pre> python3 application.py -s -i <ip_address_of_the_server> -p <port> -d 10 -f recived_foto.jpg </pre> 

#### Client mode:
-c invokes client mode. Server must be running for the client to be able to connect. 
The user must set the ip address and port number it want to connect to, and it has to be the same 
as the server is listening to.  
The filename of the file the user want to transfer must also be stated using the -f argument. It must be a jpg file.

Here is a example on how to run the application in client mode, specifying the IP and port number to connect to, the file for transefer and setting the windowsize to 5.

<pre> python3 application.py -c  -f image.jpg -i <ip_address_of_the_server> -p <server_port> -w 5 </pre>