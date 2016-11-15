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

begin = 0
end = 3

packetCount = 0

former = 0

wordList = []

testVariable = 0


while(1) :
    
    
    try :
        print 'x, begin ' + str(begin) + ', end ' + str(end)
        for x in range(begin,end + 1):
            
            msg = raw_input('Enter message to send : ')
            
            wordList.append(msg)
            
            #start the timer for timeout
            s.settimeout(10)
            
            # compute checksum of the message
            checksum = ip_checksum(msg)
            
            # making sure checksum is corrupted only once
            if testVariable == 2:
                checksum = 'ee'
            else:
                checksum = ip_checksum(msg)
            testVariable = testVariable + 1
        
            #Set the whole string
            s.sendto(str(packetStatus) + msg + checksum, (host, port))
            packetCount = packetCount + 1
            
            print 'packetStatus ' + str(packetStatus)
            packetStatus = packetStatus + 1
            
        print 'Sleeping for five seconds...'
        time.sleep(5)
        
        
        
        
        try:
            print 'y, begin ' + str(begin) + ', end ' + str(end)
            for y in range(0,4):
                # receive data from client (data, addr)
                d = s.recvfrom(1024)
                reply = d[0]
                addr = d[1]
                
                
                begin = int(reply[0])
                end = begin + 3
                
                print 'reply[0]: ' + reply[0] + ', y: ' + str(y)
                if (former != reply[0]) or (reply[0] == 0):
                    print 'Server reply : ' + reply
                    
                    
                    msg = raw_input('Enter message to send : ')
                    wordList.append(msg)
                    
                    
                    #start the timer for timeout
                    s.settimeout(10)
                    
                    # compute checksum of the message
                    checksum = ip_checksum(msg)
                    
                    # making sure checksum is corrupted only once
                    if testVariable == 2:
                        checksum = 'ee'
                    else:
                        checksum = ip_checksum(msg)
                    testVariable = testVariable + 1
                
                    #Set the whole string
                    s.sendto(str(packetStatus) + msg + checksum, (host, port))
                    
                    print 'packetStatus ' + str(packetStatus)
                    packetStatus = packetStatus + 1
                    
                    
                    former = reply[0]
                
                
                
                
                
                
                
                
        except socket.timeout:
            print 'Re-sending from packet ... ' + str(begin) + ' with end ' + str(end)
            
            for h in range(0, begin):
                checksum = ip_checksum(msg)
                
                s.sendto(str(packetStatus) + msg + checksum, (host, port))
                
                d = s.recvfrom(1024)
                reply = d[0]
                addr = d[1]
        
        
        
        
        
        
    except socket.error, msg:
        print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()