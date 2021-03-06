import os, sys
import pickle
import log_module
import proposer_module
import acceptor_module
import learner_module
from event_module import *
import time
import socket

# Given a hosts file path, parse out server information and store internally in a dictionary
# Dictionary: Stores all server connection info
# Key    =>  Server ID
# Value  =>  (IP, port, username)
def parse_config(hosts_file):
	ID = 1
	all_servers = dict()
	file = open(hosts_file)
	for line in file:
		if line.strip() == "":
			continue
		parsed_config = line.strip().split(" ")

		server_dict = dict()
		server_dict["IP"] = parsed_config[0]
		server_dict["USERNAME"] = parsed_config[1].title()
		server_dict["PROPOSER_PORT"] = int(parsed_config[2])
		server_dict["ACCEPTOR_PORT"] = int(parsed_config[3])
		server_dict["LEARNER_PORT"] = int(parsed_config[4])
		all_servers[ID] = server_dict
		ID+=1
	file.close()
	return all_servers

# Show all known server configurations
def show_server_config(all_servers):
	print("\n{:-^120}".format("SERVER CONFIGURATIONS"))
	for ID in all_servers:
		username = all_servers[ID]["USERNAME"]
		IP = all_servers[ID]["IP"]
		p_port = all_servers[ID]["PROPOSER_PORT"]
		a_port = all_servers[ID]["ACCEPTOR_PORT"]
		l_port = all_servers[ID]["LEARNER_PORT"]
		print("ID: {:<3} Username: {:<10} IP: {:<15} Proposer Port: {:<10} Acceptor Port: {:<10} Learner Port: {:<10}".format(ID, username, IP, p_port, a_port, l_port))
	print("-" * 120)

# Show all valid commands
def show_commands(valid_commands):
	print("\n{:-^120} ".format("COMMANDS"))
	print("{:^120} ".format("   ".join(valid_commands)))
	print("-" * 120)


### Message Sending Test ###
def message_test(proposer):
	message = {"TYPE": "TEST"}
	print("\n{:-^120} ".format("MESSAGE SENDING TEST"))
	# Sending to all proposers
	print("PROPOSER SENDING TO ALL PROPOSERS...")
	proposer.send_all_proposers(message)
	time.sleep(0.5)

	# Sending to all acceptors
	print("\nPROPOSER SENDING TO ALL ACCEPTORS...")
	proposer.send_all_acceptors(message)
	time.sleep(0.5)

	# Sending to all learners
	print("\nPROPOSER SENDING TO ALL LEARNERS...")
	proposer.send_all_learners(message)
	time.sleep(0.5)
	print("-" * 120)
	
# Get the server ID for the local host
def get_server_ID(all_servers):
	ip = socket.gethostbyname(socket.gethostname())
	for ID in all_servers:
		if ip == all_servers[ID]["IP"]:
			return ID
	return None

if __name__ == "__main__":
	# Read in command line arguments
	hosts_filename = "/twitter/src/hosts.txt"

	# Parse Config File
	all_servers = parse_config(hosts_filename)
	show_server_config(all_servers)

	# Extract username for this server
	server_ID = get_server_ID(all_servers)
	username = all_servers[server_ID]["USERNAME"]

	# Initialize the log
	log = log_module.Log(server_ID, all_servers, username)

	# Create proposer, acceptor, and learner
	proposer = proposer_module.Proposer(server_ID, all_servers, log)
	acceptor = acceptor_module.Acceptor(server_ID, all_servers)
	learner = learner_module.Learner(server_ID, all_servers, log)

	# Message Sending Test
	message_test(proposer)

	proposer.update_log()

	# GUI - Terminate on Quit/Exit Command
	valid_commands = ["tweet", "block", "unblock", "view", "blocklist", "log", "servers", "drop", "commands", "exit"]
	show_commands(valid_commands)
	while True:
		text = input("({}) Message => ".format(username))
		if text.strip() == "":
			continue

		parsed_text = text.split(" ")
		command = parsed_text.pop(0).lower()

		if command not in valid_commands:
			print("Invalid Command")
			continue

		elif command == "servers":
			show_server_config(all_servers)

		elif command == "view":
			log.view_timeline()

		elif command == "log":
			log.view_log()

		elif command == "blocklist":
			log.view_blocklist()

		elif command == "tweet":
			# Repeatedly run the synod algorithm until successful
			event = Tweet(username, " ".join(parsed_text))
			while not proposer.insert_event(event):
				print("Failure to tweet, retrying in 10 seconds.")
				time.sleep(10)

		elif command == "block":
			blockee = " ".join(parsed_text).title()
			if blockee == username:
				print("Error: You can not block yourself.")
				continue

			# Repeatedly run the synod algorithm until successful
			event = InsertBlock(username, blockee)
			while not proposer.insert_event(event):
				print("Failure to block, retrying in 10 seconds.")
				time.sleep(10)

		elif command == "unblock":
			blockee = " ".join(parsed_text).title()
			if blockee == username:
				print("Error: You can not unblock yourself.")
				continue

			# Repeatedly run the synod algorithm until successful
			event = DeleteBlock(username, blockee)
			while not proposer.insert_event(event):
				print("Failure to unblock, retrying in 10 seconds.")
				time.sleep(10)

		elif command == "drop":
			if len(parsed_text) != 2:
				continue
			elif not parsed_text[1].isdigit():
				continue
			dropee = parsed_text[0].lower()
			drop_num = int(parsed_text[1])
			if dropee == "proposer":
				proposer.drop_messages(drop_num)
			elif dropee == "acceptor":
				acceptor.drop_messages(drop_num)
			elif dropee == "learner":
				learner.drop_messages(drop_num)
				
		elif command == "commands":
			show_commands(valid_commands)

		elif command == "exit":
			break
