#!/usr/bin/env python

import time

from raft import RaftNode

# To Distribute our challange we made a raft 
# In Raft lite library we have Talker and Listener per node that we starting 
# So we let to decicde raft by voting among the joined nodes to which node must be leader and other nodes must be follower role.
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
nodes: list[RaftNode] = [] # a list of Raft Node
for name, address in comm_dict.items():
    nodes.append(RaftNode(comm_dict, name))
    nodes[-1].start() # we starting the nodes here in separeted thereads

# Let a leader emerge
# a time out needed to vote and leader emerege
time.sleep(2)

# Make some chat requests to evaluate the processint and token generation time 
# So we measure this lines 
messages = ["How can I Write a python array ?",
            "Should I use semicolon at the end of each line in C programming ?",
            "Write me a random number generation in Rust lang",
            "What does mean struct in C ?",
            "May I ask you to write B shell script to print date and time"
            ]
for message_id in range(5):
    # send client request to a random node in raft network to distribute the message by it hands.
    # we assign a message id to track message in queue
    nodes[0].client_request({'message::eval': messages[message_id]},message_id)
time.sleep(5)



# Check and see what the most recent entry is
for n in nodes:
    print(n.check_role())
    print(n.check_committed_entry())

# Stop all the nodes
for n in nodes:
    n.stop()