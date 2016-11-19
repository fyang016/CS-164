#...
#	Simple udp socket server
#...

import socket
import sys

HOST = ''	# Symbolic name meaning all available interfaces
PORT = 8888	# Arbitrary non-privileged port


# Datagram (udp) socket
try :
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'Socket created'
except socket.error, msg :
	print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

# Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error, msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Socket bind complete'



userList = ['user1', 'AdrenResi', 'user3', 'mercy', 'professor']

passList = ['123', '6995', '1234', 'angela', 'pro']

numAccounts = 5

while 1:
	while 1:
		d = s.recvfrom(1024)
		username = d[0]
		d = s.recvfrom(1024)
		password = d[0]
		
		addr = d[1]
		
		print 'username: ' + username + ' password: ' + password
		
		for x in range(0,numAccounts + 1):
			y = x
			if x < numAccounts and username == userList[x] and password == passList[y]:
				break
		
		# for y in range(0,numAccounts + 1):
		# 	if y < numAccounts and password == passList[y]:
		# 		break
		
		print 'x ' + str(x) + ' y ' + str(y) 
		
		if x == y and x < numAccounts:
			print 'Successfully logged in!'
			s.sendto('yes', addr)
			break
		else:
			print 'Username and password do not match'
			print numAccounts
			s.sendto('no', addr)
	
	#now keep talking with the client
	while 1:
		print 'second while loop'
		# receive data from client (data, addr)
		d = s.recvfrom(1024)
		data = d[0]
		addr = d[1]
	
		if not data:
			break
		
		
		if data[0] == '1':
			print 'Changing password... '
			
			d = s.recvfrom(1024)
			oldPass = d[0]
			
			d = s.recvfrom(1024)
			newPass = d[0]
			
			if oldPass == passList[y]:
				passList[y] = newPass
				print 'Password changed! ' + passList[y]
				s.sendto('yes', addr)
				continue
			
			else:
				print 'Your old password is incorrect'
				s.sendto('no', addr)
				continue
		
		elif data[0] == '2':
			print 'Logging out...'
			x = 0
			y = 0
			break
		
		else:
			break
		reply = 'OK...' + data
		
		s.sendto(reply, addr)
		print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + data.strip()

s.close()
