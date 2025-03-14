import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional
from .database import Session, Block

class Blockchain:
    def _init_(self):
        self.current_transactions = []
        self.nodes = set()
        self.initialize_chain()

    def initialize_chain(self):
        with Session() as session:
            if not session.query(Block).first():
                self.create_block(proof=100, previous_hash='1')

    def create_block(self, proof: int, previous_hash: Optional[str] = None) -> Dict:
        with Session() as session:
            block = Block(
                index=len(self.chain) + 1,
                transactions=self.current_transactions,
                proof=proof,
                previous_hash=previous_hash or self.hash(self.last_block)
            )
            session.add(block)
            session.commit()
            
            self.current_transactions = []
            return self.block_to_dict(block)

    def add_transaction(self, sender: str, recipient: str, amount: float) -> int:
        from .smart_contracts import validate_transaction
        if not validate_transaction(sender, recipient, amount):
            raise ValueError("Invalid transaction")
            
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'timestamp': str(datetime.utcnow())
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block_data: Dict) -> str:
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def chain(self) -> List[Dict]:
        with Session() as session:
            return [self.block_to_dict(block) for block in session.query(Block).all()]

    @property
    def last_block(self) -> Dict:
        return self.chain[-1]

    def proof_of_work(self, last_proof: int) -> int:
        difficulty = 4
        proof = 0
        while not self.valid_proof(last_proof, proof, difficulty):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof: int, proof: int, difficulty: int) -> bool:
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash.startswith('0' * difficulty)

    @staticmethod
    def block_to_dict(block: Block) -> Dict:
        return {
            'index': block.index,
            'timestamp': block.timestamp.isoformat(),
            'transactions': block.transactions,
            'proof': block.proof,
            'previous_hash': block.previous_hash
        }