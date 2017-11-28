import socket
import _thread
import os, sys
import pickle
from event_module import *


# Learner Class
class Learner():
	def __init__(self, ID, server_config, log):
		self.ID = ID
		self.server_config = server_config
		self.log = log
		
		# IP/Port Configuration for this Learner
		self.IP = server_config[ID]["IP"]
		self.port = server_config[ID]["LEARNER_PORT"]

		# Start listening thread for incoming messages
		_thread.start_new_thread(self.listen, ())

		
	# Listen for incoming connections by binding to the socket specified in the hosts file
	def listen(self):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
			self.sock.bind((self.IP, self.port))
			while True:
				msg, source = self.sock.recvfrom(4096)
				self.process_message(msg, source)
				
		except:
			# Restart listening thread
			_thread.start_new_thread(self.listen, ())
			
	# Process the received message
	def process_message(self, msg, source):
		msg = pickle.loads(msg)
		
		# Display Debug Information
		type = msg["TYPE"]
		s1 = "Server: [{}   {}]".format(self.ID, " LEARNER")
		s2 = "Status: [{} {}]".format("RECEIVED", type)
		s3 = "Source:      [{}:{}]".format(source[0], source[1])
		print("{:<40} {:<40} {:<40}".format(s1, s2, s3))
		
		if type == "COMMIT":
			pass
			
	# Given a destination IP and port, send a message
	def send_msg(self, dest_ip, dest_port, message):
		try:
			# Display Debug Information
			s1 = "Server: [{}   {}]".format(self.ID, " LEARNER")
			s2 = "Status: [{} {}]".format("SENDING", message["TYPE"])
			s3 = "Destination: [{}:{}]".format(dest_ip, dest_port)
			print("{:<40} {:<40} {:<40}".format(s1, s2, s3))
			
			# Send Message
			msg = pickle.dumps(message)
			self.sock.sendto(msg, (dest_ip, dest_port))
		except:
			pass