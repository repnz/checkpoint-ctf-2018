import socket
import time

address = '35.157.111.68', 10187

s=socket.socket()
s.connect(address)


data = s.recv(1024)

while data:
	print data
	value = data.split(':')
	if len(value) > 1:
		value = value[1].strip()
		print 'value is ' + value
		s.send(value+'\n')
	data = s.recv(1024)
