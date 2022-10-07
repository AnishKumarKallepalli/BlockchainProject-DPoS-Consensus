from flask import Flask, jsonify, request
 
from blockchain import Blockchain
 
#Initialising the node with identifier and instantiating the Blockchain class
app = Flask(__name__)
blockchain = Blockchain()



#API call for adding HTTP address of new nodes along with their stakes in the network.
@app.route('/addnode', methods=['POST'])
def add_nodes():
    values = request.get_json()
    required = ['nodeaddress','stake']
 
    if not all(k in values for k in required):
        return 'Error',400
 
    blockchain.add_node(values['nodeaddress'], values['stake'])
 
    response = {
        'message': 'New nodes are added!',
        'total_nodes': list(blockchain.nodes)
    }
    print(blockchain.nodes)
    return jsonify(response), 201
 


 #API call to start the voting process
@app.route('/vote',methods=['GET'])
def voting():
 
    if(port == 7000):
        show_votes = blockchain.add_vote()
 
        response ={
            'message': 'The voting results are as follows:',
            'nodes': blockchain.voteNodespool
            }
 
        return jsonify(response),200
 
    else:
        response={
            'message': 'You are not authorized to conduct the election process!'
        }
        return jsonify(response),400
 


#API call to view the list of the top elected delegate nodes
@app.route('/show',methods=['GET'])
def delegates():
    show_delegates = blockchain.selection()
 
    response={
        'message': 'The top 2 nodes selected for block mining are:',
        'node_delegates': blockchain.delegates
    }
    return jsonify(response),200
 


#API call to synchronise the list of elected delegates with all other nodes in the network 
@app.route('/sync',methods=['GET'])
def sync_delegates():
    sync_delegates = blockchain.sync()
 
    response ={
        'message': 'The delegate nodes are:',
        'node_delegates':blockchain.delegates
    }
    return jsonify(response),200
 


 #API call for a new transaction
@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['Buyer name','Seller name','Property name','Amount']
    if not all(k in values for k in required):
        return 'Missing values! Please enter buyer name, seller name, property name and amount.', 400
    
    index = blockchain.new_transaction(values['Buyer name'], values['Seller name'], values['Property name'], values['Amount'])

    response = {
        'message': f'Transaction will be added to block {index}'
    }
    return jsonify(response), 201
 


#API call using an HTTP GET request to mine a block
@app.route('/mine', methods=['GET'])
def mine():
 
    #Ensuring that only elected delegates can mine a new block
    current_port = "localhost:"+ str(port)
    if(current_port in blockchain.delegates):
 
        #Ensuring that a new block is mined only if there are atleast 2 transactions
        if len(blockchain.unverified_transactions) >= 2:
            last_block = blockchain.last_block
            previous_hash = blockchain.hash(last_block)
            block = blockchain.new_block(previous_hash)
 
            response = {
                'message': "New block mined!",
                'index': block['index'],
                'transactions': block['transactions'],
                'previous_hash': block['previous_hash']
            }
            print(len(blockchain.unverified_transactions))
            return jsonify(response), 200
 
        else:
            response = {
                'message' : 'Not enough transactions to mine a new block and add to chain!'
            }
            print(len(blockchain.unverified_transactions))
            return jsonify(response),400
    else:
        response = {
            'message': 'You are not authorised to mine block! Only delegates can mine.'
        }
        return jsonify(response),400
 

 
#API call for viewing the blockchain
@app.route('/blockchain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

 

#API call to achieve consensus by resolving and replacing current chain with the longest validated chain
@app.route('/blockchain/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_chain()
 
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200
 
 
 
if __name__ == '__main__':
    from argparse import ArgumentParser
 
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=7000, type=int, help='Listening on port')
    args = parser.parse_args()
    port = args.port
    app.run(host = '0.0.0.0', port = port) 
