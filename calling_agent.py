# all import

import os
from dotenv import load_dotenv

# hugging face for model, embedding, chatmodel
from langchain_huggingface import HuggingFaceEndpoint,HuggingFaceEmbeddings,ChatHuggingFace

# for the promt templeate
from langchain_core.prompts import PromptTemplate

# parser which give only string as output from messy data
from langchain_core.output_parsers import StrOutputParser

# for RAG Components load doc, split, embed, vector store
from langchain_core.documents import Document
from langchain_community.document_loaders import DirectoryLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS,chroma
from langchain_core.runnables import RunnablePassthrough,RunnableLambda,RunnableSequence,RunnableParallel

load_dotenv()

# now we load our buisness data .md files 
#------------------------------------------------------------------------------------------
# RAG : Step-1 Load the Documents

loader = DirectoryLoader(
    path='knowledge_base',
    glob='*.md',
    loader_cls=TextLoader
)

my_document = loader.load()

print("✅ Documents Loaded Successfully!")

# for doc in docs:
#     print(doc.metadata)


#------------------------------------------------------------------------------------------
#RAG Step : 2 split into chunks 

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 100
)

chunks = text_splitter.split_documents(my_document)

# print(len(my_document)) : 9
# print(len(chunks)) : 165

# for i,chunk in enumerate(chunks):
#     print(f"\nChunk {i + 1}:")
#     print(chunk.page_content)

print(f"✅ {len(chunks)} Chunks Created Successfully!")

#------------------------------------------------------------------------------------------
# RAG step : 3 creating embedding model 

embeddings = HuggingFaceEmbeddings(
     model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# check it is working or not ?
# sample_embedding = embedding.embed_query("Hey i am creating one fantaatic project")
# print(sample_embedding)
# print(len(sample_embedding))


#now we create vector store, which can store our chunks in vector of number format 
DB_FAISS_PATH = "VectorStore/chunks_convert_into_vectors"

if os.path.exists(DB_FAISS_PATH):
    
    print("📦 Vector Store Found Locally! Loading the Vector Store...")
    
    vector_store = FAISS.load_local(
        DB_FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    print("Vector Loaded Succesfully")
    
else:
    print("🔄 Creating Vectors... Calling the Model... Please Wait a Few Minutes ⏳")
    
    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )
    
    vector_store.save_local(DB_FAISS_PATH)
    
#------------------------------------------------------------------------------------

# RAG step : 4 Retriver

retriever = vector_store.as_retriever(
    search_kwargs={
        "k": 3
    },
    search_type="similarity"
)

print("\n✅ Retriever Created Successfully!\n")

query = "tell me about membership plan"

retrevied_docs = retriever.invoke(query)

# for i,chunk in enumerate(retrevied_docs):
#     print("\n {i+1} Chunk : ")
#     print(chunk.page_content)

#------------------------------------------------------------

# now we format our retrevied docs bcz, it have multiple chunks 

def format_docs(docs):
    """
      convert list of document obj in to string 
    """
    
    return "\n\n".join(
        doc.page_content 
        for doc in docs
    )
    
#--------------------------------------------------------------
# model making 

model_name = os.getenv("MODEL_NAME")

llm = HuggingFaceEndpoint(
    repo_id=model_name,
    task='text-generation'
)

model = ChatHuggingFace(llm=llm)

# result = model.invoke("What is capital of the france ?")

# print(result.content)
 
promt_text =  """You are the official AI assistant for PR Gym.
                Your job is ONLY to answer questions related to PR Gym.

                IMPORTANT RULES:

                1. Answer ONLY using the information provided in the Context.
                2. Never use your general knowledge to answer.
                3. Never invent, guess, or assume information.
                4. If the answer is not clearly available in the Context,
                respond exactly:

                "Sorry, I don't have that information about PR Gym."

                5. If the user asks something unrelated to PR Gym, respond:

                "Sorry, I can only help with questions related to PR Gym."

                6. Keep your answer clear, natural, and concise.
                7. Do not mention the words "context", "retriever", "RAG",
                "knowledge base", or "vector database" to the customer.

                Context:
                {context}

                Customer Question:
                {question}

                Answer:"""  
                        
promt = PromptTemplate(
    template= promt_text,  
    input_variables=['context','question']
)

parser = StrOutputParser()

parellel_chain = RunnableParallel({
       "context" : retriever | RunnableLambda(format_docs),
       "question" : RunnablePassthrough()
   })


RAG_chain = parellel_chain | promt | model | parser


print("================================== PR GYM ==================================")
print("🏋️ Welcome to PR GYM!!")
print("🤖 You can talk with our Gym AI Assistant if you have any questions.")
print("🚪 Type 'exit' or 'quit' to exit the chatbot.\n")


while True:
    User_Query = input("💬 Tell me your doubt here: ")

    if User_Query.lower() == 'quit' or User_Query.lower() == 'exit':
        print("\n🙏 Thank you for visiting PR GYM! Have a nice day! 😊")
        break

    Result = RAG_chain.invoke(User_Query)

    print("🤖 Gym AI:", Result)

# chatbot done