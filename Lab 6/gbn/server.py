import os
import select
import socket
import sys
import time
from check import ip_checksum


HOST=''
PORT=8888
try:
	s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
except socket.error:
	print 'Socket bind failed'
	sys.exit()
print 'Socket Created'

try:
	s.bind((HOST,PORT))
except socket.error:
	print 'Socket bind Failed'
	sys.exit()
print 'Socket Bind Complete'

latestPacket = 0

while 1:
	receivedData=s.recvfrom(1024)
	d=receivedData[0]
	addr=receivedData[1]
	
	data=d.split(' | ', 4)
	
	if (data[0]=='0' and ip_checksum(data[2])==data[1] and data[3] == str(latestPacket)):
		print '[' + addr[0] + ':' + str(addr[1]) + '] - ' + data[2]
		ack='ACK'
		s.sendto(ack + str(latestPacket),(addr[0],addr[1]))
		latestPacket = latestPacket + 1
	elif (data[3] != latestPacket):
		print '[' + addr[0] + ':' + str(addr[1]) + '] - SKIPPED PACKET; DUPLICATING ACK'
		# ack='NACK'
		ack = 'ACK'
		
		if latestPacket > 0:
			s.sendto(ack + str(latestPacket - 1),(addr[0],addr[1]))
		elif latestPacket == 0:
			s.sendto(ack + str(latestPacket),(addr[0],addr[1]))
	continue
s.close()