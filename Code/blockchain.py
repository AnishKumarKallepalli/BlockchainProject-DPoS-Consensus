import hashlib
import json
from datetime import datetime
from urllib.parse import urlparse
import requests
from random import randint
from typing import List
import typing

# Node class
class Node:
    def __init__(self, left, right, value: str)-> None:
        self.left: Node = left
        self.right: Node = right
        self.value = value

    @staticmethod
    def hash(val: str)-> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()

    @staticmethod
    def doubleHash(val: str)-> str:
        return Node.hash(Node.hash(val))


# Merkletree class
class MerkleTree:
    def __init__(self, values: List[str])-> None:
        self.__buildTree(values)

    def __buildTree(self, values: List[str])-> None:
        leaves: List[Node] = [Node(None, None, Node.doubleHash(e)) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1:][0]) # duplicate last elem if odd number of elements
        self.root: Node = self.__buildTreeRec(leaves)

    def __buildTreeRec(self, nodes: List[Node])-> Node:
        half: int = len(nodes) // 2

        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], Node.doubleHash(nodes[0].value + nodes[1].value))

        left: Node = self.__buildTreeRec(nodes[:half])
        right: Node = self.__buildTreeRec(nodes[half:])
        value: str = Node.doubleHash(left.value + right.value)
        return Node(left, right, value)

    def printTree(self)-> None:
        self.__printTreeRec(self.root)

    def __printTreeRec(self, node)-> None:
        if node != None:
            print(node.value)
            self.__printTreeRec(node.left)
            self.__printTreeRec(node.right)

    def getRootHash(self)-> str:
        return self.root.value


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

        #List storing the transactions as strings
        self.transactions_strings = []
 
        #Defining the Genesis block        
        self.new_block(previous_hash = 1)
 
        #Storing nodes in the network in a set to prevent duplicate nodes from getting added to the blockchain
        self.nodes = set()
 
        #List containing all the nodes along with their stake in the network
        self.all_nodes = []
 
        #List containing all the voting nodes in the network
        self.voteNodespool = []
 
        #Sorted List storing nodes in the order of most votes received
        self.sortedNodespool = []
 
        #List storing the top 2 nodes with the highest value of stake*votes_received
        self.topNodespool = []
 
        #List storing the address of the delegate node selected for mining
        self.delegates = []
 
 
    # Creating a new block in the Blockchain
    def new_block(self,previous_hash = None):
        merkleroot = '1'
        if(len(self.transactions_strings)!=0):
            mtree = MerkleTree(self.transactions_strings)
            merkleroot = mtree.getRootHash()
        print(self.transactions_strings)
        block = {
            'index': len(self.chain) + 1,
            'merkle_root': merkleroot,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'transactions': self.unverified_transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.verified_transactions += self.unverified_transactions
        print(self.verified_transactions)
        self.unverified_transactions = []
        
        self.transactions_strings = []
 
        #appending the block at the end of the blockchain
        self.chain.append(block)
        return block
 
 
    #Adding a new transaction in the next block
    def new_transaction(self, buyer_name, seller_name, property_name, amount):
        self.transactions_strings.append(
            ' Buyer name '+ str(buyer_name) +
            ' Seller name '+ str(seller_name) +
            ' Property name '+ str(property_name) +
            ' Amount '+ str(amount)
        )
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
 
 
    #Selecting the top 2 nodes with the most votes
    def selection(self):
        self.sortedNodespool = sorted(self.voteNodespool, key = lambda vote: vote[2],reverse = True)
        print(self.sortedNodespool)
 
        for x in range(2):
            self.topNodespool.append(self.sortedNodespool[x])
        print(self.topNodespool)
 
        for y in self.topNodespool:
            self.delegates.append(y[0])
        print(self.delegates)
 
 
    #Syncing the list
    def sync(self):
        r = requests.get('http://localhost:7000/show')
        print(r)
 
        if(r.status_code == 200):
            delegates = r.json()['node_delegates']
            self.delegates = delegates[0:2]
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
