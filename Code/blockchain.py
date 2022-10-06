import hashlib
import json
from datetime import datetime
from urllib.parse import urlparse
import requests
from random import randint
 
# Blockchain class
class Blockchain(object):
 
    # Constructor to create data structures for storing various elements and transaction of the blockchain
    def __init__(self):
 
        #List storing the blockchain
        self.chain = []
 
        #List storing the unverified transactions
        self.unverified_transactions = []  
 
        #List storing the verified transactions
        self.verified_transactions = []
 
        #Defining the Genesis block        
        self.new_block(previous_hash = 1)
 
        #Storing nodes in the network in a set to prevent duplicate nodes from getting added to the blockchain
        self.nodes = set()
 
        #List containing all the nodes along with their stake in the network
        self.all_nodes = []
 
        #List containing all the voting nodes in the network
        self.voteNodespool = []
 
        #Sorted List storing nodes in the order of most votes received
        self.starNodespool = []
 
        #List storing the top 3 nodes with the highest value of stake*votes_received
        self.superNodespool = []
 
        #List storing the address of the delegate nodes selected for mining
        self.delegates = []
 
 
    # Creating a new block in the Blockchain
    def new_block(self,previous_hash = None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'transactions': self.unverified_transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.verified_transactions += self.unverified_transactions
        print(self.verified_transactions)
        self.unverified_transactions = []
 
        #appending the block at the end of the blockchain
        self.chain.append(block)
        return block
 
 
    #Adding a new transaction in the next block
    def new_transaction(self, buyer_name, seller_name, property_name, amount):
        self.unverified_transactions.append({
            'Buyer name': buyer_name,
            'Seller name': seller_name,
            'Property name': property_name,
            'Amount': amount,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return self.last_block['index'] + 1

 
    @property
    def last_block(self):
        return self.chain[-1]
 
 
    #Static method to create a SHA-256 Hash of a given block
    @staticmethod
    def hash(block):       
        block_string = json.dumps(block, sort_keys = True).encode()
        hash_val = hashlib.sha256(block_string).hexdigest()
        return hash_val
 
 
    #Adding a node using its IP address to the Blockchain network. 
    def add_node(self, address, stake):
        parsed_url = urlparse(address)
        authority = stake
        self.nodes.add((parsed_url.netloc,authority))
 
 
    #Simulating the voting process
    def add_vote(self):
        self.all_nodes = list(self.nodes)
 
        for x in self.all_nodes:
            y=list(x)
            y.append(int(x[1]) * randint(0,100))
            self.voteNodespool.append(y)
 
        print(self.voteNodespool)
 
 
    #Selecting the top node with the most votes
    def selection(self):
        self.starNodespool = sorted(self.voteNodespool, key = lambda vote: vote[2],reverse = True)
        print(self.starNodespool)
 
        for x in range(1):
            self.superNodespool.append(self.starNodespool[x])
        print(self.superNodespool)
 
        for y in self.superNodespool:
            self.delegates.append(y[0])
        print(self.delegates)
 
 
    #Syncing the list
    def sync(self):
        r = requests.get('http://localhost:7000/delegates/show')
        print(r)
 
        if(r.status_code == 200):
            delegates = r.json()['node_delegates']
            self.delegates = delegates[0:1]
            print(self.delegates)
 
 
    #Checking if the chain is validated (using hash values)
    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1
 
        while current_index < len(chain):
            block = chain[current_index]
 
            #Return false if the hash value of the current block doesn't match
            if block['previous_hash'] != self.hash(last_block):
                return False
 
            last_block = block
            current_index += 1
 
        return True
 
 
    #Choosing the longest validated chain as the primary blockchain
    def resolve_chain(self):
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)
 
        for node in neighbours: 
            response = requests.get(f'http://{node}/chain')
 
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
 
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain
 
        if new_chain:
            self.chain = new_chain
            return True
 
        return False 
 
