#FDS MINI PROJECT
# MADE BY: ARJUN DASHRATH 
#DATE 4/12/2020


#FOR TIMESTAMP
import datetime

#FOR SHA 256 HASH
import hashlib

#FOR JSON MANIPULATIONS
import json

#TO HOST ON LOCALHOST
from flask import Flask, jsonify

#TO RUN SYSTEM COMMANDS
import os

#BLOCKCHAIN CLASS
class Blockchain:
    
    #CONSTRUCTOR/INIT FUNCTION
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash='0')
    
    #CREATE/MINE BLOCK
    def create_block(self, proof, previous_hash):
        
        #OPENING THE DOCUMENT TO ADD TO BLOCKCHAIN
        with open('document.txt','r') as file:
            data = file.read()
            
        #BLOCK DATA DICTIONARY
        block = {
                    'index': len(self.chain)+1,
                    'timestamp': str(datetime.datetime.now()),
                    'proof':proof, 
                    'previous_hash': previous_hash, 'data': data
                }
        
        #ADDING BLOCK TO THE CHAIN
        self.chain.append(block)
        
        #RUNNING NODE JS PROGRAM ON SERVER(COMPUTER)
        os.system('cmd /c "node BlockChainData.js"')
        
        return block
    
    def get_previous_block(self):
        
        #PREVIOUS BLOCK TO COMPARE
        return self.chain[-1]
    
    #FUNCTION TO CHECK VALIDITY OF BLOCKCHAIN
    def proof_of_work(self, previous_proof):
        
        #MINING THE BLOCK
        #NONCE
        new_proof = 1
        
        check_proof = False 
        
        while check_proof is False:
            
            #SECURE HASH ALGORITHM 256 BEING USED
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest() 
            
            #CHECKING IF THE BLOCK MINED MEETS THE REQUIREMENTS
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
                
        return new_proof
    
    #FUNCTION TO HASH THE DATA INTO A 64 BIT HEXADECIMAL STRING
    def hash(self, block):
        
        #CONVERTING THE DATA DICTIONARY TO JSON OBJECT
        encoded_block = json.dumps(block, sort_keys = True).encode()
        
        #HASHING THE DATA AND RETURNING
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    #FUNCTION TO CHECK VALIDITY OF THE BLOCKCHAIN
    def is_chain_valid(self, chain):
        
        #STARTING POINT: GENESIS BLOCK
        previous_block = chain[0]
        
        block_index = 1
        
        #TRAVELLING THE BLOCKCHAIN
        while block_index < len(chain):
            
            block = chain[block_index]
            
            #COMPARING PREVIOUS HASH
            if block['previous_hash'] != self.hash(previous_block):
                return False
            
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            #CHECKING IF ALL THE HASHES ARE VALID
            if hash_operation[:4] != '0000':
                return False
            
            previous_block = block
            block_index += 1
            
        return True


#WEB APP
#IMPORTING FLASK PACKAGE
app = Flask(__name__)

#OBJECT OF BLOCKCHAIN CLASS
blockchain = Blockchain()

#MINING
#MINING URL
@app.route('/mine_block', methods=['GET'])

#FUNCTION FOR MINING
def mine_block():
    
    previous_block = blockchain.get_previous_block()
    
    #RECIEVING PROOF OF PREVIOUS BLOCK
    previous_proof = previous_block['proof']
    
    proof = blockchain.proof_of_work(previous_proof)
    
    #RECEIVING PREVIOUS HASH
    previous_hash = blockchain.hash(previous_block)
    
    #BLOCK MINED
    block=blockchain.create_block(proof, previous_hash)
    
    response = {
                'message': 'Congratulations, block mined',
                'index':block['index'],
                'timestamp':block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash']
                }
    
    #200 RESPONSE INDICATES THAT EVERYTHING IS IN ORDER
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])

#FUNCTION TO DISPLAY CHAIN
def get_chain():
    #datachain = json.load(blockchain.chain)
    response = {
                'chain': blockchain.chain,
                'length': len(blockchain.chain)
                }
    
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])

#FUNCTION TO CHECK IF THE CHAIN IS VALID
def is_valid():
    is_valid=blockchain.is_chain_valid(blockchain.chain)
    
    if is_valid: 
        response='Chain is valid'
    else:
        response='Chain not valid'
        
    return jsonify(response),200

@app.route('/show_data',methods=['GET'])

#FUNCTION TO SHOW THE DATA
def show_data():
    data = "BLOCKCHAIN DATA: "
    with open('data.json','r') as json_file: 
        datafile = json_file.read().replace('}'," -> ")
        datafile = datafile.replace('\"','')
        datafile = datafile.replace('{','')
        
        data = data + datafile
        
        response = data
        
    return jsonify(response), 200
    
#HOSTED ON LOCAL HOST
app.run(host='0.0.0.0', port = 5000)
            