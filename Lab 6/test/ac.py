import os
import select
import socket
import sys
from check import ip_checksum


try:
	s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print 'Failed to create socket'
	sys.exit()

host='localhost'
port=8888
inputs = [sys.stdin, s]
outputs = [ ]
exceptional = [s]

stringList = [ ]

packetNumbers = [ ]
packetIndex = 0

print 'Please enter your messages + Press Enter'
while 1:
    timeout = 5
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
    
    if not (readable or writable or exceptional):
        print ' timed out, do some other work here'
        continue
    
    for x in readable:
		if x is sys.stdin:
			messageText=sys.stdin.readline()
			messageText=messageText.strip()
			
			stringList.append(messageText)
			
			
			print 'Displaying stored string: '
			print stringList[:len(stringList)]
			
			if messageText == 'EXIT' or messageText == 'exit' or messageText == 'Exit':
			    print 'Closing...'
				
			    s.close()
			    sys.exit()
			else:
				print 'Sending Packet... '
				messageText= '0 | ' + ip_checksum(messageText) + ' | ' + messageText + ' | ' + str(packetIndex)
				s.sendto(messageText,(host, port))
			continue
		
		elif x is s:
			d=s.recvfrom(1024)
			data=d[0]
			addr=d[1]
			if data[0:3] == 'ACK':
				print 'ACK ' + data[3] + ' RECVD'
				latestACK = data[3]
			else:
				print 'ERR'
		continue
sys.exit()