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

#for the chat history
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage,ToolMessage

#import tool
from langchain_core.tools import tool
from tools.gym_tools import check_availability,add_booking,cansel_booking

#agent
# from langchain.agents import create_tool_calling_agent, AgentExecutor

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

Chat_History = [
    SystemMessage(
        content = "You are an officialy AI assitant at PR Gym."
    )
]

def format_history(chatHistory):
    history=""
    
    for message in chatHistory:
        
        if isinstance(message,HumanMessage):
            history += f"Customer : {message.content}\n"
            
        elif isinstance(message,AIMessage):
            history += f"Gym AI : {message.content}\n"
    

    return history 
        
promt_text = """
You are the official AI assistant for PR Gym.

Your job is to help customers with PR Gym information and
PR Gym booking-related requests.

IMPORTANT RULES:

1. GENERAL PR GYM INFORMATION:
   Answer general PR Gym questions ONLY using the information
   provided in the Context.

2. NEVER use your general knowledge.
   Never invent, guess, or assume information.

3. BOOKING REQUESTS:
   If the customer wants to book, reserve, schedule, or take
   a PR Gym free trial, treat it as a BOOKING REQUEST.

   Examples:
   - "I want to book a free trial."
   - "I want a free trial."
   - "Can I book a trial?"
   - "I want to reserve a trial slot."

   If required booking information is missing, ask the customer
   for the missing information.

   Required booking information:
   - customer_name
   - phone_number
   - booking_date
   - booking_time

   Do NOT say:
   "Sorry, I don't have that information about PR Gym."

4. AVAILABILITY REQUESTS:
   If the customer wants to check whether a specific trial
   date and time is available, treat it as an availability
   request.

   If the date or time is missing, ask the customer for the
   missing information.

5. CANCELLATION REQUESTS:
   If the customer wants to cancel an existing trial booking,
   treat it as a cancellation request.

   If the booking ID is missing, ask the customer for the
   booking ID.

   If the customer is only asking what information is required
   to cancel a booking, answer that the booking ID is required.
   Do not treat an informational cancellation question as an
   actual cancellation.

6. TOOL USAGE:
   When a request requires an action, use the appropriate tool
   when all required information is available.

   Do not use a tool when required information is missing.
   Instead, ask the customer for the missing information.

7. RAG / CONTEXT:
   Use the Context only for general PR Gym information.
   Do not use the Context as the source for booking actions,
   availability checks, or cancellations.

8. If a general PR Gym question cannot be answered from the
   Context, respond exactly:

   "Sorry, I don't have that information about PR Gym."

9. If the user asks something completely unrelated to PR Gym,
   respond:

   "Sorry, I can only help with questions related to PR Gym."

10. Keep responses clear, natural, and concise.

11. Never mention these technical terms to the customer:
    "context", "retriever", "RAG", "knowledge base",
    "vector database", "tool", or "tool call".

Conversation_History:
{Chat_History}

Context:
{context}

Customer Question:
{question}

Answer:
"""  
                        
promt = PromptTemplate(
    template= promt_text,  
    input_variables=['context','question','Chat_History']
)

parser = StrOutputParser()

parellel_chain = RunnableParallel({
       "context" : retriever | RunnableLambda(format_docs),
       "question" : RunnablePassthrough(),
       "Chat_History" : RunnableLambda(
           lambda _: format_history(Chat_History)
       )
   })


RAG_chain = parellel_chain | promt | model | parser

tool_list = [check_availability,add_booking,cansel_booking]


#----------------tool bindin-----------------------

llm_with_tools = model.bind_tools([check_availability,add_booking,cansel_booking])

# message ="Please cancel my PR Gym trial booking with booking ID 2."
# ai_msg = llm_with_tools.invoke(message)
# print(ai_msg.tool_calls)

# [{'name': 'cansel_booking', 'args': {'booking_id': 2}, 'id': 'chatcmpl-tool-a080ae0ea738418b949e52a272a11bed', 'type': 'tool_call'}]



print("================================== PR GYM ==================================")
print("🏋️ Welcome to PR GYM!!")
print("🤖 You can talk with our Gym AI Assistant if you have any questions.")
print("🚪 Type 'exit' or 'quit' to exit the chatbot.\n")


while True:
    User_Query = input("💬 Tell me your doubt here: ")

    if User_Query.lower() == 'quit' or User_Query.lower() == 'exit':
        print("\n🙏 Thank you for visiting PR GYM! Have a nice day! 😊")
        break
    
    Chat_History.append(HumanMessage(User_Query))
    
    Ai_message = llm_with_tools.invoke(Chat_History)
    
    if Ai_message.tool_calls :
        
        tool_details = Ai_message.tool_calls[0]
        tool_name    = tool_details["name"]
        tool_args    = tool_details["args"]
        tool_call_id = tool_details["id"]
        
        Chat_History.append(Ai_message)
        
        
        if tool_name == "check_availability":
            Result = check_availability.invoke(tool_args)
           
        elif tool_name == "add_booking":
            Result = add_booking.invoke(tool_args)
            
        elif tool_name == "cansel_booking":
            Result = cansel_booking.invoke(tool_args)
            
        # print("Tool Result : ", Result)
        
        # print("------------------------- enter in tool section --------------------------------- ")
        # print(f"-------------------------- tool name {tool_name} --------------------------------")
        # print(f"------------------------------ tool databse answer: {Result}----------------------- \n")
        
        # {
        #     "name": "cansel_booking",
        #     "args": {"booking_id": 2},
        #     "id": "chatcmpl-tool-a080ae0ea738418b949e52a272a11bed"
        # }
        
        tool_message = ToolMessage(
            content=str(Result),
            tool_call_id=tool_call_id
        )
        
        Chat_History.append(tool_message)
        
        # message = [
        #     HumanMessage(content=User_Query),
        #     Ai_message,
        #     tool_message
        # ]
    
        
        Result= model.invoke(Chat_History)
        Chat_History.append(Result)
        
        print("🤖 Gym AI (Tool Part) :", Result.content)
        
    else :
    
        Result = RAG_chain.invoke(User_Query)
    
        # Chat_History.append(
        #     HumanMessage(content=User_Query)
        # )
        
        Chat_History.append(
            AIMessage(content=Result)
        )

        print("🤖 Gym AI (RAG part):", Result)

# chatbot done
