#...
#udp socket client
#Silver Moon
#...

import socket #for sockets
import sys #for exit
import getpass

#create dgram udp socket
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
	print 'Failed to create socket'
	sys.exit()

host = '10.0.0.4';
port = 8888;

for x in range(0,2):
	if x == 0:
		msg = raw_input('Please enter your username: ')
	else:
		msg = getpass.getpass('Please enter your password: ')
	try:
		s.sendto(msg, (host, port))
	except socket.error, msg:
		print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()


while (1):
	msg = raw_input('Enter message to send : ')

	try :
		#Set the whole string
		s.sendto(msg, (host, port))

		#receive data from client (data, addr)
		d = s.recvfrom(1024)
		reply = d[0]
		addr = d[1]

		print 'Server reply : ' + reply

	except socket.error, msg:
		print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

