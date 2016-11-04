#'''
#    udp socket client
#'''

import random
import select
import socket   #for sockets
import sys  #for exit
import time
from socket import timeout
from check import ip_checksum

# create dgram udp socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()
 
host = 'localhost';
port = 8888;

packetStatus = 0

# testVariable = 0

while(1) :
    msg = raw_input('Enter message to send : ')
    
    # compute checksum of the message
    checksum = ip_checksum(msg)
    
    # making sure checksum is corrupted only once
    # if testVariable == 1:
    #     checksum = 'ee'
    # else:
    #     checksum = ip_checksum(msg)
    # testVariable = testVariable + 1
    
    try :
        #Set the whole string
        s.sendto(str(packetStatus) + msg + checksum, (host, port))
        
        #start the timer for timeout
        s.settimeout(10)
        
        
        try:
            # receive data from client (data, addr)
            d = s.recvfrom(1024)
            reply = d[0]
            addr = d[1]
        
        except socket.timeout:
            print 'Re-sending...'
            checksum = ip_checksum(msg)
            
            s.sendto(str(packetStatus) + msg + checksum, (host, port))
            
            d = s.recvfrom(1024)
            reply = d[0]
            addr = d[1]
        
        
        print 'Server reply : ' + reply
        
        packetStatus = 1 - packetStatus
        
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()