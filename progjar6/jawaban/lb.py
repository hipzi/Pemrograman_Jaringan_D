import socket
import time
import sys
import asyncore
import logging


class BackendList:
	def __init__(self):
		self.servers=[]
		#self.servers.append(('192.168.122.134',9002))
		self.servers.append(('127.0.0.1',9003))
		#self.servers.append(('192.168.122.134',9004))
		#self.servers.append(('192.168.122.134',9005))
		#self.servers.append(('192.168.122.134',9005))
		self.current=0
	def getserver(self):
		s = self.servers[self.current]
		self.current=self.current+1
		if (self.current>=len(self.servers)):
			self.current=0
		return s


class Backend(asyncore.dispatcher_with_send):
	def __init__(self,targetaddress):
		asyncore.dispatcher_with_send.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect(targetaddress)
		self.connection = self

	def handle_read(self):
		try:
			self.client_socket.send(self.recv(8192))
		except:
			pass
	def handle_close(self):
		try:
			self.close()
			self.client_socket.close()
		except:
			pass


class ProcessTheClient(asyncore.dispatcher):
	def handle_read(self):
		data = self.recv(8192)
		if data:
			self.backend.client_socket = self
			self.backend.send(data)
	def handle_close(self):
		self.close()

class Server(asyncore.dispatcher):
	def __init__(self,portnumber):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(('',portnumber))
		self.listen(10)
		self.bservers = BackendList()
		logging.warning("load balancer running on port {}" . format(portnumber))

	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			logging.warning("connection from {}" . format(repr(addr)))

			#menentukan ke server mana request akan diteruskan
			bs = self.bservers.getserver()
			logging.warning("koneksi dari {} diteruskan ke {}" . format(addr, bs))
			backend = Backend(bs)

			#mendapatkan handler dan socket dari client
			handler = ProcessTheClient(sock)
			handler.backend = backend
			logging.warning("ini apa {}" . format(handler.backend))
			logging.warning("ini apa 2 {}" . format(sock))

def main():
	portnumber=18000
	try:
		portnumber=int(sys.argv[1])
	except:
		pass
	svr = Server(portnumber)
	asyncore.loop()

if __name__=="__main__":
	main()


