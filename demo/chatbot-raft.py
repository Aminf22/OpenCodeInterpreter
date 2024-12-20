#!/usr/bin/env python

import time

from raft import RaftNode

# To Distribute our challange we made a raft 
# In Raft lite library we have Talker and Listener per node that we starting 
# So we let to decicde raft joined nodes to which node must be leader and other nodes must be follower role.
# Every values that sent by client_request public method may recieve by any other nodes and be proccessed in mean time.
# After some seconds (valid and acceptable timeout to process messages in each raft node) we try to 
# check the commited value by check_committed_entry method .

# Create the intercommunication json 
comm_dict = {"node0": {"ip": "127.0.0.1", "port": "5560"}, 
    "node1": {"ip": "127.0.0.1", "port": "5561"}, 
    "node2": {"ip": "127.0.0.1", "port": "5562"},
    "node3": {"ip": "127.0.0.1", "port": "5563"},
    "node4": {"ip": "127.0.0.1", "port": "5564"},
    "node5": {"ip": "127.0.0.1", "port": "5565"},
    }

# Start a few nodes
nodes = []
for name, address in comm_dict.items():
    nodes.append(RaftNode(comm_dict, name))
    nodes[-1].start()

# Let a leader emerge
time.sleep(2)

# Make some chat requests
for val in range(5):
    nodes[0].client_request({'message::eval': val})
time.sleep(5)

# Check and see what the most recent entry is
for n in nodes:
    print(n.check_committed_entry())

# Stop all the nodes
for n in nodes:
    n.stop()