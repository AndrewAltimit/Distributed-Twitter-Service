import time as time_mod
import calendar

# Tweet Object
class Tweet():
	def __init__(self, username, message):
		self.username = username
		self.message = message
		self.utc_time = time_mod.asctime(time_mod.gmtime())
		
		
	# Return string representation of a tweet object
	def __str__(self):
		return "{:<23} | {}: {}".format(self.utc_to_local(), self.username, self.message)
		
	# Return the hash for a Tweet object
	def __hash__(self):
		return hash("{}::{}::{}".format(self.username, self.message, self.utc_time))
		
	# Order tweets by UTC time
	def __lt__(self, other):
		return self.utc_time < other.utc_time
		
	# Determine if two Tweet objects are the same
	def __eq__(self, other):
		return isinstance(other, Tweet) and (self.username == other.username and self.message == other.message and self.utc_time == other.utc_time)
		
	# converts from UTC time to local time on this machine
	def utc_to_local(self):
		# get the time struct from the formatted string
	    utc_struct = time_mod.strptime(self.utc_time, '%a %b %d %H:%M:%S %Y')
		
	    # convert this time struct to seconds since epoch time
	    utc_seconds = calendar.timegm(utc_struct)
		
	    # convert these seconds to our local time
	    loc_struct = time_mod.localtime(utc_seconds)
		
	    return time_mod.asctime(loc_struct)
		
	# Return whether self is a certain object type
	def is_type(self, object_type):
		return type(self) is object_type
		
	# Return self since already unpacked
	def unpack(self):
		return self
		
	# Return the username which created this object
	def get_username(self):
		return self.username

		
# Insert Block Object
class InsertBlock():
	# username = user who initiated block
	# follower = user who is blocked
	def __init__(self, username, follower):
		self.username = username
		self.follower = follower
		
	# Return string representation of a insert block object
	def __str__(self):
		return "{} blocking {}".format(self.username, self.follower)
		
	# Return the hash for a InsertBlock object
	def __hash__(self):
		return hash("{}::BLOCK::{}".format(self.username, self.follower))
		
	# Determine if two InsertBlock objects are the same
	def __eq__(self, other):
		return isinstance(other, InsertBlock) and (self.username == other.username and self.follower == other.follower)
		
	# Return whether self is a certain object type
	def is_type(self, object_type):
		return type(self) is object_type
		
	# Return self since already unpacked
	def unpack(self):
		return self
		
	# Return the username which created this object
	def get_username(self):
		return self.username
		
# Delete Block Object
class DeleteBlock():
	# username = user who initiated block
	# follower = user who is being unblocked
	def __init__(self, username, follower):
		self.username = username
		self.follower = follower
		
	# Return string representation of a insert block object
	def __str__(self):
		return "{} unblocking {}".format(self.username, self.follower)
		
	# Return the hash for a DeleteBlock object
	def __hash__(self):
		return hash("{}::UNBLOCK::{}".format(self.username, self.follower))
		
	# Determine if two DeleteBlock objects are the same
	def __eq__(self, other):
		return isinstance(other, DeleteBlock) and (self.username == other.username and self.follower == other.follower)
		
	# Return whether self is a certain object type
	def is_type(self, object_type):
		return type(self) is object_type
		
	# Return self since already unpacked
	def unpack(self):
		return self
		
	# Return the username which created this object
	def get_username(self):
		return self.username
		
	# Return the corresponding InsertBlock for this DeleteBlock
	def convert_to_IB(self):
		return InsertBlock(self.username, self.follower)