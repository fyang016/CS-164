import os
import select
import socket
import sys
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


while 1:
	receivedData=s.recvfrom(1024)
	d=receivedData[0]
	addr=receivedData[1]
	
	data=d.split(' | ', 4)
	
	if (data[0]=='0' and ip_checksum(data[2])==data[1]):
		print '[' + addr[0] + ':' + str(addr[1]) + '] - ' + data[2]
		ack='ACK'
		s.sendto(ack,(addr[0],addr[1]))
		
	else:
		print '[' + addr[0] + ':' + str(addr[1]) + '] - PACK_ERR'
		ack='NACK'
		s.sendto(ack,(addr[0],addr[1]))
	continue
s.close()