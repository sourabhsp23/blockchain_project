from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .blockchain import Blockchain

app = FastAPI()
blockchain = Blockchain()

# Setup templates
templates = Jinja2Templates(directory="app/templates")

@app.post("/transactions/new")
async def new_transaction(sender: str, recipient: str, amount: float):
    try:
        index = blockchain.add_transaction(sender, recipient, amount)
        return {"message": f"Transaction added to Block {index}"}
    except ValueError as e:
        return {"error": str(e)}, 400

@app.get("/mine")
async def mine_block():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(last_block)
    block = blockchain.create_block(proof, previous_hash)
    return {"block": block}

@app.get("/chain")
async def full_chain():
    return {"chain": blockchain.chain, "length": len(blockchain.chain)}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})