# Blockchain Assignment - 1

## How to run
1) Make sure Python 3.8+ , Flask and requests library is installed.
    *  If not downloaded, Download any version of Python (>=3.8) from the [official website](https://www.python.org/downloads/).
    *  Install flask   => `pip install flask`
    *  Install request => `pip install requests`

2) `cd Code` and run the server:
    * `py main.py`
        We can open different network ports on different terminals to simulate multinode network
    * `py main.py -p 7001`
    * `py main.py -p 7002`

3) Run the API endpoints on a browser or a HTTP Client like [Postman](https://www.postman.com/downloads/).

## Delegated Proof of Stake (DPoS) algorithm 
Delegated Proof Of Stake (DPoS) is a consensus algorithm which is an advancement of the fundamental concepts of Proof Of Stake. Delegated Proof of Stake (DPoS) consensus algorithm was developed by Daniel Larimer, founder of BitShares, Steemit and EOS in 2014. In DPoS, each node that has a stake in the system can delegate the validation of a transaction to other nodes by voting. In DPoS, user's vote weight is proportional to their stake rather than block mining being tied to the stakeholders' total tokens.

### How to interact with our blockchain

1). `/addnode`

The first step is to add the nodes along with their stakes. This is done by a POST route. The URL address of the nodes along with their stakes need to be added.

![Nodes add](./Images/add_nodes.jpg)

2). `/vote`

Voting is done using a GET route. Voting can only be conducted by the primary node (`localhost:7000`), and all other nodes receive an error message. Once called, a JSON response which consists the address of the node, stake of the node and the value of (stake * votes) corresponding to the nodes is sent to the primary node.

Voting results showing address, stake and (votes * stake) of all participating nodes
![Voting](./Images/voting.jpg)

Nodes apart from the primary node receive an error message.
![Error](./Images/voting_error.jpg)

3). `/show`

This GET route sends all the delegates elected to the primary node.

![Show delegates](./Images/delegates_show.jpg)

4). `/sync`

This GET route allows all the other nodes in the network to fetch the list of delegate nodes.

![Sync delegates](./Images/delegates_sync.jpg)

5). `/transaction/new`

This POST route initiates a new transaction and requires the user to enter the buyer name, seller name, property name and amount in JSON format.

![New transaction](./Images/transaction.jpg)

6). `/mine`

This GET route facilitates validating transactions and mining new blocks. Adhering to the DPoS consensus, only delegate nodes can mine the new blocks.To ensure no block goes underfilled, a new block can be mined only when there are atleast two unverified transactions.

This error message will be received by a non-delegate node that tries to mine a new block.
![Mine error](./Images/error_mine.jpg)

There must be atleast 2 transactions per block
![Under transaction](./Images/transaction2.jpg)

Structure of a typical block mined by a delegated node
![Block structure](./Images/block.jpg)

7). `/blockchain`

This GET route facilitates the user to view the entire blockchain and its length.

![Blockchain](./Images/chain.jpg)

8). `/blockchain/resolve`

This route finds the longest validated chain by checking all the nodes in the network and sets the node with the longest length as the primary blockchain.

## Team members - (Group 34)
1) [Anish Kumar Kallepalli](https://github.com/AnishKumarKallepalli) (2020A7PS0282H)
2) [Yash Pramod Kadam](https://github.com/RakuidN) (2020A3PS2123H)
3) [Anurag Bachchu Sarkar](https://github.com/AnuragSarkar3) (2020A3PS2117H)
