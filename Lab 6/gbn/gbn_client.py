import os
import select
import socket
import sys
import time
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

lossBool = 0
lossIndex = 0

u = 0
vee = 0

flip = 0

print 'Please input your message and then press the Enter key: '
while 1:
    timeout = 5
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
    
    # timeout part of go back n
    if not (readable or writable or exceptional):
        # print ' timed out, do some other work here'
        
        if lossBool == 1:
        	print 'reverting to lost packet and re-sending...'
        	packetIndex = lossIndex
        	
        	if (lossIndex + 4 > len(stringList)):
        		maxNum = len(stringList)
        	else:
        		maxNum = lossIndex + 4
        	for t in range(lossIndex, maxNum):
        		# print 't is ' + str(t)
        		messageText = stringList[t]
	        	messageText= '0 | ' + ip_checksum(messageText) + ' | ' + messageText + ' | ' + str(packetIndex)
	        	
	        	# print 'MessageText: ' + messageText
	        	s.sendto(messageText,(host, port))
	        	packetIndex = packetIndex + 1
        	
        	lossBool = 0
        	
        continue
    
    for x in readable:
		if x is sys.stdin:
			
			vee = u
			for u in range (vee,4):
				# print 'u is ' + str(u) + ' and vee is ' + str(vee)
				
				
				if (packetIndex < len(stringList)):
					# print 'messageText = stringList[packetIndex]'
					messageText = stringList[packetIndex]
				else:
					# print 'messageText=sys.stdin.readline()'
					messageText=sys.stdin.readline()
					messageText=messageText.strip()
					
					stringList.append(messageText)
				
				
				print 'Displaying stored strings: '
				print stringList[:len(stringList)]
				
				if messageText == 'EXIT' or messageText == 'exit' or messageText == 'Exit':
				    print 'Closing...'
					
				    s.close()
				    sys.exit()
				else:
					
					# pkt2 is lost (not sent at all in this case)
					if packetIndex == 2:
						# print 'packetIndex == 2'
						lossIndex = 2
						lossBool = 1
						packetIndex = packetIndex + 1
						
						continue
					
					print 'Sending Packet... '
					messageText= '0 | ' + ip_checksum(messageText) + ' | ' + messageText + ' | ' + str(packetIndex)
					s.sendto(messageText,(host, port))
					
					packetIndex = packetIndex + 1
			
			if flip == 0:
				print 'Sleeping for three seconds...'
				time.sleep(3)
				flip = 1
			
			continue
		
		elif (x is s) and (vee < 4):
			d=s.recvfrom(1024)
			data=d[0]
			addr=d[1]
			if data[0:3] == 'ACK':
				print 'ACK ' + data[3] + ' RECVD'
				latestACK = data[3]
				
				
				# print 'packetIndex ' + str(packetIndex) + ' lossIndex ' + str(lossIndex)
				if (packetIndex != lossIndex):
					# decrement counter if packet is successfully transmitted
					vee = vee - 1
				
				
			else:
				print 'ERR'
		continue
sys.exit()