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

host = 'localhost';
port = 8888;

while 1:
	
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
	
	#receive data from client (data, addr)
	d = s.recvfrom(1024)
	reply = d[0]
	addr = d[1]
	
	if reply == 'yes':
		print 'Logged in successfully.'
		break
	else:
		print 'uname and pass do not match'


while (1):
	print 'MENU: \n'
	print '1) Change password'
	print '2) Logout'
	
	msg = raw_input('Select the corresponding number to perform the action: ')
	
	try:
		s.sendto(msg, (host, port))
	except socket.error, msg:
		print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	
	if msg == '1':
		msg = getpass.getpass('Enter your old password: ')
		try:
			s.sendto(msg, (host, port))
		except socket.error, msg:
			print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()
		
		msg = getpass.getpass('Enter your new password: ')
		try:
			s.sendto(msg, (host, port))
		except socket.error, msg:
			print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
			sys.exit()
		
		d = s.recvfrom(1024)
		reply = d[0]
		addr = d[1]
		
		if reply == 'yes':
			print 'Password changed successfully'
		else:
			print 'Your old password does not match.'
		
	if msg == '2':
		print 'Goodbye!'
		sys.exit()
	# try :
	# 	#Set the whole string
	# 	s.sendto(msg, (host, port))

	# 	#receive data from client (data, addr)
	# 	d = s.recvfrom(1024)
	# 	reply = d[0]
	# 	addr = d[1]

	# 	print 'Server reply : ' + reply

	# except socket.error, msg:
	# 	print 'Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	# 	sys.exit()

