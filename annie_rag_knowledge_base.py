import os

import gradio as gr
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.globals import set_verbose
from langchain.memory import ConversationBufferMemory
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
import tiktoken

import openai_common
from annie_constants import PODCAST_DIR

DB_NAME = "vector_db"
os.environ['OPENAI_API_KEY'] = openai_common.api_key

def add_metadata(doc, doc_type):
    doc.metadata["doc_type"] = doc_type
    return doc

def load_documents():
    text_loader_kwargs = {'encoding': 'utf-8'}
    loader = DirectoryLoader(PODCAST_DIR, glob="*.txt", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
    documents = loader.load()
    return documents

def vectorize_documents(documents):
    embeddings = OpenAIEmbeddings(chunk_size=100)
    if os.path.exists(DB_NAME):
        vectorstore = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)
        if vectorstore._collection.count() > 0:
            print(f"Vectorstore existing with {vectorstore._collection.count()} documents")
            return vectorstore
        else:
            vectorstore.delete_collection()

    vectorstore = Chroma.from_documents(documents=documents, embedding=embeddings, persist_directory=DB_NAME)
    print(f"Vectorstore created with {vectorstore._collection.count()} documents")
    return vectorstore

def create_conversation_chain(vector_store):
    llm = ChatOpenAI(temperature=0.7, model_name=openai_common.MODEL_GPT_4O_MINI)
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    retriever = vector_store.as_retriever(search_kwargs={"k": 25})
    return ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, memory=memory, verbose=True)

documents = load_documents()

def inspect_documents(documents):
    enc = tiktoken.encoding_for_model("text-embedding-3-small")
    max_len = 0
    max_len_doc = None
    for i, doc in enumerate(documents):
        tokens = len(enc.encode(doc.page_content))
        if tokens > max_len:
            max_len = tokens
            max_len_doc = doc
        if tokens > 8191:  # soft limit for text-embedding-3-small
            print(f"Doc {i} too long: {tokens} tokens")

    print ("Max len: " + str(max_len))
    print ("Longest:\n" + max_len_doc.__str__())


vector_store = vectorize_documents(documents)
conversation_chain = create_conversation_chain(vector_store)

def chat(question, history):
    result = conversation_chain.invoke({"question": question})
    return result["answer"]

view = gr.ChatInterface(chat, type="messages").launch(inbrowser=True)