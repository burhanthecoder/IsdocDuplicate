import openai
import pinecone
import uuid
from dotenv import load_dotenv
load_dotenv()
import os

openai.api_key = os.getenv("OPENAI_API_KEY") 
pinecone.init(api_key= os.getenv("PINECONE_API_KEY")
              ,environment= os.getenv("PINECONE_ENVIRONMENT"))

pinecone_index = pinecone.Index('doc-checker')

def create_embeddings(input):
    q_embeddings = openai.Embedding.create(
        input=input, engine='text-embedding-ada-002')['data'][0]['embedding']
    return q_embeddings

def addDocumentPinecone(input, q_embeddings):
    document_id = str(uuid.uuid4())
    upsertIndex =pinecone_index.upsert(   
        vectors=[
        {
        'id': document_id, 
        'values': q_embeddings, 
        'metadata': {'question': input}
        }
        ]
    )
    return upsertIndex

def checkDocumentDuplicate(input):
    print(input)
    embeddings = create_embeddings(input)
    search_results = pinecone_index.query(queries=[embeddings], top_k=1)
    if search_results['results'][0]['matches'][0]['score'] > 0.9:
        return True
    else:
        addDocumentPinecone(input, embeddings)
        return False
